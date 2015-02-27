bind = 'unix:/run/gunicorn-{{ project_name }}.sock'
workers = 2
preload_app = True
timeout = 30