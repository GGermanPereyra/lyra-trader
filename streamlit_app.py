import streamlit as st
import yfinance as yf
import pandas as pd
import feedparser
import time

# Configuración de la página
st.set_page_config(page_title="Lyra Sentinel: Niveles Operativos", layout="wide")

def get_market_data():
    # Tu ajuste de calibración actualizado
    offset = 20.33
    
    # Descarga de datos
    gold = yf.Ticker("GC=F").history(period="1d", interval="1m")
    if gold.empty: 
        return None
    
    df = gold.copy()
    df['Close_Adj'] = df['Close'] - offset
    
    # Cálculo de RSI (14)
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    df['RSI'] = 100 - (100 / (1 + (gain / loss)))
    
    # Cálculo de MACD (12, 26, 9)
    df['EMA12'] = df['Close'].ewm(span=12, adjust=False).mean()
    df['EMA26'] = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = df['EMA12'] - df['EMA26']
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    
    # Cálculo de Bandas de Bollinger (20)
    df['SMA20'] = df['Close_Adj'].rolling(window=20).mean()
    df['STD20'] = df['Close_Adj'].rolling(window=20).std()
    df['Upper'] = df['SMA20'] + (df['STD20'] * 2)
    df['Lower'] = df['SMA20'] - (df['STD20'] * 2)
    
    return df.iloc[-1]

# Ejecución de la App
data = get_market_data()

st.title("🛡️ Lyra Sentinel: Niveles Operativos")

if data is not None:
    precio = round(data['Close_Adj'], 2)
    rsi_val = round(data['RSI'], 2)
    macd_alcista = data['MACD'] > data['Signal']
    
    # Precios Sugeridos
    tp_compra = round(data['Upper'], 2)
    sl_compra = round(data['Lower'] - 5, 2)
    
    tp_venta = round(data['Lower'], 2)
    sl_venta = round(data['Upper'] + 5, 2)

    # Lógica de Señales
    if rsi_val < 35 and macd_alcista:
        st.success(f"🚀 SEÑAL: COMPRA (RSI: {rsi_val})")
        c1, c2, c3 = st.columns(3)
        c1.metric("ENTRADA SUGERIDA", f"${precio}")
        c2.metric("TAKE PROFIT", f"${tp_compra}")
        c3.metric("STOP LOSS", f"${sl_compra}")
        
    elif rsi_val > 70 and not macd_alcista:
        st.error(f"⚠️ SEÑAL: VENTA (RSI: {rsi_val})")
        c1, c2, c3 = st.columns(3)
        c1.metric("ENTRADA SUGERIDA", f"${precio}")
        c2.metric("TAKE PROFIT", f"${tp_venta}")
        c3.metric("STOP LOSS", f"${sl_venta}")
    else:
        st.warning("⏳ ESPERAR: Sin niveles claros en este momento")

    st.divider()
    st.write(f"📊 **Estado actual:** Precio en ${precio} | RSI en {rsi_val}")
else:
    st.error("Error al obtener datos. Reintenta en unos segundos.")

# Auto-refresco
time.sleep(30)
st.rerun()
    
