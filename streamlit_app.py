import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime

st.set_page_config(page_title="Lira Pro - Germán", layout="centered")

def obtener_datos_optimizados(ticker_simbolo):
    try:
        # Usamos period="1d" pero forzamos el intervalo más pequeño
        ticker = yf.Ticker(ticker_simbolo)
        df = ticker.history(period="1d", interval="1m", prepost=True)
        
        if not df.empty:
            ultimo_registro = df.iloc[-1]
            precio = float(ultimo_registro['Close'])
            hora_dato = df.index[-1].strftime('%H:%M:%S')
            
            # RSI de 14 periodos para coincidir con tu MetaTrader
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain.iloc[-1] / loss.iloc[-1]
            rsi = 100 - (100 / (1 + rs))
            
            return precio, float(rsi), hora_dato
    except:
        return None, None, None

# --- INTERFAZ ---
st.title("🚀 Lira Gold Precision")
st.write(f"Operador: **Germán** | Cuenta: $32.14 USD")

# Selector con los símbolos que YA sabemos que te funcionan
activo = st.selectbox("Activo en MetaTrader:", ["GC=F", "XAUUSD=X", "EURUSD=X"])

precio, rsi, hora = obtener_datos_optimizados(activo)

if precio:
    col1, col2 = st.columns(2)
    with col1:
        st.metric("PRECIO ACTUAL", f"{precio:.2f}")
    with col2:
        st.metric("RSI (14)", f"{rsi:.2f}")
    
    st.caption(f"🕒 Hora del dato: {hora} (Compará con tu MT4)")
    st.divider()

    # --- LÓGICA DE TRADING AUTOMÁTICA ---
    # Definimos el riesgo (3 dólares de Stop Loss para cuidar tus $32)
    riesgo = 3.0 
    ganancia_esperada = 5.0

    if rsi <= 30:
        st.success("🟢 SEÑAL: COMPRA (BUY)")
        st.write(f"**Punto de Entrada:** {precio:.2f}")
        st.write(f"**STOP LOSS:** {precio - riesgo:.2f}")
        st.write(f"**TAKE PROFIT:** {precio + ganancia_esperada:.2f}")
    elif rsi >= 70:
        st.error("🔴 SEÑAL: VENTA (SELL)")
        st.write(f"**Punto de Entrada:** {precio:.2f}")
        st.write(f"**STOP LOSS:** {precio + riesgo:.2f}")
        st.write(f"**TAKE PROFIT:** {precio - ganancia_esperada:.2f}")
    else:
        st.info("⚖️ MERCADO NEUTRAL - Esperando extremo (30/70)")

else:
    st.warning("🔄 Sincronizando... Si tarda, cambiá el activo en el selector.")

# Reducimos a 10 segundos para mayor precisión sin bloqueo
time.sleep(10)
st.rerun()
