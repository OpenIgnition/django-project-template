import os
import time

from contextlib import contextmanager
from fabric.api import cd, env, hosts, prefix, run, sudo, task
from fabric.contrib import django


PROJECT_NAME = '{{ project_name }}'
PROJECT_ROOT = '/var/www/%s' % PROJECT_NAME
VENV_DIR = os.path.join(PROJECT_ROOT, '.env')
REPO = 'git@github.com:OpenIgnition/{{ project_name }}.git'


env.hosts = [
    'staging',
    'production',
]

@contextmanager
def source_virtualenv():
    with prefix('source ' + os.path.join(VENV_DIR, 'bin/activate')):
        yield

@task
def staging():
    env.hosts = ['centos@host']
    env.environment = 'staging'


@task
def production():
    env.hosts = ['centos@host']
    env.environment = 'production'


@task
def bootstrap():
    sudo('chmod 777 /run')

    # Configure firewall
    sudo('iptables -P INPUT ACCEPT')
    sudo('iptables -F')
    sudo('iptables -A INPUT -i lo -j ACCEPT')
    sudo('iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT')
    sudo('iptables -A INPUT -p tcp --dport 22 -j ACCEPT')
    sudo('iptables -A INPUT -p tcp --dport 80 -j ACCEPT')
    sudo('iptables -A INPUT -p tcp --dport 443 -j ACCEPT')
    sudo('iptables -P INPUT DROP')
    sudo('iptables -P FORWARD DROP')
    sudo('iptables -P OUTPUT ACCEPT')
    sudo('/sbin/service iptables save')
    sudo('firewall-cmd --permanent --zone=public --add-service=ssh')
    sudo('firewall-cmd --permanent --zone=public --add-service=http')
    sudo('firewall-cmd --permanent --zone=public --add-service=https')


    # Install dev tools
    sudo('yum groupinstall -y development')
    sudo('yum install -y zlib-devel openssl-devel sqlite-devel bzip2-devel libxslt libxslt-devel libjpeg-turbo '
         'libjpeg-turbo-devel nodejs npm')
    sudo('npm install -g less')

    # Install PostgreSQL
    sudo('rpm -iUvh http://yum.postgresql.org/9.4/redhat/rhel-6-x86_64/pgdg-centos94-9.4-1.noarch.rpm')
    sudo('yum -y update')
    sudo('yum -y install postgresql94 postgresql94-server postgresql94-contrib postgresql94-libs postgresql94-devel '
         '--disablerepo=* --enablerepo=pgdg94')
    sudo('/usr/pgsql-9.4/bin/postgresql94-setup initdb')
    sudo('ln -s /usr/pgsql-9.4/bin/pg_config /usr/local/bin/pg_config')
    sudo('vi /var/lib/pgsql/9.4/data/pg_hba.conf')

    # Install services
    sudo('yum -y install htop nginx memcached supervisor')
    sudo('rm -rf /etc/nginx/conf.d/*.conf')

    # Python stuff
    sudo('yum -y install python-virtualenv python-virtualenvwrapper')

    # Enable services on boot
    sudo('systemctl enable nginx')
    sudo('systemctl enable memcached')
    sudo('systemctl enable supervisord')
    sudo('systemctl enable postgresql-9.4')

    # Start services
    sudo('systemctl restart postgresql-9.4')
    sudo('systemctl restart nginx')
    sudo('systemctl restart memcached')
    sudo('systemctl restart supervisord')

    # Create a database user and a database itself
    sudo('psql -d postgres -c "CREATE USER {0} WITH PASSWORD \'{0}\';"'.format(PROJECT_NAME), user='postgres')
    db_name = '{0}_{1}'.format(PROJECT_NAME, env.environment)
    sudo('createdb -E UTF-8 -O {0} {1}'.format(PROJECT_NAME, db_name), user='postgres')

    # Deploy a copy of the project
    sudo('mkdir -p %s' % PROJECT_ROOT)
    sudo('chown -R %s:%s %s' % (env.user, env.user, PROJECT_ROOT))
    run('git clone %s %s' % (REPO, PROJECT_ROOT))

    with cd(PROJECT_ROOT):
        run('git pull origin master')
        run('virtualenv .env')
        with source_virtualenv():
            with prefix('export DJANGO_SETTINGS_MODULE={{ project_name }}.settings.{0}'.format(env.environment)):
                run('source .env/bin/activate && pip install -r requirements/production.txt')
                run('./manage.py syncdb')
                run('./manage.py migrate')
                run('./manage.py collectstatic --noinput')
                run('./manage.py compress')

    # Deploy web and app server configs
    sudo('cat {project_root}/deploy/{environment}/supervisor.conf >> /etc/supervisord.conf'.format(
        project_root=PROJECT_ROOT, environment=env.environment))
    sudo('ln -s {project_root}/deploy/{environment}/nginx.conf /etc/nginx/conf.d/{project_name}.conf'.format(
        project_root=PROJECT_ROOT, environment=env.environment, project_name=PROJECT_NAME))

    restart()


@task
def deploy():
    sudo('chown -R %s:%s %s' % (env.user, env.user, PROJECT_ROOT))

    with cd(PROJECT_ROOT):
        run('git pull origin master')
        with source_virtualenv():
            with prefix('export DJANGO_SETTINGS_MODULE={{ project_name }}.settings.{0}'.format(env.environment)):
                run('source .env/bin/activate && pip install -r requirements/production.txt')
                run('./manage.py syncdb')
                run('./manage.py migrate')
                run('./manage.py collectstatic --noinput')
                run('./manage.py compress')

    restart()


@task
def clean():
    sudo('find . -name \'*.py?\' -exec rm -rf {} \;')


def restart():
    sudo('service supervisord restart')
    sudo('service memcached restart')
    sudo('service nginx restart')
