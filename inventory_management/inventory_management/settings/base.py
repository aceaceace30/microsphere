"""
Django settings for inventory_management project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

import environ

root = environ.Path(__file__) - 3  # get root of the project
env = environ.Env()
environ.Env.read_env()  # reading .env file


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=False)


# Application definition

INSTALLED_APPS = [
    'inventory',
    'account',
    'report',
    'import_export',
    'widget_tweaks',
    'admin_reorder',
    'simple_history',
    'django_summernote',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
    'admin_reorder.middleware.ModelAdminReorder',
]

ROOT_URLCONF = 'inventory_management.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'inventory_management.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

#accepted time formats
TIME_INPUT_FORMATS = ('%I:%M %p',)


#SUMMER NOTE THEME (can use bs3 for bootstrap 3)
SUMMERNOTE_THEME = 'bs4'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

STATIC_URL = '/static/'
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]

STATIC_ROOT = os.path.join(BASE_DIR, '../../mystatic/')

DASHBOARD_URL = 'account:dashboard'

# where users sent once successfull login
LOGIN_REDIRECT_URL = DASHBOARD_URL
LOGOUT_REDIRECT_URL = 'account:login'

# same as the default LOGIN_URL for convention
LOGIN_URL = 'account:login'

#email settings
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = env.str('EMAIL_USERNAME')
EMAIL_HOST_PASSWORD = env.str('EMAIL_PASS')
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL  = env.str('EMAIL_USERNAME')

BCC_EMAIL = 'marcababao@gmail.com'

#EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")


COMPANY_NAME = 'Microsphere Systems Technology'
COMPANY_ADDRESS = '53B Acacia St., Cembo Makati City'
COMPANY_CONTACT = 'Tel. no. 882-8638 / 556-2398'

# Docs: https://pypi.org/project/django-modeladmin-reorder/
ADMIN_REORDER = (
    # Rename app
    {'app': 'auth', 'label': 'Accounts', 'models': (
        {'model': 'auth.User', 'label': 'Users'},)},

    {'app': 'auth', 'label': 'Group Permissions', 'models': (
        {'model': 'auth.Group', 'label': 'Groups'},)},

    {'app': 'inventory', 'label': 'Clients', 'models': (
        {'model': 'inventory.ClientProfile', 'label': 'Client accounts'},
        {'model': 'inventory.BusinessUnit', 'label': 'Business units'},)},

    {'app': 'inventory', 'label': 'Inventory', 'models': (
        {'model': 'inventory.Unit', 'label': 'Units'},)},

    {'app': 'inventory', 'label': 'Preventive Maintenance', 'models': (
        {'model': 'inventory.PreventiveMaintenance', 'label': 'PM Schedules'},)},

    {'app': 'inventory', 'label': 'Details Maintenance', 'models': (
        {'model': 'inventory.MachineType', 'label': 'Machine types'},
        {'model': 'inventory.Brand', 'label': 'Brands'},
        {'model': 'inventory.Model', 'label': 'Models'},
        {'model': 'inventory.OperatingSystem', 'label': 'Operating systems'},
        {'model': 'inventory.OfficeApplication', 'label': 'Office application'},
        {'model': 'inventory.Processor', 'label': 'Processor'},
        {'model': 'inventory.TotalRam', 'label': 'RAM'},
        {'model': 'inventory.HddSize', 'label': 'HDD size'},)},

    {'app': 'inventory', 'label': 'Email Templates', 'models': (
        {'model': 'inventory.EmailTemplate', 'label': 'Templates'},)},
)