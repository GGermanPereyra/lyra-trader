import streamlit as st
import yfinance as yf
import pandas as pd
import feedparser
import time

st.set_page_config(page_title="Lyra Sentinel: Expert Advisor", layout="wide")

def get_market_data():
    # Tu ajuste de calibración actual
    offset = 20.33
    
    try:
        # Intentamos descargar los datos con un margen de error más amplio
        ticker = yf.Ticker("GC=F")
        gold = ticker.history(period="1d", interval="1m")
        
        # Si la descarga falla o no hay suficientes velas para los indicadores
        if gold.empty or len(gold) < 30:
            return None
        
        df = gold.copy()
        df['Close_Adj'] = df['Close'] - offset
        
        # --- CÁLCULOS TÉCNICOS ---
        # RSI
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        df['RSI'] = 100 - (100 / (1 + (gain / loss)))
        
        # MACD
        df['EMA12'] = df['Close'].ewm(span=12, adjust=False).mean()
        df['EMA26'] = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = df['EMA12'] - df['EMA26']
        df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        
        # Bollinger
        df['SMA20'] = df['Close_Adj'].rolling(window=20).mean()
        df['STD20'] = df['Close_Adj'].rolling(window=20).std()
        df['Upper'] = df['SMA20'] + (df['STD20'] * 2)
        df['Lower'] = df['SMA20'] - (df['STD20'] * 2)
        
        return df.iloc[-1]
    except Exception as e:
        return None

# --- INTERFAZ ---
data = get_market_data()

st.title("🛡️ Lyra Sentinel: Niveles Operativos")

if data is not None:
    precio = round(data['Close_Adj'], 2)
    rsi_val = round(data['RSI'], 2)
    macd_alcista = data['MACD'] > data['Signal']
    
    # Niveles de salida sugeridos
    tp_compra = round(data['Upper'], 2)
    sl_compra = round(data['Lower'] - 5, 2)
    tp_venta = round(data['Lower'], 2)
    sl_venta = round(data['Upper'] + 5, 2)

    # SEMÁFORO DE SEÑALES
    if rsi_val < 35 and macd_alcista:
        st.success(f"🚀 SEÑAL: COMPRA (RSI: {rsi_val})")
        c1, c2, c3 = st.columns(3)
        c1.metric("ENTRADA", f"${precio}")
        c2.metric("TAKE PROFIT", f"${tp_compra}")
        c3.metric("STOP LOSS", f"${sl_compra}")
    elif rsi_val > 70 and not macd_alcista:
        st.error(f"⚠️ SEÑAL: VENTA (RSI: {rsi_val})")
        c1, c2, c3 = st.columns(3)
        c1.metric("ENTRADA", f"${precio}")
        c2.metric("TAKE PROFIT", f"${tp_venta}")
        c3.metric("STOP LOSS", f"${sl_venta}")
    else:
        st.warning(f"⏳ ESPERAR: Mercado en calma (RSI: {rsi_val})")

    st.divider()
    st.write(f"📊 **Estado:** ORO en ${precio} | MACD {'Alcista ✅' if macd_alcista else 'Bajista ❌'}")
else:
    # Si falla, mostramos un aviso amigable y reintentamos rápido
    st.info("🔄 Lyra está reconectando con el mercado de Ginebra...")
    time.sleep(5)
    st.rerun()

# Refresco cada 30 segundos
time.sleep(25)
st.rerun()
    
