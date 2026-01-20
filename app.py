import streamlit as st
import pandas as pd

from scrapers.rimi import search_rimi
from scrapers.barbora import search_barbora
from scrapers.etop import search_etop
from scrapers.utils import is_similar

st.set_page_config(layout="wide")
st.title("Price Comparison – Similar Products")

query = st.text_input("Product")

def group_similar(products):
    groups = []

    for p in products:
        matched = False
        for g in groups:
            if is_similar(p["norm_name"], g[0]["norm_name"]):
                g.append(p)
                matched = True
                break
        if not matched:
            groups.append([p])

    return groups

if query:
    all_products = []

    for fn in (search_rimi, search_barbora, search_etop):
        try:
            all_products.extend(fn(query))
        except:
            pass

    if not all_products:
        st.write("No results")
    else:
        groups = group_similar(all_products)

        for idx, group in enumerate(groups, start=1):
            st.subheader(f"Similar product #{idx}")

            df = pd.DataFrame(group)
            df = df.sort_values("price")
            st.dataframe(df[["shop", "name", "price"]], use_container_width=True)

            cheapest = df.iloc[0]
            st.write(f"Cheapest: {cheapest['shop']} — {cheapest['price']} €")
