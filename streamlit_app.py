import streamlit as st
import yfinance as yf
import pandas as pd
import time

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Lyra Sentinel", layout="wide")

# Estilo visual personalizado
st.markdown("""
    <style>
    .main { background-color: #0E1117; color: white; }
    .stMetric { background-color: #161B22; border-radius: 10px; padding: 15px; border: 1px solid #30363D; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Lyra Sentinel: Oro & Ginebra")

# --- LÓGICA DE DATOS ---
def get_gold_data():
    # Sincronizado con tu MetaTrader (ajuste de offset)
    offset = 18.5 
    gold = yf.Ticker("GC=F").history(period="1d", interval="1m")
    precio_real = gold['Close'].iloc[-1] - offset
    return round(precio_real, 2)

def get_news():
    # Simulación de radar de noticias (Se puede conectar a RSS de Reuters/Bloomberg)
    news = [
        {"tema": "Ginebra", "titulo": "Tensión en negociaciones con Irán aumenta", "impacto": "Alcista"},
        {"tema": "Trump", "titulo": "Cumbre de paz en Ginebra muestra avances", "impacto": "Bajista"},
        {"tema": "Macro", "titulo": "Dólar se fortalece frente a activos refugio", "impacto": "Bajista"}
    ]
    return news

# --- INTERFAZ ---
col1, col2 = st.columns([1, 2])

with col1:
    precio = get_gold_data()
    st.metric(label="XAU/USD (SPOT)", value=f"${precio}", delta=f"{precio - 5191.40:.2f} vs Entrada")
    
    # Semáforo de Riesgo
    if precio > 5200:
        st.error("⚠️ RIESGO ALTO: Precio en zona de resistencia.")
    elif precio < 5160:
        st.success("✅ OPORTUNIDAD: Precio en zona de soporte/toma de ganancias.")
    else:
        st.warning("⚖️ BALANCE: Mercado en zona de pelea.")

with col2:
    st.subheader("📰 Radar de Noticias: Ginebra")
    for n in get_news():
        color = "red" if n['impacto'] == "Alcista" else "green"
        st.markdown(f"**[{n['tema']}]** {n['titulo']} | Impacto: :{color}[{n['impacto']}]")

st.info("💡 Consejo de Lyra: Las noticias de Ginebra son el motor hoy. Si sale acuerdo, el oro cae.")

# Auto-refresh cada 30 segundos
time.sleep(30)
st.rerun()
