import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="Flash Monitor - Germán", layout="centered")

# Función de alta velocidad sin caché para reacción inmediata
def obtener_datos_flash():
    try:
        # Usamos el Ticker de futuros que es el más rápido en actualizar
        oro = yf.Ticker("GC=F")
        # Pedimos el intervalo de 1 minuto para máxima precisión
        df = oro.history(period="1d", interval="1m")
        
        if not df.empty:
            precio = float(df['Close'].iloc[-1])
            
            # RSI rápido (especial para scalping con $25)
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=7).mean() # Ventana corta para rapidez
            loss = (-delta.where(delta < 0, 0)).rolling(window=7).mean()
            rs = gain.iloc[-1] / loss.iloc[-1]
            rsi = 100 - (100 / (1 + rs))
            
            return precio, float(rsi)
    except:
        return None, None
    return None, None

# --- PANEL DE CONTROL ---
st.title("⚡ Ejecución en Tiempo Real")
st.write(f"**Operador:** Germán | **Cuenta:** $25.00 USD")

precio, rsi = obtener_datos_flash()

if precio:
    # Color dinámico según el precio para alertarte rápido
    st.metric("PRECIO XAU/USD", f"${precio:,.2f}", delta_color="normal")
    st.progress(int(rsi) if 0 <= rsi <= 100 else 50, text=f"Fuerza del Mercado (RSI): {rsi:.2f}")

    st.divider()

    # --- SEÑALES DE GATILLO INMEDIATO ---
    if rsi <= 30:
        st.success("🟢 **¡COMPRA YA! (OVER-SOLD)**")
        st.write(f"👉 **Punto de Entrada:** ${precio:,.2f}")
        st.write(f"🛑 **Stop Loss Obligatorio:** ${precio - 2.50:,.2f}") # Ajustado para cuenta de $25
    
    elif rsi >= 70:
        st.error("🔴 **¡VENTA YA! (OVER-BOUGHT)**")
        st.write(f"👉 **Punto de Entrada:** ${precio:,.2f}")
        st.write(f"🛑 **Stop Loss Obligatorio:** ${precio + 2.50:,.2f}")
    
    else:
        st.info("⚖️ **MERCADO VOLÁTIL - ESPERAR**")
        st.write("No hay confirmación de entrada. Protegiendo tus $25.")

else:
    st.warning("🔄 Reintentando conexión ultra-rápida...")
    time.sleep(5)
    st.rerun()

# Refresco cada 30 segundos: El equilibrio perfecto entre velocidad y seguridad de IP
time.sleep(30)
st.rerun()
