import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import time
from datetime import datetime

# --- CONFIGURACIÓN PARA MÓVIL ---
st.set_page_config(page_title="Protección Alemana XAU", layout="centered")

def obtener_datos_seguros():
    try:
        # Descargamos Oro (XAUUSD) y Dólar (DXY)
        # Usamos un periodo de 2 días para asegurar que el RSI tenga datos suficientes
        oro = yf.download("XAUUSD=X", period="2d", interval="1m", progress=False)
        dxy = yf.download("DX-Y.NYB", period="2d", interval="1m", progress=False)
        
        if not oro.empty and len(oro) > 14:
            precio_actual = oro['Close'].iloc[-1]
            
            # Cálculo del RSI Real
            oro['RSI'] = ta.rsi(oro['Close'], length=14)
            rsi_actual = oro['RSI'].iloc[-1]
            
            # Media Móvil 200 (Tendencia)
            # Usamos un periodo más largo para la SMA
            hist_sma = yf.download("XAUUSD=X", period="5d", interval="15m", progress=False)
            sma_200 = hist_sma['Close'].rolling(window=200).mean().iloc[-1]
            
            val_dxy = dxy['Close'].iloc[-1] if not dxy.empty else 104.20
            
            return precio_actual, rsi_actual, sma_200, val_dxy
    except Exception as e:
        return None, None, None, None
    return None, None, None, None

# --- INTERFAZ VISUAL ---
st.title("🛡️ Protección Alemana")
st.write(f"**Capital:** $25.00 USD | **Lote Sugerido:** 0.01")

# Intentamos obtener los datos
resultado = obtener_datos_seguros()

if resultado[0] is not None:
    precio, rsi, sma, dxy = resultado
    
    # Métricas Estilo TradingView
    col1, col2 = st.columns(2)
    with col1:
        st.metric("ORO (XAU/USD)", f"${precio:,.2f}")
        st.metric("RSI REAL", f"{rsi:.2f}")
    with col2:
        st.metric("DXY (Dólar)", f"{dxy:.2f}")
        st.write(f"SMA 200: ${sma:,.2f}")

    st.divider()

    # --- EL VEREDICTO ---
    st.subheader("📢 Veredicto del Sistema")
    
    # Basado en tu RSI de 38.79: "Esperar" es lo correcto
    if rsi < 32 and precio > sma:
        st.success("🟢 COMPRA: Precio bajo en tendencia alcista.")
    elif rsi > 68 and precio < sma:
        st.warning("🔴 VENTA: Precio alto en tendencia bajista.")
    else:
        st.info("🟡 ESPERAR: Buscando oportunidad segura...")

    # --- PROTECCIÓN DE CAPITAL ---
    st.divider()
    st.write("### 🧮 Gestión de Riesgo ($25)")
    sl_pips = st.slider("Stop Loss (Pips)", 10, 60, 30)
    riesgo_usd = sl_pips * 0.1 # 0.1 USD por pip en 0.01 lotes
    
    if riesgo_usd > 1.25:
        st.error(f"Riesgo de ${riesgo_usd:.2f} es muy alto para tu cuenta.")
    else:
        st.write(f"Si falla, pierdes: **${riesgo_usd:.2f}**")

else:
    st.warning("🔄 Conectando con los servidores financieros... Espera un momento.")
    # Forzamos una recarga si falla la primera vez
    time.sleep(5)
    st.rerun()

# Auto-refresh cada 15 segundos
time.sleep(15)
st.rerun()
