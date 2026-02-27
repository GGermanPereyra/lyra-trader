import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
import pytz

# Configuración de sesiones (Hora UTC)
def check_market_session():
    now = datetime.datetime.now(pytz.utc).time()
    # Londres: 08:00 - 16:00 | NY: 13:00 - 21:00
    is_london = datetime.time(8,0) <= now <= datetime.time(16,0)
    is_ny = datetime.time(13,0) <= now <= datetime.time(21,0)
    return is_london, is_ny

def get_smart_data():
    try:
        ticker = yf.Ticker("GC=F")
        df = ticker.history(period="1d", interval="1m")
        if df.empty: return None
        
        # Ajuste FBS (Calibrado a tu última captura)
        fbs_offset = 17.90 
        df['Price'] = df['Close'] - fbs_offset
        
        # INDICADORES TÉCNICOS
        # RSI 14
        delta = df['Price'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        df['RSI'] = 100 - (100 / (1 + (gain / loss)))
        
        # MACD (Confirmador de tendencia)
        df['EMA12'] = df['Price'].ewm(span=12).mean()
        df['EMA26'] = df['Price'].ewm(span=26).mean()
        df['MACD'] = df['EMA12'] - df['EMA26']
        df['Signal'] = df['MACD'].ewm(span=9).mean()
        
        return df.iloc[-1], check_market_session()
    except:
        return None, (False, False)

# --- INTERFAZ ---
st.title("🛡️ Sentinel: Inteligencia Germán")
data, sessions = get_smart_data()

if data is not None:
    precio = round(data['Price'], 2)
    rsi = round(data['RSI'], 2)
    macd_val = data['MACD']
    signal_val = data['Signal']
    
    # Lógica de Sugerencia con Filtros
    london, ny = sessions
    sesion_activa = london or ny
    
    st.metric("PRECIO FBS", f"${precio}")
    
    # REGLAS DE ORO PARA AUTOMATIZAR
    if rsi > 75 and macd_val < signal_val and sesion_activa:
        st.error("🚀 SEÑAL DE VENTA CONFIRMADA (Técnica + Sesión)")
    elif rsi < 30 and macd_val > signal_val and sesion_activa:
        st.success("🚀 SEÑAL DE COMPRA CONFIRMADA (Técnica + Sesión)")
    elif not sesion_activa:
        st.warning("⏳ MERCADO LENTO: Fuera de sesiones principales. No operar.")
    else:
        st.info(f"⏳ BUSCANDO CONFLUENCIA (RSI: {rsi})")

    st.divider()
    st.write(f"Sincronizado: {'Londres ✅' if london else 'Londres ❌'} | {'NY ✅' if ny else 'NY ❌'}")
    
