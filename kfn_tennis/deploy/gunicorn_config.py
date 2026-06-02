import multiprocessing


bind = '127.0.0.1:8001'
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
timeout = 60
graceful_timeout = 30
keepalive = 5
max_requests = 1000
max_requests_jitter = 100
accesslog = '-'
errorlog = '-'
loglevel = 'info'
