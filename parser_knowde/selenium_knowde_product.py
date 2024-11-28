import os
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
from bs4 import BeautifulSoup
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
# browser = webdriver.Chrome(service=service, options=chrome_options)

def init_webdriver():
    driver = webdriver.Chrome(service=service, options=chrome_options)
    stealth()
with webdriver.Chrome(service=service, options=chrome_options) as browser:
    # Enable CDP to capture network requests
    browser.get("https://www.knowde.com/stores/wacker-chemie-ag/products/elastosil-n199-transparent")

    # Allow time for the page to load and for requests to be made
    time.sleep(5)

    # Capture network requests (CDP)
    browser.execute_cdp_cmd('Network.enable', {})

    # List to store captured network responses
    captured_responses = []

    # Define callback function to capture responses
    def capture_response(request):
        if 'application/json' in request.get('response', {}).get('content-type', ''):
            captured_responses.append(request['response'])
    
    # Set up event listener for network responses
    browser.request_interceptor = capture_response
    
    # Give time to capture network responses
    time.sleep(5)

    # Print captured JSON responses
    for response in captured_responses:
        try:
            # Try to parse and print the response body
            body = response.get('body', '')
            if body:
                data = json.loads(body)
                print(json.dumps(data, indent=4, ensure_ascii=False))
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
