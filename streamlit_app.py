import requests
import pandas as pd
from datetime import datetime

def obtener_noticias_impacto():
    # Usamos una API gratuita de calendario (ejemplo conceptual con FinancialModelingPrep o un scraper)
    # Lo ideal es filtrar por moneda 'USD' y relevancia 'High' (3 estrellas/toros)
    url = "https://site.financialmodelingprep.com/api/v3/economic_calendar?from=2026-03-06&to=2026-03-06&apikey=TU_API_KEY"
    
    response = requests.get(url)
    if response.status_code == 200:
        eventos = response.json()
        # Filtramos solo lo que afecta al Dólar (y por ende al Oro) de alto impacto
        noticias_peligrosas = [e for e in eventos if e['currency'] == 'USD' and e['impact'] == 'High']
        return noticias_peligrosas
    return []

# En tu interfaz de Streamlit:
noticias = obtener_noticias_impacto()
if noticias:
    st.error(f"⚠️ ¡CUIDADO! Hay {len(noticias)} noticias de alto impacto hoy para el USD.")
    for n in noticias:
        st.write(f"📌 {n['event']} a las {n['date']}")
        
