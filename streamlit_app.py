import streamlit as st
import yfinance as yf
import time

# Configuración básica
st.set_page_config(page_title="Monitor Germán", layout="centered")

def obtener_datos():
    try:
        # Usamos intervalo de 5m para que no se bloquee la conexión
        df = yf.download("XAUUSD=X", period="1d", interval="5m", progress=False)
        if not df.empty:
            precio = df['Close'].iloc[-1]
            
            # Cálculo rápido de RSI
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rsi = 100 - (100 / (1 + (gain / loss).iloc[-1]))
            
            return precio, rsi
    except:
        return None, None
    return None, None

# --- INTERFAZ ---
st.title("📊 Monitor de Oro")
st.write(f"Cuenta: **Germán** | Capital: $25.00 USD")

precio, rsi = obtener_datos()

if precio:
    # PRECIO REAL DE TU METATRADER
    st.metric("XAU/USD (ORO)", f"${precio:,.2f}")
    st.metric("RSI (Fuerza)", f"{rsi:.2f}")
    
    st.divider()
    
    # --- VEREDICTO DE TRADING ---
    if rsi < 30:
        st.success("🟢 COMPRAR: El precio está en descuento.")
    elif rsi > 70:
        st.warning("🔴 VENDER: El precio está muy caro.")
    else:
        st.info("🟡 ESPERAR: No hay señal clara. Cuidá tus $25.")

    # GESTIÓN DE RIESGO
    st.divider()
    pips = st.slider("Pips de Stop Loss", 10, 50, 30)
    st.write(f"Si la operación sale mal, perdés: **${pips * 0.1:.2f} USD**")

else:
    st.warning("Conectando con el mercado... (Dale 10 segundos)")
    time.sleep(10)
    st.rerun()

# Refresco automático
time.sleep(30)
st.rerun()
