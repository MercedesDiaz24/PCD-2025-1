import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

# Cargar datos
@st.cache_data
def load_data():
    df = pd.read_csv("data/Catalogo_con_distritos.csv")
    df["AÑO"] = df["FECHA_UTC"].astype(str).str[:4]
    df["FECHA_UTC_DT"] = pd.to_datetime(df["FECHA_UTC"].astype(str), format="%Y%m%d", errors="coerce")
    return df

df = load_data()

# Sidebar visual con íconos
with st.sidebar:
    selected = option_menu(
        menu_title="",
        options=["📘 Presentación", "📊 Dashboard"],
        default_index=0,
        styles={
            "container": {"padding": "10px", "background-color": "#1E1E1E"},
            "icon": {"color": "#ffffff", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "5px",
                "color": "#ffffff"
            },
            "nav-link-selected": {
                "background-color": "#339af0",
                "color": "#ffffff",
                "font-weight": "bold",
                "border-radius": "8px"
            },
        }
    )


# VISTA 1 – PRESENTACIÓN
if selected == "📘 Presentación":
    st.title("🌍 Catálogo de Sismos del Perú")
    st.header("🧾 Descripción del Dataset")
    st.markdown(f"""
    Este conjunto de datos contiene **{len(df):,} registros sísmicos** ocurridos en el Perú.

    - **Rango de fechas:** `{df["FECHA_UTC_DT"].astype(str).min()}` → `{df["FECHA_UTC_DT"].astype(str).max()}`
    - **Columnas clave:** `MAGNITUD`, `PROFUNDIDAD`, `LATITUD`, `LONGITUD`, `NOMBDEP`, `NOMBDIST`
    """)

    st.subheader("📑 Vista Preliminar del Dataset")
    st.dataframe(df.head(10), use_container_width=True)

    st.subheader("📈 Estadísticas Generales")
    st.write(df.describe())

# VISTA 2 – DASHBOARD
elif selected == "📊 Dashboard":
    st.title("📊 Dashboard Sísmico Interactivo")

    st.subheader("🎛️ Filtros")
    mag_min, mag_max = st.slider("Filtrar por magnitud:", float(df["MAGNITUD"].min()), float(df["MAGNITUD"].max()), (5.0, 8.0))
    depth_min, depth_max = st.slider("Filtrar por profundidad (km):", int(df["PROFUNDIDAD"].min()), int(df["PROFUNDIDAD"].max()), (0, 600))

    df_filtered = df[(df["MAGNITUD"] >= mag_min) & (df["MAGNITUD"] <= mag_max) &
                     (df["PROFUNDIDAD"] >= depth_min) & (df["PROFUNDIDAD"] <= depth_max)]

    col1, col2, col3 = st.columns(3)
    col1.metric("Eventos", len(df_filtered))
    col2.metric("Magnitud Máxima", df_filtered["MAGNITUD"].max())
    col3.metric("Profundidad Promedio (km)", round(df_filtered["PROFUNDIDAD"].mean(), 1))

    st.subheader("🗺️ Mapa de Eventos Sísmicos")
    fig_map = px.scatter_map(
        df_filtered,
        lat="LATITUD",
        lon="LONGITUD",
        color="MAGNITUD",
        size="MAGNITUD",
        size_max=8,
        zoom=4,
        hover_name="NOMBDEP",
        template="plotly"
    )
    st.plotly_chart(fig_map, use_container_width=True)

    st.subheader("📉 Histograma de Magnitudes")
    fig_hist = px.histogram(df_filtered, x="MAGNITUD", nbins=30)
    st.plotly_chart(fig_hist, use_container_width=True)

    st.subheader("📅 Evolución Anual de Sismos")
    fig_ano = px.histogram(df_filtered, x="AÑO", title="Sismos por Año")
    st.plotly_chart(fig_ano, use_container_width=True)
