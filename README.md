# My Django Project

## Overview

This project is a web application built with Django, a high-level Python web framework. It provides [describe the main features of your application].

## Requirements

Before you begin, ensure you have the following software installed:

- Python (3.x)
- pip (Python package installer)
- virtualenv (Optional but recommended)
- Django (2.x/3.x/4.x depending on your version)

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```
### 2. Create a Virtual Environment
```bash
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Apply Migrations
```bash
python manage.py migrate
```
### 5. Create a Superuser
```bash
python manage.py createsuperuser

```
### 6. Run the Development Server
```bash
python manage.py runserver

```
Basic Commands
Running the Development Server
```bash
python manage.py runserver
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
python manage.py test

```
Settings.py configuration instructions
Configuring Personal Information in settings.py
Secret Key
It's crucial to keep your secret key safe and not hard-coded in your settings file. Use an environment variable to set it:
```
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'your-default-secret-key')
```
Debug Mode
Ensure DEBUG is set to False in production:
```
DEBUG = os.environ.get('DJANGO_DEBUG', '') != 'False'
```
Allowed Hosts
Specify your allowed hosts:
```
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',')
```
Database Configuration
Set your database configuration using environment variables:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': os.environ.get('DB_NAME', 'megatech'),
        'USER': os.environ.get('DB_USER', 'root'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '3306'),
    }
}
```
Email Configuration
Configure your email settings using environment variables:
```
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'your-email@example.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'your-email-password')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'webmaster@example.com')
```
Paystack Configuration
Set your Paystack keys using environment variables:

```
PAYSTACK_SECRET_KEY = os.environ.get('PAYSTACK_SECRET_KEY', 'your-paystack-secret-key')
PAYSTACK_PUBLIC_KEY = os.environ.get('PAYSTACK_PUBLIC_KEY', 'your-paystack-public-key')
```
Environment Variables
Ensure you set the environment variables in your .env file:
```
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
DB_NAME=megatech
DB_USER=root
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=3306
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
DEFAULT_FROM_EMAIL=webmaster@example.com
PAYSTACK_SECRET_KEY=your-paystack-secret-key
PAYSTACK_PUBLIC_KEY=your-paystack-public-key
```



