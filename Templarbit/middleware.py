import time
import requests
import multiprocessing
from .templarbit_settings import TEMPLARBIT_PROPERTY_ID, \
    TEMPLARBIT_API_TOKEN, TEMPLARBIT_FETCH_INTERVAL, TEMPLARBIT_API_URL

import logging
logger = logging.getLogger(__name__)


class TemplarbitProc:
    __slots__ = (
        'templarbit_property_id', 'templarbit_api_token', 'templarbit_fetch_interval', 'templarbit_api_url',
        'data', 'headers', 'params'
    )

    def __init__(self, data, templarbit_property_id, templarbit_api_token,
                 templarbit_fetch_interval=5, templarbit_api_url='https://api.templarbit.com/v1'):
        self.data = data
        self.templarbit_property_id = templarbit_property_id
        self.templarbit_api_token = templarbit_api_token
        self.templarbit_fetch_interval = templarbit_fetch_interval
        self.templarbit_api_url = templarbit_api_url
        self.headers = {
            "Content-Type": "application/json"
        }
        self.params = {
            "token": self.templarbit_api_token,
            "property_id": self.templarbit_property_id
        }

    def templarbit_loop(self):
        while True:
            try:
                templarbit_request = requests.post(
                    url=self.templarbit_api_url + "/csp",
                    headers=self.headers,
                    params=self.params
                )

                if templarbit_request.status_code == 401:
                    logger.warning("invalid templarbit_api_token and/or templarbit_property_id")
                elif templarbit_request.status_code != 200:
                    logger.warning("Fetch failed, returned status {}".format(templarbit_request.status_code))
                else:
                    result_data = templarbit_request.json()

                    if not result_data['csp'] and not result_data['csp_report_only']:
                        logger.warning("Fetch successful, but Content-Security-Policy was empty.")
                    else:
                        self.data['csp'] = result_data['csp']
                        self.data['csp_report_only'] = result_data['csp_report_only']

                time.sleep(self.templarbit_fetch_interval)
            except KeyboardInterrupt:
                pass
            finally:
                break

    def start_proc(self):
        if not self.templarbit_property_id:
            logger.warning('templarbit_property_id not set')
        if not self.templarbit_api_token:
            logger.warning('templarbit_api_token not set')

        if self.templarbit_property_id and self.templarbit_api_token:
            proc = multiprocessing.Process(name="templarbit-process", target=self.templarbit_loop)
            proc.start()
            proc.join()


class TemplarbitMiddleware:
    __slots__ = ('manager', 'data', 'templarbit_proc')

    def __init__(self, templarbit_property_id=TEMPLARBIT_PROPERTY_ID, templarbit_api_token=TEMPLARBIT_API_TOKEN,
                 templarbit_fetch_interval=TEMPLARBIT_FETCH_INTERVAL, templarbit_api_url=TEMPLARBIT_API_URL):
        self.manager = multiprocessing.Manager()
        self.data = self.manager.dict({"csp": "", "csp_report_only": ""})
        self.templarbit_proc = TemplarbitProc(
            self.data,
            templarbit_property_id=templarbit_property_id,
            templarbit_api_token=templarbit_api_token,
            templarbit_fetch_interval=templarbit_fetch_interval,
            templarbit_api_url=templarbit_api_url
        )
        self.templarbit_proc.start_proc()

    def process_response(self, request, response):
        csp_header = self.data["csp"]
        if csp_header:
            response['Content-Security-Policy'] = str(csp_header)

        csp_report_only = self.data["csp_report_only"]
        if csp_report_only:
            response['Content-Security-Policy-Report-Only'] = str(csp_report_only)

        return response

