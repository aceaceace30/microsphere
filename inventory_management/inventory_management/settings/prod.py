from inventory_management.settings.base import *

ALLOWED_HOSTS = ['0.0.0.0', 'localhost']

DEBUG = env.bool('DEBUG')

#SECRET_KEY = os.environ['SECRET_KEY']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.str('DB_NAME'),
        'USER': env.str('DB_USER'),
        'PASSWORD': env.str('DB_PASS'),
        'HOST': env.str('DB_HOST'),
        'PORT': env.int('DB_PORT'),
    }
}

