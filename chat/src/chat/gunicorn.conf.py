# Gunicorn configuration file
# https://docs.gunicorn.org/en/stable/settings.html

from chat.core.config import get_settings

settings = get_settings()

# Server socket
bind = f"{settings.server.host}:{settings.server.port}"

# Worker processes
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
