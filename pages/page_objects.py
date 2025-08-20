from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class OllamaPage:
    def __init__(self, driver):
        # Locators
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        self.MODEL_DROPDOWN = (By.CSS_SELECTOR, "button[role='combobox']")
        self.MODEL_OPTIONS = (By.XPATH, "//div[@role='dialog']//button[contains(text(),'gemma3:1b')]")
        self.CHAT_INPUT = (By.NAME, "message")
        self.SEND_BUTTON = (By.CLASS_NAME, "lucide-send-horizontal")
    
    
    # Actions
    def open(self, url):
        self.driver.get(url)

    def select_model(self, target_model):
        # Open dropdown
        model_button = self.wait.until(EC.element_to_be_clickable(self.MODEL_DROPDOWN))
        model_button.click()

        # Wait for model options to appear
        popover_buttons = self.wait.until(EC.presence_of_all_elements_located(self.MODEL_OPTIONS))

        # Click the target model
        model_option = None
        for btn in popover_buttons:
            if btn.text.strip() == target_model:
                model_option = btn
                break

        if model_option is None:
            raise Exception(f"Model '{target_model}' not found in dialog!")

        self.driver.execute_script("arguments[0].scrollIntoView(true);", model_option)
        try:
            model_option.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", model_option)

        # Verify selection
        model_button = self.wait.until(EC.presence_of_element_located(self.MODEL_DROPDOWN))
        assert target_model in model_button.text, f"Model '{target_model}' not selected!"

    def send_message(self, message):
        chat_input = self.wait.until(EC.presence_of_element_located(self.CHAT_INPUT))
        chat_input.clear()
        chat_input.send_keys(message)
        send_button = self.wait.until(EC.element_to_be_clickable(self.SEND_BUTTON))
        send_button.click()
        