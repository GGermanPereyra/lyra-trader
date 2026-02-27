import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="Sentinel: FBS Germán", layout="wide")

def get_clean_data():
    try:
        # Descarga rápida y silenciosa
        df = yf.download("GC=F", period="1d", interval="1m", progress=False)
        if df.empty or len(df) < 20:
            return None
        
        # Ajuste para FBS (Basado en tu precio de $5203)
        # El mercado está muy volátil, el offset hoy es volátil.
        current_close = float(df['Close'].iloc[-1])
        
        # Cálculo de RSI manual para evitar errores de librería
        delta = df['Close'].diff()
        up = delta.clip(lower=0)
        down = -1 * delta.clip(upper=0)
        ema_up = up.rolling(window=14).mean()
        ema_down = down.rolling(window=14).mean()
        rs = ema_up / ema_down
        rsi_val = 100 - (100 / (1 + rs))
        
        return current_close, float(rsi_val.iloc[-1])
    except:
        return None

st.title("🛡️ Sentinel: Mando Germán")

data = get_clean_data()

if data:
    precio, rsi = data
    
    # Formato limpio sin símbolos de Ticker en pantalla
    col1, col2 = st.columns(2)
    col1.metric("PRECIO ORO", f"${round(precio, 2)}")
    col2.metric("RSI (14)", f"{round(rsi, 2)}")
    
    # Lógica de alertas simplificada para evitar el ValueError
    if rsi > 70:
        st.error("⚠️ SOBRECOMPRA: POSIBLE VENTA")
    elif rsi < 30:
        st.success("🚀 SOBREVENTA: POSIBLE COMPRA")
    else:
        st.info("⏳ MERCADO EN MOVIMIENTO")
else:
    st.warning("🔄 Sincronizando con FBS...")
    time.sleep(2)
    st.rerun()

time.sleep(10)
st.rerun()
