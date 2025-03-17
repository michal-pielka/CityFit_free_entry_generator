import time
from typing import Dict
import logging
from datetime import date, timedelta
import random

from config import Config

logger = logging.getLogger(__name__)


class UserDataError(Exception):
    """Custom exception for user generation errors"""


class UserGenerator:
    @staticmethod
    def generate_user() -> Dict[str, str]:
        """Generate realistic Polish user data"""
        try:
            user = {
                "phone": Config.PHONE_NUMBER,
                "country_code": Config.PHONE_COUNTRY_CODE,
                "country_name": Config.PHONE_COUNTRY_NAME,
                "name": "Jan",
                "surname": "Kowalski",
                "email": f"x{str(int(time.time()))[-6:]}@gmail.com",
                "password": Config.PASSWORD,
                "street": Config.STREET,
                "house_number": Config.HOUSE_NR,
                "postal": Config.POSTAL,
                "city": "Warszawa",
                "pesel": UserGenerator.generate_pesel()
            }
            return user

        except Exception as e:
            logger.error(f"User generation failed: {str(e)}")
            raise UserDataError("Failed to generate user data") from e

    @staticmethod

    def generate_pesel():
        """
        Generates a valid PESEL number.
        """
        # Generate a random birth date between January 1, 1900 and December 31, 2099.
        start_date = date(1900, 1, 1)
        end_date = date(2099, 12, 31)
        days_between = (end_date - start_date).days
        birth_date = start_date + timedelta(days=random.randint(0, days_between))
        
        # Extract year, month, day parts.
        year = birth_date.year % 100  # last two digits of year
        month = birth_date.month
        day = birth_date.day
        
        # Adjust month based on century.
        if 1900 <= birth_date.year <= 1999:
            month_code = month
        elif 2000 <= birth_date.year <= 2099:
            month_code = month + 20
        elif 1800 <= birth_date.year <= 1899:
            month_code = month + 80
        elif 2100 <= birth_date.year <= 2199:
            month_code = month + 40
        elif 2200 <= birth_date.year <= 2299:
            month_code = month + 60
        else:
            month_code = month  # default fallback

        # First six digits (YYMMDD) with adjusted month.
        first_six = f"{year:02d}{month_code:02d}{day:02d}"
        
        # Generate next four digits randomly.
        middle = f"{random.randint(0, 9999):04d}"
        first_ten = first_six + middle
        
        # Calculate the checksum digit using weights.
        weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
        s = sum(int(digit) * weight for digit, weight in zip(first_ten, weights))
        checksum = (10 - (s % 10)) % 10
        
        # Return the complete 11-digit PESEL.
        pesel = first_ten + str(checksum)
        return pesel
