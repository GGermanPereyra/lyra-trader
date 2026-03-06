import streamlit as st
import yfinance as yf
import time

# Título limpio y directo
st.set_page_config(page_title="Monitor de Oro - Germán", layout="centered")

def obtener_datos_vivos():
    try:
        # Pedimos el Oro (XAUUSD=X) con un intervalo más estable (5 minutos)
        oro = yf.Ticker("XAUUSD=X")
        df = oro.history(period="1d", interval="5m")
        
        if not df.empty:
            precio = df['Close'].iloc[-1]
            
            # Cálculo de RSI manual (sin librerías extras que den error)
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rsi = 100 - (100 / (1 + (gain / loss).iloc[-1]))
            
            return precio, rsi
    except:
        return None, None
    return None, None

# --- INTERFAZ ---
st.title("📊 Monitor de Oro")
st.write(f"Operador: **Germán** | Capital: $25.00 USD")

precio, rsi = obtener_datos_vivos()

if precio:
    # Mostramos los valores que ves en tu MetaTrader
    st.metric("PRECIO XAU/USD", f"${precio:,.2f}")
    st.metric("RSI (Fuerza)", f"{rsi:.2f}")
    
    st.divider()
    
    # --- EL VEREDICTO QUE BUSCÁS ---
    # Según tu captura, el RSI está en 56.69. El bot te dirá:
    if rsi < 30:
        st.success("🟢 COMPRAR: El precio está en zona de descuento.")
    elif rsi > 70:
        st.warning("🔴 VENDER: El precio está muy inflado.")
    else:
        st.info("🟡 ESPERAR: El mercado está en el medio. No arriesgues tus $25.")

    st.divider()
    st.write("💡 *Este monitor es un apoyo para tu MetaTrader 4.*")

else:
    st.warning("🔄 Intentando conectar con el mercado... (Reintento automático)")
    time.sleep(10)
    st.rerun()

# Refresco cada 30 segundos
time.sleep(30)
st.rerun()
