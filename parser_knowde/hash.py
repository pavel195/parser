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
# <script src="/_next/static/67796398ac472c2d1ead32261d5090739325dab5/_buildManifest.js" defer=""></script>
# https://www.knowde.com/_next/data/67796398ac472c2d1ead32261d5090739325dab5/stores/braskem-america/brands/braskem-recycled.json
# https://www.knowde.com/_next/data/67796398ac472c2d1ead32261d5090739325dab5/stores/wacker-chemie-ag/brands/dehesive.json
# <li class="storefront-breadcrumbs_wrapper__lbnM1 storefront-breadcrumbs_wrapperLast__fYMgM"><a class="storefront-breadcrumbs_link__nmc_X" hreflang="en-US" href="/stores/wacker-chemie-ag/brands/vinnapas"><div class="storefront-breadcrumbs_container__0eGz1"><span class="storefront-breadcrumbs_title__aUzi3">Brand</span><span class="storefront-breadcrumbs_name__a1yBG">VINNAPAS</span></div></a><svg class="icon_icon___L1OO storefront-breadcrumbs_arrow__TfGN0"><use href="/_next/static/media/icons.d7622331.svg#arrow-right"></use></svg></li>

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

