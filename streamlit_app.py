import streamlit as st
import yfinance as yf
import pandas as pd
import time

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Lyra Sentinel v2", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0E1117; color: white; }
    .signal-box { padding: 20px; border-radius: 10px; text-align: center; font-weight: bold; font-size: 24px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

def get_data():
    offset = 18.5
    gold = yf.Ticker("GC=F").history(period="1d", interval="1m")
    precio = round(gold['Close'].iloc[-1] - offset, 2)
    # Cálculo simple de RSI para la señal
    delta = gold['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1+rs))
    return precio, round(rsi.iloc[-1], 2)

precio_actual, rsi_actual = get_data()

# --- INTERFAZ DE USUARIO ---
st.title("🛡️ Lyra Sentinel: Monitor de Señales")

# 1. Input para tu entrada actual
mi_entrada = st.number_input("Tu precio de entrada actual (0 si no tenés)", value=0.0)

# 2. Lógica de SEÑAL CLARA
st.subheader("📢 Recomendación de Lyra")

if rsi_actual > 70:
    st.markdown('<div class="signal-box" style="background-color: #ff4b4b; color: white;">⚠️ VENDER (Sobrecompra)</div>', unsafe_allow_html=True)
elif rsi_actual < 35:
    st.markdown('<div class="signal-box" style="background-color: #28a745; color: white;">🚀 COMPRAR (Sobrevendido)</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="signal-box" style="background-color: #f1c40f; color: black;">⏳ ESPERAR (Mercado Neutral)</div>', unsafe_allow_html=True)

# 3. Métricas Principales
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("PRECIO ACTUAL", f"${precio_actual}")
with col2:
    st.metric("RSI (14)", f"{rsi_actual}")
with col3:
    if mi_entrada > 0:
        pnl = precio_actual - mi_entrada
        st.metric("P&L ACTUAL", f"{pnl:.2f} pts")
    else:
        st.metric("P&L", "Sin operación")

st.divider()
st.info(f"💡 Análisis: El RSI está en {rsi_actual}. Basado en las noticias de Ginebra, {'buscamos rebotes' if rsi_actual < 40 else 'cuidado con nuevas subidas'}.")

time.sleep(30)
st.rerun()
                
