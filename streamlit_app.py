import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Sentinel: FBS Edition", layout="wide")

def get_fbs_data():
    try:
        # XAUUSD=X suele ser más parecido al precio de FBS que los Futuros
        ticker = yf.Ticker("XAUUSD=X")
        gold = ticker.history(period="1d", interval="1m")
        
        if gold.empty:
            return None
            
        df = gold.copy()
        
        # AJUSTE ESPECÍFICO PARA FBS
        # Basado en tu captura, FBS está ~11.09 puntos por debajo del mercado internacional
        offset_fbs = 11.09
        df['Close_Adj'] = df['Close'] - offset_fbs
        
        # RSI con la sensibilidad de FBS
        delta = df['Close_Adj'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        df['RSI'] = 100 - (100 / (1 + (gain / loss)))
        
        return df.iloc[-1]
    except:
        return None

st.title("🛡️ Sentinel: Conexión FBS")
data = get_fbs_data()

if data is not None:
    precio_fbs = round(data['Close_Adj'], 2)
    rsi_fbs = round(data['RSI'], 2)
    
    col1, col2 = st.columns(2)
    col1.metric("PRECIO FBS (Estimado)", f"${precio_fbs}")
    col2.metric("RSI FBS", f"{rsi_fbs}")

    # Alerta basada en tu RSI de 78.24
    if rsi_fbs > 75:
        st.error("⚠️ FBS: SOBRECOMPRA - POSIBLE VENTA")
    elif rsi_fbs < 30:
        st.success("🚀 FBS: SOBREVENTA - POSIBLE COMPRA")
else:
    st.warning("Buscando señal de FBS...")
        
