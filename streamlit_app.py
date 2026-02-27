import streamlit as st
import yfinance as yf
import pandas as pd
import feedparser
import time

st.set_page_config(page_title="Lyra Sentinel PRO", layout="wide")

# Estilo Oscuro Premium
st.markdown("""
    <style>
    .main { background-color: #0E1117; color: white; }
    .signal-box { padding: 30px; border-radius: 15px; text-align: center; font-weight: bold; font-size: 32px; border: 2px solid #30363D; }
    </style>
    """, unsafe_allow_html=True)

def get_data():
    offset = 18.5
    gold = yf.Ticker("GC=F").history(period="1d", interval="1m")
    precio = round(gold['Close'].iloc[-1] - offset, 2)
    delta = gold['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1+rs))
    return precio, round(rsi.iloc[-1], 2)

def get_real_news():
    url = "https://news.google.com/rss/search?q=Gold+price+Geneva+Iran+Trump&hl=es-419&gl=AR&ceid=AR:es-419"
    feed = feedparser.parse(url)
    return feed.entries[:3]

precio_actual, rsi_actual = get_data()

st.title("🛡️ Lyra Sentinel: Control de Ginebra")

# SEÑAL CLARA
if rsi_actual > 70:
    st.markdown('<div class="signal-box" style="background-color: #ff4b4b;">⚠️ SEÑAL: VENDER (Sobrecompra)</div>', unsafe_allow_html=True)
elif rsi_actual < 35:
    st.markdown('<div class="signal-box" style="background-color: #28a745;">🚀 SEÑAL: COMPRAR (Sobrevendido)</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="signal-box" style="background-color: #f1c40f; color: black;">⏳ SEÑAL: ESPERAR (Neutral)</div>', unsafe_allow_html=True)

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.metric("ORO SPOT", f"${precio_actual}")
    st.metric("RSI (14)", f"{rsi_actual}")

with col2:
    st.subheader("📰 Noticias Reales de Ginebra")
    noticias = get_real_news()
    for n in noticias:
        st.write(f"🔗 [{n.title}]({n.link})")

time.sleep(30)
st.rerun()
