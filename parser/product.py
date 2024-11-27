from requests_html import HTMLSession
import re

# Создаем сессию
session = HTMLSession()

# Загружаем страницу
url = "https://www.knowde.com/stores/evonik/products/dynasylan-vps-7163"  # Замените на нужный URL
response = session.get(url)


# Ищем <script> с хэшем
script_tags = response.html.xpath('/html/head/script[@src]')  # Все <script> с атрибутом src
hash_pattern = re.compile(r'/_next/static/([a-f0-9]{40})/')

hash_value = None
for tag in script_tags:
    src = tag.attrs.get("src", "")
    match = hash_pattern.search(src)
    if match:
        hash_value = match.group(1)
        break

if hash_value:
    print("Хэш найден:", hash_value)
else:
    print("Хэш не найден.")

