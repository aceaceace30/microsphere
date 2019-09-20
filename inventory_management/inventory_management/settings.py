"""
Django settings for inventory_management project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!8s!mxg^t#9)n=e4_e*xmeg%6qvv2p4s)ds2@7825st(r1kw7x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'inventory',
    'account',
    'import_export',
    'widget_tweaks',
    'admin_reorder',
    'simple_history',
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
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'microsphere',
        'USER': 'postgres',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': '5433',
    }
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

# where users sent once successfull login
LOGIN_REDIRECT_URL = 'inventory:unit-list'
LOGOUT_REDIRECT_URL = 'account:login'

# same as the default LOGIN_URL for convention
LOGIN_URL = 'account:login'

#email settings
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'aceaceace.test@gmail.com'
EMAIL_HOST_PASSWORD = 'ace87654321!'
EMAIL_PORT = 587

EMAIL_HEADER_MESSAGE = 'Good Day! This is the updated list of units after the Preventive Maintenance.'

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
        {'model': 'inventory.PreventiveMaintenance', 'label': 'Schedules'},)},

    {'app': 'inventory', 'label': 'Details Maintenance', 'models': (
        {'model': 'inventory.MachineType', 'label': 'Machine types'},
        {'model': 'inventory.Brand', 'label': 'Brands'},
        {'model': 'inventory.Model', 'label': 'Models'},
        {'model': 'inventory.OperatingSystem', 'label': 'Operating systems'},
        {'model': 'inventory.OfficeApplication', 'label': 'Office application'},
        {'model': 'inventory.Processor', 'label': 'Processor'},
        {'model': 'inventory.TotalRam', 'label': 'RAM'},
        {'model': 'inventory.HddSize', 'label': 'HDD size'},)},
)