# Django Project Setup Guide

This guide will help you set up and run a Django project on your local machine. Follow these steps to get started:

## Prerequisites

Before you begin, ensure you have the following installed:

- Python (version 3.6 or later)
- pip (Python package installer)
- Virtualenv (optional but recommended)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/lerchik-salata/coursework_tvprogram.git
cd coursework_tvprogram
```

### 2. Create and activate the environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Make and apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a superuser

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```



