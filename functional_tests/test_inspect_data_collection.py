from selenium import webdriver
from selenium.webdriver.common.by import By
from . import base
import os


class InspectDataTest(base.FunctionalTest):

    def test_can_inspect_fetched_data(self):
        # Mateusz goes to the collections page to fetch the data
        self.browser.get(self.live_server_url)
        collections_link = self.browser.find_element(By.ID, 'id_collections_link')
        collections_link.click()

        # He clicks on the button and waits for success message
        fetch_button = self.browser.find_element(By.ID, "id_fetch_btn")
        fetch_button.click()
        self.wait_for(lambda: self.assertIn(
            self.browser.find_element(By.CLASS_NAME, 'has-message').text,
            "Data fetched successfully."
        ))

        # He clicks again on the fetch button and also waits for the succes message
        fetch_button = self.browser.find_element(By.ID, "id_fetch_btn")
        fetch_button.click()
        self.wait_for(lambda: self.assertIn(
            self.browser.find_element(By.CLASS_NAME, 'has-message').text,
            "Data fetched successfully."
        ))
        self.wait_for_row_in_table(self.get_media_files()[-1])

        # Mateusz can see that the file names are hyperlinks.
        table_rows = self.browser.find_elements(By.TAG_NAME, 'td')
        for row in table_rows:
            self.assertTrue(len(row.find_elements(By.TAG_NAME, 'a')))
        self.browser.add_cookie({'name': 'file_name', 'value': table_rows[0].text})

        # He clicks one of them out of curiosity
        table_rows[0].click()

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
        load_more_btn.click()
        table = self.browser.find_element(By.ID, 'id_collection_details')
        table_rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertEqual(len(table_rows) - 1, 30)

        # Satisfied

