import streamlit as st
import yfinance as yf
import pandas as pd
import time

# Título para tu cuenta
st.set_page_config(page_title="Monitor Germán", layout="centered")

def obtener_datos_seguros():
    try:
        # Usamos el Ticker directamente para mayor estabilidad
        oro = yf.Ticker("XAUUSD=X")
        # Pedimos solo los datos necesarios para el RSI
        df = oro.history(period="2d", interval="2m")
        
        if not df.empty:
            precio = df['Close'].iloc[-1]
            
            # Cálculo de RSI manual (sin librerías externas)
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rsi = 100 - (100 / (1 + (gain / loss).iloc[-1]))
            
            return precio, rsi
    except:
        return None, None
    return None, None

# --- INTERFAZ ---
st.title("📊 Monitor de Oro")
st.write(f"Operador: **Germán** | Capital: $25.00 USD")

precio, rsi = obtener_datos_seguros()

if precio:
    # Mostramos los valores reales de tu MetaTrader
    st.metric("PRECIO XAU/USD", f"${precio:,.2f}")
    st.metric("RSI (Fuerza)", f"{rsi:.2f}")
    
    st.divider()
    
    # --- VEREDICTO ---
    # Con el RSI en 56.69 (según tu captura), el sistema dirá:
    if rsi < 32:
        st.success("🟢 COMPRAR: Sobreventa.")
    elif rsi > 68:
        st.warning("🔴 VENDER: Sobrecompra.")
    else:
        st.info("🟡 ESPERAR: Zona neutral. Protegiendo tus $25.")

else:
    st.warning("🔄 Sincronizando datos... (Reintento automático)")
    time.sleep(10)
    st.rerun()

# Refresco cada 30 segundos
time.sleep(30)
st.rerun()
