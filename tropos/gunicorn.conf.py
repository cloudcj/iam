# # gunicorn.conf.py
# import multiprocessing

# # bind = "127.0.0.1:8001"  # or "0.0.0.0:8000" for public access
# bind = "unix:run/gunicorn.sock"
# workers = multiprocessing.cpu_count() * 2 + 1
# accesslog = "logs/gunicorn-access.log"
# errorlog = "logs/gunicorn-error.log"
# loglevel = "info"

import multiprocessing
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

bind = f"unix:{BASE_DIR}/run/gunicorn.sock"

workers = multiprocessing.cpu_count() * 2 + 1

accesslog = f"{BASE_DIR}/logs/gunicorn-access.log"
errorlog = f"{BASE_DIR}/logs/gunicorn-error.log"

loglevel = "info"
