import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime

st.set_page_config(page_title="Lira Real-Time", layout="centered")

def obtener_datos_frescos(ticker_simbolo):
    try:
        # Usamos un periodo muy corto (1 día) e intervalo de 1m para forzar datos nuevos
        ticker = yf.Ticker(ticker_simbolo)
        # 'prepost=True' ayuda a capturar movimientos fuera de hora o más recientes
        df = ticker.history(period="1d", interval="1m", prepost=True)
        
        if not df.empty:
            # Tomamos el último registro absoluto
            ultimo_registro = df.iloc[-1]
            precio = float(ultimo_registro['Close'])
            hora_dato = df.index[-1].strftime('%H:%M:%S')
            
            # Cálculo de RSI ultra-rápido (7 periodos)
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=7).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=7).mean()
            rs = gain.iloc[-1] / loss.iloc[-1]
            rsi = 100 - (100 / (1 + rs))
            
            return precio, float(rsi), hora_dato
    except:
        return None, None, None
    return None, None, None

# --- INTERFAZ ---
st.title("⚡ Monitor de Precisión")
st.write(f"Operador: **Germán** | Refresco: 15 seg")

# Selector de activo para que no se mezcle Oro con Euro
activo = st.selectbox("Elegí el activo que tenés en MetaTrader:", ["EURUSD=X", "GC=F"])

precio, rsi, hora = obtener_datos_frescos(activo)

if precio:
    # Verificación de "Tiempo Real"
    st.metric("PRECIO ACTUAL", f"{precio:.5f}")
    st.caption(f"🕒 Hora del dato: {hora} (Verificá que coincida con tu MetaTrader)")
    
    st.progress(int(rsi) if 0 <= rsi <= 100 else 50, text=f"Fuerza (RSI): {rsi:.2f}")

    st.divider()

    # SUGERENCIA SEGÚN PRECIO ACTUALIZADO
    if rsi < 30:
        st.success(f"🟢 COMPRA SUGERIDA en {precio:.5f}")
    elif rsi > 70:
        st.error(f"🔴 VENTA SUGERIDA en {precio:.5f}")
    else:
        st.info("🟡 ESPERAR: El mercado está lateral.")
else:
    st.warning("🔄 Sincronizando con el servidor... verificá tu conexión.")

# Refresco cada 15 segundos para no ser bloqueado pero mantener velocidad
time.sleep(15)
st.rerun()
