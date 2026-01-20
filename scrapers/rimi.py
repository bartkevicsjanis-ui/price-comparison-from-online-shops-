from playwright.sync_api import sync_playwright
from scrapers.utils import normalize_name, strip_diacritics

def search_rimi(product_name):
    query = strip_diacritics(product_name)
    url = f"https://www.rimi.lv/e-veikals/lv/meklesana?q={query}"

    products = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=30000)
        page.wait_for_selector("div.product-grid__item", timeout=15000)

        items = page.query_selector_all("div.product-grid__item")

        for item in items:
            name = item.query_selector("p.product-name")
            price = item.query_selector("span.price__integer")

            if not name or not price:
                continue

            products.append({
                "shop": "Rimi",
                "name": name.inner_text().strip(),
                "norm_name": normalize_name(name.inner_text()),
                "price": float(price.inner_text().replace(",", "."))
            })

        browser.close()

    return products
