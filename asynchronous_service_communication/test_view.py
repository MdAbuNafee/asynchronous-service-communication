import unittest

from django.test import Client


class ViewTests(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_valid_request(self):
        response = self.client.post(
            path='/charge_point/session/',
            data={
                "station_id": "123e4567-e89b-12d3-a456-426614174000",
                "driver_token": "validDriverToken1234567",
                "callback_url": "https://webhook.site/a02530e4-62e6-433b-ae31-d1392e823f12"
            },
            content_type="application/json",
        )
        assert response.status_code == 200
        self.assertDictEqual(
            d1=response.json(),
            d2={
            "status": "accepted",
            "message": "Request is being processed asynchronously. The result will be sent to the provided callback URL."
        })

    def test_not_valid_request_body(self):
        response = self.client.post(
            path='/charge_point/session/',
            data={
                "station_id": "123e4567-e89b-12d3-a456-42661417400",
                "driver_token": "valid",
                "callback_url": "https://webhook/a02530e4-62e6-433b-ae31-d1392e823f12"
            },
            content_type="application/json",
        )
        assert response.status_code == 400
        self.assertDictEqual(
            d1=response.json(),
            d2={
            "status": "failed",
            "error": "station id is not a valid uuid \n"
                'driver token len is 5. But it should be between 20 and 80 '
                    'characters \n'
                'callback_url is not a valid URL'
        })

    def test_get_request_should_post(self):
        response = self.client.get(
            path='/charge_point/session/',
        )
        assert response.status_code == 400
        self.assertDictEqual(
            d1=response.json(),
            d2={
                "status": "failed",
                "error": f"Invalid request method. request is "
                f"GET. But should be POST."
            })
