bind = 'unix:/tmp/gunicorn-{{ project_name }}.sock'
workers = 2
preload_app = True
timeout = 30