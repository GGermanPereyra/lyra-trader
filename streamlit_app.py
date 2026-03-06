import streamlit as st
import yfinance as yf
import pandas as pd
import time

# --- CONFIGURACIÓN PARA TU CELULAR ---
st.set_page_config(page_title="Protección Alemana", layout="centered")

def obtener_datos():
    try:
        # Descargamos el Oro (XAUUSD=X)
        df = yf.download("XAUUSD=X", period="2d", interval="1m", progress=False)
        if df.empty: return None
        
        precio = df['Close'].iloc[-1]
        
        # --- CÁLCULO MANUAL DEL RSI (14) ---
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs.iloc[-1]))
        
        # --- SMA 200 (Tendencia) ---
        sma = df['Close'].rolling(window=200).mean().iloc[-1]
        
        return precio, rsi, sma
    except:
        return None

# --- INTERFAZ VISUAL ---
st.title("🛡️ Protección Alemana")
st.write(f"**Germán**, monitoreando tus $25.00 USD")

datos = obtener_datos()

if datos:
    precio, rsi, sma = datos
    
    col1, col2 = st.columns(2)
    col1.metric("XAU/USD (ORO)", f"${precio:,.2f}")
    col1.metric("RSI (M1)", f"{rsi:.2f}")
    col2.write(f"**Media Móvil (200):**\n${sma:,.2f}")
    
    st.divider()
    
    # --- VEREDICTO CLARO ---
    st.subheader("📢 Veredicto")
    
    if rsi < 32 and precio > sma:
        st.success("🟢 COMPRA: Precio bajo en tendencia alcista.")
    elif rsi > 68 and precio < sma:
        st.warning("🔴 VENTA: Precio alto en tendencia bajista.")
    else:
        st.info("🟡 ESPERAR: No hay señal clara todavía.")
    
    # --- GESTIÓN DE RIESGO ---
    st.divider()
    sl_pips = st.slider("Pips de Stop Loss", 10, 50, 30)
    st.write(f"Riesgo de la operación: **${sl_pips * 0.1:.2f} USD**")

else:
    st.error("Conectando con el mercado...")
    time.sleep(5)
    st.rerun()

# Refresco cada 15 segundos
time.sleep(15)
st.rerun()
