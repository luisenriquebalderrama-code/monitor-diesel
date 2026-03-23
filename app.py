import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Diesel Intelligence PRO", layout="wide")

st.title("🚛 Plataforma Inteligente de Diésel - México")

# -----------------------------
# 📡 BASE DE DATOS SIMULADA (ESCALABLE A API REAL)
# -----------------------------
@st.cache_data(ttl=3600)
def cargar_datos():
    estados = ["NL", "TAMPS", "COAH", "CHIH", "SIN", "SON", "DGO", "JAL", "CDMX"]
    
    data = []
    for i in range(500):
        data.append({
            "Estacion": f"Estación {i}",
            "Estado": np.random.choice(estados),
            "Precio": round(np.random.uniform(25.5, 27.8), 2),
            "Lat": np.random.uniform(19, 30),
            "Lon": np.random.uniform(-110, -95)
        })
    
    return pd.DataFrame(data)

df = cargar_datos()

# -----------------------------
# 🚦 SEMÁFORO INTELIGENTE
# -----------------------------
promedio = df["Precio"].mean()

def clasificar(p):
    if p < promedio - 0.3:
        return "🟢 Económico"
    elif p < promedio + 0.3:
        return "🟡 Regular"
    else:
        return "🔴 Caro"

df["Clasificación"] = df["Precio"].apply(clasificar)

# -----------------------------
# 🎛️ PANEL DE CONTROL
# -----------------------------
st.sidebar.header("⚙️ Panel Empresa")

estado = st.sidebar.selectbox("Filtrar Estado", ["Todos"] + list(df["Estado"].unique()))
tipo = st.sidebar.selectbox("Tipo", ["Todos", "🟢 Económico", "🟡 Regular", "🔴 Caro"])

filtro = df.copy()

if estado != "Todos":
    filtro = filtro[filtro["Estado"] == estado]

if tipo != "Todos":
    filtro = filtro[filtro["Clasificación"] == tipo]

# -----------------------------
# 📊 DASHBOARD
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Precio Promedio", f"${round(promedio,2)}")
col2.metric("Estaciones", len(filtro))
col3.metric("Más Barato", f"${filtro['Precio'].min()}")

# -----------------------------
# 🗺️ MAPA
# -----------------------------
st.subheader("🗺️ Estaciones en México")
st.map(filtro.rename(columns={"Lat": "lat", "Lon": "lon"}))

# -----------------------------
# 🚛 RUTAS (SIMULACIÓN BASE)
# -----------------------------
st.subheader("🚛 Planificador de Ruta")

origen = st.text_input("Origen")
destino = st.text_input("Destino")
litros = st.number_input("Litros por cargar", value=300)

if st.button("Optimizar ruta"):

    ruta = df.sample(15)
    mejor = ruta.sort_values("Precio").iloc[0]
    
    ahorro = (ruta["Precio"].mean() - mejor["Precio"]) * litros

    st.success(f"""
    📍 Mejor estación: {mejor['Estacion']}  
    💰 Precio: ${mejor['Precio']}  
    💸 Ahorro estimado: ${round(ahorro,2)}
    """)

    st.dataframe(ruta)

# -----------------------------
# 🚚 FLOTILLA
# -----------------------------
st.subheader("🚚 Control de Flotilla")

unidades = st.number_input("Número de unidades", value=10)
consumo = st.number_input("Litros por unidad", value=300)

gasto_promedio = promedio * consumo * unidades
mejor_precio = df["Precio"].min()
gasto_optimo = mejor_precio * consumo * unidades

ahorro_total = gasto_promedio - gasto_optimo

st.metric("Gasto estimado", f"${round(gasto_promedio,2)}")
st.metric("Gasto optimizado", f"${round(gasto_optimo,2)}")
st.metric("Ahorro potencial", f"${round(ahorro_total,2)}")

# -----------------------------
# 📋 TABLA
# -----------------------------
st.subheader("📋 Base de estaciones")
st.dataframe(filtro, use_container_width=True)