import streamlit as st
import yfinance as yf
import pandas as pd
import time

# Configuración ligera
st.set_page_config(page_title="Lira Celular", layout="centered")

def obtener_tick_rapido():
    try:
        # Pedimos solo 1 hora de datos para que la descarga sea instantánea en el cel
        ticker = yf.Ticker("XAUUSD=X")
        df = ticker.history(period="1h", interval="1m")
        if not df.empty:
            precio = float(df['Close'].iloc[-1])
            # RSI de respuesta inmediata
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=7).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=7).mean()
            rsi = 100 - (100 / (1 + (gain.iloc[-1] / loss.iloc[-1])))
            return precio, float(rsi)
    except:
        return None, None
    return None, None

st.title("🎯 Monitor Móvil")
st.write("Operador: **Germán**")

precio, rsi = obtener_tick_rapido()

if precio:
    st.metric("PRECIO XAU/USD", f"${precio:,.2f}")
    st.write(f"**Fuerza (RSI):** {rsi:.2f}")
    
    if rsi <= 30:
        st.success("🟢 POSIBLE COMPRA")
    elif rsi >= 70:
        st.error("🔴 POSIBLE VENTA")
    else:
        st.info("⚖️ MERCADO EN RANGO")
else:
    st.warning("Sincronizando... Refrescá la pestaña si tarda mucho.")

# Refresco cada 10 segundos (ideal para datos móviles)
time.sleep(10)
st.rerun()
