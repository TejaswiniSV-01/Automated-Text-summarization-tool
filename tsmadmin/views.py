from django.shortcuts import render
from django.views import generic
import datetime
import warnings
warnings.filterwarnings("ignore")
import torch
from transformers import PegasusForConditionalGeneration, PegasusTokenizerFast
from transformers import BartTokenizerFast, BartForConditionalGeneration
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, BartForQuestionAnswering

# from rouge_score import rouge_scorer
# scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)

src_data = None
torch_device = 'cpu'

pegasus_model = PegasusForConditionalGeneration.from_pretrained("google/pegasus-cnn_dailymail").to(torch_device)
pegasus_tokenizer = PegasusTokenizerFast.from_pretrained("google/pegasus-cnn_dailymail")

bart_large_model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn").to(torch_device)
bart_large_tokenizer = BartTokenizerFast.from_pretrained("facebook/bart-large-cnn")

bart_samsum_model = BartForConditionalGeneration.from_pretrained("philschmid/bart-large-cnn-samsum").to(torch_device)
bart_samsum_tokenizer = BartTokenizerFast.from_pretrained("philschmid/bart-large-cnn-samsum")

# bart_distil_model = BartForConditionalGeneration.from_pretrained("sshleifer/distilbart-cnn-12-6").to(torch_device)
# bart_distil_tokenizer = BartTokenizerFast.from_pretrained("sshleifer/distilbart-cnn-12-6")

bart_brio_model = BartForConditionalGeneration.from_pretrained("yale-lily/brio-cnndm-cased").to(torch_device)
bart_brio_tokenizer = BartTokenizerFast.from_pretrained("yale-lily/brio-cnndm-cased")

# bart_ctrlsum_model = BartForConditionalGeneration.from_pretrained("hyunwoongko/ctrlsum-cnndm").to(torch_device)
# bart_ctrlsum_tokenizer = BartTokenizerFast.from_pretrained("hyunwoongko/ctrlsum-cnndm")

# prophetnet_tokenizer = ProphetNetTokenizer.from_pretrained("microsoft/prophetnet-large-uncased-cnndm")
# prophetnet_model = ProphetNetForConditionalGeneration.from_pretrained("microsoft/prophetnet-large-uncased-cnndm")

roberta_tokenizer = AutoTokenizer.from_pretrained("google/roberta2roberta_L-24_cnn_daily_mail")
roberta_model = AutoModelForSeq2SeqLM.from_pretrained("google/roberta2roberta_L-24_cnn_daily_mail")

from nltk.tokenize import RegexpTokenizer
def data_cleaner(data):
    lst = data.split("\n")
    
    while "" in lst:
        lst.remove("")

    def token(text):
        tokenizer = RegexpTokenizer(r'\w+')
        tokens= tokenizer.tokenize(text)
        tokens = " ".join(tokens)
        tokens = tokens.lower()
        return tokens

    data = ". ".join([token(i) for i in lst])
    return data

all_details = {"PEGASUS": "PEGASUS stands for Pre-training with Extracted Gap-sentences for Abstractive Summarization. Pegasus is based on \
                the transformer architecture and is trained using a variant of the unsupervised sequence-to-sequence pre-training method \
                introduced by the original transformer model. The pre-training process for Pegasus involves masking out random tokens in \
                the input text and training the model to predict the masked tokens based on the context provided by the unmasked tokens. \
                Pegasus is known for its high summarization performance, particularly on long and complex documents.",
               "PEGASUS_rougel": "41.11",
               
               "BART": "BART stands for Bidirectional and Auto-Regressive Transformer. BART uses an encoder-decoder architecture with a \
                bidirectional transformer network. The model is trained to take in a long document and generate a shorter, more concise \
                summary of the document. BART is an abstractive summarization model, which means it can generate summaries that do not simply \
                copy and paste sentences from the original document, but instead use the input document to generate a new summary that conveys \
                the most important information.",
               "BART_rougel": "40.90",
               
               "RoBERTa": "RoBERTa stands for A Robustly Optimized BERT Pretraining Approach. RoBERTa is a transformer-based neural network \
                architecture for natural language processing (NLP) tasks, developed by Facebook AI Research (FAIR). It is an extension of the \
                BERT (Bidirectional Encoder Representations from Transformers) architecture, which was released by Google in 2018. However, it \
                incorporates several improvements over BERT, such as using larger batch sizes, longer training sequences, and dynamically \
                changing the masking pattern during training.",
               "RoBERTa_rougel": "40.30",
               }

def HomeView(request):
    if request.method == "POST":
        data = request.POST["data"]
        if data:
            context = {
                "data": request.POST["data"],
                "model_name": "PEGASUS",
                "description": all_details["PEGASUS"],
                "minlength": 32,
                "avg_rougel": all_details["PEGASUS_rougel"]
            }
            return SummaryView(request, context)
        else:
            return render(request, "index.html")
    else:
        return render(request, "index.html")

