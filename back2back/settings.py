import os

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as DEFAULT_TEMPLATE_CONTEXT_PROCESSORS
import dj_database_url


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Deployment settings
SECRET_KEY = os.environ.get('SECRET_KEY', 'ASDFJOIqo3r892p938huidnw')
DEBUG = not os.environ.get('PRODUCTION', False) == 'True'
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [
    'back-2-back.herokuapp.com',
    'back2back.mjtamlyn.co.uk',
]

# Application definition
INSTALLED_APPS = (
    'back2back',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'back2back.urls'
WSGI_APPLICATION = 'back2back.wsgi.application'

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_TEMPLATE_CONTEXT_PROCESSORS + ('back2back.context_processors.categories',)

# Database
DATABASES = {'default': dj_database_url.config(default='postgres://localhost/back2back')}

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}
