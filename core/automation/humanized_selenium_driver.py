from requests import head
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium_stealth import stealth
import random
import time

from config import Config


class HumanizedDriver:
    def __init__(self, headless):
        self.config = Config()
        self.driver = self.configure_driver(headless)
        self.actions = ActionChains(self.driver)
        self.wait = WebDriverWait(self.driver, 10)

    def configure_driver(self, headless):
        chrome_options = Options()

        if headless:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--window-size=1920,1080")

        # chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--lang=pl-PL")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_experimental_option("detach", True)

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=chrome_options
        )

        # Apply stealth configuration
        stealth(
            driver,
            languages=["pl-PL", "pl"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )

        return driver

    def human_delay(self, delay_range):
        time.sleep(random.uniform(*delay_range))

    def human_click(self, xpath):
        element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        self.actions.move_to_element(element).pause(
            random.uniform(*self.config.ACTION_DELAY)
        ).click().perform()
        self.human_delay(self.config.ACTION_DELAY)

    def human_type(self, xpath, text, with_errors=False):
        element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        self.actions.move_to_element(element).pause(
            random.uniform(*self.config.ACTION_DELAY)
        ).click().perform()

        for char in text:
            # Simulate typing speed variations
            self.actions.send_keys(char)
            self.actions.pause(random.uniform(*self.config.TYPING_SPEED))

            # Simulate occasional typos (5% chance)
            if with_errors and random.random() < 0.05:
                self.actions.send_keys(Keys.BACK_SPACE)
                self.actions.pause(random.uniform(*self.config.TYPING_SPEED))
                self.actions.send_keys(char)

        self.actions.perform()
        self.human_delay(self.config.ACTION_DELAY)

    def random_mouse_movement(self):
        window_size = self.driver.get_window_size()

        for _ in range(random.randint(2, 4)):
            x_offset = random.randint(0, window_size["width"])
            y_offset = random.randint(0, window_size["height"])
            self.actions.move_by_offset(x_offset, y_offset).pause(0.2)

        self.actions.perform()

    def cleanup(self):
        self.driver.quit()

    def get(self, url):
        self.driver.get(url)
