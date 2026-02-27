import streamlit as st
import yfinance as yf
import time

st.set_page_config(page_title="Sentinel: Germán v4", layout="wide")

def get_fast_data():
    try:
        # Usamos un ticker más estable para evitar que la app se quede en blanco
        data = yf.download("GC=F", period="1d", interval="1m", progress=False)
        if data.empty: return None
        
        # AJUSTE DINÁMICO FBS (10:07 AM)
        # Sincronizamos con tu último precio de $5194
        current_price = data['Close'].iloc[-1]
        fbs_price = current_price - 1.20 # Ajuste fino para FBS hoy
        
        # RSI rápido
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rsi = 100 - (100 / (1 + (gain / loss)))
        
        return fbs_price, rsi.iloc[-1]
    except:
        return None

st.title("🛡️ Sentinel: Inteligencia Germán")

result = get_fast_data()

if result:
    precio, rsi = result
    st.metric("ORO (FBS)", f"${round(precio, 2)}")
    st.metric("RSI (14)", f"{round(rsi, 2)}")
    
    if rsi > 70:
        st.error("⚠️ ZONA DE VENTA")
    elif rsi < 30:
        st.success("🚀 ZONA DE COMPRA")
    else:
        st.info("⏳ BUSCANDO ENTRADA")
else:
    st.warning("🔄 Reconexión automática en curso...")
    time.sleep(2)
    st.rerun()

time.sleep(15) # Refresco más rápido
st.rerun()
