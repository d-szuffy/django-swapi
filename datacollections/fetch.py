"""
This module handles backend operations to fetch data from an API endpoint.
Fetched data gets converted to JSON format, transformed into petl tables
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
from requests.exceptions import ConnectionError, InvalidURL, MissingSchema, InvalidSchema
from collections import UserDict
WORK_DIR = os.getcwd()

COLUMNS = ['name',
           'height',
           'mass',
           'hair_color',
           'skin_color',
           'eye_color',
           'birth_year',
           'gender',
           'homeworld',
           'date']


class FetchData(object):

    def get_all_pages(self, page: UserDict):
        try:
            data = [page["results"]]
            while page["next"]:
                next_page = self.send_get_request_to(page["next"])
                page = next_page
                data.append(page["results"])
            return list(itertools.chain.from_iterable(data))
        except (ValueError, TypeError, IndexError, AttributeError):
            return None

    def send_get_request_to(self, url):
        try:
            response = requests.get(url)
            return response.json()
        except (ConnectionError, InvalidURL, MissingSchema, InvalidSchema):
            return None

    def get_complete_dataset(self, url):
        try:
            first_page = self.send_get_request_to(url)
            # Check if the API has more than one Page
            # If no return the page right away and exit function
            # Saves unnecessary further function calls.
            if first_page["next"]:
                dataset = self.get_all_pages(first_page)
                return dataset
            return first_page["results"]
        except TypeError:
            return None

    def transform_data(self, people, homeworlds):
        """
        This function transforms data fetched from SWAPI.

        Takes two json objects as input, and using the petl package
        converts them to tables on which transformations are performed.
        After all transformations, saves data to a .csv file

        Returns path to the created .csv file.
        """
        people_table1 = petl.fromdicts(people, header=[key for key in people[0].keys()])
        # Get the id of a homeworld from its url by splitting it on "/" and convert it to int.
        # Next, pass the id-1 value as an index of homeworlds list to get the value of "name" assigned to it.
        people_table2 = petl.convert(people_table1,
                                     'homeworld',
                                     lambda v: homeworlds[int(v.split('/')[-2]) - 1]["name"])
        # Add 'date' column based on the 'edited' column.
        # Date is in %Y-%m-%d format. Didn't use strptime() -> strftime()
        # Because after examination looks like splitting the str is simpler in this case
        people_table3 = petl.addfield(people_table2,
                                      'date',
                                      lambda rec: rec["edited"].split("T")[0])
        # Drop all unnecessary columns
        people_table4 = petl.cutout(people_table3, *COLUMNS)

        file_name = str(time.time())
        path = os.path.join(WORK_DIR, f"datacollections/media/{file_name}")
        petl.tocsv(people_table4, path)
        return file_name, path

    def create_csv_file(self):
        people = self.get_complete_dataset("https://swapi.dev/api/people/")
        homeworlds = self.get_complete_dataset("https://swapi.dev/api/planets/")
        if people is not None and homeworlds is not None:
            return self.transform_data(people, homeworlds)
        return None


# Defined this method outside FetchData class because I also use it in the FTs
def get_media_files_names(directory):
    files = []
    for filename in os.listdir(directory):
        files.append(filename)
    return files
