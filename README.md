# Automated Text Summarization Tool

An automated text summarization web application built with Django that helps users summarize text efficiently through a simple, user-friendly interface.

## Features

- **Text Summarization:** Generate concise summaries from longer text.
- **File-Based Summarization:** Work with text content provided through the file interface.
- **Question-Based Interaction:** Access the question interface for interacting with text.
- **Advanced Interface:** Provides additional options through the advanced page.
- **Web Interface:** Built with HTML, CSS, and JavaScript.
- **Django Backend:** Uses Django to handle application routing and server-side functionality.

## Technologies Used

- Python
- Django
- HTML5
- CSS3
- JavaScript
- SQLite (Django's default database, if configured)

## Project Structure

```text
Automated-Text-summarization-tool/
├── TextS/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── tsmadmin/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── templates/
│   ├── advanced.html
│   ├── file.html
│   ├── index.html
│   ├── layout.html
│   ├── question.html
│   └── summary.html
├── static/
│   ├── advanced.css
│   ├── advanced.js
│   ├── file.css
│   ├── index.css
│   ├── question.css
│   └── summary.css
├── manage.py
└── README.md
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/TejaswiniSV-01/Automated-Text-summarization-tool.git
```

### 2. Navigate to the Project Directory

```bash
cd Automated-Text-summarization-tool
```

### 3. Create a Virtual Environment

**Windows:**

```powershell
python -m venv env
env\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
python3 -m venv env
source env/bin/activate
```

### 4. Install Django

```bash
python -m pip install django
```

If the project uses additional Python packages, install them as well.

### 5. Apply Database Migrations

```bash
python manage.py migrate
```

### 6. Start the Development Server

```bash
python manage.py runserver
```

Open the following address in your browser:

http://127.0.0.1:8000/

## Usage

1. Start the Django development server.
2. Open the application in your browser.
3. Navigate through the available interfaces.
4. Enter text or use the file interface as supported by the application.
5. Generate and review summaries using the application's summarization functionality.

## Future Enhancements

- Support for additional document formats.
- Improved summary quality and customization.
- Summary export and download options.
- Enhanced user experience and responsive design.
- Deployment to a production web server.

## Author

**TejaswiniSV-01**

## GitHub Repository

[Automated-Text-summarization-tool](https://github.com/TejaswiniSV-01/Automated-Text-summarization-tool)

## License

This project is available for educational and personal use. Add a specific open-source license if you intend to define formal reuse and distribution permissions.
