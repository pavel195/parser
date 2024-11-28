import requests
import json

# URL для получения JSON данных
json_url = "https://www.knowde.com/_next/data/67796398ac472c2d1ead32261d5090739325dab5/stores/wacker-chemie-ag/brands/elastosil.json"

# Отправляем GET-запрос
response = requests.get(json_url)

# Проверяем, что запрос успешен
if response.status_code == 200:
    # Парсим JSON из ответа
    data = response.json()
    
    # Выводим JSON в красивом формате
    print(json.dumps(data, indent=4))  # Pretty-print JSON
else:
    print(f"Не удалось получить данные. Статус код: {response.status_code}")
