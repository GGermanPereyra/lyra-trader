import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="Monitor Germán", layout="centered")

def obtener_datos():
    try:
        # Usamos un Ticker con configuración para evitar bloqueos
        ticker = yf.Ticker("GC=F")
        # Pedimos el historial con un intervalo más largo para que no nos bloqueen
        df = ticker.history(period="1d", interval="5m")
        
        if df.empty:
            # Si falla GC=F, intentamos con GLD (el respaldo)
            df = yf.download("GLD", period="1d", interval="5m", progress=False)

        if not df.empty:
            # Corrección del error de logs: usamos .iloc[0] para extraer el valor puro
            ultimo_precio = float(df['Close'].iloc[-1:].values[0])
            
            # Cálculo de RSI manual blindado
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            
            last_gain = gain.iloc[-1]
            last_loss = loss.iloc[-1]
            
            if last_loss == 0 or pd.isna(last_loss):
                rsi_val = 100
            else:
                rs = last_gain / last_loss
                rsi_val = 100 - (100 / (1 + rs))
                
            return ultimo_precio, float(rsi_val)
    except Exception:
        return None, None
    return None, None

# --- INTERFAZ ---
st.title("📊 Monitor de Oro")
st.write(f"Operador: **Germán** | Capital: $25.00 USD")

precio, rsi = obtener_datos()

if precio is not None:
    st.metric("PRECIO ORO", f"${precio:,.2f}")
    st.metric("RSI (Fuerza)", f"{rsi:.2f}")
    
    st.divider()
    
    if rsi < 30:
        st.success("🟢 COMPRA: Oportunidad detectada.")
    elif rsi > 70:
        st.warning("🔴 VENTA: Riesgo de caída.")
    else:
        st.info("🟡 ESPERAR: No hay señal clara todavía.")
else:
    st.error("⏳ Yahoo está saturado. Reintentando en 20 segundos...")
    time.sleep(20)
    st.rerun()

# Refresco más lento (60 seg) para evitar nuevos bloqueos de IP
time.sleep(60)
st.rerun()
