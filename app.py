import streamlit as st
import pandas as pd
import plotly.express as px

# Carga de datos
@st.cache_data
def load_data():
    return pd.read_csv("Catalogo_con_distritos.csv")

df = load_data()

st.title("📈 Monitoreo Sísmico en Perú")
st.markdown("Visualización interactiva del catálogo de sismos históricos registrados en el país.")

# Filtros
st.sidebar.header("🔍 Filtros")
mag_min, mag_max = st.sidebar.slider("Magnitud", float(df["MAGNITUD"].min()), float(df["MAGNITUD"].max()), (5.0, 8.0))
depth_min, depth_max = st.sidebar.slider("Profundidad (km)", int(df["PROFUNDIDAD"].min()), int(df["PROFUNDIDAD"].max()), (0, 600))

df_filtered = df[(df["MAGNITUD"] >= mag_min) & (df["MAGNITUD"] <= mag_max) &
                 (df["PROFUNDIDAD"] >= depth_min) & (df["PROFUNDIDAD"] <= depth_max)]

# Indicadores
st.subheader("📌 Indicadores Principales")
col1, col2, col3 = st.columns(3)
col1.metric("Total de Sismos", len(df_filtered))
col2.metric("Magnitud Máxima", df_filtered["MAGNITUD"].max())
col3.metric("Profundidad Promedio (km)", round(df_filtered["PROFUNDIDAD"].mean(), 1))

# Mapa interactivo
st.subheader("🗺️ Mapa de Eventos Sísmicos")
fig_map = px.scatter_map(
    df_filtered,
    lat="LATITUD",
    lon="LONGITUD",
    color="MAGNITUD",
    size="MAGNITUD",
    hover_name="NOMBDEP",
    zoom=4,
    size_max=3,
    title="Mapa de Sismos en Perú",
    template="plotly"  # Esto reemplaza el mapbox_style
)
st.plotly_chart(fig_map, use_container_width=True)

# Histograma de magnitud
st.subheader("📉 Distribución de Magnitudes")
fig_hist = px.histogram(df_filtered, x="MAGNITUD", nbins=30, title="Histograma de Magnitudes")
st.plotly_chart(fig_hist, use_container_width=True)

# Gráfico temporal (si hay fechas válidas)
st.subheader("📅 Sismos por Año")
df_filtered["AÑO"] = df_filtered["FECHA_UTC"].astype(str).str[:4]
fig_time = px.histogram(df_filtered, x="AÑO", title="Cantidad de Sismos por Año")
st.plotly_chart(fig_time, use_container_width=True)
