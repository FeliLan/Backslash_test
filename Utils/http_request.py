import json
import requests
from Utils.logging_utils import logging


class HttpRequest:
    base_url = ""

    @staticmethod
    def http_req(method, suffix, headers=None, body=None):
        """General http req, send the info of what you want to request
            and pass it to the server for handling.

        Args:
            method (str): Method of the function ("Get"/"Post"/"Put/Delete")
            suffix (str): suffix to add to server_url
            headers (dict): header to add to request. default {}
            body (dict): body (data) to add to request
        """
        if headers is None:
            headers = {"Content-Type": "application/json"}
        url = "{}{}".format(HttpRequest.base_url, suffix)
        req = ""
        try:
            if body:
                body = json.dumps(body)
            req = requests.request(method=method, url=url, headers=headers, data=body)
            assert 300 > req.status_code >= 200
            return req.json()
        except ValueError as exception:
            msg = "Could not parse json from url [{}]\nHeaders [{}]\nBody: [{}]\nText: [{}]".format(
                url, headers, body, req.text if req else "")
            logging.exception(msg)
            raise exception
        except AssertionError:
            msg = "Got unexpected status code [{}]".format(req.status_code)
            logging.exception(msg)
            raise AssertionError