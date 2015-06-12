from {{ project_name }}.settings.staging import *   # noqa

# There should be only minor differences from staging

DATABASES['default']['NAME'] = '{{ project_name }}_production'

EMAIL_SUBJECT_PREFIX = '[{{ project_name|title }} Prod] '

ALLOWED_HOSTS = []  # TODO

# Uncomment if using celery worker configuration
# BROKER_URL = 'amqp://{{ project_name }}_production:%(BROKER_PASSWORD)s@%(BROKER_HOST)s/{{ project_name }}_production' % os.environ  # noqa