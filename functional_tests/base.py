import os
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from django.conf import settings
MAX_WAIT = 300


class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()
        # for future purposes if the app would go live to production
        # I put below an option to test it against the staging/production server
        # To invoke it just provide the STAGING_SERVER variable in the terminal session where you run your test
        staging_sever = os.environ.get("STAGING_SERVER")
        if staging_sever:
            self.live_server_url = "http://" + staging_sever

    # Deleting the files created during functional tests should be automated
    # This manual removal needs refactoring
    def tearDown(self) -> None:
        self.browser.quit()

    def wait_for_row_in_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, 'id_collections_table')
                rows = table.find_elements(By.TAG_NAME, "tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def wait_for(self, fn):
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def get_media_files(self):
        return sorted([file for file in os.listdir(settings.MEDIA_ROOT)])
