import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="Sentinel: FBS Germán", layout="wide")

def get_fbs_data():
    try:
        ticker = yf.Ticker("GC=F")
        gold = ticker.history(period="1d", interval="1m")
        if gold.empty or len(gold) < 20:
            return None
        
        df = gold.copy()
        
        # --- CALIBRACIÓN FINAL PARA FBS ---
        # Ajustamos el offset para eliminar esos $6 de diferencia
        fbs_offset = 17.90 
        df['Close_Adj'] = df['Close'] - fbs_offset
        
        # RSI (14)
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
    precio = round(data['Close_Adj'], 2)
    rsi_val = round(data['RSI'], 2)
    
    # Visualización en celular
    st.metric("ORO (FBS)", f"${precio}")
    st.metric("RSI (14)", f"{rsi_val}")

    # Alerta según tu RSI real de 51.07
    if rsi_val > 75:
        st.error("⚠️ SOBRECOMPRA")
    elif rsi_val < 30:
        st.success("🚀 OPORTUNIDAD DE COMPRA")
    else:
        st.warning("⏳ ESPERAR: Zona Neutral")
    
    st.divider()
    st.caption(f"Última sincronización: {time.strftime('%H:%M:%S')}")
else:
    st.info("🔄 Reconectando...")
    time.sleep(5)
    st.rerun()

time.sleep(30)
st.rerun()
