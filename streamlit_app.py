import streamlit as st
import yfinance as yf
import pandas as pd
import time

# Título simple para Germán
st.set_page_config(page_title="Monitor Oro - Germán", layout="centered")

def obtener_datos_oro():
    try:
        # Intentamos obtener el ticker directamente
        ticker = yf.Ticker("XAUUSD=X")
        # Pedimos solo los datos de hoy para que sea ultra liviano
        df = ticker.history(period="1d", interval="1m")
        
        if not df.empty:
            precio = df['Close'].iloc[-1]
            
            # Cálculo de RSI manual basado en los datos recibidos
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
st.title("📊 Monitor de Oro")
st.write(f"Cuenta: **Germán** | Capital: $25.00 USD")

precio, rsi = obtener_datos_oro()

if precio:
    # Mostramos los valores reales
    st.metric("PRECIO XAU/USD", f"${precio:,.2f}")
    st.metric("RSI (Fuerza)", f"{rsi:.2f}")
    
    st.divider()
    
    # --- VEREDICTO DE TRADING ---
    if rsi < 30:
        st.success("🟢 COMPRAR: Precio bajo (Sobreventa).")
    elif rsi > 70:
        st.warning("🔴 VENDER: Precio alto (Sobrecompra).")
    else:
        # El RSI de 56.69 que vimos antes cae acá
        st.info("🟡 ESPERAR: No hay señal clara. Cuidá tus $25.")

else:
    st.error("⚠️ Error de conexión temporal. Reintentando...")
    time.sleep(10)
    st.rerun()

# Refresco cada 30 segundos
time.sleep(30)
st.rerun()
