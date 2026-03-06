import streamlit as st
import yfinance as yf
import pandas as pd
import time

# --- TITULO PERSONALIZADO ---
st.set_page_config(page_title="Monitor de Trading - Germán", layout="centered")

def obtener_datos_oro():
    try:
        # Intentamos obtener datos del Oro (XAUUSD=X)
        # Cambiamos a un periodo de 1 día con intervalo de 2 minutos para mayor estabilidad
        df = yf.download("XAUUSD=X", period="1d", interval="2m", progress=False)
        if not df.empty:
            precio = df['Close'].iloc[-1]
            
            # Cálculo de RSI manual
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs.iloc[-1]))
            
            return precio, rsi
    except:
        return None, None
    return None, None

# --- INTERFAZ ---
st.title("📊 Monitor de Oro (XAU/USD)")
st.write(f"Cuenta de **Germán** | Capital: $25.00 USD")

precio, rsi = obtener_datos_oro()

if precio:
    # Mostramos los valores actuales
    st.metric("Precio del Oro", f"${precio:,.2f}")
    st.metric("Fuerza del Mercado (RSI)", f"{rsi:.2f}")
    
    st.divider()
    
    # --- LÓGICA DE TRADING ---
    # Según tu MetaTrader, el RSI actual está cerca de 56.69 (Zona Neutral)
    if rsi < 30:
        st.success("🟢 OPORTUNIDAD: El precio está bajo (Sobreventa).")
    elif rsi > 70:
        st.warning("🔴 RIESGO: El precio está muy alto (Sobrecompra).")
    else:
        st.info("🟡 ESPERAR: El mercado está tranquilo. No arriesgues tus $25.")

else:
    st.warning("🔄 Buscando conexión con el mercado... Esperá un momento.")
    time.sleep(5)
    st.rerun()

# Actualizar cada 30 segundos
time.sleep(30)
st.rerun()
