from datetime import timezone

from datetime import timedelta
from time import sleep

from django.core.management.base import BaseCommand
from django.utils import timezone

from asynchronous_service_communication import (
    constant,
    logger,
    callback,
    decision_data_access,
)


class Command(BaseCommand):
    help = "Gives unknown decision after timeout"

    def handle(self, *args, **options):
        while True:
            target_time = timezone.now() - timedelta(
                hours=0,
                seconds=constant.TIMEOUT_IN_SECONDS,
            )
            logger.info(f"target_time: {target_time}")
            decision_instance_list = (
                decision_data_access.get_unattened_decision_instance(
                    target_time=target_time,
                )
            )
            logger.info("decision_instance_list: {}".format(decision_instance_list))
            for decision_instance in decision_instance_list:
                decision_instance.decision_taken = True
                decision_instance.save()
                callback.make_callback(
                    station_id=str(decision_instance.station_id),
                    driver_token=str(decision_instance.driver_token),
                    status=str(decision_instance.decision),
                    callback_url=str(decision_instance.callback_url),
                )
            sleep(1 * 30)
