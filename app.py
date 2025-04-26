import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

# ---------------------- CARGA DE DATOS ---------------------- #
@st.cache_data
def load_data():
    df = pd.read_csv("data/Catalogo_con_distritos.csv")
    df["AÑO"] = df["FECHA_UTC"].astype(str).str[:4]
    fecha_dt = pd.to_datetime(df["FECHA_UTC"].astype(str), format="%Y%m%d", errors="coerce")
    df["FECHA"] = fecha_dt.dt.strftime("%d/%m/%Y")
    df["HORA"] = df["HORA_UTC"].astype(str).str.zfill(6).str[:2]  # extrae las 2 primeras cifras (horas)
    df["HORA"] = df["HORA"].astype(int)
    return df

df = load_data()

# ----------------------- MENÚ LATERAL ----------------------- #
with st.sidebar:
    selected = option_menu(
        menu_title="📈 Plataforma de Monitoreo Sísmico",
        options=["📘 Inicio", "📊 Dashboard"],
        default_index=0,
        styles={
            "container": {"padding": "10px", "background-color": "#1E1E1E"},
            "icon": {"color": "#ffffff", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "color": "#ffffff"
            },
            "nav-link-selected": {
                "background-color": "#339af0",
                "color": "#ffffff",
                "font-weight": "bold",
                "border-radius": "8px"
            },
            "menu-title": {
                "font-size": "24px",
                "text-align": "center",
                "color": "#ffffff",
                "font-weight": "bold",
                "background-image": "none",
            }
        }
    )

# ------------------- PESTAÑA: INICIO ------------------ #
if selected == "📘 Inicio": 
    st.title("🌍 Plataforma de Monitoreo Sísmico del Perú")
    st.markdown("""
    _Un recurso interactivo para la exploración histórica y territorial de los eventos sísmicos en el país._
    """)

    st.header("🧾 Descripción del conjunto de datos")
    st.markdown(f"""
    Este conjunto de datos contiene **{len(df):,} registros sísmicos** ocurridos en el Perú.

    - **Rango de fechas:** `{df["FECHA"].dropna().iloc[0]}` → `{df["FECHA"].dropna().iloc[-1]}`
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

    Esta plataforma busca brindar acceso abierto y comprensible a información clave sobre la sismicidad nacional, con el fin de fomentar una **cultura de prevención, investigación y resiliencia** frente a los riesgos naturales.
    """)

    st.subheader("📑 Vista Preliminar del Conjunto de Datos")
    st.dataframe(df.iloc[:, :10].head(10))

    st.subheader("📈 Estadísticas Generales")
    st.dataframe(
        df.describe().T.drop("FECHA_CORTE", axis=0).style.format("{:.0f}", na_rep="")
    )

    st.subheader("🔗 Fuentes de Datos")
    st.markdown("""
    Este análisis se basa en el catálogo sísmico oficial publicado por el **Instituto Geofísico del Perú (IGP)**, que contiene información detallada sobre los eventos sísmicos registrados desde 1960 hasta 2023.

    #### 📁 Fuente del Dataset
    - **Catálogo Sísmico 1960–2023 – IGP**  
    [datosabiertos.gob.pe](https://datosabiertos.gob.pe/dataset/cat%C3%A1logo-s%C3%ADsmico-1960-2023-instituto-geof%C3%ADsico-del-per%C3%BA-igp)

    #### 📚 Fuentes informativas y técnicas
    La información contextual sobre la sismicidad y su impacto en el Perú ha sido elaborada con base en fuentes oficiales:

    - 📌 **Tectónica del Perú – IGP**  
    [https://www.igp.gob.pe/](https://www.igp.gob.pe/)

    - 🌍 **Perfil de Riesgo de Desastres – Perú (UNDRR)**  
    [https://www.undrr.org/](https://www.undrr.org/)

    - 🌐 **USGS – Terremotos: conceptos básicos**  
    [https://earthquake.usgs.gov/learn/kids/eqscience.php](https://earthquake.usgs.gov/learn/kids/eqscience.php)
                
    #### 🛠️ Herramientas utilizadas
    - Visualización: **Streamlit** + **Plotly**
    - Procesamiento de datos: **Pandas**, **Python 3.12**
    """)

    st.subheader("👨‍💻 Elaborado por")

    st.markdown("""
    Esta plataforma fue desarrollada como una herramienta educativa e informativa de acceso abierto, 
    combinando técnicas de ciencia de datos, visualización interactiva y fuentes oficiales del monitoreo sísmico en el Perú.

    **Desarrolladores:**  
    - **Mercedes Díaz Pichiule**  
    Bachiller en Ingeniería Informática – Pontificia Universidad Católica del Perú

    - **Ángel Mayta Coaguila**  
    Ingeniero Civil - Universidad Nacional de San Agustín

    - **Miguel Lescano Avalos**  
    Bachiller en Ingeniería de Sistemas - Universidad Nacional de Ingeniería

    - **Sun Ji Sánchez**  
    Bachiller en Ingeniería Informática – Pontificia Universidad Católica del Perú

    **Fecha de publicación:** Abril 2025  
    **Ubicación:** Lima, Perú
    """)

