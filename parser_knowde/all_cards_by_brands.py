import os
import time
import json
import csv
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
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
        time.sleep(5)

        # Извлекаем ссылки из элементов с нужным классом
        elements = browser.find_elements(By.XPATH, "//*[starts-with(@class, 'homepage-categories_tilesList')]//a")
        links = []

        for element in elements:
            link = element.get_attribute('href')
            links.append(link+'/brands')
            # Добавляем дополнительные страницы
            for i in range(2, 11):
                modified_link = f"{link}/brands/{i}"
                links.append(modified_link)

        return links

# Извлекаем ссылки на бренды из каждой категории
def extract_view_brand_links_from_categories():
    links = extract_and_store_category_links()
    brand_links = {}

    with webdriver.Chrome(service=service, options=chrome_options) as browser:
        for url in links:
            print(f"Скрапим страницу: {url}")

            try:
                browser.get(url)
                time.sleep(5)

                elements = browser.find_elements(By.XPATH, "//a[contains(text(), 'View Brand')]")
                category_links = []

                for element in elements:
                    link = element.get_attribute('href')
                    category_links.append(link)

                brand_links[url] = category_links

            except TimeoutException as e:
                print(f"Ошибка тайм-аута на странице {url}: {e}")
            except WebDriverException as e:
                print(f"Ошибка WebDriver на странице {url}: {e}")
            except Exception as e:
                print(f"Ошибка на странице {url}: {e}")

    return brand_links

# Извлекаем ссылки на продукты с текста "View Product"
def extract_view_product_links_from_brands():
    brand_links = extract_view_brand_links_from_categories()
    product_links = {}

    with webdriver.Chrome(service=service, options=chrome_options) as browser:
        for brand_url, brand_page_links in brand_links.items():
            for page_url in brand_page_links:
                print(f"Скрапим страницу бренда: {page_url}")

                try:
                    browser.get(page_url)
                    time.sleep(5)

                    # Ищем все ссылки с текстом "View Product"
                    product_elements = browser.find_elements(By.XPATH, "//a[contains(text(), 'View Product')]")
                    product_page_links = []

                    for product_element in product_elements:
                        product_link = product_element.get_attribute('href')
                        product_page_links.append(product_link)

                    product_links[page_url] = product_page_links

                except TimeoutException as e:
                    print(f"Ошибка тайм-аута на странице {page_url}: {e}")
                except WebDriverException as e:
                    print(f"Ошибка WebDriver на странице {page_url}: {e}")
                except Exception as e:
                    print(f"Ошибка на странице {page_url}: {e}")

    return product_links


# # Сохраняем данные в CSV файл
# def save_to_csv(data, filename="brand_links.csv"):
#     with open(filename, mode='w', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         writer.writerow(["Category URL", "Brand URL"])  # Заголовки

#         for category_url, links in data.items():
#             for link in links:
#                 writer.writerow([category_url, link])

# # Сохраняем данные в JSON файл
# def save_to_json(data, filename="brand_links.json"):
#     with open(filename, 'w', encoding='utf-8') as file:
#         json.dump(data, file, ensure_ascii=False, indent=4)

# # Главная функция для вывода и сохранения данных
# def print_and_save_extracted_links():
#     brand_links = extract_view_brand_links_from_categories()

#     # Печатаем все ссылки
#     for category_url, links in brand_links.items():
#         print(f"\Categories: {category_url}")
#         for link in links:
#             print(f"  - {link}")

#     # Сохраняем данные в CSV и JSON файлы
#     save_to_csv(brand_links)
#     save_to_json(brand_links)



# Пример использования
if __name__ == "__main__":
    product_links = extract_view_product_links_from_brands()
    # Сохраняем или выводим полученные ссылки
    for brand_page, products in product_links.items():
        print(f"Для страницы бренда {brand_page} найдены следующие продукты:")
        for product_link in products:
            print(f" - {product_link}")