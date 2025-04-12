################################################
##      Copyright, Tartabit, LLC.             ##
################################################
import copy
import requests
import urllib.parse
import json
import logging

class ApiReturn:
    status = 0
    body = None

    def __init__(self, status=0, body=None):
        self.status = status
        self.body = body

    def bodyJson(self):
        return json.dumps(self.body, indent=4)

    def bodyText(self):
        if type(self.body) is dict:
            return json.dumps(self.body, indent=4)
        else:
            return self.body

    def to_dict(self):
        return {
            'status': self.status,
            'body': self.body
        }


class IotbClient:
    url = "https://bridge-us.tartabit.com/api/v1/"
    bearer_token = "<token>"
    debug = False
    logger = logging.getLogger("iotb")

    requestHeaders = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json",
    }

    def __init__(self, url=None, token=None, user=None, password=None, debug=False, insecure=False):
        if url:
            self.url = url
        self.debug = debug
        if token:
            self.bearer_token = token
            self.requestHeaders = {
                "Authorization": f"Bearer {self.bearer_token}",
                "Content-Type": "application/json",
            }
        elif user and password:
            self.bearer_token = self.login(user, password)
            self.requestHeaders = {
                "Authorization": f"Bearer {self.bearer_token}",
                "Content-Type": "application/json",
            }
        if insecure:
            self.insecure = True
        else:
            self.insecure = False

    def login(self, user, password):
        response = self.request("POST", "login", query={"emailAddress": user, "password": password},
                                headers={"Content-Type": "application/x-www-form-urlencoded"} )
        # print(f"Body: {response} {response['token']}")
        return response.body['token']

    def request(self, method, uri, query=None, body=None, headers=None, account_id = None):
        requestHeaders = copy.copy(self.requestHeaders)
        if account_id:
            requestHeaders["Authorization"] = self.requestHeaders["Authorization"] + ':' + account_id
        if headers:
            requestHeaders = headers
        if self.debug:
            self.logger.debug(f"Request: {method} {self.url + uri}")
            self.logger.debug(f"Body: {requestHeaders}")
            self.logger.debug(f"Query: {query}")
            self.logger.debug(f"Body: {body}")
        response = requests.request(
            method=method,
            url=self.url + uri,
            params=query,
            headers=requestHeaders,
            json=body,
            verify=not self.insecure)
        try:
            response_body = response.json()  # Parse the response as JSON
            if self.debug:
                self.logger.debug("Response JSON:")
                self.logger.debug(json.dumps(response_body, indent=4))  # Pretty-print the JSON response
        except:
            try:
                response_body = response.text
            except:
                response_body = None
        return ApiReturn(response.status_code, response_body)
