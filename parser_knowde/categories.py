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

# Function to extract links with the class starting with 'homepage-categories_tilesList' and store them in a list
def extract_and_store_category_links():
    # Initialize the browser
    with webdriver.Chrome(service=service, options=chrome_options) as browser:
        # Construct the URL for the target page
        url = "https://www.knowde.com"  # замените на нужный URL
        print(f"Scraping page: {url}")

        # Navigate to the page
        browser.get(url)

        # Allow time for the page to load
        time.sleep(5)

        # Find all elements with class starting with 'homepage-categories_tilesList'
        elements = browser.find_elements(By.XPATH, "//*[starts-with(@class, 'homepage-categories_tilesList')]//a")

        # Initialize a list to store links
        links = []

        # Extract links from the found elements and store them in the list
        for element in elements:
            link = element.get_attribute('href')
            links.append(link+'/brands')
            # adding additional pages
            for i in range(2, 11):
                modified_link = f"{link}/brands/{i}"
                links.append(modified_link)

        # Return the list of links
        return links

if __name__ == "__main__":
    links = extract_and_store_category_links()

    # Optionally, print the links or use them further
    for link in links:
        print(f"Found link: {link}")