# ------------------- PESTAÑA: DASHBOARD --------------------- #
elif selected == "📊 Dashboard":
    st.title("📊 Dashboard Sísmico Interactivo")

    # Filtros
    st.sidebar.subheader("🎛️ Filtros")

    # Filtro de año
    ano_min, ano_max = st.sidebar.slider("Filtrar por año:", int(df["AÑO"].min()), int(df["AÑO"].max()), (2000, 2023))

    # Filtros de ubicación
    col1a, col1b = st.sidebar.columns(2)
    with col1a:
        departamentos = sorted(df["DEPARTAMENTO"].dropna().unique())
        departamento_seleccionado = st.selectbox("Departamento", ["Todos"] + departamentos)
    with col1b:
        if departamento_seleccionado != "Todos":
            provincias = sorted(df[df["DEPARTAMENTO"] == departamento_seleccionado]["PROVINCIA"].dropna().unique())
        else:
            provincias = sorted(df["PROVINCIA"].dropna().unique())
        provincia_seleccionada = st.selectbox("Provincia", ["Todos"] + provincias)
    col2 = st.sidebar.container()
    with col2:
        if provincia_seleccionada != "Todos":
            distritos = sorted(df[df["PROVINCIA"] == provincia_seleccionada]["DISTRITO"].dropna().unique())
        elif departamento_seleccionado != "Todos":
            distritos = sorted(df[df["DEPARTAMENTO"] == departamento_seleccionado]["DISTRITO"].dropna().unique())
        else:
            distritos = sorted(df["DISTRITO"].dropna().unique())
        distrito_seleccionado = st.selectbox("Distrito", ["Todos"] + distritos)

    # Filtros de magnitud y profundidad
    col3a, col3b = st.sidebar.columns(2)
    with col3a:
        mag_min, mag_max = st.slider("Magnitud:", float(df["MAGNITUD"].min()), float(df["MAGNITUD"].max()), (5.0, 8.0))
    with col3b:
        prof_min, prof_max = st.slider("Profundidad (km):", int(df["PROFUNDIDAD"].min()), int(df["PROFUNDIDAD"].max()), (0, 600))

    # Aplicación de filtros
    df_filtered = df[
        df["AÑO"].astype(int).between(ano_min, ano_max) &
        df["MAGNITUD"].between(mag_min, mag_max) &
        df["PROFUNDIDAD"].between(prof_min, prof_max)
    ]
    if departamento_seleccionado != "Todos":
        df_filtered = df_filtered[df_filtered["DEPARTAMENTO"] == departamento_seleccionado]
    if provincia_seleccionada != "Todos":
        df_filtered = df_filtered[df_filtered["PROVINCIA"] == provincia_seleccionada]
    if distrito_seleccionado != "Todos":
        df_filtered = df_filtered[df_filtered["DISTRITO"] == distrito_seleccionado]

    # Indicadores
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Eventos", len(df_filtered))
    col2.metric("Magnitud Máxima", df_filtered["MAGNITUD"].max())
    col3.metric("Magnitud Promedio", round(df_filtered["MAGNITUD"].mean(), 1)) 
    col4.metric("Profundidad Promedio (km)", round(df_filtered["PROFUNDIDAD"].mean(), 1))

    # Mapa de eventos sísmicos
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
        hover_data=["PROFUNDIDAD", "FECHA"],
        color_continuous_scale=px.colors.sequential.Bluered,
    )
    st.plotly_chart(fig_map, use_container_width=True)

    # Crear las columnas para colocar los gráficos lado a lado
    col1, col2 = st.columns(2)

    # Gráfico de línea de frecuencia de sismos por año
    with col1:
        st.markdown("##### 📊 Frecuencia de Sismos por Año")
        sismos_por_anio = df_filtered.groupby("AÑO").size().reset_index(name="Número de Sismos")
        fig4 = px.bar(
            sismos_por_anio,
            x="AÑO",
            y="Número de Sismos",
            labels={"AÑO": "Año", "Número de Sismos": "Número de sismos"},
            color_discrete_sequence=["#9467bd"]
        )
        st.plotly_chart(fig4, use_container_width=True)
        max_year = sismos_por_anio.loc[sismos_por_anio["Número de Sismos"].idxmax(), "AÑO"]
        st.info(f"El año con más sismos fue **{max_year}**.")

    # Gráfico de línea de promedio de magnitud por año
    with col2:
        st.markdown("##### 📉 Promedio de Magnitud por Año")
        avg_mag_per_year = df_filtered.groupby("AÑO")["MAGNITUD"].mean().reset_index()
        fig5 = px.line(
            avg_mag_per_year,
            x="AÑO",
            y="MAGNITUD",
            labels={"AÑO": "Año", "MAGNITUD": "Promedio de magnitud"},
            color_discrete_sequence=["#1f77b4"],
        )
        st.plotly_chart(fig5, use_container_width=True)
        max_mag_year = avg_mag_per_year.loc[avg_mag_per_year["MAGNITUD"].idxmax(), "AÑO"]
        max_mag_value = round(avg_mag_per_year["MAGNITUD"].max(), 2)
        st.info(f"El año con el mayor promedio de magnitud fue **{max_mag_year}** con **{max_mag_value}**.")

    # Boxplot de magnitud por departamento
    st.subheader("📦 Magnitudes de sismos a lo largo del Perú")
    fig6 = px.box(
        df_filtered,
        x="DEPARTAMENTO",
        y="MAGNITUD",
        labels={"DEPARTAMENTO": "Departamento", "MAGNITUD": "Magnitud"},
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    fig6.update_layout(xaxis_title="Departamento", yaxis_title="Magnitud")
    st.plotly_chart(fig6, use_container_width=True)
    dep_mayor_mag = df_filtered.groupby("DEPARTAMENTO")["MAGNITUD"].mean().idxmax()
    st.info(f"El departamento con mayor magnitud promedio es **{dep_mayor_mag}**.")

    # Gráfico de dispersión de magnitud vs profundidad
    st.subheader("📉 Relación entre Magnitud y Profundidad")
    fig2 = px.scatter(
        df_filtered, 
        x="MAGNITUD", 
        y="PROFUNDIDAD",
        labels={"MAGNITUD": "Magnitud", "PROFUNDIDAD": "Profundidad (km)", "FECHA": "Fecha", "DEPARTAMENTO": "Departamento"},
        color_discrete_sequence=["#1f77b4"],
        hover_data={
        "FECHA": True,        
        "DEPARTAMENTO": True, 
        "MAGNITUD": True,     
        "PROFUNDIDAD": True  
        }
    )
    st.plotly_chart(fig2)
    profundidad_media = round(df_filtered["PROFUNDIDAD"].mean(), 1)
    st.info(f"La profundidad promedio de los eventos analizados es de **{profundidad_media} km**.")

    # Histograma de frecuencia de sismos por hora del día
    st.subheader("⏰ Frecuencia de Sismos por Hora del Día")
    df_hora = df_filtered["HORA"].value_counts().sort_index().reset_index()
    df_hora.columns = ["Hora del día", "Cantidad de sismos"]
    fig_hora = px.bar(
        df_hora,
        x="Hora del día",
        y="Cantidad de sismos",
        labels={"Hora del día": "Hora del día", "Cantidad de sismos": "Cantidad de sismos"},
        color_discrete_sequence=["#17becf"]
    )
    fig_hora.update_layout(bargap=0.1, xaxis=dict(dtick=1))
    st.plotly_chart(fig_hora, use_container_width=True)
    hora_mas_sismos = df_hora.loc[df_hora["Cantidad de sismos"].idxmax(), "Hora del día"]
    st.info(f"La hora con más actividad sísmica fue alrededor de las **{hora_mas_sismos}:00 horas**.")