import os
import tempfile
import time

from fabric.api import env, execute, get, hide, lcd, local, put, require, run, settings, sudo, task
from fabric.colors import red
from fabric.contrib import files, project
from fabric.contrib.console import confirm
from fabric.utils import abort

PROJECT_ROOT = os.path.dirname(__file__)


@task
def staging():
    env.environment = 'staging'


@task
def production():
    env.environment = 'production'
