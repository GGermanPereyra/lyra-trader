import streamlit as st
import yfinance as yf
import pandas as pd
import time

# --- CONFIGURACIÓN PARA GERMÁN ---
st.set_page_config(page_title="Protección Alemana", layout="centered")

def obtener_precio_real():
    try:
        # Intentamos descargar el Oro (XAUUSD=X)
        data = yf.download("XAUUSD=X", period="1d", interval="1m", progress=False)
        if not data.empty:
            precio = data['Close'].iloc[-1]
            
            # Cálculo de RSI manual (sin librerías extras)
            delta = data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs.iloc[-1]))
            
            return precio, rsi
    except:
        return None, None
    return None, None

# --- INTERFAZ ---
st.title("🛡️ Protección Alemana")
st.write(f"**Germán**, monitoreando tus $25.00 USD")

precio, rsi = obtener_precio_real()

if precio is not None:
    # Mostramos el precio real de MetaTrader
    st.metric("XAU/USD (ORO)", f"${precio:,.2f}")
    st.metric("RSI (1M)", f"{rsi:.2f}")
    
    st.divider()
    
    # --- VEREDICTO SIMPLE Y SEGURO ---
    st.subheader("📢 Veredicto")
    if rsi < 30:
        st.success("🟢 COMPRA: Sobreventa detectada.")
    elif rsi > 70:
        st.warning("🔴 VENTA: Sobrecompra detectada.")
    else:
        st.info("🟡 ESPERAR: Mercado en zona neutral.")

    # --- RIESGO ---
    st.divider()
    sl_pips = st.slider("Pips de Stop Loss", 10, 50, 30)
    st.write(f"Pérdida potencial: **${sl_pips * 0.1:.2f} USD**")

else:
    st.warning("🔄 Sincronizando con el servidor... Reintentando en 5 segundos.")
    time.sleep(5)
    st.rerun()

# Refresco cada 30 segundos para no saturar la conexión del cel
time.sleep(30)
st.rerun()
