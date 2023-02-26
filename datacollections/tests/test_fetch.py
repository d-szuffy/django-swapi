import itertools

from django.test import TestCase

import datacollections.fetch
from datacollections.models import DataSet
from unittest.mock import patch, Mock
from datacollections.fetch import FetchData
from requests.exceptions import ConnectionError, InvalidURL, MissingSchema
from datacollections.fetch import FetchData, COLUMNS
from .constants import PAGE_PEOPLE, LAST_PAGE_PEOPLE, PAGE_PLANETS
import petl


class TestFetchData(TestCase):

    @patch('datacollections.fetch.requests.get')
    def test_send_get_request_to(self, mock_get):
        mock_response = Mock()

        mock_response.json.return_value = PAGE_PEOPLE
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = FetchData().send_get_request_to("test.com")

        self.assertEqual(result, PAGE_PEOPLE)

    def test_get_people_return_None_with_invalid_input(self):
        self.assertEqual(FetchData().send_get_request_to("https://wrong.url"), None)

    @patch('datacollections.fetch.FetchData.send_get_request_to')
    def test_get_all_pages_merges_pages_to_list(self, mock_send_req_to):
        mock_send_req_to.return_value = LAST_PAGE_PEOPLE

        result = FetchData().get_all_pages(PAGE_PEOPLE)

        self.assertEqual(mock_send_req_to.called, True)
        self.assertEqual(result, list(itertools.chain.from_iterable([PAGE_PEOPLE["results"], LAST_PAGE_PEOPLE["results"]])))

    def test_get_all_pages_returns_None_with_invalid_input(self):
        self.assertEqual(FetchData().get_all_pages("invalid"), None)

    @patch('datacollections.fetch.FetchData.get_all_pages')
    @patch('datacollections.fetch.FetchData.send_get_request_to')
    def test_get_complete_dataset_returns_first_page_only(self,
                                                          mock_send_req_to,
                                                          mock_get_all_pages):
        mock_send_req_to.return_value = LAST_PAGE_PEOPLE

        result = FetchData().get_complete_dataset("test.com")

        self.assertFalse(mock_get_all_pages.called)
        self.assertEqual(result, LAST_PAGE_PEOPLE["results"])

    @patch('datacollections.fetch.FetchData.get_all_pages')
    @patch('datacollections.fetch.FetchData.send_get_request_to')
    def test_get_complete_dataset_returns_all_existing_pages(self,
                                                             mock_send_req_to,
                                                             mock_get_all_pages):
        mock_send_req_to.return_value = PAGE_PEOPLE
        mock_get_all_pages.return_value = list(itertools.chain.from_iterable([PAGE_PEOPLE["results"],
                                                                              LAST_PAGE_PEOPLE["results"]]))

        result = FetchData().get_complete_dataset("test.com")

        self.assertTrue(mock_get_all_pages.called)
        self.assertEqual(result, mock_get_all_pages.return_value)

    def test_get_complete_dataset_handles_wrong_url(self):
        self.assertEqual(FetchData().get_complete_dataset("test.com"), None)

    def test_transform_data_passes_validation(self):
        constraints = [
            dict(name='edited_date', field='date', test=petl.dateparser('%Y-%m-%d')),
            dict(name='homeworld_resolved', field='homeworld', assertion=lambda v: "https" not in v)
            ]

        _, _, result_table = FetchData().transform_data(PAGE_PEOPLE["results"], PAGE_PLANETS["results"])

        # After reviewing petl's docs I decided to not reinvent the wheel and test
        # the behaviour of transform_data() function with the use of validate() method
        problems = petl.validate(result_table, constraints=constraints, header=COLUMNS)

        # If the validate method does not find any problems the table must have 0 rows.
        self.assertFalse(petl.nrows(problems))
