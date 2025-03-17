import time
import random
import logging
from selenium.webdriver.common.keys import Keys

from config import Config
from core.automation.humanized_selenium_driver import HumanizedDriver
from core.api.onlinesim_api import OnlineSimAPI, OnlineSimAPIError
from core.api.cityfit_api import CityFitAPI, CityFitAPIError
from core.utils.user_generator import UserGenerator
from core.utils.logger import configure_logging
from data.xpaths import XPATH_DICT

configure_logging()
logger = logging.getLogger(__name__)

class CityFitAutomator:
    def __init__(self, headless: bool = False):
        self.driver = HumanizedDriver(headless)
        self.user = UserGenerator().generate_user()
        self.onlinesim = OnlineSimAPI(Config.ONLINESIM_API_KEY)
        self.cityfit = CityFitAPI()

    def run(self):
        try:
            target_url = f"{Config.BASE_URL}/offers/training/clubs/{Config.CLUB_ID}"

            logger.info("Opening the website.")
            self.driver.get(target_url)

            logger.info("Starting registration process")
            self._create_base_account()
            self._complete_registration_flow()

            verification_code = self._retrieve_sms_code(self.user.get("country_code", ""), self.user["phone"])

            if verification_code:
                self._finalize_registration(verification_code)
                logger.info("Registration completed successfully")

            else:
                logger.error("Failed to retrieve verification code")

        except Exception as e:
            logger.error(f"Registration failed: {str(e)}")
            self.driver.cleanup()

        finally:
            print(f"\nAccount successfully generated!\nEmail: {self.user["email"]}\nPassword: {self.user["password"]}")
            self.driver.cleanup()

    def _create_base_account(self):
        logger.debug("Creating base account through API")
        response = self.cityfit.create_account(self.user)

        if not response.ok:
            raise CityFitAPIError("Account creation API failed")

    def _complete_registration_flow(self):
        self._handle_cookies()
        self._apply_promo_code(Config.PROMO_CODE)
        self._complete_personal_info_form()
        self._fill_address_information()

    def _handle_cookies(self):
        try:
            self.driver.human_click(XPATH_DICT["accept_cookies_button"])
            logger.debug("Accepted cookies")
        except Exception as e:
            logger.warning(f"Cookie handling failed: {str(e)}")

    def _apply_promo_code(self, code: str):
        self.driver.human_type(XPATH_DICT["promo_code_input"], code)
        self.driver.human_click(XPATH_DICT["use_promo_code_button"])
        self.driver.human_click(XPATH_DICT["accept_marketing_button"])

    def _complete_personal_info_form(self):
        self.driver.human_click(XPATH_DICT["choose_free_entry_button"])
        self.driver.human_click(XPATH_DICT["login_button"])
        self.driver.human_type(XPATH_DICT["login_email_input"], self.user["email"])
        self.driver.human_type(XPATH_DICT["login_password_input"], self.user["password"])
        self.driver.human_click(XPATH_DICT["log_in_button"])

    def _fill_address_information(self):
        time.sleep(10)
        fields = {
            "change_phone_number_country": self.user.get("country_name", self.user.get("country_code", "")) + Keys.ENTER,
            "phone_number_input": self.user["phone"],
            "street_input": self.user["street"],
            "house_number_input": self.user["house_number"],
            "postal_code_input": self.user["postal"],
            "city_input": self.user["city"],
            "pesel_input": self.user["pesel"],
        }
        for field, value in fields.items():
            self.driver.human_type(XPATH_DICT[field], value)
        self.driver.human_click(XPATH_DICT["save_personal_info2_button"])

    def _handle_phone_verification(self):
        logger.info("Waiting for verification code")
        return 

    def _retrieve_sms_code(self, country_code: str, phone_number: str):
        for _ in range(Config.VERIFICATION_TIMEOUT):
            try:
                messages = self.onlinesim.get_free_list(int(country_code), int(phone_number))
                code = self.onlinesim.extract_verification_code(messages)
                if code:
                    return code

            except OnlineSimAPIError as e:
                logger.warning(f"SMS retrieval attempt failed: {str(e)}")

            time.sleep(1)

        return None

    def _finalize_registration(self, verification_code: str):
        # Enter the verification code and submit
        self.driver.human_type(XPATH_DICT["code_input"], verification_code)
        self.driver.human_click(XPATH_DICT["confirm_code_button"])
        # Change the phone number to trigger the security bug, as in the old code
        self.driver.human_click(XPATH_DICT["edit_personal_info2_button"])
        new_number_suffix = str(random.randint(100, 999))
        backspaces = Keys.BACK_SPACE * 3
        self.driver.human_type(XPATH_DICT["phone_number_input"], backspaces + new_number_suffix)
        self.driver.human_click(XPATH_DICT["save_personal_info2_button"])
        self.driver.human_click(XPATH_DICT["accept_agreements2_button"])
        self.driver.human_click(XPATH_DICT["confirm_creating_account_button"])

if __name__ == "__main__":
    automator = CityFitAutomator(headless=False)
    automator.run()
