import multiprocessing

name = "Gunicorn config for FastAPI"


bind = "0.0.0.0:8000"

worker_class = "uvicorn.workers.UvicornWorker"
