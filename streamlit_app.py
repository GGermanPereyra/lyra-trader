import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta

# --- CONFIGURACIÓN DE PÁGINA PARA MÓVIL ---
st.set_page_config(page_title="Sistema de Protección Alemán", layout="centered")

# --- 1. LÓGICA DE DATOS (SIMULADA PARA EJECUCIÓN INMEDIATA) ---
# Aquí conectarás tu API de FBS/MetaTrader en el futuro
def obtener_datos_mercado():
    precio_oro = 2345.50 + np.random.uniform(-5, 5)
    rsi = np.random.uniform(20, 80)
    sma_200 = 2340.00
    dxy = 104.20 + np.random.uniform(-0.1, 0.1)
    return precio_oro, rsi, sma_200, dxy

# --- 2. CALENDARIO DE NOTICIAS DE IMPACTO ---
# En una versión avanzada, esto vendría de una API de noticias
noticias_hoy = [
    {"evento": "NFP (Nóminas EE.UU.)", "hora": "10:30", "impacto": "Alto"},
    {"evento": "Discurso de la FED", "hora": "14:00", "impacto": "Alto"}
]

def verificar_riesgo_noticias(noticias):
    ahora = datetime.now()
    for n in noticias:
        h_noticia = datetime.strptime(n['hora'], "%H:%M").replace(
            year=ahora.year, month=ahora.month, day=ahora.day
        )
        if h_noticia - timedelta(minutes=45) <= ahora <= h_noticia + timedelta(minutes=20):
            return True, n['evento']
    return False, None

# --- 3. INTERFAZ DE USUARIO (UI) ---
st.title("🛡️ Oro: Protección Alemana")
st.write(f"**Capital:** $25.00 USD | **Lote Sugerido:** 0.01")

precio, rsi, sma, dxy = obtener_datos_mercado()
hay_noticia, evento = verificar_riesgo_noticias(noticias_hoy)

# --- COLUMNAS DE MONITOREO ---
col1, col2 = st.columns(2)
with col1:
    st.metric("XAU/USD (ORO)", f"{precio:.2f}")
    st.metric("RSI (1M)", f"{rsi:.1f}")
with col2:
    st.metric("DXY (Dólar)", f"{dxy:.2f}")
    st.write(f"SMA 200: {sma:.2f}")

st.divider()

# --- 4. EL VEREDICTO (PREVISIÓN CLARA) ---
st.subheader("📢 Veredicto del Sistema")

if hay_noticia:
    st.error(f"🚫 BLOQUEADO: {evento} inminente. No operar.")
    veredicto = "ESPERAR"
    color_boton = "secondary"
elif rsi < 30 and precio > sma:
    st.success("🟢 COMPRA FUERTE: Tendencia alcista + Precio bajo.")
    veredicto = "COMPRAR"
elif rsi > 70 and precio < sma:
    st.warning("🔴 VENTA FUERTE: Tendencia bajista + Precio caro.")
    veredicto = "VENDER"
else:
    st.info("🟡 ESPERAR: No hay confluencia clara de indicadores.")
    veredicto = "ESPERAR"

# --- 5. GESTIÓN DE RIESGO REALISTA ---
st.divider()
st.write("### 🧮 Calculadora de Riesgo (25 USD)")
stop_loss_pips = st.slider("Pips de Stop Loss", 10, 100, 30)
riesgo_usd = (stop_loss_pips * 0.1) # Cálculo para lote 0.01 en Oro

if riesgo_usd > 2.5: # Si arriesgas más del 10% de la cuenta
    st.error(f"Riesgo muy alto: ${riesgo_usd:.2f} (Cuidado con tus 25 USD)")
else:
    st.write(f"Pérdida potencial: **${riesgo_usd:.2f}**")

# --- BOTÓN DE ACCIÓN ---
if veredicto != "ESPERAR":
    if st.button(f"🚀 EJECUTAR {veredicto} EN FBS"):
        st.write("Conectando con MetaTrader... Enviando orden 0.01")
else:
    st.button("🚀 Buscando oportunidad...", disabled=True)

# Auto-refresh cada 10 segundos para ver el precio en el cel
time.sleep(10)
st.rerun()
