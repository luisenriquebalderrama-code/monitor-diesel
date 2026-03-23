import streamlit as st
import pandas as pd

st.set_page_config(page_title="Monitor Diesel", layout="wide")

st.title("🚛 Monitor de Precios de Diésel")

data = [
    {"Estacion": "Pemex Chihuahua", "Estado": "CHIH", "Precio": 26.40},
    {"Estacion": "BP Durango", "Estado": "DGO", "Precio": 26.60},
    {"Estacion": "Ultra Sinaloa", "Estado": "SIN", "Precio": 26.90},
    {"Estacion": "Pemex Sonora", "Estado": "SON", "Precio": 27.20},
]

df = pd.DataFrame(data)

def semaforo(precio):
    if precio < 26.5:
        return "🟢 Económico"
    elif precio < 27:
        return "🟡 Regular"
    else:
        return "🔴 Caro"

df["Clasificación"] = df["Precio"].apply(semaforo)

st.dataframe(df, use_container_width=True)

estado = st.selectbox("Filtrar por estado", ["Todos"] + list(df["Estado"].unique()))

if estado != "Todos":
    df = df[df["Estado"] == estado]

st.write("### Resultado filtrado")
st.dataframe(df, use_container_width=True)
