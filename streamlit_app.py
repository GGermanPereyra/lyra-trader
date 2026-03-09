import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="Monitor de Oro - Germán", layout="centered")

def obtener_datos():
    try:
        # Probamos con el símbolo más estable para Yahoo hoy
        df = yf.download("GC=F", period="1d", interval="2m", progress=False)
        
        # Si falla, probamos con el respaldo GLD
        if df is None or df.empty:
            df = yf.download("GLD", period="1d", interval="2m", progress=False)

        if df is not None and not df.empty:
            # Forzamos que sea un número flotante para evitar el ValueError
            ultimo_precio = float(df['Close'].iloc[-1])
            
            # Cálculo manual de RSI
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            
            if loss.iloc[-1] == 0:
                rsi_val = 100
            else:
                rs = gain.iloc[-1] / loss.iloc[-1]
                rsi_val = 100 - (100 / (1 + rs))
                
            return ultimo_precio, float(rsi_val)
    except Exception:
        return None, None
    return None, None

# --- INTERFAZ ---
st.title("📊 Monitor de Oro Real")
st.write(f"Operador: **Germán** | Capital: $25.00 USD")

precio, rsi = obtener_datos()

if precio is not None:
    col1, col2 = st.columns(2)
    col1.metric("PRECIO ORO", f"${precio:,.2f}")
    col2.metric("RSI (Fuerza)", f"{rsi:.2f}")
    
    st.divider()
    
    # Veredicto para proteger tus $25
    if rsi < 30:
        st.success("🟢 COMPRA: El precio está en zona de oportunidad.")
    elif rsi > 70:
        st.warning("🔴 VENTA: El precio está muy alto.")
    else:
        st.info("🟡 ESPERAR: Zona neutral. No arriesgues capital.")
else:
    st.error("🔄 Buscando señal estable... Reintentando en 10 segundos.")
    time.sleep(10)
    st.rerun()

time.sleep(30)
st.rerun()
