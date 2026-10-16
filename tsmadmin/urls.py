from . import views
from django.urls import path
urlpatterns = [
    path("", views.HomeView, name="home_view"),
    path("admin", views.Adm.as_view(), name="admin"),
    path("file/", views.FileView, name="file_view"),
    path("summary/", views.SummaryView, name="summary_view"),
    path("advanced/", views.AdvancedView, name="advanced_view"),
    path("question/", views.QuestionView, name="question_view")
]