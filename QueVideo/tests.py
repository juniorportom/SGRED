from _future_ import unicode_literals

from django.test import TestCase
_author_ = 'Joan Torres - Andres Ortiz - Daniel Hurtado'

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
        chromedriver = '/usr/local/bin/chromedriver'
        self.browser = webdriver.Chrome(chromedriver)
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()
