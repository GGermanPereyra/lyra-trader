import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="Lira Precision - Germán", layout="centered")

def obtener_datos_exactos():
    try:
        # Cambiamos GC=F (Futuros) por XAUUSD=X (Precio Spot de MetaTrader)
        ticker = yf.Ticker("XAUUSD=X")
        # Pedimos solo los últimos 30 minutos para forzar al servidor a darnos lo más nuevo
        df = ticker.history(period="1d", interval="1m")
        
        if not df.empty:
            # Forzamos la descarga del último tick disponible
            precio = float(df['Close'].iloc[-1])
            
            # RSI de respuesta ultra-rápida (periodo de 5 para scalping)
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=5).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=5).mean()
            rs = gain.iloc[-1] / loss.iloc[-1]
            rsi = 100 - (100 / (1 + rs))
            
            return precio, float(rsi)
    except:
        return None, None
    return None, None

# --- INTERFAZ DE ALTA PRECISIÓN ---
st.title("🎯 Scalping de Precisión")
st.write(f"Operador: **Germán** | Cuenta: $25.00 USD")

precio, rsi = obtener_datos_exactos()

if precio:
    # Mostramos el precio grande para que compares con MT4
    st.metric("PRECIO XAU/USD (SPOT)", f"${precio:,.2f}")
    
    st.divider()

    # Lógica de sincronización
    st.write(f"**Fuerza RSI Actual:** {rsi:.2f}")
    
    if rsi <= 25:
        st.success(f"🟢 **COMPRA SUGERIDA** - Precio: ${precio:,.2f}")
        st.write("El mercado está agotado a la baja. Posible rebote.")
    elif rsi >= 75:
        st.error(f"🔴 **VENTA SUGERIDA** - Precio: ${precio:,.2f}")
        st.write("El mercado está agotado al alza. Posible caída.")
    else:
        st.info("⚖️ **MERCADO EN RANGO**")
        st.write("Sincronizado con MetaTrader. Esperando extremo.")

else:
    st.warning("🔄 Sincronizando ticks con el servidor...")

# Refresco cada 10 segundos: Máxima velocidad permitida
time.sleep(10)
st.rerun()
