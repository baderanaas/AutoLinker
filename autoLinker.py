import os
import time
import csv
import logging
from dotenv import load_dotenv
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("auto_linker.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

load_dotenv()

profile_path = os.getenv("PROFILE_PATH")


def _scrolling(driver, scroll_pause_time=3):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        time.sleep(scroll_pause_time)
    time.sleep(scroll_pause_time)


def _buttonXPATH(driver, xpath):
    try:
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        button.click()
    except NoSuchElementException:
        logger.warning(f"No {xpath} button found. Skipping...")
        return False
    except TimeoutException:
        logger.warning(f"No {xpath} button found. Skipping...")
        return False
    return True


def _addToCSV(company, profile_name, profile_link, company_link, send_message):
    folder_path = "Companies"
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, f"{company}.csv")

    with open(file_path, "a", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "Company",
                "Profile Name",
                "Send Message",
                "Profile Link",
                "Company Link",
                "Date",
            ],
        )
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(
            {
                "Company": company,
                "Profile Name": profile_name,
                "Profile Link": profile_link,
                "Company Link": company_link,
                "Send Message": send_message,
                "Date": time.strftime("%Y-%m-%dT%H:%M:%S"),
            }
        )


def _inputTextXPATH(driver, xpath, text):
    try:
        input_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        input_box.send_keys(text)
    except NoSuchElementException:
        logger.warning(f"No {xpath} input box found. Skipping...")
        return False
    except TimeoutException:
        logger.warning(f"No {xpath} input box found. Skipping...")
        return False
    return True


def autoLinker(url, message, note, premium=True):
    options = uc.ChromeOptions()
    options.add_argument(f"--user-data-dir={profile_path}")
    options.add_argument("--headless=new")
    driver = uc.Chrome(options=options)

    try:
        driver.get(url)

        logger.info("Getting company name...")
        company_name_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//h1[contains(@class, 'org-top-card-summary__title')]")
            )
        )
        company_name = company_name_element.text.strip()
        logger.info(f"Company name: {company_name}")

        _scrolling(driver)

        profile_links = []
        profile_elements = driver.find_elements(
            By.XPATH, "//a[contains(@href, '/in/')]"
        )
        for profile_element in profile_elements:
            profile_url = profile_element.get_attribute("href")
            if profile_url not in profile_links:
                profile_links.append(profile_url)

        logger.info(f"Found {len(profile_links)} profiles.")

        for profile_url in profile_links:
            max_attempts = 3
            processed_successfully = False
            last_exception = None
            profile_url = profile_url.split("?")[0]

            for attempt in range(max_attempts):
                try:
                    logger.info(
                        f"Processing {profile_url} (Attempt {attempt + 1}/{max_attempts})"
                    )
                    send_message = False
                    driver.get(profile_url)

                    # Company check
                    company_profile = (
                        WebDriverWait(driver, 10)
                        .until(
                            EC.presence_of_element_located(
                                (
                                    By.XPATH,
                                    """//button[contains(@aria-label, 'Current company:')]""",
                                )
                            )
                        )
                        .text.strip()
                    )

                    if not (
                        company_profile in company_name
                        or company_name in company_profile
                    ):
                        logger.warning("Profile not in target company. Skipping...")
                        break

                    # Profile processing
                    profile_name = (
                        WebDriverWait(driver, 10)
                        .until(
                            EC.presence_of_element_located(
                                (
                                    By.XPATH,
                                    "//span[contains(@class, 'artdeco-hoverable-trigger')]//h1",
                                )
                            )
                        )
                        .text.strip()
                    )

                    _scrolling(driver)

                    connection_status = (
                        WebDriverWait(driver, 10)
                        .until(
                            EC.presence_of_element_located(
                                (
                                    By.XPATH,
                                    """//span[contains(@class, 'dist-value')]""",
                                )
                            )
                        )
                        .text.strip()
                    )
                    logger.info(f"Connection status: {connection_status}")

                    if not message:
                        logger.warning("No message provided. Skipping...")
                        break

                    # Message handling logic
                    if connection_status == "1st":
                        if _buttonXPATH(
                            driver, "//button[starts-with(@aria-label, 'Message')]"
                        ):
                            if _inputTextXPATH(
                                driver,
                                xpath="//div[@role='textbox' and @aria-label='Write a message…']",
                                text=message,
                            ):
                                send_message = _buttonXPATH(
                                    driver,
                                    "//button[contains(@class, 'msg-form__send-button') and text()='Send']",
                                )

                            _buttonXPATH(
                                driver,
                                "//button[contains(@class, 'msg-overlay-bubble-header__control') and contains(span, 'Close your conversation')]",
                            )

                    elif connection_status == "2nd":
                        _buttonXPATH(
                            driver, "//button[starts-with(@aria-label, 'Invite')]"
                        )
                    else:
                        _buttonXPATH(driver, "//button[@aria-label='More actions']")
                        _buttonXPATH(driver, "//div[contains(@aria-label, 'Invite')]")

                    if not premium or not note:
                        _buttonXPATH(
                            driver, "//button[@aria-label='Send without a note']"
                        )
                    else:
                        _buttonXPATH(driver, "//button[@aria-label='Add a note']")
                        _inputTextXPATH(
                            driver, xpath="//textarea[@id='custom-message']", text=note
                        )

                        send_message = _buttonXPATH(
                            driver, "//button[@aria-label='Send invitation']"
                        )

                    if profile_name == "LinkedIn Member" or profile_name == "FAILED":
                        break
                    elif profile_name:
                        _addToCSV(
                            company_name, profile_name, profile_url, url, send_message
                        )
                    processed_successfully = True
                    break

                except TimeoutException as e:
                    last_exception = e
                    logger.warning(
                        f"Timeout occurred during attempt {attempt + 1}: {str(e)}"
                    )
                    if attempt < max_attempts - 1:
                        time.sleep(3)
                except Exception as e:
                    last_exception = e
                    logger.error(
                        f"Error occurred during attempt {attempt + 1}: {str(e)}"
                    )
                    if attempt < max_attempts - 1:
                        time.sleep(3)

            if not processed_successfully:
                logger.error(
                    f"Failed to process profile after {max_attempts} attempts. Last error: {str(last_exception)}"
                )
                _addToCSV(company_name, "FAILED", profile_url, url, False)

    finally:
        driver.quit()
