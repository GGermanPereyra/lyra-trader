import streamlit as st
import pandas as pd
import yfinance as yf
import time

st.set_page_config(page_title="Lira Pro Precision", layout="centered")

def obtener_datos_pro():
    try:
        # Usamos un 'proxy' interno de Yahoo que a veces salta el bloqueo
        # Pedimos el Oro Spot (XAUUSD=X)
        ticker = yf.Ticker("XAUUSD=X")
        df = ticker.history(period="1d", interval="1m", prepost=True)
        
        if not df.empty:
            precio = float(df['Close'].iloc[-1])
            # RSI de respuesta ultra-veloz (5 periodos)
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=5).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=5).mean()
            rs = gain.iloc[-1] / loss.iloc[-1]
            rsi = 100 - (100 / (1 + rs))
            return precio, float(rsi)
    except:
        return None, None
    return None, None

st.title("🎯 Monitor Profesional XAU/USD")
st.write("Operador: **Germán** | Estado: Sincronizando...")

precio, rsi = obtener_datos_pro()

if precio:
    st.metric("PRECIO EN VIVO", f"${precio:,.2f}")
    st.write(f"**Fuerza del Mercado (RSI):** {rsi:.2f}")
    
    st.divider()

    # --- LÓGICA DE ENTRADA Y NIVELES ---
    if rsi <= 25:
        st.success(f"🟢 **SUGERENCIA: BUY (COMPRA)**")
        st.write(f"**Entrada:** {precio:.2f}")
        st.write(f"**Stop Loss:** {precio - 2.5:.2f}")
        st.write(f"**Take Profit:** {precio + 4.0:.2f}")
    elif rsi >= 75:
        st.error(f"🔴 **SUGERENCIA: SELL (VENTA)**")
        st.write(f"**Entrada:** {precio:.2f}")
        st.write(f"**Stop Loss:** {precio + 2.5:.2f}")
        st.write(f"**Take Profit:** {precio - 4.0:.2f}")
    else:
        st.info("⚖️ **MERCADO NEUTRAL** - Esperando extremo.")
else:
    st.warning("⚠️ Yahoo sigue bloqueado. Usá tu MetaTrader para el precio por ahora.")

time.sleep(20) # Pausa larga para no irritar al servidor
st.rerun()
