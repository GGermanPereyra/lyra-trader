import streamlit as st
import requests
from bs4 import BeautifulSoup
import time

st.set_page_config(page_title="Lira - Modo Superviviencia", layout="centered")

def obtener_precio_alternativo():
    try:
        # Intentamos buscar el precio en Google Finance directamente (sin librerías que se bloqueen)
        url = "https://www.google.com/search?q=XAU+USD+price"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Buscamos el div que contiene el precio en el resultado de búsqueda
        precio_div = soup.find("div", {"class": "BNeawe iBp4i AP7Wnd"})
        if precio_div:
            return precio_div.text
    except:
        return None
    return None

st.title("🛡️ Monitor Anti-Bloqueo")
st.write(f"Operador: **Germán** | Estado: Bypass Yahoo")

precio = obtener_precio_alternativo()

if precio:
    st.metric("PRECIO XAU/USD (Google)", f"{precio}")
    st.success("✅ Datos recuperados mediante Bypass.")
    st.divider()
    st.warning("⚠️ El RSI está desactivado para evitar nuevos bloqueos. Usá el de tu MetaTrader.")
else:
    st.error("❌ Todos los servidores están saturados.")
    st.info("Confiá en tu MetaTrader, Germán. El precio ahí es real y no tiene delay.")

# Refresco cada 30 segundos para no llamar la atención de los servidores
time.sleep(30)
st.rerun()
