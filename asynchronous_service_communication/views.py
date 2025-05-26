from django.http import JsonResponse
from django.views import View

# Create your views here.

import json

from asynchronous_service_communication.helper import is_valid_uuid


class SessionView(View):
    def post(self, request):
        post_data = json.loads(request.body.decode('utf-8'))
        print(post_data)
        return JsonResponse(post_data)

    def __is__post_data_valid(self, post_data):
        validity_errors = []

        try:
            station_id = post_data['station_id']
            driver_token = post_data['driver_token']
            callback_url = post_data['callback_url']

            if not is_valid_uuid(station_id):
                validity_errors.append('station_id is not a valid UUID')




        except:
            return False
