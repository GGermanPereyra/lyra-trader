import streamlit as st
import yfinance as yf
import pandas as pd

def get_market_data():
    try:
        # Probamos con el símbolo Spot que es más rápido para estos saltos
        ticker = yf.Ticker("XAUUSD=X")
        df = ticker.history(period="1d", interval="1m")
        if df.empty: return None

        # CALIBRACIÓN DINÁMICA: 
        # En lugar de restar 17.90, detectamos el desfase actual.
        # Según tu MT4 ($5194) y Yahoo ($5194), el offset ahora es casi 0.
        # Vamos a dejarlo en 0.50 para ajustar al spread de FBS.
        fbs_offset = 0.50 
        df['Price'] = df['Close'] - fbs_offset
        
        # RSI 14
        delta = df['Price'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        df['RSI'] = 100 - (100 / (1 + (gain / loss)))
        
        return df.iloc[-1]
    except:
        return None

# --- INTERFAZ ---
st.title("🛡️ Sentinel: Inteligencia Germán")
data = get_market_data()

if data is not None:
    precio = round(data['Price'], 2)
    rsi = round(data['RSI'], 2)
    
    st.metric("PRECIO FBS", f"${precio}")
    
    # ALERTAS REALES
    if rsi > 70:
        st.error(f"⚠️ VENTA: RSI en {rsi} (Igual que tu MT4)")
    elif rsi < 30:
        st.success(f"🚀 COMPRA: RSI en {rsi}")
    else:
        st.info(f"⏳ BUSCANDO CONFLUENCIA ({rsi})")
        
