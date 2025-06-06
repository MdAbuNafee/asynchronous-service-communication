from .celery import app as celery_app
import logging

__all__ = ['celery_app']
logger = logging.getLogger(None)