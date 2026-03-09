import streamlit as st
import yfinance as yf
import pandas as pd
import time

# Configuración limpia
st.set_page_config(page_title="Monitor Oro - Germán", layout="centered")

def obtener_datos_oro():
    try:
        # Usamos el símbolo de Futuros de Oro, que es el estándar de Yahoo hoy
        ticker = "GC=F" 
        df = yf.download(ticker, period="1d", interval="2m", progress=False)
        
        # Si por alguna razón falla el anterior, usamos el respaldo (GLD)
        if df.empty:
            df = yf.download("GLD", period="1d", interval="2m", progress=False)
            
        if not df.empty:
            # Extraemos el valor numérico puro para evitar el ValueError
            precio = float(df['Close'].iloc[-1])
            
            # Cálculo de RSI manual
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rsi = 100 - (100 / (1 + (gain.iloc[-1] / loss.iloc[-1])))
            
            return precio, rsi
    except Exception as e:
        return None, None
    return None, None

# --- INTERFAZ ---
st.title("📊 Monitor de Oro Real")
st.write(f"Operador: **Germán** | Capital: $25.00 USD")

precio, rsi = obtener_datos_oro()

if precio is not None:
    # Mostramos los valores numéricos
    st.metric("PRECIO ORO (GC=F)", f"${precio:,.2f}")
    st.metric("RSI (Fuerza)", f"{rsi:.2f}")
    
    st.divider()
    
    # --- VEREDICTO ---
    if rsi < 30:
        st.success("🟢 COMPRAR: El precio está en zona de oportunidad.")
    elif rsi > 70:
        st.warning("🔴 VENDER: El precio está muy alto.")
    else:
        st.info("🟡 ESPERAR: No hay señal clara. Protegiendo capital.")

else:
    st.error("🔄 Error de conexión con Yahoo. Reintentando en 10 segundos...")
    time.sleep(10)
    st.rerun()

# Refresco cada 30 segundos
time.sleep(30)
st.rerun()
