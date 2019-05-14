"""
Django settings for pleio_account project.

Generated by 'django-admin startproject' using Django 1.10.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""
import os
import ast
from collections import OrderedDict

import dj_database_url
from django.utils.translation import ugettext_lazy as _
from datetime import timedelta
import logging

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Set debugging to log everthing to console.
INTERNAL_IPS = '127.0.0.1'

try:
    DEBUG = os.environ['DEBUG']
except KeyError:
    DEBUG = False

if DEBUG:
    # will output to your console
    logging.basicConfig(
        level = logging.DEBUG,
        format = '%(asctime)s %(levelname)s %(message)s',
    )

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'bundles/',
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
    }
}

# Application definition

INSTALLED_APPS = [
    'constance',
    'constance.backends.database',
    'core',
    'emailvalidator',
    'api',
    'oauth2_provider',
    'rest_framework',
    'webpack_loader',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'user_sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_otp',
    'django_otp.plugins.otp_static',
    'django_otp.plugins.otp_totp',
    'two_factor',
    'oidc_provider',
    'axes',
    'corsheaders',
    'debug_toolbar'
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '10/minute',
        'user': '100/minute'
    }
}

MIDDLEWARE = [
    'core.middleware.XRealIPMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'user_sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'core.middleware.PartnerSiteMiddleware',
    'core.middleware.DeviceIdMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesModelBackend',
    'django.contrib.auth.backends.ModelBackend',
    'core.backends.ElggBackend'
]

ROOT_URLCONF = 'pleio_account.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'constance.context_processors.config',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'pleio_account.context.app'
            ],
        },
    },
]

WSGI_APPLICATION = 'pleio_account.wsgi.application'


SESSION_ENGINE = 'user_sessions.backends.db'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/0',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    },
    'axes_cache': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient'
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'UserAttributeSimilarityValidator'
        )
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            # NIST Special Publication 800-63B Minimum for subscriber-chosen
            # passwords.
            'min_length': 8,
        }
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.CommonPasswordValidator'
        )
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    }
]

AUTH_USER_MODEL = 'core.User'

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('en', _('English')),
    ('fr', _('French'))
]

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

TIME_ZONE = 'America/Toronto'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'assets/'),
]

GEOIP_PATH = os.path.join(BASE_DIR, 'assets/geopip2/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/profile/'
LOGOUT_REDIRECT_URL = '/logout/'

OIDC_USERINFO = 'pleio_account.oidc_provider_settings.userinfo'
OIDC_EXTRA_SCOPE_CLAIMS = (
    'pleio_account.oidc_provider_settings.CustomScopeClaims'
)

EMAIL_BACKEND = "core.backends.SiteConfigEmailBackend"

PASSWORD_RESET_TIMEOUT_DAYS = 1

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}

# RabbitMq settings
MQ_USER = ""
MQ_PASSWORD = ""
MQ_CONNECTION = ""

# Axes Lockout
AXES_CACHE = 'axes_cache'
AXES_COOLOFF_TIME = timedelta(minutes=5)
AXES_LOCKOUT_TEMPLATE = 'locked_out.html'
AXES_ONLY_USER_FAILURES = True
AXES_USERNAME_FORM_FIELD = 'auth-username'
AXES_PASSWORD_FORM_FIELD = 'auth-password'
AXES_FAILURE_LIMIT=5
AXES_PROXY_COUNT=1


CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_IGNORE_ADMIN_VERSION_CHECK = True
CONSTANCE_ADDITIONAL_FIELDS = {
    'security_selector': ['django.forms.fields.ChoiceField', {
        'widget': 'django.forms.Select',
        'choices': (
            ('none', 'None'),
            ('ssl', 'SSL'),
            ('tls', 'TLS')
        )
    }],
    'color_picker': ['django.forms.fields.CharField', {
        'widget': 'django.forms.TextInput',
        'widget_kwargs': {
            'attrs': {
                'placeholder': '#000000',
                'type': 'color'
            }
        },
        'max_length': 7,
    }],
    'image_field': ['django.forms.fields.ImageField', {
        'required': False
    }],
    'bg_image_selector': ['django.forms.fields.ChoiceField', {
        'widget': 'django.forms.Select',
        'choices': (
            ('C', 'Cover'),
            ('T', 'Tiled')
        )
    }],
    'url': ['django.forms.fields.URLField', {
        'required': False
    }],
    'email': ['django.forms.fields.EmailField', {
        'required': False
    }]
}
CONSTANCE_CONFIG = {
    'ELGG_URL': ('https://gccollab.ca', 'Elgg URL', str),

    'FRESHDESK_URL': ('', 'Freshdesk URL', 'url'),
    'FRESHDESK_SECRET_KEY': ('', 'Freshdesk Secret Key', str),

    'EMAIL_FROM': ('', 'Address to use when sending email', 'email'),
    'EMAIL_HOST': ('', 'SMTP Host', str),
    'EMAIL_PORT': (25, 'SMTP Port', int),
    'EMAIL_USER': ('', 'SMTP Username', str),
    'EMAIL_PASS': ('', 'SMTP Paswsord', str),
    'EMAIL_TIMEOUT': (5, 'SMTP Timeout', int),
    'EMAIL_SECURITY': ('none', 'SMTP Security', 'security_selector'),
    'EMAIL_FAIL_SILENTLY': (False, 'Should sending email fail quietly?', bool),

    'ACCOUNT_ACTIVATION_DAYS': (7, '', int),
    'GRAPHQL_TRIGGER':(False, 'Get information from Profile as a Service', bool),
    'GRAPHQL_ENDPOINT':('', 'Profile as a Service Endpoint', 'url'),

    'APP_TITLE': ('', 'Name to use for branding.', str),
    'APP_BRAND_COLOR': ('#2185d0', 'Primary branding color.', 'color_picker'),
    'APP_LOGO': ('', 'Logo to use for branding.', 'image_field'),
    'APP_FAVICON': ('', '', 'image_field'),
    'APP_BACKGROUND_IMAGE': (
        '',
        'Image to use for the background.',
        'image_field'
    ),
    'APP_BACKGROUND_OPTIONS': (
        '',
        'How to display the background image.',
        'bg_image_selector',
    ),
    'APP_HELPDESK_LINK': ('', '', 'url'),
    'APP_LANGUAGE_TOGGLE': (True, 'Show the language toggle.', bool),
    'APP_USE_ALL_LANGUAGES_IN_EMAIL': (
        True,
        'Use all available langauges when sending emails.',
        bool
    ),
    'APP_FOOTER_IMAGE_LEFT': ('', '', 'image_field'),
    'APP_FOOTER_IMAGE_RIGHT': ('', '', 'image_field'),
    'RECAPTCHA_ENABLED': (
        True,
        'Enable reCAPTCHA validation on logins.',
        bool
    ),
    'RECAPTCHA_SITE_KEY': (
        '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI',
        'The reCAPTCHA site key to use (debug key by default)',
        str
    ),
    'RECAPTCHA_SECRET_KEY': (
        '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe',
        'The reCAPTCHA secret key to use (debug key by default)',
        str
    )
}
CONSTANCE_CONFIG_FIELDSETS = OrderedDict([
    ('Branding', (
        'APP_TITLE',
        'APP_BRAND_COLOR',
        'APP_LOGO',
        'APP_FAVICON',
        'APP_BACKGROUND_IMAGE',
        'APP_BACKGROUND_OPTIONS',
        'APP_HELPDESK_LINK',
        'APP_LANGUAGE_TOGGLE',
        'APP_USE_ALL_LANGUAGES_IN_EMAIL',
        'APP_FOOTER_IMAGE_LEFT',
        'APP_FOOTER_IMAGE_RIGHT'
    )),
    ('Misc.', (
        'ACCOUNT_ACTIVATION_DAYS',
        'GRAPHQL_TRIGGER',
        'GRAPHQL_ENDPOINT',
    )),
    ('Email', (
        'EMAIL_FROM',
        'EMAIL_HOST',
        'EMAIL_PORT',
        'EMAIL_USER',
        'EMAIL_PASS',
        'EMAIL_SECURITY',
        'EMAIL_FAIL_SILENTLY',
        'EMAIL_TIMEOUT'
    )),
    ('Elgg Integration', (
        'ELGG_URL',
    )),
    ('Freshdesk Integration', (
        'FRESHDESK_URL',
        'FRESHDESK_SECRET_KEY'
    )),
    ('reCAPTCHA Integration', (
        'RECAPTCHA_ENABLED',
        'RECAPTCHA_SITE_KEY',
        'RECAPTCHA_SECRET_KEY'
    ))
])

SECRET_KEY = os.environ.get('CONCIERGE_SECRET_KEY')

default_db_path = os.path.join(BASE_DIR, 'db.sqlite3')
DATABASES = {
    'default': dj_database_url.config(
        env='CONCIERGE_DATABASE_URL',
        default=f'sqlite:///{default_db_path}',
        conn_max_age=600
    )
}

try:
    allowed_hosts = os.environ['CONCIERGE_ALLOWED_HOSTS']
except KeyError:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '::1']
else:
    ALLOWED_HOSTS = ast.literal_eval(allowed_hosts)
