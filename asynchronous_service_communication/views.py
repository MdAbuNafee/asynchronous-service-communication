import json
import asyncio

from django.http import JsonResponse


from django.views.decorators.csrf import csrf_exempt

from asynchronous_service_communication import helper
# from tasks import get_decision
from asynchronous_service_communication import tasks

@csrf_exempt
def post_session(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    post_data = json.loads(request.body)
    print("inside post_session = " + str(post_data))
    post_data_validity_error = get_session_post_data_validity_error(
        post_data=post_data
    )
    if len(post_data_validity_error) > 0:
        return JsonResponse(
            {'error': "\n".join(post_data_validity_error)}, status=400
        )
    station_id = post_data.get('station_id')
    driver_token = post_data.get('driver_token')
    callback_url = post_data.get('callback_url')

    tasks.make_decision.delay(
        station_id=station_id,
        driver_token=driver_token,
        callback_url=callback_url,
    )

    # asyncio.run(forward_data_to_internal_authorization_service(post_data))
    return JsonResponse({'success': True})


def get_session_post_data_validity_error(post_data: dict[str, str]) -> list[str]:
    validity_errors = []
    try:
        station_id = post_data['station_id']
        if not helper.is_valid_uuid(uuid_to_test=station_id):
            validity_errors.append('station id is not a valid uuid')

        driver_token = post_data['driver_token']
        driver_token_validity_error = helper.get_driver_token_validity_error(
            driver_token=driver_token
        )
        validity_errors.extend(driver_token_validity_error)

        if 'callback_url' not in post_data:
            validity_errors.append('callback_url is missing')
    except:
        validity_errors.append('invalid post data. failed to validate')
    return validity_errors


async def forward_data_to_internal_authorization_service(post_data: dict[str,
str]) -> None:
    await asyncio.sleep(10)
    print("inside forward_data_to_internal_authorization_service")
    return None

#
# class SessionView(View):
#     def post(self, request):
#         post_data = json.loads(request.body.decode('utf-8'))
#         print(post_data)
#         return JsonResponse(post_data)
#
