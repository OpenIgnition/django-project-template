# Django settings for {{ project_name }} project.
import json
import os
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, os.pardir))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '{{ project_name }}',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-US'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'public', 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'public', 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '{{ secret_key }}'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'reversion.middleware.RevisionMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware'
)

SITE_ID = 1

ROOT_URLCONF = '{{ project_name }}.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = '{{ project_name }}.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

FIXTURE_DIRS = (
    os.path.join(BASE_DIR, 'fixtures'),
)

INSTALLED_APPS = (
    'grappelli',
    'filebrowser',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django.contrib.redirects',
    'django.contrib.admin',

    # External apps
    'haystack',
    'crispy_forms',
    'raven.contrib.django.raven_compat',
    'compressor',
    'south',
    'tinymce',
    'mptt',
    'reversion',
    'sorl.thumbnail',
    'robots',

    # CMS
    'bonfire',

    # Project itself
    '{{ project_name }}'
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'basic': {
            'format': '%(asctime)s %(name)-20s %(levelname)-8s %(message)s',
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'basic',
            'filename': os.path.join(PROJECT_ROOT, '{{ project_name }}.log'),
            'maxBytes': 10 * 1024 * 1024,  # 10 MB
            'backupCount': 10,
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        '{{ project_name }}': {
            'handlers': ['file', 'mail_admins'],
            'level': 'INFO',
        },
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# Application settings
COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)

# Haystack
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(PROJECT_ROOT, 'whoosh_index'),
    },
}

# Bonfire
PROJECT_DIR = BASE_DIR

TEMPLATES = {}
PAGES_TEMPLATE_DIR = os.path.join(PROJECT_DIR, 'templates/pages')

for template in os.listdir(PAGES_TEMPLATE_DIR):
    _file = open(os.path.join(PAGES_TEMPLATE_DIR, template))
    content = _file.readline()
    template_name = re.findall("template-name:\"([^\"]+)\"", content)
    if template_name:
        TEMPLATES[template_name[0]] = {"template_file": "pages/" + template}
    else:
        TEMPLATES[template] = {"template_file": "pages/" + template}

BONFIRE_CONFIG = {
    "WIDGET_PATHS": ("main.widgets", ),
    "PAGES_PATHS": ("pages", ),
    "WIDGETS": {"FormWidget": {"FORM_PATHS": ("main.forms", )}}
}

LOGIN_URL = "/bonfire/login/"

def tinymce_get_style_formats():
    #load custom_formats file
    try:
        cf_file = open(os.path.join(PROJECT_DIR, 'static', 'custom_formats.json'))
    except IOError, e:
        cf_file = None
        pass
    try:
        cf_json = json.loads(cf_file.read())
        cf_json["style_formats"]
    except:
        cf_json = {"style_formats": [
            {"title": "Headers", "items": [
                {"title": "Header 1", "format": "h1"},
                {"title": "Header 2", "format": "h2"},
                {"title": "Header 3", "format": "h3"},
                {"title": "Header 4", "format": "h4"},
                {"title": "Header 5", "format": "h5"},
                {"title": "Header 6", "format": "h6"}
            ]},
            {"title": "Inline", "items": [
                {"title": "Bold", "icon": "bold", "format": "bold"},
                {"title": "Italic", "icon": "italic", "format": "italic"},
                {"title": "Underline", "icon": "underline", "format": "underline"},
                {"title": "Strikethrough", "icon": "strikethrough", "format": "strikethrough"},
                {"title": "Superscript", "icon": "superscript", "format": "superscript"},
                {"title": "Subscript", "icon": "subscript", "format": "subscript"},
                {"title": "Code", "icon": "code", "format": "code"}
            ]},
            {"title": "Blocks", "items": [
                {"title": "Paragraph", "format": "p"},
                {"title": "Blockquote", "format": "blockquote"},
                {"title": "Div", "format": "div"},
                {"title": "Pre", "format": "pre"}
            ]},
            {"title": "Alignment", "items": [
                {"title": "Left", "icon": "alignleft", "format": "alignleft"},
                {"title": "Center", "icon": "aligncenter", "format": "aligncenter"},
                {"title": "Right", "icon": "alignright", "format": "alignright"},
                {"title": "Justify", "icon": "alignjustify", "format": "alignjustify"}
            ]}],
                   }
    return cf_json["style_formats"]


def tinymce_get_css():
    try:
        cf_file = open(os.path.join(PROJECT_DIR, 'static', 'custom_formats.json'))
    except IOError, e:
        cf_file = None
        pass

    try:
        cf_json = json.loads(cf_file.read())
        cf_json["content_css"]
    except:
        cf_json = {"content_css": []}

    return map(lambda x: STATIC_URL + x, cf_json["content_css"])


TINYMCE_DEFAULT_CONFIG = {
    'plugins': "advlist, anchor, charmap, code, contextmenu, fullscreen, image, link, "
               "lists, media, paste, preview, print, searchreplace, table, wordcount",
    'skin': "lightgray",
    'custom_undo_redo_levels': 10,
    'width': "700px",
    'style_formats': tinymce_get_style_formats(),
    'content_css': tinymce_get_css(),
    'extended_valid_elements': 'a[class|href|onmouseover|onmouseout|onclick]',
}

ADMIN_TITLE = "Bonfire - Admin Backend"

CRISPY_TEMPLATE_PACK = 'bootstrap3'

# django-filebrowser
FILEBROWSER_DIRECTORY = ''
