import multiprocessing

wsgi_app = "poll4dates.wsgi:application"
workers = multiprocessing.cpu_count() * 2 + 1
bind = "0.0.0.0:8000"
accesslog = '/var/log/gunicorn/access.log'
errorlog = '/var/log/gunicorn/error.log'
capture_output = True
pidfile = '/var/run/gunicorn/prod.pid'
daemon = True