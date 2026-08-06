import streamlit as st
import pandas as pd

from pellet_ai import Historial
from pellet_ai import PelletAI
from pellet_ai.ui import Formulario



# ==========================================================
# RECOMENDACIÓN AUTOMÁTICA
# ==========================================================

def generar_recomendacion(
    prediccion,
    positivos,
    negativos
):

    mensaje = ""


    if prediccion >= 60:

        mensaje += (
            "✅ La fórmula presenta una "
            "peletabilidad esperada alta.\n\n"
        )


    elif prediccion >= 55:

        mensaje += (
            "🟡 La fórmula presenta una "
            "peletabilidad esperada aceptable.\n\n"
        )


    else:

        mensaje += (
            "⚠ La fórmula presenta una "
            "peletabilidad esperada baja.\n\n"
        )



    if len(positivos) > 0:

        mensaje += (
            "Factores positivos principales:\n"
        )


        for item in positivos[:3]:

            mensaje += (
                f"✔ {item['Ingrediente']}\n"
            )


        mensaje += "\n"



    if len(negativos) > 0:

        mensaje += (
            "Factores a revisar:\n"
        )


        for item in negativos[:3]:

            mensaje += (
                f"⚠ {item['Ingrediente']}\n"
            )


    return mensaje





# ==========================================================
# CONFIGURACIÓN
# ==========================================================

st.set_page_config(

    page_title="Predicción",

    page_icon="🏭",

    layout="wide"

)



st.title(
    "🏭 Predicción de Peletabilidad"
)



# ==========================================================
# CARGAR MODELO
# ==========================================================

modelo = PelletAI()

modelo.load()



formulario = Formulario(modelo)




# ==========================================================
# INFORMACIÓN RECETA
# ==========================================================

st.subheader(
    "Información de la simulación"
)



nombre_receta = st.text_input(

    "Nombre de la receta",

    placeholder="Ej. Cerdo Engorde 35-60 5 mm"

)


peso_bache = st.number_input(

    "Peso Bache (Kg)",

    min_value=1.0,

    value=1800.0,

    step=10.0,

    help="Peso total de la fórmula."
)


# ==========================================================
# TABLA INGREDIENTES KG
# ==========================================================

tabla = formulario.mostrar()




# ==========================================================
# BOTÓN PREDECIR
# ==========================================================

if st.button("🚀 PREDECIR"):

    # ==========================================
    # Validar peso del bache
    # ==========================================

    total_kg = tabla["Kg"].sum()

    diferencia = abs(
        total_kg - peso_bache
    )

    if diferencia > 5:

        st.warning(

            f"⚠ El total ingresado es "

            f"{total_kg:.2f} Kg "

            f"y el Peso Bache es "

            f"{peso_bache:.2f} Kg."

        )

    # ==========================================
    # Convertir automáticamente Kg -> %
    # ==========================================

    formula = formulario.obtener_formula(

        tabla,

        peso_bache

    )

    # ==========================================
    # Predicción
    # ==========================================

    resultado = modelo.predict_report(

        formula

    )

    # ==========================================
    # Guardar historial
    # ==========================================

    historial = Historial()

    historial.guardar(

        formula=formula,

        prediccion=resultado["prediccion"],

        semaforo=resultado["semaforo"],

        nombre=nombre_receta

    )

    # ======================================================
    # RESULTADOS
    # ======================================================


    prediccion = resultado["prediccion"]

    semaforo = resultado["semaforo"]

    positivos = resultado["top_positivos"]

    negativos = resultado["top_negativos"]



    recomendacion = generar_recomendacion(

        prediccion,

        positivos,

        negativos

    )



    st.divider()



    st.subheader(
        "📊 Resultado de Peletabilidad"
    )



    col1, col2 = st.columns(2)



    with col1:


        st.metric(

            label="Alimentación esperada",

            value=f"{prediccion:.2f}%"

        )



    with col2:


        st.metric(

            label="Estado",

            value=semaforo

        )




    st.divider()



    # ======================================================
    # IMPACTO POSITIVO
    # ======================================================

    st.subheader(

        "📈 Ingredientes que favorecen la peletabilidad"

    )



    df_positivos = pd.DataFrame(

        positivos

    )



    if not df_positivos.empty:


        st.dataframe(

            df_positivos[

                [

                    "Ingrediente",

                    "Impacto"

                ]

            ],

            use_container_width=True

        )



        st.bar_chart(

            df_positivos.set_index(

                "Ingrediente"

            )[

                "Impacto"

            ]

        )




    # ======================================================
    # IMPACTO NEGATIVO
    # ======================================================


    st.subheader(

        "📉 Ingredientes que reducen la peletabilidad"

    )



    df_negativos = pd.DataFrame(

        negativos

    )



    if not df_negativos.empty:


        st.dataframe(

            df_negativos[

                [

                    "Ingrediente",

                    "Impacto"

                ]

            ],

            use_container_width=True

        )



        st.bar_chart(

            df_negativos.set_index(

                "Ingrediente"

            )[

                "Impacto"

            ]

        )





    st.divider()



    st.subheader(

        "🧠 Interpretación automática"

    )



    st.info(

        recomendacion

    )