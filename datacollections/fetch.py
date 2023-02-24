"""
This module handles fetching data from an API endpoint. Fetched data gets converted to JSON format, transformed
and then written to a CSV file.
"""
import collections

import requests
import itertools
import time
import os
import pathlib
import petl
import json
from requests.exceptions import ConnectionError

WORK_DIR = os.getcwd()

class FetchData(object):

    def fetch_data(self, url):
        try:
            response = requests.get(url)
            data = []
            page = response.json()
            data.append(page["results"])
            while page["next"]:
                response = requests.get(page["next"])
                page = response.json()
                data.append(page["results"])
            return list(itertools.chain.from_iterable(data))
        except ConnectionError:
            return None

    def transform_data(self):
        people = self.fetch_data("https://swapi.dev/api/people/")
        homeworlds = self.fetch_data("https://swapi.dev/api/people/")

    def create_csv_file(self):
        people = self.fetch_data("https://swapi.dev/api/people/")
        homeworlds = self.fetch_data("https://swapi.dev/api/planets/")
        for person in people:
            id_ = person["homeworld"].split("/")[-2]
            person["homeworld"] = homeworlds[int(id_) - 1]["name"]
        people_table = petl.fromdicts(people, header=[key for key in people[0].keys()])
        homeworlds_table = petl.fromdicts(homeworlds, header=[key for key in people[0].keys()])
        file_name = f"datacollections/media/{str(time.time())}"
        path = os.path.join(WORK_DIR, file_name)
        petl.tocsv(people_table, path)
        return get_media_files_names(os.path.join(WORK_DIR, 'datacollections/media'))


# *** defined this method outside FetchData class because I also use it in the FTs ****
def get_media_files_names(directory):
    files = []
    for filename in os.listdir(directory):
        files.append(filename)
    return files
