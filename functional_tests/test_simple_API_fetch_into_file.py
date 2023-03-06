from selenium import webdriver
from selenium.webdriver.common.by import By
from . import base
import os


class NewFetchTest(base.FunctionalTest):

    def test_can_fetch_data_from_API(self):
        # Mateusz has heard about a cool app which allows you to view and analyze
        # data from Start Wars universe.
        self.browser.get(self.live_server_url)

        # He notices that page title and header mention Star Wars
        # this makes him sure he found the correct app
        self.assertIn('Star Wars', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("Star Wars", header_text)

        # He notices a link named "collections"
        navbar_text = self.browser.find_element(By.CLASS_NAME, "navbar").text
        self.assertIn("Collections", navbar_text)

        # He clicks the link and gets redirected to "collections page"
        collections_link = self.browser.find_element(By.ID, 'id_collections_link')
        collections_link.click()

        # He is invited to fetch his own set of data right away
        fetch_button = self.browser.find_element(By.ID, "id_fetch_btn")
        self.assertEqual(fetch_button.text, "Fetch")

        # He clicks on the "fetch" button
        fetch_button.click()

        # The page updates, and he sees that a new item appeared in the collections table
        self.wait_for(lambda: self.assertIn(
            self.browser.find_element(By.CLASS_NAME, 'has-message').text,
            "Data fetched successfully."
        ))
        self.wait_for_row_in_table(self.get_media_files()[-1])

        # Just to be sure that it was not a coincidence he clicks the button once again
        fetch_button = self.browser.find_element(By.ID, "id_fetch_btn")
        fetch_button.click()

        # The page updates again, and now he can see two records in the collections table
        self.wait_for(lambda: self.assertIn(
            self.browser.find_element(By.CLASS_NAME, 'has-message').text,
            "Data fetched successfully."
        ))
        self.wait_for_row_in_table(self.get_media_files()[-1])
        # Satisfied
