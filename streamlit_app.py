import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import time
from datetime import datetime, timedelta

# --- CONFIGURACIÓN PARA EL CELULAR ---
st.set_page_config(page_title="Sistema Protección Alemana", layout="centered")

def obtener_datos_reales():
    try:
        # Descargamos Oro y Dólar (DXY)
        # XAUUSD=X suele ser el ticker más preciso para el precio spot
        oro = yf.download("XAUUSD=X", period="2d", interval="1m", progress=False)
        dxy = yf.download("DX-Y.NYB", period="2d", interval="1m", progress=False)
        
        if not oro.empty:
            precio_actual = oro['Close'].iloc[-1]
            
            # Cálculo del RSI (14 periodos)
            oro['RSI'] = ta.rsi(oro['Close'], length=14)
            rsi_actual = oro['RSI'].iloc[-1]
            
            # SMA 200 (Media Móvil para tendencia)
            # Usamos intervalo de 15m para una media más estable
            hist_sma = yf.download("XAUUSD=X", period="5d", interval="15m", progress=False)
            sma_200 = hist_sma['Close'].rolling(window=200).mean().iloc[-1]
            
            precio_dxy = dxy['Close'].iloc[-1] if not dxy.empty else 104.20
            
            return precio_actual, rsi_actual, sma_200, precio_dxy
    except Exception as e:
        return None, None, None, None

# --- INTERFAZ VISUAL ---
st.title("🛡️ Protección Alemana")
st.write(f"**Capital Actual:** $25.00 USD | **Lote:** 0.01")

precio, rsi, sma, dxy = obtener_datos_reales()

if precio is not None:
    # Mostramos las métricas principales
    col1, col2 = st.columns(2)
    with col1:
        st.metric("ORO (XAU/USD)", f"${precio:,.2f}")
        st.metric("RSI REAL", f"{rsi:.2f}")
    with col2:
        st.metric("DXY (Dólar)", f"{dxy:.2f}")
        st.write(f"SMA 200: ${sma:,.2f}")

    st.divider()

    # --- VEREDICTO DE SEGURIDAD ---
    st.subheader("📢 Veredicto del Sistema")
    
    # Lógica basada en tu MetaTrader: RSI < 30 es sobreventa (Compra)
    if rsi < 32 and precio > sma:
        st.success("🟢 COMPRA FUERTE: Precio en descuento y tendencia alcista.")
        estado = "COMPRAR"
    elif rsi > 68 and precio < sma:
        st.warning("🔴 VENTA FUERTE: Precio caro y tendencia bajista.")
        estado = "VENDER"
    else:
        st.info("🟡 ESPERAR: No hay señales claras de entrada segura.")
        estado = "ESPERAR"

    # --- GESTIÓN DE RIESGO ---
    st.divider()
    st.write("### 🧮 Calculadora de Riesgo ($25)")
    sl_pips = st.slider("Distancia Stop Loss (Pips)", 10, 60, 30)
    riesgo_usd = sl_pips * 0.1 # 0.1 USD por pip con lote 0.01
    
    if riesgo_usd > 1.25:
        st.error(f"⚠️ ¡RIESGO ALTO! Estás arriesgando ${riesgo_usd:.2f} (5%+) de tu cuenta.")
    else:
        st.write(f"Pérdida estimada si falla: **${riesgo_usd:.2f}**")

    # Botón de acción (por ahora solo aviso)
    if estado != "ESPERAR":
        st.button(f"🚀 EJECUTAR {estado} EN FBS")

else:
    st.warning("🔄 Sincronizando datos con el mercado real...")

# Actualización cada 20 segundos
time.sleep(20)
st.rerun()
