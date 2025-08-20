import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from selenium import webdriver
from pages.page_objects import OllamaPage
from  tests.driver_factory import get_driver

OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://localhost:3000')  # Default to localhost if not set

class OllamaTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = get_driver()
        self.page = OllamaPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_text_to_prompt(self):
        self.page.open(OLLAMA_URL)
        self.page.select_model("gemma3:1b")
        self.page.send_message("write hello world!")

        # Optional: Wait for response to appear (replace this with your actual selector)
        # self.page.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "selector-for-response")))

if __name__ == '__main__':
    unittest.main()
