from .celery import app as celery_app
import logging
import os
import environ

service_name = os.environ.get("service_name")


__all__ = ["celery_app"]
logger = logging.getLogger(service_name)
