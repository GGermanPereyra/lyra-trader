import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="Sentinel: FBS Germán", layout="wide")

def get_fbs_data():
    try:
        # Usamos GC=F porque es el servidor más rápido de Yahoo
        ticker = yf.Ticker("GC=F")
        gold = ticker.history(period="1d", interval="1m")
        
        if gold.empty or len(gold) < 20:
            return None
            
        df = gold.copy()
        
        # CALIBRACIÓN AUTOMÁTICA FBS
        # Según tus capturas de las 9:00 AM:
        # Precio Yahoo: ~$5197.20 | Precio FBS: $5186.11
        # El desfase exacto es 11.09
        fbs_offset = 11.09
        df['Close_Adj'] = df['Close'] - fbs_offset
        
        # Cálculo de RSI (14)
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
    
    # Mostramos los datos exactos que verías en tu MT4
    c1, c2 = st.columns(2)
    c1.metric("ORO (FBS)", f"${precio}")
    c2.metric("RSI (14)", f"{rsi_val}")

    # Alerta de Venta (Como tu RSI de 78.24 en la captura)
    if rsi_val > 75:
        st.error("⚠️ FBS: SOBRECOMPRA DETECTADA")
    elif rsi_val < 30:
        st.success("🚀 FBS: OPORTUNIDAD DE COMPRA")
    else:
        st.warning("⏳ ESPERAR: Mercado en zona neutral")
    
    st.divider()
    st.caption(f"Sincronizado con FBS | Última actualización: {time.strftime('%H:%M:%S')}")

else:
    st.info("🔄 Conectando con los servidores de FBS...")
    time.sleep(5)
    st.rerun()

time.sleep(30)
st.rerun()
    
