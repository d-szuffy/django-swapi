"""
This module handles fetching data from an API endpoint. Fetched data gets converted to JSON format
and then written to a CSV file.
"""
import collections

import requests
import itertools
import pathlib
import petl
import json
from requests.exceptions import ConnectionError


class FetchData(object):

    def fetch_data(self, url):
        try:
            response = requests.get(url)
            data = []
            page = response.json()
            data.append(page["results"])
            # while page["next"]:
            #     response = requests.get(page["next"])
            #     page = response.json()
            #     data.append(page["results"])
            return list(itertools.chain.from_iterable(data))
        except ConnectionError:
            return None

    def create_csv_file(self):
        people = self.fetch_data("https://swapi.dev/api/people/")
        homeworlds = self.fetch_data("https://swapi.dev/api/people/")
        people_table = petl.fromdicts(people, header=[key for key in people[0].keys()])
        homeworlds_table = petl.fromdicts(homeworlds, header=[key for key in people[0].keys()])
        return people_table
        # for person in people:
        #     homeworld_id = person["homeworld"].split("/")[-1]
        #     person["homeworld"]
