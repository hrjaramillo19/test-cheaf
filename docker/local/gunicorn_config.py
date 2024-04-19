# gunicorn_config.py

bind = '0.0.0.0:8005'
workers = 4
timeout = 120
worker_class = 'gevent'