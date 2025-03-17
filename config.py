import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class Config:
    # OnlineSIM Configuration
    PHONE_NUMBER = "466352676"
    PHONE_COUNTRY_CODE = "32"
    PHONE_COUNTRY_NAME = "belgium"
    ONLINESIM_API_KEY = os.getenv("ONLINESIM_API_KEY") 

    # CityFit Configuration
    PROMO_CODE = "FERIE2025"
    CLUB_ID = 100020
    PASSWORD = "Test123."
    STREET = "Wesola"
    HOUSE_NR = "7"
    POSTAL = "00101"

    # Selenium Timing Configuration
    PAGE_LOAD_DELAY = (2, 5)
    ACTION_DELAY = (0.2, 0.8)
    TYPING_SPEED = (0.05, 0.2)
    VERIFICATION_TIMEOUT = 60

    # Constants
    CITYFIT_PHONE_NUMBER = "8128"
    BASE_URL = "https://klubowicz.cityfit.pl"
    CITYFIT_API_URL = "https://klubowicz.cityfit.pl/api/registrations/v2"
    ONLINESIM_API_URL = "https://onlinesim.io/api"
