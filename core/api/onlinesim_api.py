import requests
from requests.exceptions import RequestException
from typing import Dict, Optional
from config import Config
import logging

logger = logging.getLogger(__name__)


class OnlineSimAPIError(Exception):
    """Custom exception for OnlineSim API errors"""


class OnlineSimAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = Config.ONLINESIM_API_URL

    def get_free_list(self, country: int, number: int) -> Dict:
        """
        Retrieve messages list from OnlineSim
        Args:
            country: Country code (e.g. 32 for Belgium)
            number: Phone number without country code
        Returns:
            Dictionary with API response data
        Raises:
            OnlineSimAPIError: If API request fails
        """
        params = {"country": country, "number": number, "apikey": self.api_key}

        try:
            response = requests.get(f"{self.base_url}/getFreeList", params=params)
            response.raise_for_status()
            return response.json()

        except RequestException as e:
            logger.error(f"OnlineSim API request failed: {str(e)}")
            raise OnlineSimAPIError(f"API request failed: {str(e)}") from e

    def extract_verification_code(self, messages: Dict) -> Optional[str]:
        """
        Extract verification code from SMS messages
        Args:
            messages: API response messages dictionary
        Returns:
            Extracted code or None if not found
        """
        if not messages.get("messages", {}).get("data"):
            return None

        for message in messages["messages"]["data"][:3]:  # TODO: instead of checking last 3 messages, check whether last message from CityFit is recent
            if message.get("in_number") == Config.CITYFIT_PHONE_NUMBER:
                return message.get("text", "")[33:39]

        return None
