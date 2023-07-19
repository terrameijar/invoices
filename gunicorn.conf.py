import multiprocessing

# workers = multiprocessing.cpu_count() * 2 + 1
workers = 4
accesslog = "-"
errorlog = "-"
bind = "0.0.0.0:8000"
