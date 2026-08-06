import streamlit as st
import plotly.express as px

from pellet_ai import FeedbackAnalyzer



# ==========================================================
# CONFIGURACIÓN
# ==========================================================

st.set_page_config(

    page_title="Análisis Modelo",

    page_icon="📊",

    layout="wide"

)



st.title(

    "📊 Análisis de desempeño del modelo"

)



# ==========================================================
# OBJETO ANALIZADOR
# ==========================================================

analizador = FeedbackAnalyzer()



# ==========================================================
# CARGAR FEEDBACK
# ==========================================================

try:


    datos = analizador.cargar()
    datos_grafico = analizador.datos_graficos()


except FileNotFoundError:


    st.warning(

        "Todavía no existe información de feedback."

    )

    st.stop()





# ==========================================================
# INDICADORES
# ==========================================================

resumen = analizador.resumen()



st.subheader(

    "Indicadores del modelo"

)



col1, col2, col3, col4, col5 = st.columns(5)



with col1:


    st.metric(

        "Lotes evaluados",

        resumen["lotes_registrados"]

    )



with col2:


    st.metric(

        "Error promedio",

        f"{resumen['error_promedio']:.2f}%"

    )



with col3:


    st.metric(

        "Error absoluto promedio",

        f"{resumen['error_abs_promedio']:.2f}%"

    )



with col4:


    st.metric(

        "Mayor error",

        f"{resumen['error_maximo']:.2f}%"

    )

with col5:


    precision = analizador.precision_operacional()


    st.metric(

        "Precisión ±5%",

        f"{precision['precision']:.1f}%"

    )


# ==========================================================
# SESGO
# ==========================================================

sesgo = analizador.sesgo()



st.divider()


precision = analizador.precision_operacional()


# ==========================================================
# TABLA DE FEEDBACK
# ==========================================================

st.subheader(

    "Resultados reales registrados"

)



st.dataframe(

    datos,

    use_container_width=True,

    hide_index=True

)





# ==========================================================
# ESTADO DE ACTUALIZACIÓN
# ==========================================================

st.divider()



st.subheader(

    "Estado de actualización del modelo"

)



if analizador.necesita_reentrenamiento():


    st.error(

        "⚠️ El modelo requiere reentrenamiento."

    )


else:


    st.success(

        "✅ El modelo todavía no requiere actualización."

    )
    
    # ==========================================================
# GRÁFICOS DE DESEMPEÑO
# ==========================================================

st.divider()

st.subheader(
    "📈 Predicción vs Resultado Real"
)


if not datos_grafico.empty:


    grafico = px.scatter(

        datos_grafico,

        x="Prediccion",

        y="Resultado_Real",

        text="Error",

        labels={

            "Prediccion":
            "Predicción del modelo (%)",

            "Resultado_Real":
            "Resultado real planta (%)"

        },

        title=
        "Comparación entre predicción y realidad"

    )


    grafico.add_shape(

        type="line",

        x0=0,

        y0=0,

        x1=100,

        y1=100,

        line=dict(

            dash="dash"

        )

    )


    st.plotly_chart(

        grafico,

        use_container_width=True

    )


else:

    st.info(

        "No existen suficientes datos para graficar."

    )
    
    # ==========================================================
# EVOLUCIÓN DEL ERROR
# ==========================================================

st.divider()


st.subheader(
    "📉 Evolución del error del modelo"
)


error_tiempo = analizador.evolucion_error()



if not error_tiempo.empty:


    grafico_error = px.line(

        error_tiempo,

        x="Fecha",

        y="Error_Absoluto",

        markers=True,

        labels={

            "Fecha":
            "Fecha",

            "Error_Absoluto":
            "Error absoluto (%)"

        },

        title=
        "Comportamiento del error en producción"

    )


    st.plotly_chart(

        grafico_error,

        use_container_width=True

    )


else:


    st.info(

        "No existen datos suficientes."

    )
    
    