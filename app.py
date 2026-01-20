import streamlit as st
import pandas as pd

from scrapers.rimi import search_rimi
from scrapers.barbora import search_barbora
from scrapers.etop import search_etop

st.set_page_config(layout="wide")
st.title("Price Comparison")

product = st.text_input("Product name")

if product:
    results = []

    try:
        results.extend(search_rimi(product))
    except:
        pass

    try:
        results.extend(search_barbora(product))
    except:
        pass

    try:
        results.extend(search_etop(product))
    except:
        pass

    if results:
        df = pd.DataFrame(results)
        df = df.sort_values("price")
        st.dataframe(df, use_container_width=True)

        cheapest = df.iloc[0]
        st.write(f"Cheapest: {cheapest['shop']} — {cheapest['price']} €")
    else:
        st.write("No results")
