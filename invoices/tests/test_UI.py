import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class TestInvoicingApp(StaticLiveServerTestCase):
    def setUp(self):
        self.base_url = self.live_server_url
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        # Make sure chrome driver is added to sys PATH first
        self.driver = webdriver.Chrome(options=chrome_options)

    def test_landing_page_load(self):
        self.driver.get(self.base_url)
        self.assertEqual(self.driver.title, "Invoices Landing Page")

    @unittest.skip("This view isn't complete yet")
    def test_new_invoice_can_be_created(self):
        self.driver.get(self.base_url)
        invoices_link = self.driver.find_element_by_id("invoices-dropdown")
        invoices_link.click()

    def tearDown(self):
        self.driver.quit()
