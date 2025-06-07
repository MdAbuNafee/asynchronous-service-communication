import logging
from datetime import timezone

from datetime import datetime, timedelta
from time import sleep

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.db.models.functions import Trunc

from asynchronous_service_communication import constant, models, callback
from asynchronous_service_communication import callback


class Command(BaseCommand):
    help = 'Gives unknown decision after timeout'

    def handle(self, *args, **options):
        while True:
            target_time = timezone.now() - timedelta(hours=0,
                                           seconds=constant.TIMEOUT_IN_SECONDS)
            logging.info(f"target_time: {target_time}")
            decision_instance_list = models.DecisionInstance.objects.filter(
                created_at__gte=target_time,
                decision_taken=False,
            )
            print("decision_instance_list: {}".format(decision_instance_list))
            for decision_instance in decision_instance_list:
                decision_instance.decision_taken = True
                decision_instance.save()
                callback.make_callback(
                    station_id=str(decision_instance.station_id),
                    driver_token=decision_instance.driver_token,
                    status=str(decision_instance.decision),
                    callback_url=decision_instance.callback_url,
                )
            sleep(1 * 30)


