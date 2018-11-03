
author = 'Joan Torres - Andres Ortiz - Danny Hurtado'

from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class Sgrd105FunctionalTest(TestCase):

    # Mac OSX installation of selenium
    # brew install selenium-server-standalone
    # brew cask install chromedriver
    # Also
    # https://www.seleniumhq.org/download/

    def setUp(self):
        chromedriver ='/usr/local/bin/chromedriver'
        self.browser = webdriver.Chrome(chromedriver)
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_activity_check_link_location(self):
        self.browser.get('http://localhost:8090/actividades/')
        self.browser.implicitly_wait(3)
        span = WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located((By.ID, "activitySpan")))
        # span.click()

        self.assertEquals('Done', span.text)

    def test_notification_message(self):
        self.browser.get('http://localhost:8090/actividades/')
        self.browser.implicitly_wait(3)

        span = WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located((By.ID, "activitySpan")))
        span.click()

        nofication = WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located((By.ID, "notify")))

        self.assertEquals('Actividad completada', nofication.text)