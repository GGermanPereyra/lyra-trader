import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import time
from datetime import datetime, timedelta

# --- CONFIGURACIÓN DE PÁGINA PARA EL CELULAR ---
st.set_page_config(page_title="Protección Alemana XAU", layout="centered")

# --- 1. OBTENCIÓN DE DATOS REALES (MARZO 2026) ---
def obtener_datos_vivos():
    try:
        # Extraemos Oro (GC=F es el futuro, XAUUSD=X es el spot)
        # Usamos XAUUSD=X para que coincida mejor con brokers como FBS
        oro = yf.download(tickers="XAUUSD=X", period="1d", interval="1m", progress=False)
        dxy = yf.download(tickers="DX-Y.NYB", period="1d", interval="1m", progress=False)
        
        if not oro.empty:
            precio_actual = oro['Close'].iloc[-1]
            
            # Calculamos RSI real usando pandas_ta (periodo 14)
            oro['RSI'] = ta.rsi(oro['Close'], length=14)
            rsi_actual = oro['RSI'].iloc[-1]
            
            # Calculamos SMA 200 (usamos más datos para la media móvil)
            oro_hist = yf.download(tickers="XAUUSD=X", period="5d", interval="15m", progress=False)
            sma_200 = oro_hist['Close'].rolling(window=200).mean().iloc[-1]
            
            precio_dxy = dxy['Close'].iloc[-1] if not dxy.empty else 104.25
            
            return precio_actual, rsi_actual, sma_200, precio_dxy
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return None, None, None, None

# --- 2. FILTRO DE NOTICIAS (CALENDARIO DE RIESGO) ---
# Nota: En producción, esto debería conectar con una API de noticias real
noticias_impacto = [
    {"evento": "NFP (Nóminas no agrícolas)", "hora": "10:30", "impacto": "Alto"},
    {"evento": "Decisión de Tasas FED", "hora": "15:00", "impacto": "Alto"}
]

def verificar_seguridad_noticias(noticias):
    ahora = datetime.now()
    for n in noticias:
        h_noticia = datetime.strptime(n['hora'], "%H:%M").replace(
            year=ahora.year, month=ahora.month, day=ahora.day
        )
        # Bloqueo 45 min antes por volatilidad previa
        if h_noticia - timedelta(minutes=45) <= ahora <= h_noticia + timedelta(minutes=15):
            return True, n['evento']
    return False, None

# --- 3. INTERFAZ VISUAL ---
st.title("🛡️ Sistema de Protección Alemana")
st.write(f"**Capital de Trabajo:** $25.00 USD | **Lote:** 0.01")

precio, rsi, sma, dxy = obtener_datos_vivos()
hay_riesgo, evento = verificar_seguridad_noticias(noticias_impacto)

if precio:
    # Métricas principales
    c1, c2 = st.columns(2)
    with c1:
        st.metric("ORO (XAU/USD)", f"${precio:,.2f}")
        st.metric("RSI REAL", f"{rsi:.2f}")
    with c2:
        st.metric("DXY (Dólar)", f"{dxy:.2f}")
        st.write(f"SMA 200: ${sma:,.2f}")

    st.divider()

    # --- 4. VEREDICTO CLARO ---
    st.subheader("📢 Veredicto del Sistema")
    
    # Lógica de decisión segura
    if hay_riesgo:
        st.error(f"❌ BLOQUEADO: {evento} inminente. Riesgo de barrido.")
        decision = "ESPERAR"
    elif rsi < 32 and precio > sma:
        st.success("🟢 COMPRA: Sobreventa en tendencia alcista.")
        decision = "COMPRAR"
    elif rsi > 68 and precio < sma:
        st.warning("🔴 VENTA: Sobrecompra en tendencia bajista.")
        decision = "VENDER"
    else:
        st.info("🟡 ESPERAR: No hay confluencia segura.")
        decision = "ESPERAR"

    # --- 5. GESTIÓN DE RIESGO PARA 25 USD ---
    st.divider()
    st.write("### 🧮 Calculadora de Riesgo Estricta")
    distancia_sl = st.slider("Distancia de Stop Loss (Pips)", 10, 80, 30)
    riesgo_dinero = distancia_sl * 0.1 # Para lote 0.01 en oro

    if riesgo_dinero > 1.25: # Más del 5% de la cuenta
        st.error(f"Riesgo Excesivo: ${riesgo_dinero:.2f} (Supera el 5% de tus $25)")
    else:
        st.write(f"Pérdida si toca SL: **${riesgo_dinero:.2f}**")

    # --- BOTÓN DE ACCIÓN ---
    if decision != "ESPERAR":
        if st.button(f"🚀 ENVIAR ORDEN DE {decision} A FBS"):
            st.write("Intentando conectar con MetaTrader 4...")
            # Aquí irá la lógica de ejecución real que configuraremos después
    else:
        st.button("🔍 Buscando entrada segura...", disabled=True)

else:
    st.warning("Cargando datos del mercado...")

# Actualización automática cada 15 segundos para no saturar la API gratuita
time.sleep(15)
st.rerun()
