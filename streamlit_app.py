import streamlit as st
import yfinance as yf
import pandas as pd
import time

# Configuración de la página
st.set_page_config(page_title="Monitor de Oro - Germán", layout="centered")

def obtener_datos_estables():
    try:
        # Usamos un intervalo de 2 minutos para evitar bloqueos del servidor
        ticker = yf.Ticker("XAUUSD=X")
        df = ticker.history(period="1d", interval="2m")
        
        if not df.empty:
            precio_actual = df['Close'].iloc[-1]
            
            # Cálculo de RSI manual (Sin librerías externas)
            delta = df['Close'].diff()
            subidas = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            bajadas = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = subidas / bajadas
            rsi_actual = 100 - (100 / (1 + rs.iloc[-1]))
            
            return precio_actual, rsi_actual
    except:
        return None, None
    return None, None

# --- INTERFAZ PARA GERMÁN ---
st.title("📊 Monitor de Oro XAU/USD")
st.write(f"Operador: **Germán** | Capital de Trabajo: $25.00 USD")

precio, rsi = obtener_datos_estables()

if precio:
    # Métricas principales
    col1, col2 = st.columns(2)
    col1.metric("Precio Actual", f"${precio:,.2f}")
    col2.metric("RSI (Fuerza)", f"{rsi:.2f}")
    
    st.divider()
    
    # --- LÓGICA DE TRADING SEGURA ---
    st.subheader("📢 Veredicto del Sistema")
    if rsi < 30:
        st.success("🟢 COMPRA: El precio está bajo. Oportunidad para tus $25.")
    elif rsi > 70:
        st.warning("🔴 VENTA: El precio está muy alto. Riesgo de caída.")
    else:
        # El RSI de 56.69 que vimos en tu MT4 cae aquí
        st.info("🟡 ESPERAR: Mercado neutral. No arriesgues capital sin señal.")

else:
    st.warning("🔄 Conectando con los servidores financieros... Por favor, espera.")
    time.sleep(10)
    st.rerun()

# Refresco automático cada 30 segundos
time.sleep(30)
st.rerun()
