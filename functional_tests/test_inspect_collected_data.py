import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from . import base
import os
from typing import List
import random


class InspectDataTest(base.FunctionalTest):

    def fetch_data_from_api(self):
        """
        This function is a helper function for test cases. It goes to the 'view_collections' view fetches
        the data from API. It ensures that the data has been fetched successfully and await for the file
        to appear in the table on the page.
        """

        # go to the datacollections list view
        self.browser.get(self.live_server_url + '/datacollections/')

        # Click on the fetch button to collect data from API and wait for a message to show up.
        fetch_button = self.browser.find_element(By.ID, "id_fetch_btn")
        fetch_button.click()
        self.wait_for(lambda: self.assertIn(
            self.browser.find_element(By.CLASS_NAME, 'has-message').text,
            "Data fetched successfully."
        ))
        self.wait_for_row_in_table(self.get_media_files()[-1])

    def test_can_inspect_fetched_data(self):
        # Mateusz goes to the collections page to fetch the data.
        # He collects the data twice just to be sure everything works.
        self.fetch_data_from_api()
        self.fetch_data_from_api()

        # Mateusz can see that the file names are hyperlinks.
        table_rows = self.browser.find_elements(By.TAG_NAME, 'td')
        for row in table_rows:
            self.assertTrue(len(row.find_elements(By.TAG_NAME, 'a')))
        self.browser.add_cookie({'name': 'file_name', 'value': table_rows[0].text})

        # He clicks one of them out of curiosity
        table_rows[0].find_element(By.TAG_NAME, 'a').click()

        # He gets redirected to the collection_details page
        self.assertIn('collection_details', self.browser.current_url)

        # He sees a table. There is a title above the table.
        table_title = self.browser.find_element(By.TAG_NAME, "h1").text
        file_name = self.browser.get_cookie('file_name')['value']

        self.assertEqual(table_title, file_name)

        # This table's has 10 rows. Headers and rows match data from file
        table = self.browser.find_element(By.ID, 'id_collection_details')
        table_rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertEqual(len(table_rows) - 1, 10)

        # Below the table he sees a button. This button encourages him to load more data
        load_more_btn = self.browser.find_element(By.ID, 'id_load_more')
        self.assertEqual(load_more_btn.text, "Load more")

        # He clicks the "Load more" button and now the table has 20 rows
        load_more_btn.click()
        table = self.browser.find_element(By.ID, 'id_collection_details')
        table_rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertEqual(len(table_rows) - 1, 20)

        # To be sure that the button works he clicks it again.
        # Another 10 rows loaded
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        load_more_btn = self.browser.find_element(By.ID, 'id_load_more')
        time.sleep(1)
        load_more_btn.click()
        table = self.browser.find_element(By.ID, 'id_collection_details')
        table_rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertEqual(len(table_rows) - 1, 30)

        # Satisfied

    def test_can_group_data_by_columns(self):
        # Mateusz goes to the collections page to fetch the data. He clicks on the fetch button.
        # A filename appears in the table, and he clicks it.
        self.fetch_data_from_api()
        files_table = self.browser.find_element(By.TAG_NAME, 'td')
        files_table.find_element(By.TAG_NAME, 'a').click()

        # He gets redirected to the detailed page where he can see a table with data.
        data_table = self.browser.find_element(By.ID, 'id_collection_details')

        # He notices that each table header has a checkbox.
        data_table_headers = data_table.find_elements(By.TAG_NAME, 'th')
        for h in data_table_headers:
            self.assertTrue(h.find_element(By.ID, 'id_' + h.text).get_attribute('type'), 'checkbox')

        # Mateusz also sees a "Value count" button.
        value_count_btn = self.browser.find_element(By.ID, 'id_value_count')

        # He decides to check some of them and then press the button just to see what happens
        checked_columns = self.pick_random_columns(data_table_headers)
        checked_columns_str = ','.join(column.text for column in checked_columns)
        self.browser.add_cookie({'name': 'checked_columns', 'value': checked_columns_str})
        for column in checked_columns:
            column.find_element(By.TAG_NAME, 'label').click()
        value_count_btn.click()

        # The page reloads and now the table has columns which have been checked and one extra column labeled "count"
        cookie_value = self.browser.get_cookie('checked_columns')['value']
        checked_columns = (cookie_value + ',Count').split(',')
        data_table = self.browser.find_element(By.ID, 'id_collection_details')
        data_table_headers = [header.text for header in data_table.find_elements(By.TAG_NAME, 'th')]

        self.assertEqual(sorted(data_table_headers), sorted(checked_columns))

        # Satisfied

    def pick_random_columns(self, headers: List):
        """
        This function returns a list with random number of elements from headers input.
        """

        num_headers = random.randint(1, len(headers))
        return random.sample(headers, num_headers)
