import json

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

from asynchronous_service_communication import (
    tasks,
    validation,
    decision_data_access,
    logger,
)


@csrf_exempt
def post_session(request):
    if request.method != "POST":
        return JsonResponse(
            data={
                'status': 'failed',
                "error": f"Invalid request method. request is "
                f"{request.method}. But should be POST."
            },
            status=400
        )
    post_data = json.loads(request.body)
    logger.info(f"POST session request: {post_data}")
    post_data_validity_error = validation.get_session_post_data_validity_error(
        post_data=post_data
    )
    if len(post_data_validity_error) > 0:
        return JsonResponse(
            {"status": "failed", "error": " \n".join(post_data_validity_error)},
            status=400,
        )
    station_id = post_data.get("station_id")
    driver_token = post_data.get("driver_token")
    callback_url = post_data.get("callback_url")

    decision_instance = decision_data_access.create_initial_decision(
        station_id=station_id,
        driver_token=driver_token,
        callback_url=callback_url,
    )
    logger.info(f"saved decision instance: {decision_instance}")

    tasks.make_decision.delay(
        decision_instance.pk,
    )
    logger.info("passed decision instance to the "
                "internal authorization service ")

    return JsonResponse(
        {
            "status": "accepted",
            "message": "Request is being processed asynchronously. "
            "The result will be sent to the provided callback URL.",
        }
    )
