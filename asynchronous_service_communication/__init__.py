from asynchronous_service_communication.celery_config import app as celery_app
import logging
import os

service_name = os.environ.get("service_name", "django")


__all__ = ["celery_app"]
logger = logging.getLogger(service_name)
