import requests
from config import SERVER_URL


class HttpRequest:
    base_url = SERVER_URL

    @staticmethod
    def http_req(method, suffix, headers=None, body=None):
        """General http req, send the info of what you want to request
            and pass it to the server for handling.

        Args:
            method (str): Method of the function ("Get"/"Post"/"Put/Delete")
            suffix (str): suffix to add to server_url
            headers (dict): header to add to request. default {}
            body (dict): body (data) to add to request

        Return: the request
        """
        if headers is None:
            headers = {"Content-Type": "application/json"}
        url = "{}{}".format(HttpRequest.base_url, suffix)
        req = ""
        req = requests.request(method=method, url=url, headers=headers, json=body)
        return req
