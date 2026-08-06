import streamlit as st

from pellet_ai import Historial, FeedbackManager



# ==========================================================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================================================

st.set_page_config(
    page_title="Historial",
    page_icon="📚",
    layout="wide"
)


st.title(
    "📚 Historial de Simulaciones"
)



# ==========================================================
# CARGAR DATOS
# ==========================================================


historial = Historial()

feedback = FeedbackManager()


datos = historial.cargar()

datos_feedback = feedback.cargar()



# ==========================================================
# UNIR RESULTADOS REALES
# ==========================================================


if not datos.empty:


    if not datos_feedback.empty:


        datos_feedback = datos_feedback[
            [
                "ID_Simulacion",
                "Resultado_Real"
            ]
        ]


        datos = datos.merge(

            datos_feedback,

            how="left",

            left_on="ID",

            right_on="ID_Simulacion"

        )


    else:


        datos["Resultado_Real"] = None



estadisticas = historial.resumen()



# ==========================================================
# INDICADORES
# ==========================================================


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Simulaciones",
        estadisticas["total"]
    )


with col2:

    st.metric(
        "Promedio",
        f"{estadisticas['promedio']:.2f}%"
    )


with col3:

    st.metric(
        "Máximo",
        f"{estadisticas['maximo']:.2f}%"
    )


with col4:

    st.metric(
        "Mínimo",
        f"{estadisticas['minimo']:.2f}%"
    )



# ==========================================================
# FILTROS
# ==========================================================


st.divider()


col1, col2 = st.columns(2)



with col1:


    filtro = st.selectbox(

        "Estado",

        [

            "Todos",

            "🟢 Excelente",

            "🟡 Bueno",

            "🟠 Riesgo moderado",

            "🔴 Bajo rendimiento"

        ]

    )



with col2:


    buscar = st.text_input(

        "Buscar en la fórmula"

    )




# ==========================================================
# APLICAR FILTROS
# ==========================================================


datos_filtrado = datos.copy()



if not datos_filtrado.empty:


    if filtro != "Todos":


        datos_filtrado = datos_filtrado[

            datos_filtrado["Semaforo"]

            ==

            filtro

        ]



    if buscar:


        datos_filtrado = datos_filtrado[

            datos_filtrado["Formula"]

            .str.contains(

                buscar,

                case=False,

                na=False

            )

        ]




# ==========================================================
# TABLA
# ==========================================================


st.divider()


st.subheader(
    "📋 Historial de simulaciones"
)



columnas = [

    "ID",

    "Fecha",

    "Nombre",

    "Prediccion",

    "Resultado_Real",

    "Semaforo"

]



tabla = datos_filtrado[

    columnas

].copy()



# Cambiar vacíos por guion

tabla["Resultado_Real"] = (

    tabla["Resultado_Real"]

    .fillna("-")

)



st.dataframe(

    tabla,

    use_container_width=True,

    hide_index=True

)



# ==========================================================
# MENSAJE FINAL
# ==========================================================


if datos.empty:


    st.info(

        "Todavía no existen simulaciones registradas."

    )