from {{ project_name }}.settings.base import *  # noqa

os.environ.setdefault('CACHE_HOST', '127.0.0.1:11211')
os.environ.setdefault('BROKER_HOST', '127.0.0.1:5672')

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES['default']['NAME'] = '{{ project_name }}_staging'
DATABASES['default']['USER'] = '{{ project_name }}'
DATABASES['default']['PORT'] = '{{ project_name }}'
DATABASES['default']['PASSWORD'] = '{{ project_name }}'

WEBSERVER_ROOT = '/var/www/{{ project_name }}/'

PUBLIC_ROOT = os.path.join(WEBSERVER_ROOT, 'public')

STATIC_ROOT = os.path.join(PUBLIC_ROOT, 'static')

MEDIA_ROOT = os.path.join(PUBLIC_ROOT, 'media')

LOGGING['handlers']['file']['filename'] = os.path.join(
    WEBSERVER_ROOT, 'log', '{{ project_name }}.log')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '%(CACHE_HOST)s' % os.environ,
    }
}

EMAIL_SUBJECT_PREFIX = '[{{ project_name|title }} Staging] '

COMPRESS_CSS_FILTERS = ['compressor.filters.css_default.CssAbsoluteFilter',  'compressor.filters.cssmin.CSSMinFilter']

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_ENABLED = True

COMPRESS_OFFLINE = True

ALLOWED_HOSTS = []  # TODO

# Uncomment if using celery worker configuration
# CELERY_SEND_TASK_ERROR_EMAILS = True
# BROKER_URL = 'amqp://{{ project_name }}_staging:%(BROKER_PASSWORD)s@%(BROKER_HOST)s/{{ project_name }}_staging' % os.environ  # noqa
