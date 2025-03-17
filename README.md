# CityFit Gym Account Generator

**Disclaimer:**  
This project was developed for research and educational purposes only. I discovered a security vulnerability in the CityFit gym registration system that allowed the creation of unlimited free one-time entry accounts. The vulnerability was responsibly disclosed and has since been fixed. The code provided here is a record of my research and is not intended for any unauthorized use.

---

## Overview

During my security research, I identified a gap in the CityFit registration process. The system requires SMS verification in order to create an account. When the same phone number was used more than once, the system correctly prompted for payment because the free code had already been used. However, by changing the phone number after providing the SMS code during the registration process, the system failed to require a new SMS code, sent to freshly changed phone number. This oversight allows users to generate unlimited free entry accounts.

Due to the implementation of Google's reCaptcha v3 on CityFit's API endpoints, the registration process could not be automated with simple HTTP requests. Instead, I used Selenium with a custom “humanized” driver—enhanced with stealth techniques—to mimic realistic user behavior which allowed me to avoid being flagged as a bot.

---

## Project Structure

```
├── config.py                   # Configuration settings (API keys, endpoints, etc.)
├── requirements.txt            # Project dependencies and exact package versions
├── main.py                     # Main entry point for the automation process
├── core/
│   ├── api/
│   │   ├── cityfit_api.py      # Interacts with CityFit's API for account creation
│   │   └── onlinesim_api.py    # Interacts with OnlineSIM API for SMS code retrieval
│   ├── automation/
│   │   └── humanized_selenium_driver.py  # Custom Selenium driver with human-like behavior
│   └── utils/
│       ├── logger.py         # Custom logging configuration
│       └── user_generator.py # Generates realistic Polish user data (including PESEL)
└── data/
    └── xpaths.py               # XPath locators used in the Selenium automation
```

---

## Technologies Used

- **Python 3**
- **Selenium 4.10.0** – For browser automation and overcoming reCaptcha v3 challenges.
- **selenium-stealth 1.0.6** – To mimic human behavior and avoid bot detection.
- **webdriver-manager 3.8.6** – Simplifies the management of the Chrome WebDriver.
- **python-dotenv 0.21.0** – For managing sensitive configuration data.
- **Requests 2.31.0** – For API communication with CityFit and OnlineSIM.

---

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/michal-pielka/CityFitFreeEntryGenerator.git
   cd CityFitFreeEntryGenerator
   ```

2. **Create and activate a virtual environment:**

   - **Windows:**
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file** in the project root with your OnlineSIM API key:

   ```dotenv
   ONLINESIM_API_KEY=your_actual_api_key_here
   ```

---

## Usage

Run the main script to start the automation process:

```bash
python main.py
```

The script uses a humanized Selenium driver to navigate the CityFit website, perform the registration steps, and exploit the security gap by altering the phone number during SMS verification. Note that CityFit patched this vulnerability quickly after my report, so the exploit is now non-functional.

---

## Security Research and Ethical Considerations

- **Responsible Disclosure:**  
  After discovering the vulnerability, I promptly reported the issue to CityFit. The vulnerability was addressed rapidly, demonstrating the importance of responsible disclosure in the security community.

- **Educational Purpose:**  
  This project documents the methodology used to identify and demonstrate the flaw. It serves as a case study on the importance of secure input validation and proper session handling in modern web applications.

- **Automation Challenges:**  
  Due to advanced security measures (Google's reCaptcha v3), I was forced to use Selenium with custom human-like interactions rather than simple GET/POST requests.

---

## Final Note

The code in this repository is far from perfect since it was developed rapidly after reporting the security issue. The vulnerability has been fixed, and this repository now stands as a testament to proactive security testing and responsible disclosure.

---

## Contact

For further information or to discuss this project, please [contact me](mpielka726@gmail.com).
