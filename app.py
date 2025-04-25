import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

# Cargar datos
@st.cache_data
def load_data():
    df = pd.read_csv("data/Catalogo_con_distritos.csv")
    df["AÑO"] = df["FECHA_UTC"].astype(str).str[:4]
    fecha_dt = pd.to_datetime(df["FECHA_UTC"].astype(str), format="%Y%m%d", errors="coerce")
    df["FECHA_UTC_FORMAT"] = fecha_dt.dt.strftime("%d/%m/%Y")  # solo para visualización
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
    st.title("🌍 Plataforma de Monitoreo Sísmico del Perú")
    st.markdown("""
    _Un recurso interactivo para la exploración histórica y territorial de los eventos sísmicos en el país._
    """)

    st.header("🧾 Descripción del Dataset")
    st.markdown(f"""
    Este conjunto de datos contiene **{len(df):,} registros sísmicos** ocurridos en el Perú.

    - **Rango de fechas:** `{df["FECHA_UTC_FORMAT"].dropna().iloc[0]}` → `{df["FECHA_UTC_FORMAT"].dropna().iloc[-1]}`
    - **Columnas clave:** `MAGNITUD`, `PROFUNDIDAD`, `LATITUD`, `LONGITUD`, `DEPARTAMENTO`, `PROVINCIA`, `DISTRITO`

    El dataset permite analizar la frecuencia, magnitud y distribución geográfica de los sismos ocurridos a lo largo de más de 60 años en el país.
    """)

    st.subheader("🌋 ¿Por qué es importante estudiar los sismos en Perú?")
    st.markdown("""
    Perú se encuentra ubicado en el **Cinturón de Fuego del Pacífico**, una zona altamente sísmica donde se produce el contacto entre la Placa de Nazca y la Placa Sudamericana.
    
    Los sismos son fenómenos naturales inevitables, pero su impacto puede reducirse mediante **conocimiento, prevención y planificación**.  
    El análisis histórico de eventos sísmicos permite:

    - 📍 Identificar **zonas de mayor recurrencia** y peligrosidad.
    - 🚨 Mejorar los **protocolos de alerta temprana y evacuación**.
    - 🏗️ Diseñar **infraestructura sismo-resistente** y desarrollo urbano seguro.
    - 📊 Apoyar a investigadores, autoridades y comunidades en la **toma de decisiones basadas en datos**.

    Esta plataforma busca **fomentar una cultura de prevención y resiliencia** ante los riesgos sísmicos en el Perú.
    """)

    # Imagen ilustrativa (opcional, colocar archivo en carpeta 'images/')
    #st.image("images/placas_tectonicas_peru.jpg", caption="Zonas sísmicas del Perú", use_column_width=True)

    st.subheader("📑 Vista Preliminar del Dataset")
    st.dataframe(df.iloc[:, :10].head(10))

    st.subheader("📈 Estadísticas Generales")
    st.dataframe(
        df.describe().T.drop("FECHA_CORTE", axis=0).style.format("{:.0f}", na_rep="")
    )

    st.subheader("🔗 Fuentes de Datos y Créditos")
    st.markdown("""
    Este análisis se basa en el catálogo sísmico oficial publicado por el **Instituto Geofísico del Perú (IGP)**, que contiene información detallada sobre los eventos sísmicos registrados desde 1960 hasta la actualidad.

    #### 📁 Fuente del Dataset
    - **Catálogo Sísmico 1960–2023 – IGP**  
    [datosabiertos.gob.pe](https://datosabiertos.gob.pe/dataset/cat%C3%A1logo-s%C3%ADsmico-1960-2023-instituto-geof%C3%ADsico-del-per%C3%BA-igp)

    #### 📚 Fuentes informativas y técnicas
    La información contextual sobre la sismicidad y su impacto en el Perú ha sido elaborada con base en fuentes oficiales:

    - 📌 **Tectónica del Perú – IGP**  
    [https://www.igp.gob.pe/servicios/sismologia/tectonica-del-peru](https://www.igp.gob.pe/servicios/sismologia/tectonica-del-peru)

    - 🌍 **Perfil de Riesgo de Desastres – Perú (UNDRR)**  
    [https://www.undrr.org/publication/disaster-risk-profile-peru](https://www.undrr.org/publication/disaster-risk-profile-peru)

    - 📈 **Reporte de Sismicidad Mensual – IGP**  
    [https://www.igp.gob.pe/servicios/sismologia/reportes-de-sismicidad](https://www.igp.gob.pe/servicios/sismologia/reportes-de-sismicidad)

    - 🌐 **USGS – Terremotos: conceptos básicos**  
    [https://earthquake.usgs.gov/learn/kids/eqscience.php](https://earthquake.usgs.gov/learn/kids/eqscience.php)
                
    #### 🛠️ Herramientas utilizadas
    - Visualización: **Streamlit** + **Plotly**
    - Procesamiento de datos: **Pandas**, **Python 3.12**
    - Formato de app: Interfaz interactiva web orientada a exploración ciudadana y académica

    Esta plataforma busca brindar acceso abierto y comprensible a información clave sobre la sismicidad nacional, con el fin de fomentar una **cultura de prevención, investigación y resiliencia** frente a los riesgos naturales.
    """)


