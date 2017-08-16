from django.http.response import HttpResponseBase
from django.test import TestCase
from .middleware import TemplarbitMiddleware


class Test1(TestCase):
    def setUp(self):
        self.response = HttpResponseBase()
        self.params = {
            "templarbit_fetch_interval": 5,
            "templarbit_api_url": "https://api.tb-stag-01.net/v1"
        }

    def test_process_response_return_valid(self):
        self.middleware = TemplarbitMiddleware(
            templarbit_property_id="571f4f43-ad7a-415d-894b-1a1f234899db",
            templarbit_api_token="return_valid",
            **self.params
        )
        response = self.middleware.process_response(None, self.response)
        if 'content-security-policy' not in response._headers:
            self.fail('status api 200: Content-Security-Policy header is missing.')
        if 'content-security-policy-report-only' not in response._headers:
            self.fail('status api 200: Content-Security-Policy-Report-Only is missing.')

    def test_process_response_return_invalid(self):
        self.middleware = TemplarbitMiddleware(
            templarbit_property_id="571f4f43-ad7a-415d-894b-1a1f234899db",
            templarbit_api_token="return_invalid",
            **self.params
        )
        response = self.middleware.process_response(None, self.response)
        if 'content-security-policy' in response._headers:
            self.fail('status api invalid: Content-Security-Policy exists.')
        if 'content-security-policy-report-only' in response._headers:
            self.fail('status api invalid: Content-Security-Policy-Report-Only exists.')

    def test_process_response_return_error(self):
        self.middleware = TemplarbitMiddleware(
            templarbit_property_id="571f4f43-ad7a-415d-894b-1a1f234899db",
            templarbit_api_token="return_error",
            **self.params
        )
        response = self.middleware.process_response(None, self.response)
        if 'content-security-policy' in response._headers:
            self.fail('status api error: Content-Security-Policy exists.')
        if 'content-security-policy-report-only' in response._headers:
            self.fail('status api error: Content-Security-Policy-Report-Only exists.')

    def test_process_response_return_500(self):
        self.middleware = TemplarbitMiddleware(
            templarbit_property_id="571f4f43-ad7a-415d-894b-1a1f234899db",
            templarbit_api_token="return_500",
            **self.params
        )
        response = self.middleware.process_response(None, self.response)
        if 'content-security-policy' in response._headers:
            self.fail('status api 500: Content-Security-Policy exists.')
        if 'content-security-policy-report-only' in response._headers:
            self.fail('status api 500: Content-Security-Policy-Report-Only exists.')

    def test_process_response_return_401(self):
        self.middleware = TemplarbitMiddleware(
            templarbit_property_id="571f4f43-ad7a-415d-894b-1a1f234899db",
            templarbit_api_token="return_401",
            **self.params
        )
        response = self.middleware.process_response(None, self.response)
        if 'content-security-policy' in response._headers:
            self.fail('status api 401: Content-Security-Policy exists.')
        if 'content-security-policy-report-only' in response._headers:
            self.fail('status api 401: Content-Security-Policy-Report-Only exists.')

    def test_process_response_missing_property_id(self):
        self.middleware = TemplarbitMiddleware(
            templarbit_property_id="",
            templarbit_api_token="return_valid",
            **self.params
        )
        response = self.middleware.process_response(None, self.response)
        if 'content-security-policy' in response._headers:
            self.fail('missing property id:  Content-Security-Policy exists.')
        if 'content-security-policy-report-only' in response._headers:
            self.fail('missing property id: Content-Security-Policy-Report-Only exists.')

    def test_process_response_missing_api_token(self):
        self.middleware = TemplarbitMiddleware(
            templarbit_property_id="571f4f43-ad7a-415d-894b-1a1f234899db",
            templarbit_api_token="",
            **self.params
        )
        response = self.middleware.process_response(None, self.response)
        if 'content-security-policy' in response._headers:
            self.fail('missing api token: Content-Security-Policy exists.')
        if 'content-security-policy-report-only' in response._headers:
            self.fail('missing api token: Content-Security-Policy-Report-Only exists.')

    def test_process_response_invalid_property_id(self):
        self.middleware = TemplarbitMiddleware(
            templarbit_property_id="571f4f43-ad7a-415d-894b-1a1f234899db12",
            templarbit_api_token="return_500",
            **self.params
        )
        response = self.middleware.process_response(None, self.response)
        if 'content-security-policy' in response._headers:
            self.fail('missing api token: Content-Security-Policy exists.')
        if 'content-security-policy-report-only' in response._headers:
            self.fail('missing api token: Content-Security-Policy-Report-Only exists.')
