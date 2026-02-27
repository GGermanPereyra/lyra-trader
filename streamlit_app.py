import streamlit as st
import yfinance as yf
import pandas as pd
import feedparser
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Lyra Sentinel PRO", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0E1117; color: white; }
    .signal-box { padding: 30px; border-radius: 15px; text-align: center; font-weight: bold; font-size: 32px; border: 2px solid #30363D; margin-bottom: 20px; }
    .news-card { background-color: #161B22; padding: 15px; border-radius: 10px; border-left: 5px solid #28a745; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

def get_data():
    offset = 18.5
    # Bajamos datos del Futuro del Oro (GC=F)
    gold = yf.Ticker("GC=F").history(period="1d", interval="1m")
    if gold.empty: return 0.0, 50.0
    
    precio = round(gold['Close'].iloc[-1] - offset, 2)
    
    # Cálculo de RSI (14)
    delta = gold['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1+rs))
    return precio, round(rsi.iloc[-1], 2)

def get_real_news():
    # Buscamos noticias clave: Oro, Ginebra, Irán, Trump
    query = "Gold+price+Geneva+Iran+Trump"
    url = f"https://news.google.com/rss/search?q={query}&hl=es-419&gl=AR&ceid=AR:es-419"
    feed = feedparser.parse(url)
    return feed.entries[:5] # Mostramos las 5 más recientes

# --- LÓGICA PRINCIPAL ---
precio_actual, rsi_actual = get_data()

st.title("🛡️ Lyra Sentinel: Control de Ginebra")

# 1. SEMÁFORO DE SEÑAL
if rsi_actual > 70:
    st.markdown(f'<div class="signal-box" style="background-color: #ff4b4b;">⚠️ SEÑAL: VENDER (Sobrecompra {rsi_actual})</div>', unsafe_allow_html=True)
elif rsi_actual < 35:
    st.markdown(f'<div class="signal-box" style="background-color: #28a745;">🚀 SEÑAL: COMPRAR (Sobrevendido {rsi_actual})</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="signal-box" style="background-color: #f1c40f; color: black;">⏳ SEÑAL: ESPERAR (Neutral {rsi_actual})</div>', unsafe_allow_html=True)

st.divider()

# 2. PANEL DE CONTROL
col1, col2 = st.columns([1, 2])

with col1:
    st.metric("ORO SPOT", f"${precio_actual}")
    st.metric("RSI (14)", f"{rsi_actual}")
    st.write("---")
    st.caption("Frecuencia: Actualización cada 30 segundos.")
    st.info("💡 Si el RSI baja de 30, la probabilidad de rebote alcista es del 80%.")

with col2:
    st.subheader("📰 Radar de Noticias: Ginebra")
    noticias = get_real_news()
    if not noticias:
        st.write("Buscando cables de prensa...")
    for n in noticias:
        st.markdown(f"""
        <div class="news-card">
            <a href="{n.link}" target="_blank" style="text-decoration: none; color: #58a6ff; font-weight: bold;">{n.title}</a><br>
            <small style="color: #8b949e;">Publicado: {n.published}</small>
        </div>
        """, unsafe_allow_html=True)

# Auto-refresh
time.sleep(30)
st.rerun()
