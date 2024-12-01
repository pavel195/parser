import csv
import requests
from requests_html import HTMLSession
import re
import json
import os

# Функция для получения хэша с каждой страницы бренда
def get_hash_from_brand_page(url):
    session = HTMLSession()
    response = session.get(url)

    # Ищем <script> с хэшем
    script_tags = response.html.xpath('/html/head/script[@src]')
    hash_pattern = re.compile(r'/_next/static/([a-f0-9]{40})/')

    hash_value = None
    for tag in script_tags:
        src = tag.attrs.get("src", "")
        match = hash_pattern.search(src)
        if match:
            hash_value = match.group(1)
            break

    if hash_value:
        return hash_value
    else:
        print(f"Хэш для страницы {url} не найден.")
        return None

# Функция для формирования запроса JSON
def get_json_data_for_brand(brand_url):
    # Получаем хэш с страницы
    hash_value = get_hash_from_brand_page(brand_url)
    
    if not hash_value:
        return None

    # Формируем URL для запроса JSON
    brand_path = brand_url.split('knowde.com')[1]  # Берем часть пути после 'https://www.knowde.com'
    json_url = f"https://www.knowde.com/_next/data/{hash_value}{brand_path}.json"

    # Отправляем GET-запрос
    response = requests.get(json_url)
    if response.status_code == 200:
        return response.json()  # Возвращаем данные в формате JSON
    else:
        print(f"Ошибка при получении данных для {brand_url}: {response.status_code}")
        return None

# Функция для чтения ссылок из CSV файла
def read_brand_links_from_csv(filename="unique_brand_links.csv"):
    brand_links = []
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Пропускаем заголовок
        for row in reader:
            if row:
                brand_links.append(row[0])  # Предполагаем, что ссылки находятся в первом столбце
    return brand_links

# Функция для сохранения данных в JSON файл
def save_data_to_json(data, filename="brand_data.json"):
    with open(filename, 'a', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
        file.write("\n")

# Главная функция для получения данных для всех брендов
def get_and_save_brand_data():
    brand_links = read_brand_links_from_csv()

    # Создаем папку для хранения JSON файлов, если ее нет
    if not os.path.exists("brand_data"):
        os.makedirs("brand_data")

    for brand_url in brand_links:
        print(f"Обрабатываем бренд: {brand_url}")

        # Получаем JSON данные для бренда
        json_data = get_json_data_for_brand(brand_url)

        if json_data:
            # Сохраняем данные в отдельный файл по имени бренда
            brand_name = brand_url.split('/')[-1]  # Имя бренда из URL
            filename = os.path.join("brand_data", f"{brand_name}.json")

            # Записываем данные в файл
            save_data_to_json(json_data, filename)

if __name__ == "__main__":
    get_and_save_brand_data()
