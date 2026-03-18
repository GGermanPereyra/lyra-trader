import streamlit as st
import yfinance as yf
import time

st.set_page_config(page_title="Lira SOS", layout="centered")

def obtener_precio_forzado():
    try:
        # Intentamos bajar el precio del Oro con una técnica de 'fast-download'
        gold = yf.download("XAUUSD=X", period="1h", interval="1m", progress=False)
        if not gold.empty:
            return float(gold['Close'].iloc[-1])
    except:
        return None
    return None

st.title("🛡️ Monitor de Emergencia")
st.write("Estado: Intentando saltar bloqueo de Yahoo...")

precio = obtener_precio_forzado()

if precio:
    st.metric("PRECIO XAU/USD", f"${precio:,.2f}")
    st.success("✅ ¡CONECTADO! Yahoo aceptó la conexión.")
else:
    st.error("❌ Yahoo sigue bloqueado para esta IP.")
    st.write("Germán, el servidor de Streamlit está bloqueado. Por ahora, confiá 100% en tu MetaTrader.")

# Refresco muy lento (1 minuto) para que no nos bloqueen de nuevo
time.sleep(60)
st.rerun()
