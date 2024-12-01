import os
import json
import csv
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

# Опции для Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Безголовый режим
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")

# Пути для бинарников Chrome и ChromeDriver
user_home_dir = os.path.expanduser("~")
chrome_binary_path = os.path.join(user_home_dir, "chrome-linux64", "chrome")
chromedriver_path = os.path.join(user_home_dir, "chromedriver-linux64", "chromedriver")

# Устанавливаем сервис для Chrome
chrome_options.binary_location = chrome_binary_path
service = Service(chromedriver_path)

# Инициализация WebDriver с использованием stealth
def init_webdriver():
    driver = webdriver.Chrome(service=service, options=chrome_options)
    stealth(driver)
    return driver

# Извлекаем ссылки на страницы категорий
def extract_and_store_category_links():
    with webdriver.Chrome(service=service, options=chrome_options) as browser:
        url = "https://www.knowde.com"  # Стартовая страница
        print(f"Скрапим страницу: {url}")

        # Ожидаем загрузки страницы
        browser.get(url)
        
        # Ожидаем появления нужных элементов с категориями
        try:
            WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//*[starts-with(@class, 'homepage-categories_tilesList')]//a")))
        except TimeoutException:
            print("Не удалось загрузить страницы категорий.")
            return []

        # Извлекаем ссылки из элементов с нужным классом
        elements = browser.find_elements(By.XPATH, "//*[starts-with(@class, 'homepage-categories_tilesList')]//a")
        links = []

        for element in elements:
            link = element.get_attribute('href')
            links.append(link + '/brands')  # Формируем ссылки на бренды
            # Добавляем дополнительные страницы
            for i in range(2, 11):
                modified_link = f"{link}/brands/{i}"
                links.append(modified_link)

        return links

# Извлекаем ссылки на бренды из каждой категории
def extract_view_brand_links_from_categories():
    links = extract_and_store_category_links()
    brand_links = set()  # Используем set для уникальных ссылок

    with webdriver.Chrome(service=service, options=chrome_options) as browser:
        for url in links:
            print(f"Скрапим страницу: {url}")

            try:
                browser.get(url)
                # Ожидаем загрузки кнопок брендов
                WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(text(), 'View Brand')]")))

                elements = browser.find_elements(By.XPATH, "//a[contains(text(), 'View Brand')]")

                for element in elements:
                    link = element.get_attribute('href')
                    if link not in brand_links:  # Если ссылка новая, добавляем ее
                        brand_links.add(link)
                        print(f"Новая уникальная ссылка на бренд: {link}")
                        # Сохраняем новую ссылку сразу в файл
                        save_to_csv([link], filename="unique_brand_links.csv", append=True)

            except TimeoutException as e:
                print(f"Ошибка тайм-аута на странице {url}: {e}")
            except WebDriverException as e:
                print(f"Ошибка WebDriver на странице {url}: {e}")
            except Exception as e:
                print(f"Ошибка на странице {url}: {e}")

    return brand_links

# Сохраняем уникальные данные в CSV файл
def save_to_csv(data, filename="unique_brand_links.csv", append=False):
    mode = 'a' if append else 'w'
    with open(filename, mode=mode, newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not append:
            writer.writerow(["Brand URL"])  # Заголовки

        for link in data:
            writer.writerow([link])

# Главная функция для вывода и сохранения данных
def print_and_save_extracted_links():
    brand_links = extract_view_brand_links_from_categories()

    # Печатаем все уникальные ссылки
    print("Уникальные ссылки на бренды:")
    for link in brand_links:
        print(f"  - {link}")

if __name__ == "__main__":
    print_and_save_extracted_links()
