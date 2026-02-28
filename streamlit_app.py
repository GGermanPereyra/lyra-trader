import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="Sentinel: Protección Germán", layout="wide")

def get_market_data():
    try:
        # Descarga silenciosa y rápida
        ticker = yf.Ticker("GC=F")
        df = ticker.history(period="1d", interval="1m")
        
        if df.empty or len(df) < 15:
            return None
            
        # Limpieza de datos para evitar el ValueError
        last_price = float(df['Close'].iloc[-1])
        
        # Cálculo manual de RSI para mayor estabilidad
        delta = df['Close'].diff()
        up = delta.clip(lower=0).rolling(window=14).mean()
        down = -1 * delta.clip(upper=0).rolling(window=14).mean()
        rs = up / down
        rsi_val = 100 - (100 / (1 + rs))
        current_rsi = float(rsi_val.iloc[-1])
        
        return last_price, current_rsi
    except:
        return None

st.title("🛡️ Sistema de Protección Germán")

# --- GESTIÓN DE RIESGO EN BARRA LATERAL ---
with st.sidebar:
    st.header("💰 Control de Capital")
    saldo = st.number_input("Saldo Actual ($)", value=20.0, step=1.0)
    st.write(f"Riesgo Máx (2%): **${round(saldo * 0.02, 2)}**")
    st.warning("Regla: Si pierdes 2 operaciones seguidas, apaga la app.")

data = get_market_data()

if data:
    precio, rsi = data
    # Ajuste FBS dinámico para compensar el desfase que vimos hoy
    precio_fbs = precio - 1.50 
    
    col1, col2 = st.columns(2)
    col1.metric("ORO (FBS)", f"${round(precio_fbs, 2)}")
    col2.metric("RSI ACTUAL", f"{round(rsi, 2)}")

    # --- LÓGICA DE ALERTA REFORZADA ---
    if rsi > 78:
        st.error("⚠️ VENTA FUERTE: Mercado muy agotado.")
    elif rsi < 22:
        st.success("🚀 COMPRA FUERTE: Posible rebote.")
    else:
        st.info("⏳ BUSCANDO OPORTUNIDAD SEGURA")
    
    st.caption(f"Sincronizado: {time.strftime('%H:%M:%S')}")
else:
    st.error("🔄 Error de datos: El mercado está muy rápido. Reintentando...")
    time.sleep(2)
    st.rerun()

time.sleep(15)
st.rerun()
        
