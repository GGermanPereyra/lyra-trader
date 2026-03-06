import streamlit as st
from datetime import datetime, timedelta

# 1. Simulación de base de datos de noticias (esto lo conectaremos a la API)
# Ejemplo: "NFP (Nóminas no agrícolas)" hoy a las 10:30 AM
noticias_hoy = [
    {"evento": "NFP (Payroll)", "hora": "10:30", "impacto": "Alto"},
    {"evento": "Fed Interest Rate", "hora": "14:00", "impacto": "Alto"}
]

def verificar_bloqueo(noticias):
    ahora = datetime.now()
    for n in noticias:
        hora_noticia = datetime.strptime(n['hora'], "%H:%M").replace(
            year=ahora.year, month=ahora.month, day=ahora.day
        )
        # Bloqueamos 30 min antes y 15 min después de la noticia
        inicio_bloqueo = hora_noticia - timedelta(minutes=30)
        fin_bloqueo = hora_noticia + timedelta(minutes=15)
        
        if inicio_bloqueo <= ahora <= fin_bloqueo:
            return True, n['evento']
    return False, None

# --- INTERFAZ EN EL CELULAR ---
st.title("🛡️ Sistema de Protección Alemán")

bloqueado, evento_peligroso = verificar_bloqueo(noticias_hoy)

if bloqueado:
    st.error(f"🚫 OPERACIÓN BLOQUEADA: {evento_peligroso} en curso.")
    st.button("Operar en FBS (Desactivado)", disabled=True)
    st.warning("El mercado del ORO está muy volátil ahora. Protege tus 25 USD.")
else:
    st.success("✅ Mercado Estable (Sin noticias próximas)")
    if st.button("🚀 ENTRAR AHORA (Confirmar RSI)"):
        st.write("Enviando orden micro-lote 0.01 a FBS...")
        
