from datetime import timezone

from datetime import timedelta
from time import sleep

from django.core.management.base import BaseCommand
from django.utils import timezone

from asynchronous_service_communication import (
    logger,
    callback,
    decision_data_access,
)
from asynchronous_service_communication.constant import (
    DecisionTypes,
    DecisionTakenByTypes,
    CRON_JOB_SLEEP_TIME_IN_SECONDS,
    TIMEOUT_IN_SECONDS,
)
from asynchronous_service_communication.decision_data_access import save_decision


class Command(BaseCommand):
    help = "Gives unknown decision after timeout"

    def handle(self, *args, **options):
        logger.info(f"CRON_JOB_SLEEP_TIME_IN_SECONDS = {CRON_JOB_SLEEP_TIME_IN_SECONDS}")
        logger.info(f"given unknown decision after "
                    f" {TIMEOUT_IN_SECONDS} seconds")
        while True:
            logger.info("\n\nstarting of cron job")
            target_time = timezone.now() - timedelta(
                hours=0,
                seconds=int(TIMEOUT_IN_SECONDS),
            )
            logger.info(f"target_time: {target_time}")
            decision_instance_list = (
                decision_data_access.get_unattened_decision_instance(
                    target_time=target_time,
                )
            )
            logger.info("decision_instance_list: {}".format(decision_instance_list))
            for decision_instance in decision_instance_list:
                logger.info(
                    f"before changing decision_instance:" f" {decision_instance}"
                )
                decision_instance = save_decision(
                    primary_key=decision_instance.pk,
                    decision=DecisionTypes.UNKNOWN,
                    decision_taken_by=DecisionTakenByTypes.CRON_JOB,
                )
                logger.info(f"after changing decision_instance: {decision_instance}")
                callback.make_callback(
                    station_id=str(decision_instance.station_id),
                    driver_token=str(decision_instance.driver_token),
                    status=str(decision_instance.decision),
                    callback_url=str(decision_instance.callback_url),
                )
            logger.info(f"end of cron job")
            logger.info(f"Sleeping for : {CRON_JOB_SLEEP_TIME_IN_SECONDS} " f"seconds")
            sleep(CRON_JOB_SLEEP_TIME_IN_SECONDS)
