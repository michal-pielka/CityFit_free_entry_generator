import requests
from typing import Dict
from config import Config
import logging

logger = logging.getLogger(__name__)


class CityFitAPIError(Exception):
    """Custom exception for CityFit API errors"""


class CityFitAPI:
    def __init__(self):
        self.base_url = Config.CITYFIT_API_URL
        self.default_headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        }

    def create_account(self, user_data: Dict) -> requests.Response:
        """
        Create CityFit account through API.
        We only fill the basic fields and not phone number, pesel etc. Because CityFit's API uses Google's reCaptcha v3 tokens which are hard to work with.
        """
        payload = {
            "originClubId": Config.CLUB_ID,
            "name": user_data["name"],
            "surname": user_data["surname"],
            "email": user_data["email"],
            "emailRepeat": user_data["email"],
            "password": Config.PASSWORD,
            "passwordRepeat": Config.PASSWORD,
            "gymRulesAndRegulationAgreement": True,
            "marketingAgreement": True,
            "tradeAgreement": True,
            "serviceStartAgreement": True,
        }

        try:
            response = requests.post(
                self.base_url, json=payload, headers=self.default_headers, timeout=10
            )
            response.raise_for_status()
            return response

        except requests.exceptions.RequestException as e:
            logger.error(f"Account creation failed: {str(e)}")
            raise CityFitAPIError("API request failed") from e
