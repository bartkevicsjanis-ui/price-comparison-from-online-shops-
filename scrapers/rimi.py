import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.rimi.lv/e-veikals/lv/meklesana"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def search_rimi(product_name):
    params = {"q": product_name}
    r = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(r.text, "lxml")

    products = []
    for item in soup.select("div.product-grid__item"):
        name = item.select_one("p.product-name")
        price = item.select_one("span.price__integer")

        if not name or not price:
            continue

        products.append({
            "shop": "Rimi",
            "name": name.text.strip(),
            "price": float(price.text.replace(",", "."))
        })

    return products
