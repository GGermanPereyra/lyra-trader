import streamlit as st
import yfinance as yf
import pandas as pd
import time

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Protección Alemana", layout="centered")

def obtener_datos_limpios():
    try:
        # Traemos datos del Oro (XAUUSD) de los últimos 5 días
        df = yf.download("XAUUSD=X", period="5d", interval="1m", progress=False)
        if df.empty: return None
        
        precio = df['Close'].iloc[-1]
        
        # Cálculo manual del RSI (14) para evitar errores de librerías
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs.iloc[-1]))
        
        # SMA 200 para tendencia (usando cierres de 1 minuto)
        sma = df['Close'].rolling(window=200).mean().iloc[-1]
        
        return precio, rsi, sma
    except:
        return None

# --- INTERFAZ ---
st.title("🛡️ Sistema de Protección Alemana")
st.write(f"**Capital:** $25.00 USD | **Estado:** Monitoreando ORO")

datos = obtener_datos_limpios()

if datos:
    precio, rsi, sma = datos
    
    col1, col2 = st.columns(2)
    col1.metric("XAU/USD (ORO)", f"${precio:,.2f}")
    col1.metric("RSI REAL", f"{rsi:.2f}")
    col2.write(f"**SMA 200:** ${sma:,.2f}")
    
    st.divider()
    
    # VEREDICTO CLARO (Basado en lo que vimos en tus capturas)
    if rsi < 32 and precio > sma:
        st.success("🟢 COMPRA FUERTE: Precio bajo en tendencia alcista.")
    elif rsi > 68 and precio < sma:
        st.warning("🔴 VENTA FUERTE: Precio alto en tendencia bajista.")
    else:
        st.info("🟡 ESPERAR: No hay confirmación segura todavía.")
        
    # GESTIÓN DE RIESGO
    st.divider()
    sl_pips = st.slider("Stop Loss (Pips)", 10, 50, 30)
    st.write(f"Riesgo de la operación: **${sl_pips * 0.1:.2f} USD**")

else:
    st.error("⚠️ Error de conexión con Yahoo Finance. Reintentando...")
    time.sleep(5)
    st.rerun()

time.sleep(15)
st.rerun()
