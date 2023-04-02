import os

bind = "0.0.0.0:8000"
workers = os.getenv("GUNICORN_WORKER_NUM", 8)
worker_class = "uvicorn.workers.UvicornWorker"
accesslog = "-"
errorlog = "-"
