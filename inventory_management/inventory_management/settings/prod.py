from inventory_management.settings.base import *

ALLOWED_HOSTS = ['0.0.0.0', 'localhost']

DEBUG = False

#SECRET_KEY = os.environ['SECRET_KEY']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'microsphere-prod',
        'USER': 'microsphere',
        'PASSWORD': 'm!cr0sphere2019',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

