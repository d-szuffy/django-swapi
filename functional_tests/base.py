import os
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException


class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()
        # for future purposes if the app would go live to production
        # I put below an option to test it against the staging/production server
        # To invoke it just provide the STAGING_SERVER variable in the terminal session where you run your test
        staging_sever = os.environ.get("STAGING_SERVER")
        if staging_sever:
            self.live_server_url = "http://" + staging_sever

    def tearDown(self) -> None:
        self.browser.quit()
