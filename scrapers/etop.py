import requests
from bs4 import BeautifulSoup
from scrapers.utils import normalize_name, strip_diacritics

BASE_URL = "https://etop.lv/lv/meklet"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def search_etop(product_name):
    clean_query = strip_diacritics(product_name)

    r = requests.get(
        BASE_URL,
        params={"q": clean_query},
        headers=HEADERS,
        timeout=10
    )

    soup = BeautifulSoup(r.text, "lxml")

    products = []
    for item in soup.select("div.product-item"):
        name = item.select_one("a.product-title")
        price = item.select_one("span.price")

        if not name or not price:
            continue

        products.append({
            "shop": "eTop",
            "name": name.text.strip(),
            "norm_name": normalize_name(name.text),
            "price": float(price.text.replace(",", "."))
        })

    return products
