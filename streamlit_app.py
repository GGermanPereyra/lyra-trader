import streamlit as st
import yfinance as yf
import pandas as pd
import time

# Configuración de página
st.set_page_config(page_title="Monitor de Oro - Germán", layout="centered")

def obtener_datos_oro():
    try:
        # Probamos con el símbolo de Futuros de Oro (GC=F) que es el más confiable
        ticker_oro = "GC=F"
        data = yf.download(ticker_oro, period="1d", interval="2m", progress=False)
        
        if data.empty:
            # Si falla, probamos con una alternativa común
            data = yf.download("GLD", period="1d", interval="2m", progress=False)
            
        if not data.empty:
            precio = data['Close'].iloc[-1]
            
            # Cálculo de RSI manual
            delta = data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rsi = 100 - (100 / (1 + (gain / loss).iloc[-1]))
            
            return precio, rsi
    except:
        return None, None
    return None, None

# --- INTERFAZ ---
st.title("📊 Monitor de Oro Real")
st.write(f"Operador: **Germán** | Capital: $25.00 USD")

precio, rsi = obtener_datos_oro()

if precio:
    st.metric("ORO (GC=F)", f"${precio:,.2f}")
    st.metric("Fuerza RSI", f"{rsi:.2f}")
    
    st.divider()
    
    # Lógica de protección para tus $25
    if rsi < 30:
        st.success("🟢 COMPRA: El precio está en niveles bajos.")
    elif rsi > 70:
        st.warning("🔴 VENTA: El precio está muy alto.")
    else:
        st.info("🟡 ESPERAR: No hay señal clara en este momento.")

else:
    st.error("🔄 Error de servidor de datos. Reintentando con otro canal...")
    time.sleep(10)
    st.rerun()

# Refresco cada 30 segundos
time.sleep(30)
st.rerun()
