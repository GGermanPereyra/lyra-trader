import streamlit as st
import requests
import pandas as pd
import time

# --- CONFIGURACIÓN ---
API_KEY = "0KJHUGOLZHLYYAJC"
SYMBOL = "XAUUSD"

st.set_page_config(page_title="Lira Gold PRO", layout="centered")

def obtener_datos_alpha():
    try:
        # Consulta de Precio Real
        url_p = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=XAU&to_currency=USD&apikey={API_KEY}'
        data_p = requests.get(url_p).json()
        rate_data = data_p['Realtime Currency Exchange Rate']
        precio = float(rate_data['5. Exchange Rate'])
        actualizacion = rate_data['6. Last Refreshed']
        
        # Consulta de RSI (14)
        url_r = f'https://www.alphavantage.co/query?function=RSI&symbol=XAUUSD&interval=1min&time_period=14&series_type=close&apikey={API_KEY}'
        data_r = requests.get(url_r).json()
        last_date = list(data_r['Technical Analysis: RSI'].keys())[0]
        rsi = float(data_r['Technical Analysis: RSI'][last_date]['RSI'])
        
        return precio, rsi, actualizacion
    except:
        return None, None, None

# --- INTERFAZ ---
st.title("🎯 Lira Precision PRO")
st.write("Operador: **Germán** | Fuente: **Alpha Vantage**")

precio, rsi, hora = obtener_datos_alpha()

if precio:
    col1, col2 = st.columns(2)
    with col1:
        st.metric("PRECIO ORO", f"${precio:,.2f}")
    with col2:
        st.metric("RSI (14)", f"{rsi:.2f}")
    
    st.caption(f"🕒 Sincronizado a las: {hora}")
    st.divider()

    # --- NIVELES DE ENTRADA ---
    distancia = 2.5 
    
    if rsi <= 30:
        st.success("🟢 SEÑAL DE COMPRA (BUY)")
        st.write(f"**Entrada:** {precio:.2f}")
        st.write(f"**STOP LOSS:** {precio - distancia:.2f}")
        st.write(f"**TAKE PROFIT:** {precio + 4.0:.2f}")
    elif rsi >= 70:
        st.error("🔴 SEÑAL DE VENTA (SELL)")
        st.write(f"**Entrada:** {precio:.2f}")
        st.write(f"**STOP LOSS:** {precio + distancia:.2f}")
        st.write(f"**TAKE PROFIT:** {precio - 4.0:.2f}")
    else:
        st.info("⚖️ MERCADO EN RANGO - Esperando señal.")
else:
    st.warning("⏳ Esperando respuesta de Alpha Vantage... (Límite: 5 consultas/min)")

time.sleep(60)
st.rerun()
