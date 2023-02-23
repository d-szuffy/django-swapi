from selenium import webdriver
from . import base


class NewFetchTest(base.FunctionalTest):

    def test_can_fetch_data_from_API(self):
        # Mateusz has heard about a cool app which allows you to view and analyze
        # data from Start Wars universe.
        self.browser.get(self.live_server_url)

        # He notices that page title and header mention Star Wars
        # this makes him sure he found the correct app

        # He is invited to fetch his own set of data right away

        # He clicks on the "fetch" button

        # The page updates, and he sees that a new item appeared in the collections table

        # Just to be sure that it was not a coincidence he clicks the button once again

        # The page updates again, and now he can see two records in the collections table

        # Satisfied
