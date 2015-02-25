import time

from fabric.api import cd, env, hosts, run, sudo, task
from fabric.contrib import django


PROJECT_NAME = '{{ project_name }}'
PROJECT_ROOT = '/var/www/%s' % PROJECT_NAME
REPO = 'git@github.com:OpenIgnition/TSFWdonor.git'


env.hosts = [
    '166.78.2.228'
]

@task
@hosts('166.78.2.228')
def staging():
    env.environment = 'staging'


@task
def production():
    env.environment = 'production'


@task
def bootstrap():
    sudo('createuser {0}'.format(PROJECT_NAME), user='postgres')
    sudo('createdb -E UTF-8 -O {user} {project_name}_{environment}'.format(
         user=PROJECT_NAME, project_name=PROJECT_NAME, environment=env.environment), user='postgres')
    sudo('mkdir -p %s' % PROJECT_ROOT)
    sudo('chown -R %s:%s %s' % (env.user, env.user, PROJECT_ROOT))
    run('git clone %s %s' % (REPO, PROJECT_ROOT))

    django.settings_module('{{ project_name }}.settings.{0}'.format(env.environment))

    with cd(PROJECT_ROOT):
        run('git pull origin master')
        run('virtualenv .env')
        run('source .env/bin/activate && pip install -r requirements/{0}.txt'.format(env.environment))
        run('source .env/bin/activate && ./manage.py syncdb')
        run('source .env/bin/activate && ./manage.py migrate')
        run('bower install')
        run('source .env/bin/activate && ./manage.py collectstatic --noinput')
        run('source .env/bin/activate && ./manage.py compress')
    chown()

    sudo('ln -s {project_root}/deploy/{environment}/supervisor.conf /etc/supervisor/conf.d/{project_name}.conf'.format(
        project_root=PROJECT_ROOT, environment=env.environment, project_name=PROJECT_NAME))
    sudo('ln -s {project_root}/deploy/{environment}/nginx.conf /etc/nginx/sites-enabled/{project_name}.conf'.format(
        project_root=PROJECT_ROOT, environment=env.environment, project_name=PROJECT_NAME))

    restart()


@task
def deploy():
    pass


@task
def clean():
    sudo('find . -name \'*.py?\' -exec rm -rf {} \;')


@task
def chown():
    sudo('chown -R django:django {0}'.format(PROJECT_ROOT))


def restart():
    sudo('supervisorctl reload')
    time.sleep(5)
    sudo('supervisorctl restart {0}'.format(PROJECT_NAME))
    sudo('service memcached restart')
    sudo('service nginx restart')


@task
def compress():
    sudo('chown -R %s:%s %s' % (env.user, env.user, PROJECT_ROOT))

    django.settings_module('{{ project_name }}.settings.{0}'.format(env.environment))

    with cd(PROJECT_ROOT):
        run('source .env/bin/activate && ./manage.py compress')
    chown()
