import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Recuperación Germán", layout="wide")

def get_market_status():
    try:
        # Usamos datos directos sin filtros pesados para evitar que se cuelgue
        gold = yf.download("GC=F", period="1d", interval="1m", progress=False)
        if gold.empty: return None
        
        price = gold['Close'].iloc[-1]
        
        # RSI 14 Rápido
        delta = gold['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rsi = 100 - (100 / (1 + (gain / loss))).iloc[-1]
        
        return price, rsi
    except:
        return None

st.title("🛡️ Sistema de Protección Germán")

# --- CALCULADORA DE LOTAJE PARA CUENTAS PEQUEÑAS ---
with st.sidebar:
    st.header("💰 Gestión de Capital")
    balance = st.number_input("Saldo Actual ($)", value=20.0)
    riesgo = st.slider("% de Riesgo", 1, 5, 2)
    st.info(f"Sugerencia: No operes más de ${round(balance * (riesgo/100), 2)} por trade.")

status = get_market_status()

if status:
    precio, rsi = status
    # Ajuste para FBS basado en el último desfase visto
    precio_fbs = precio - 1.20 
    
    col1, col2 = st.columns(2)
    col1.metric("ORO (FBS)", f"${round(precio_fbs, 2)}")
    col2.metric("RSI ACTUAL", f"{round(rsi, 2)}")

    # --- LÓGICA DE PROTECCIÓN ---
    if rsi > 75:
        st.error("⚠️ ALTA PROBABILIDAD DE CAÍDA. Busca ventas pequeñas.")
    elif rsi < 25:
        st.success("🚀 ORO EN PISO. Busca compras pequeñas.")
    else:
        st.warning("⏳ ZONA NEUTRAL. Si perdiste hoy, NO ENTRES AQUÍ.")

    st.divider()
    st.write("📋 **Regla de Oro:** Si el RSI no está en los extremos, las cuentas de $20 o $50 se queman por el ruido del mercado.")
else:
    st.error("⚠️ Error de conexión. No operes hasta que carguen los datos.")
    
