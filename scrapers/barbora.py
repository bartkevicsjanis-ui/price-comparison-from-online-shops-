from playwright.sync_api import sync_playwright
from scrapers.utils import normalize_name, strip_diacritics

def search_barbora(product_name):
    query = strip_diacritics(product_name)
    products = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            locale="lv-LV",
            geolocation={"latitude": 56.9496, "longitude": 24.1052},
            permissions=["geolocation"]
        )
        page = context.new_page()

        page.goto("https://barbora.lv", timeout=30000)

        # accept cookies
        try:
            page.click("button:has-text('Piekrītu')", timeout=5000)
        except:
            pass

        # search
        page.goto(f"https://barbora.lv/meklet?q={query}", timeout=30000)
        page.wait_for_selector("div.b-product--wrap", timeout=15000)

        items = page.query_selector_all("div.b-product--wrap")

        for item in items:
            name = item.query_selector("div.b-_
