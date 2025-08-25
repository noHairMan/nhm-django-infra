# https://docs.gunicorn.org/en/23.0.0/settings.html#settings
import os

wsgi_app = "porsche.wsgi:application"
reload = False
reload_engine = "auto"
check_config = False
accesslog = "-"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
errorlog = "-"
loglevel = "info"
chdir = "."
daemon = False
pidfile = "gunicorn.pid"
user = os.geteuid()
group = os.getegid()
umask = "0o077"
bind = ["0.0.0.0:8000"]
backlog = 1000
workers = 2
worker_class = "gthread"
threads = 8
worker_connections = 1000
max_requests = 0
timeout = 30
keepalive = 2
