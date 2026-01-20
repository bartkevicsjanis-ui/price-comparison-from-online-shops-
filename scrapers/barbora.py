import requests
from bs4 import BeautifulSoup

BASE_URL = "https://barbora.lv/meklet"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def search_barbora(product_name):
    params = {"q": product_name}
    r = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(r.text, "lxml")

    products = []
    for item in soup.select("div.b-product--wrap"):
        name = item.select_one("div.b-product--title")
        price = item.select_one("span.b-product--price-number")

        if not name or not price:
            continue

        products.append({
            "shop": "Barbora",
            "name": name.text.strip(),
            "price": float(price.text.replace(",", "."))
        })

    return products
