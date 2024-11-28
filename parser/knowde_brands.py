import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
from selenium.webdriver.common.by import By

# Define Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")

# Define paths
user_home_dir = os.path.expanduser("~")
chrome_binary_path = os.path.join(user_home_dir, "chrome-linux64", "chrome")
chromedriver_path = os.path.join(user_home_dir, "chromedriver-linux64", "chromedriver")

# Set binary location and service
chrome_options.binary_location = chrome_binary_path
service = Service(chromedriver_path)

# Initialize Chrome WebDriver
def init_webdriver():
    driver = webdriver.Chrome(service=service, options=chrome_options)
    stealth(driver)
    return driver

# Function to extract links with 'View Brand' in <a> tags
def extract_view_brand_links():
    # Initialize the browser
    with webdriver.Chrome(service=service, options=chrome_options) as browser:
        # Loop through pages 1 to 10
        for page_number in range(1, 11):
            # Construct the URL for the current page
            url = f"https://www.knowde.com/b/markets-food-nutrition/brands/{page_number}"
            print(f"Scraping page: {url}")

            # Navigate to the current page
            browser.get(url)

            # Allow time for the page to load
            time.sleep(5)

            # Find all <a> elements that contain 'View Brand' in their text
            elements = browser.find_elements(By.XPATH, "//a[contains(text(), 'View Brand')]")

            # Extract and print the text and link of the elements
            for element in elements:
                link = element.get_attribute('href')
                print(f"Found 'View Brand' link: {link}")

if __name__ == "__main__":
    extract_view_brand_links()
