import os

from django.urls import reverse_lazy
import dj_database_url


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Deployment settings
SECRET_KEY = os.environ.get('SECRET_KEY', 'ASDFJOIqo3r892p938huidnw')
DEBUG = not os.environ.get('PRODUCTION', False) == 'True'
TEMPLATE_DEBUG = DEBUG

if not DEBUG:
    ALLOWED_HOSTS = [
        'back-2-back.herokuapp.com',
        'back2back.mjtamlyn.co.uk',
        'back2back.tamlynscore.co.uk',
        'back2back.archerygb.org',
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

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'back2back.urls'
WSGI_APPLICATION = 'back2back.wsgi.application'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
            'back2back.context_processors.categories',
        ]
    },
}]

# Database
DATABASES = {'default': dj_database_url.config(default='postgres://localhost/back2back')}
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')

# Auth
LOGIN_URL = reverse_lazy('admin:login')

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
