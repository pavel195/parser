from requests_html import HTMLSession
import requests

url = "https://www.knowde.com/"

session = HTMLSession()

r = session.get(url)

categories = r.html.xpath('//*[@id="__app"]/div[2]/div[1]/section[1]/div/ul[2]', first = True)
print(type(categories))

for link in categories.absolute_links:
    print(link)

responce = requests.get('https://www.knowde.com/stores/wacker-chemie-ag/products/wacker-polymer-fd-350')
data = responce.json()
print(data)

token = '51b8b715263cef06c04c24b9a2a4eebe8b07861f'
token1 = '51b8b715263cef06c04c24b9a2a4eebe8b07861f'

# /html/head/script[74]
# /html/head/script[74]
# <script src="/_next/static/51b8b715263cef06c04c24b9a2a4eebe8b07861f/_buildManifest.js" defer=""></script>   
# <script src="/_next/static/51b8b715263cef06c04c24b9a2a4eebe8b07861f/_buildManifest.js" defer=""></script>
# https://www.knowde.com/_next/data/51b8b715263cef06c04c24b9a2a4eebe8b07861f/stores/braskem-america/brands/utec-ultra-high-molecular-weight-polyethylene.json
# https://www.knowde.com/_next/data/51b8b715263cef06c04c24b9a2a4eebe8b07861f/stores/evonik/brands/dynasylan.json