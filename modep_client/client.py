import logging

import requests

logger = logging.getLogger(__name__)


class Client(object):
    def __init__(self, api_key, url="https://modep.ai/v1/", ensure_https=True):
        """
        Initialize a ModepClient object.

        :param str api_key: Your API key from the modep.ai account page (https://modep.ai/account)
        :param str url: The base URL of the modep.ai API
        :param bool ensure_https: If True, will ensure that the URL starts with https
        """

        if ensure_https and not url.startswith("https://"):
            raise Exception("The url should start with https://")

        # ensure trailing "/"
        url = url if url[-1] == "/" else url + "/"

        self.url = url
        self.api_key = api_key

        self.login()

    def response_exception(self, response):
        """ Raise an exception from a response """

        raise Exception(
            f"status_code: {response.status_code}, reason: {response.reason}, text: {response.text}"
        )

    def login(self):
        """ Login to the API """

        url = self.url + "login"

        # this is the JWT header required for protected endpoints
        self._auth_header = None

        # start a new session
        self.sess = requests.Session()

        # make login request
        resp = self.sess.post(url, json=dict(api_key=self.api_key))
        if resp.ok:
            access_token = resp.json()["access_token"]
            self._auth_header = {"Authorization": f"Bearer {access_token}"}
            logger.debug(self._auth_header)
        else:
            self.response_exception(resp)

    def auth_header(self):
        """ Get the JWT authorization header """
        url = self.url + "ping"
        resp = self.sess.get(url, headers=self._auth_header)
        if resp.ok:
            return self._auth_header

        if resp.status_code in (401, 500):
            # auth token has expired, so get a new one
            self.login()
            return self._auth_header
