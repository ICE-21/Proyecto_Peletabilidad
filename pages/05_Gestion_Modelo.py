import streamlit as st


from pellet_ai import (
    ModeloManager,
    FeedbackAnalyzer,
    LearningPipeline
)



st.set_page_config(

    page_title="Gestión Modelo",

    page_icon="🤖",

    layout="wide"

)



st.title(
    "🤖 Gestión del Modelo Predictivo"
)



modelo = ModeloManager()

feedback = FeedbackAnalyzer()

pipeline = LearningPipeline()



# ==================================================
# MODELO ACTUAL
# ==================================================


st.subheader(
    "🧠 Modelo actual"
)



estado_modelo = modelo.estado_modelo()



metadata = estado_modelo.get(
    "metadata",
    {}
)



metricas_modelo = metadata.get(
    "metricas",
    {}
)



if estado_modelo["existe"]:

    st.success(
        "Modelo activo encontrado"
    )

else:

    st.error(
        "No existe modelo activo"
    )



col1,col2,col3,col4,col5 = st.columns(5)



with col1:

    st.metric(
        "Archivo",
        estado_modelo["archivo"]
    )


with col2:

    st.metric(
        "Modelo",
        metadata.get(
            "modelo_activo",
            "CatBoost"
        )
    )


with col3:

    st.metric(
        "MAE",
        round(
            metricas_modelo.get(
                "MAE",
                0
            ),
            3
        )
    )


with col4:

    st.metric(
        "RMSE",
        round(
            metricas_modelo.get(
                "RMSE",
                0
            ),
            3
        )
    )


with col5:

    st.metric(
        "R²",
        round(
            metricas_modelo.get(
                "R2",
                0
            ),
            4
        )
    )



# ==================================================
# FEEDBACK
# ==================================================


st.divider()


st.subheader(
    "📚 Datos de aprendizaje"
)



try:


    resumen = feedback.resumen()



    col1,col2,col3 = st.columns(3)



    with col1:

        st.metric(

            "Feedback registrados",

            resumen["lotes_registrados"]

        )


    with col2:

        st.metric(

            "Error promedio",

            f"{resumen['error_abs_promedio']:.2f}%"

        )


    with col3:


        if feedback.necesita_reentrenamiento():

            st.warning(
                "Listo para evaluación"
            )

        else:

            st.success(
                "Esperando más datos"
            )


except Exception:


    st.info(
        "No existe feedback todavía"
    )



# ==================================================
# APRENDIZAJE CONTINUO
# ==================================================


st.divider()


st.subheader(
    "🚀 Aprendizaje continuo"
)



if "resultado_pipeline" not in st.session_state:

    st.session_state.resultado_pipeline = None




if st.button(
    "🚀 Ejecutar evaluación del modelo"
):


    with st.spinner(

        "Entrenando candidato y comparando modelos..."

    ):


        st.session_state.resultado_pipeline = (

            pipeline.ejecutar()

        )




resultado = st.session_state.resultado_pipeline



if resultado:



    estado = resultado.get(
        "estado",
        ""
    )



    if estado == "MODELO_ACTUALIZADO":


        st.success(
            "🟢 Modelo actualizado correctamente"
        )


    elif estado == "MODELO_MANTENIDO":


        st.warning(
            "🟡 Modelo actual conservado"
        )


    elif estado == "ESPERANDO_DATOS":


        st.info(
            resultado["mensaje"]
        )


    else:


        st.error(
            resultado.get(
                "mensaje",
                "Error desconocido"
            )
        )



    # ==================================================
    # COMPARACIÓN
    # ==================================================


    if "comparacion" in resultado:



        st.divider()


        st.subheader(
            "📊 Comparación de modelos"
        )



        comparacion = resultado["comparacion"]



        metricas = comparacion["metricas"]



        actual = metricas["actual"]

        nuevo = metricas["nuevo"]



        col1,col2 = st.columns(2)



        with col1:


            st.markdown(
                "### Modelo actual"
            )


            st.metric(
                "MAE",
                round(
                    actual["MAE"],
                    3
                )
            )


            st.metric(
                "RMSE",
                round(
                    actual["RMSE"],
                    3
                )
            )


            st.metric(
                "R²",
                round(
                    actual["R2"],
                    4
                )
            )



        with col2:


            st.markdown(
                "### Modelo candidato"
            )


            st.metric(
                "MAE",
                round(
                    nuevo["MAE"],
                    3
                )
            )


            st.metric(
                "RMSE",
                round(
                    nuevo["RMSE"],
                    3
                )
            )


            st.metric(
                "R²",
                round(
                    nuevo["R2"],
                    4
                )
            )



        st.subheader(
            "📈 Mejoras obtenidas"
        )



        mejoras = metricas["mejoras"]



        col1,col2,col3 = st.columns(3)



        with col1:

            st.metric(

                "Mejora MAE",

                f"{mejoras['MAE']:.2f}%"

            )


        with col2:

            st.metric(

                "Mejora RMSE",

                f"{mejoras['RMSE']:.2f}%"

            )


        with col3:

            st.metric(

                "Mejora R²",

                f"{mejoras['R2']:.2f}%"

            )