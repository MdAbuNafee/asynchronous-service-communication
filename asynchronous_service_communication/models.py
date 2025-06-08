from django.db import models

from asynchronous_service_communication import constant


class DecisionInstance(models.Model):
    station_id = models.UUIDField()
    driver_token = models.CharField(
        max_length=constant.MAX_DRIVER_TOKEN_LENGTH
    )
    decision = models.CharField(
        max_length=10,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    callback_url = models.URLField(null=True, blank=True)
    decision_taken = models.BooleanField(default=False)


    def __str__(self):
        return (
            f"\n\n primary key = {self.pk}, \n"
            f"station_id = {self.station_id}, \n"
            f"driver_token = {self.driver_token},  \n"
            f"created_at = {self.created_at}, \n"
            f"decision = {self.decision}, \n "
            f"updated_at = {self.updated_at}, \n"
            f"decision_taken = {self.decision_taken}, \n"
            f"callback_url = {self.callback_url}, \n\n"
        )
