import logging  # Add this import
import os
from pathlib import Path

import requests
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_DIR = Path(__file__).resolve().parent

# Load environment variables from .env file
load_dotenv()

# Configuration
GHISEUL_URL = os.getenv("GHISEULRO_URL")
USERNAME = os.getenv("GHISEULRO_USERNAME")
PASSWORD = os.getenv("GHISEULRO_PASSWORD")
DOWNLOAD_DIR = BASE_DIR / "docs"  # Set the docs folder as the download folder

# Ensure the docs folder exists
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]')

# Set up Selenium
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)


def login(driver):
    driver.get(GHISEUL_URL)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "username")))
    driver.find_element(By.ID, "username").send_keys(USERNAME)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "passwordT")))  # Wait for the temporary password field
    password_temp = driver.find_element(By.ID, "passwordT")
    password_temp.click()  # Focus on the temporary password field to trigger the change
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "passwordP")))  # Wait for the actual password field
    driver.find_element(By.ID, "passwordP").send_keys(PASSWORD)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='submit']")))  # Wait for the submit button
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()


def verify_login(driver):
    element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//h3[contains(@class, 'media-heading')]")))
    if "MOROSANU" in element.text:
        driver.get(f"{GHISEUL_URL}/plati-anterioare/")
    else:
        raise Exception("Login verification failed: 'MOROSANU' not found in the element text")


def download_receipts(driver):
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "table.table-payments")))
    rows = driver.find_elements(By.XPATH, "//table[@class='table table-payments']//tr")

    for row in rows:
        try:
            process_row(row)
        except Exception as e:
            logging.error(f"Error processing row: {e}")


def process_row(row):
    cells = row.find_elements(By.TAG_NAME, "td")
    if not cells:
        return  # Skip if no cells (e.g., header or empty rows)

    referinta = cells[0].text.strip()
    suma = cells[1].text.strip()
    date = cells[2].text.strip()
    explicatie = cells[3].text.strip()

    download_button = row.find_element(By.XPATH, ".//a[contains(@class, 'btn')]")
    download_url = download_button.get_attribute("href")

    date_parts = date.split()
    formatted_date = date_parts[0].replace(".", "-") + "-" + date_parts[1].replace(":", "")

    new_filename = f"dovadaSNEP{referinta}_{explicatie}_{suma}_{formatted_date}.pdf"
    new_filepath = os.path.join(DOWNLOAD_DIR, new_filename)

    if os.path.exists(new_filepath):
        logging.info(f"File {new_filename} already exists. Skipping download.")
        return

    response = requests.get(download_url)
    if response.status_code == 200:
        with open(new_filepath, "wb") as file:
            file.write(response.content)
        logging.info(f"Downloaded and saved as {new_filename}")
    else:
        logging.error(f"Failed to download file for {referinta}. HTTP status: {response.status_code}")


try:
    login(driver)
    verify_login(driver)
    download_receipts(driver)
finally:
    driver.quit()
