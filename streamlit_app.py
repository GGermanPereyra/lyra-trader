import streamlit as st
import requests
import pandas as pd
import time

# --- CONFIGURACIÓN ---
API_KEY = "0KJHUGOLZHLYYAJC"
SYMBOL = "XAUUSD" # Oro Spot

st.set_page_config(page_title="Lira Gold PRO", layout="centered")

def obtener_datos_alpha(symbol):
    try:
        # Consulta directa a la API profesional
        url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=XAU&to_currency=USD&apikey={API_KEY}'
        r = requests.get(url)
        data = r.json()
        
        # Extraemos el precio real
        rate_data = data['Realtime Currency Exchange Rate']
        precio = float(rate_data['5. Exchange Rate'])
        actualizacion = rate_data['6. Last Refreshed']
        
        # Para el RSI profesional necesitamos la serie de tiempo (Intraday)
        url_rsi = f'https://www.alphavantage.co/query?function=RSI&symbol={symbol}&interval=1min&time_period=14&series_type=close&apikey={API_KEY}'
        r_rsi = requests.get(url_rsi)
        data_rsi = r_rsi.json()
        
        # Obtenemos el último valor de RSI
        last_date = list(data_rsi['Technical Analysis: RSI'].keys())[0]
        rsi = float(data_rsi['Technical Analysis: RSI'][last_date]['RSI'])
        
        return precio, rsi, actualizacion
    except Exception as e:
        return None, None, None

# --- INTERFAZ ---
st.title("🎯 Lira Precision PRO")
st.write(f"Operador: **Germán** | Fuente: **Alpha Vantage API**")

precio, rsi, hora = obtener_datos_alpha(SYMBOL)

if precio:
    col1, col2 = st.columns(2)
    with col1:
        st.metric("PRECIO ORO (REAL)", f"${precio:,.2f}")
    with col2:
        st.metric("RSI (14)", f"{rsi:.2f}")
    
    st.caption(f"🕒 Última actualización de red: {hora}")
    st.divider()

    # --- LÓGICA DE TRADING PROFESIONAL ---
    # Riesgo calculado para tu cuenta de $32 USD
    sl_puntos = 2.5  # Stop Loss
    tp_puntos = 4.0  # Take Profit

    if rsi <= 30:
        st.success("🟢 SEÑAL DE COMPRA (BUY)")
        st.write(