# VISTA 2 – DASHBOARD
elif selected == "📊 Dashboard":
    st.title("📊 Dashboard Sísmico Interactivo")

    st.subheader("🎛️ Filtros")

    # Año completo en una fila
    ano_min, ano_max = st.slider("Filtrar por año:", int(df["AÑO"].min()), int(df["AÑO"].max()), (2000, 2023))

    # Fila: Departamento - Provincia - Distrito
    col1, col2, col3 = st.columns(3)

    with col1:
        departamentos = sorted(df["DEPARTAMENTO"].dropna().unique())
        departamento_seleccionado = st.selectbox("Departamento", ["Todos"] + departamentos)

    with col2:
        if departamento_seleccionado != "Todos":
            provincias = sorted(df[df["DEPARTAMENTO"] == departamento_seleccionado]["PROVINCIA"].dropna().unique())
        else:
            provincias = sorted(df["PROVINCIA"].dropna().unique())
        provincia_seleccionada = st.selectbox("Provincia", ["Todos"] + list(provincias))

    with col3:
        if provincia_seleccionada != "Todos":
            distritos = sorted(df[df["PROVINCIA"] == provincia_seleccionada]["DISTRITO"].dropna().unique())
        elif departamento_seleccionado != "Todos":
            distritos = sorted(df[df["DEPARTAMENTO"] == departamento_seleccionado]["DISTRITO"].dropna().unique())
        else:
            distritos = sorted(df["DISTRITO"].dropna().unique())
        distrito_seleccionado = st.selectbox("Distrito", ["Todos"] + list(distritos))

    # Fila: Magnitud y profundidad
    col4, col5 = st.columns(2)
    with col4:
        mag_min, mag_max = st.slider("Magnitud:", float(df["MAGNITUD"].min()), float(df["MAGNITUD"].max()), (5.0, 8.0))

    with col5:
        depth_min, depth_max = st.slider("Profundidad (km):", int(df["PROFUNDIDAD"].min()), int(df["PROFUNDIDAD"].max()), (0, 600))

    # Aplicar filtros al DataFrame
    df_filtered = df[
        (df["AÑO"].astype(int) >= ano_min) &
        (df["AÑO"].astype(int) <= ano_max) &
        (df["MAGNITUD"] >= mag_min) & 
        (df["MAGNITUD"] <= mag_max) &
        (df["PROFUNDIDAD"] >= depth_min) &
        (df["PROFUNDIDAD"] <= depth_max)
    ]

    if departamento_seleccionado != "Todos":
        df_filtered = df_filtered[df_filtered["DEPARTAMENTO"] == departamento_seleccionado]
    if provincia_seleccionada != "Todos":
        df_filtered = df_filtered[df_filtered["PROVINCIA"] == provincia_seleccionada]
    if distrito_seleccionado != "Todos":
        df_filtered = df_filtered[df_filtered["DISTRITO"] == distrito_seleccionado]


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
        size_max=6,
        zoom=4,
        hover_name="DEPARTAMENTO",
        template="plotly",
        hover_data=["PROFUNDIDAD"],
    )
    st.plotly_chart(fig_map, use_container_width=True)

    st.subheader("📉 Histograma de Magnitudes")
    fig_hist = px.histogram(df_filtered, x="MAGNITUD", nbins=30)
    st.plotly_chart(fig_hist, use_container_width=True)

    st.subheader("📅 Evolución Anual de Sismos")
    fig_ano = px.histogram(df_filtered, x="AÑO", title="Sismos por Año")
    st.plotly_chart(fig_ano, use_container_width=True)
