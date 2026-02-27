    import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="Sentinel: Control Germán", layout="wide")

# --- FUNCIÓN DE DATOS CON CALIBRACIÓN ---
def get_market_data(offset_manual):
    try:
        ticker = yf.Ticker("GC=F")
        gold = ticker.history(period="1d", interval="1m")
        if gold.empty or len(gold) < 30:
            return None
        
        df = gold.copy()
        # Aplicamos el ajuste que tú controlas desde el celu
        df['Close_Adj'] = df['Close'] - offset_manual
        
        # RSI (14)
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        df['RSI'] = 100 - (100 / (1 + (gain / loss)))
        
        # MACD (12, 26, 9)
        df['EMA12'] = df['Close'].ewm(span=12, adjust=False).mean()
        df['EMA26'] = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = df['EMA12'] - df['EMA26']
        df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        
        # Bollinger (20)
        df['SMA20'] = df['Close_Adj'].rolling(window=20).mean()
        df['STD20'] = df['Close_Adj'].rolling(window=20).std()
        df['Upper'] = df['SMA20'] + (df['STD20'] * 2)
        df['Lower'] = df['SMA20'] - (df['STD20'] * 2)
        
        return df.iloc[-1]
    except:
        return None

# --- INTERFAZ DEL CELULAR ---
st.title("🛡️ Sentinel: Mando Germán")

# CALIBRADOR EN VIVO: Si ves diferencia, mueves esto
with st.sidebar:
    st.header("⚙️ Ajuste Real")
    # El valor 11.09 es el que calculamos para tus $5186.11 actuales
    ajuste = st.slider("Calibrar Precio", 5.0, 25.0, 11.09, step=0.01)
    st.write(f"Offset actual: {ajuste}")

data = get_market_data(ajuste)

if data is not None:
    precio = round(data['Close_Adj'], 2)
    rsi_val = round(data['RSI'], 2)
    macd_alcista = data['MACD'] > data['Signal']
    
    # SEÑAL DINÁMICA
    if rsi_val > 75: # Sobrecompra fuerte como la de ahora (78.24)
        st.error(f"⚠️ SEÑAL: VENTA FUERTE (RSI: {rsi_val})")
        st.metric("PRECIO ACTUAL", f"${precio}")
        st.write(f"Salida sugerida (TP): ${round(data['Lower'], 2)}")
    elif rsi_val < 30:
        st.success(f"🚀 SEÑAL: COMPRA (RSI: {rsi_val})")
        st.metric("PRECIO ACTUAL", f"${precio}")
        st.write(f"Salida sugerida (TP): ${round(data['Upper'], 2)}")
    else:
        st.warning(f"⏳ ESPERAR (RSI: {rsi_val})")
        st.metric("PRECIO ACTUAL", f"${precio}")

    st.divider()
    st.write(f"📊 **Calibración:** Si el precio no es ${precio}, mueve el slider lateral.")
else:
    st.info("🔄 Reconectando con el mercado...")
    time.sleep(5)
    st.rerun()

time.sleep(25)
st.rerun()
        
