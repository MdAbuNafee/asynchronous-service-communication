from django.db import models

from asynchronous_service_communication import constant


class DecisionInstance(models.Model):
    station_id = models.UUIDField()
    driver_token = models.CharField(max_length=constant.MAX_DRIVER_TOKEN_LENGTH)
    decision = models.CharField(
        max_length=10,
    )