def FileView(request):
    if request.method == "POST":
        inp = request.FILES["maininput"].read().decode("latin-1")
        if inp:
            context = {
                "data": inp,
                "model_name": "PEGASUS",
                "description": all_details["PEGASUS"],
                "minlength": 32,
                "avg_rougel": all_details["PEGASUS_rougel"]
            }
            return SummaryView(request, context)
        else:
            return render(request, "file.html")
    else:
        return render(request, "file.html")

def SummaryView(request, context):
    global src_data
    if request.method == "POST":
        if context:
            # src_text = data_cleaner(context["data"])
            src_text = context["data"]
            src_data = src_text
            if context["model_name"] == "PEGASUS":
                orig_model = pegasus_model
                orig_tokenizer = pegasus_tokenizer
                tun_model = bart_brio_model
                tun_tokenizer = bart_brio_tokenizer
            elif context["model_name"] == "BART":
                orig_model = bart_large_model
                orig_tokenizer = bart_large_tokenizer
                tun_model = bart_samsum_model
                tun_tokenizer = bart_samsum_tokenizer

            if context["model_name"] != "RoBERTa":
                batch = orig_tokenizer(src_text, truncation=True, padding='longest', return_tensors='pt')
                summary_ids = orig_model.generate(**batch,
                                            num_beams=6,
                                            num_return_sequences=1,
                                            no_repeat_ngram_size = 2,
                                            length_penalty = 1,
                                            min_length = int(context["minlength"]),
                                            max_length = int(context["minlength"])*3,
                                            early_stopping = True)
                summ = orig_tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)
                context["orig_summary"] = "".join(summ).replace("<n>", "").replace("[X_SEP]", "")

                batch = tun_tokenizer(src_text, truncation=True, padding='longest', return_tensors='pt')
                summary_ids = tun_model.generate(**batch,
                                            num_beams=6,
                                            num_return_sequences=1,
                                            no_repeat_ngram_size = 2,
                                            length_penalty = 1,
                                            min_length = int(context["minlength"]),
                                            max_length = int(context["minlength"])*3,
                                            early_stopping = True)
                summ = tun_tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)
                context["summary"] = "".join(summ).replace("<n>", "").replace("[X_SEP]", "")
                context["tun_summary"] = "".join(summ).replace("<n>", "").replace("[X_SEP]", "")

                return render(request, "summary.html", context)
            else:
                input_ids = roberta_tokenizer(" ".join(context["data"].split()[:300]), return_tensors="pt").input_ids
                output_ids = roberta_model.generate(input_ids)[0]
                summ = roberta_tokenizer.decode(output_ids, skip_special_tokens=True, padding=True, truncation=True)
                context["orig_summary"] = "".join(summ).replace("<n>", "").replace("[X_SEP]", "")
                context["tun_summary"] = ""

                return render(request, "summary.html", context)
    else:
        return render(request, "index.html")
    

def AdvancedView(request):
    if request.method == "POST":
        if request.POST["model_name"] == "PEGASUS (default)":
            context = {
                "data": request.POST["data"],
                "model_name": "PEGASUS",
                "description": all_details["PEGASUS"],
                "minlength": request.POST["minlength"],
                "avg_rougel": all_details["PEGASUS_rougel"]
            }
            return SummaryView(request, context)
        else:
            context = {
                "data": request.POST["data"],
                "model_name": request.POST["model_name"],
                "description": all_details[request.POST["model_name"]],
                "minlength": request.POST["minlength"],
                "avg_rougel": all_details[request.POST["model_name"] + "_rougel"]
            }
            return SummaryView(request, context)
    else:
        return render(request, "advanced.html")
    

def QuestionView(request, context={}):
    global src_data
    if request.method == "POST":
        data = request.POST["data"]
        if data:
            tokenizer = AutoTokenizer.from_pretrained("valhalla/bart-large-finetuned-squadv1")
            model = BartForQuestionAnswering.from_pretrained("valhalla/bart-large-finetuned-squadv1")
            question, text = data, src_data

            inputs = tokenizer(question, text, return_tensors="pt")
            with torch.no_grad():
                outputs = model(**inputs)
            answer_start_index = outputs.start_logits.argmax()
            answer_end_index = outputs.end_logits.argmax()
            predict_answer_tokens = inputs.input_ids[0, answer_start_index : answer_end_index + 1]
            ans = tokenizer.decode(predict_answer_tokens, skip_special_tokens=True)
            context["ans"] = ans
            return render(request, "question.html", context)
    else:
        return render(request, "question.html", context={})


class Adm(generic.TemplateView):
    pass
