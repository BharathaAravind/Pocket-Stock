"""
Django settings for PocketStock project.

Generated by 'django-admin startproject' using Django 1.11.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import urlparse
import dj_database_url

redis_url = urlparse.urlparse(os.environ.get('REDIS_URL'))
CACHES = {
    "default": {
         "BACKEND": "redis_cache.RedisCache",
         "LOCATION": "{0}:{1}".format(redis_url.hostname, redis_url.port),
         "OPTIONS": {
             "PASSWORD": redis_url.password,
             "DB": 0,
         }
    }
}

db_from_env = dj_database_url.config(conn_max_age=500)
#DATABASES['default'].update(db_from_env)
DATABASES = { 'default' : dj_database_url.config() }

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'fz4r#k#skpa#9p+rs8p-v=87_9*ga&qnveh$2u@q+u00o9&6oc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost','127.0.0.1','silo.soic.indiana.edu','pure-bayou-28363.herokuapp.com']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'stocks',
    'django_cron',
    'django_crontab',
    'channels'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware'
]

CRON_CLASSES = [
    "PocketStock.cron.MyCronJob",
]

ROOT_URLCONF = 'PocketStock.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            './templates',
            './stocks/templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

TEMPLATE_DIRS = (
    'D:\Django Practice\PocketStock\accounts\templates',
)


WSGI_APPLICATION = 'PocketStock.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#Duo-Auth Settings
# URL for Duo login form.  This is here to match the Django URLs; change
# how the Duo URLs are included to move this.
DUO_LOGIN_URL = '/accounts/duo_login'

# Duo configuration.
DUO_IKEY = 'DIVWFTL9DWHU2F9I4FOY'
DUO_SKEY = 'G8DzN7oE6NVeTh3CRI2krg33Kr2Rpvx0hP4PcvYt'
DUO_AKEY = '166397743d205453fbd3c5af720058cfccf1a49f'
DUO_HOST = 'api-ccfb0134.duosecurity.com'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

#Heroku setup
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'stocks/static/'),
]

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# Redirect to home URL after login (Default redirects to /accounts/profile/)
LOGIN_REDIRECT_URL = '/dashboard'

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'

AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    )

# SOCIAL_AUTH_FACEBOOK_KEY = '172718546612803'
# SOCIAL_AUTH_FACEBOOK_SECRET = 'a2623fa29ae9c03fa2a3242b5bc40ebc'

SOCIAL_AUTH_FACEBOOK_KEY = '1998625850427010'
SOCIAL_AUTH_FACEBOOK_SECRET = '8bb5b7f0c88c83fa0c9894b27e1ab1cc'

SOCIAL_AUTH_LOGIN_ERROR_URL = '/settings/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/settings/'
SOCIAL_AUTH_RAISE_EXCEPTIONS = False


EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'pocketstock2017@gmail.com' # email id
EMAIL_HOST_PASSWORD = 'MAAR2094' #password
EMAIL_PORT = 587
EMAIL_USE_TLS = True


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_redis.RedisChannelLayer",
        "CONFIG": {
            "hosts": [
            os.environ.get('REDIS_URL', 'redis://localhost:6379'),
            #os.environ.get('REDIS_URL', 'redis://localhost:8000'),
            #os.environ.get('REDIS_URL', 'redis://soic.silo.indiana.edu:55555')
            ],
        },
        "ROUTING": "PocketStock.routing.channel_routing",
    },
}
