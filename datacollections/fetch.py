import requests
import json
from requests.exceptions import ConnectionError


class FetchData(object):

    def fetch_data(self, url):
        try:
            r = requests.get(url)
            return r.text
        except ConnectionError:
            return None
