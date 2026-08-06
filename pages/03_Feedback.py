import streamlit as st

from pellet_ai import Historial, FeedbackManager



# ==========================================================
# CONFIGURACIÓN
# ==========================================================

st.set_page_config(

    page_title="Feedback",

    page_icon="🔄",

    layout="wide"

)



st.title("🔄 Feedback de Producción")



# ==========================================================
# OBJETOS
# ==========================================================

historial = Historial()

feedback = FeedbackManager()



# ==========================================================
# CARGAR SIMULACIONES PENDIENTES
# ==========================================================


datos = historial.cargar()

datos_feedback = feedback.cargar()



if datos.empty:


    st.warning(

        "No existen simulaciones registradas."

    )

    st.stop()



# ==========================================================
# FILTRAR SIMULACIONES YA EVALUADAS
# ==========================================================


if not datos_feedback.empty:


    ids_evaluados = (

        datos_feedback["ID_Simulacion"]

        .astype(int)

        .tolist()

    )


    datos_pendientes = datos[

        ~datos["ID"]

        .astype(int)

        .isin(ids_evaluados)

    ]


else:


    datos_pendientes = datos.copy()



# ==========================================================
# VALIDAR SI EXISTEN PENDIENTES
# ==========================================================


if datos_pendientes.empty:


    st.success(

        "✅ Todas las simulaciones tienen feedback registrado."

    )


    st.stop()



# ==========================================================
# SELECCIÓN DE SIMULACIÓN
# ==========================================================


st.subheader(

    "Seleccione la simulación pendiente de evaluar"

)



opciones = {}



for _, fila in datos_pendientes.iterrows():


    opciones[

        f"{fila['ID']} - {fila['Nombre']} - {fila['Prediccion']:.2f}%"

    ] = fila["ID"]



seleccion = st.selectbox(

    "Simulación",

    opciones.keys()

)



id_seleccionado = opciones[seleccion]

# ==========================================================
# CARGAR REGISTRO
# ==========================================================

registro = historial.obtener(

    id_seleccionado

)



if registro is None:

    st.error(

        "No se encontró la simulación seleccionada."

    )

    st.stop()



# ==========================================================
# INFORMACIÓN DE LA SIMULACIÓN
# ==========================================================

st.divider()



col1, col2, col3 = st.columns(3)



with col1:


    st.metric(

        "Predicción",

        f"{registro['Prediccion']:.2f}%"

    )



with col2:


    st.metric(

        "Estado",

        registro["Semaforo"]

    )



with col3:


    st.metric(

        "ID",

        int(registro["ID"])

    )



# ==========================================================
# INGRESAR RESULTADO REAL
# ==========================================================

st.divider()



st.subheader(

    "Resultado obtenido en planta"

)



resultado_real = st.number_input(

    "Ingrese % Alimentador real",

    min_value=0.0,

    max_value=100.0,

    step=0.1

)



observacion = st.text_area(

    "Observaciones",

    placeholder=

    "Ejemplo: ajuste de vapor, cambio de rodillos, humedad alta..."

)



# ==========================================================
# GUARDAR FEEDBACK
# ==========================================================

st.divider()



if st.button(

    "💾 Guardar Feedback"

):


    try:


        feedback.guardar(

            id_simulacion=id_seleccionado,

            prediccion=registro["Prediccion"],

            resultado_real=resultado_real,

            observacion=observacion

        )


        st.success(

            "Feedback guardado correctamente."

        )



    except ValueError as e:


        st.warning(

            str(e)

        )



    except Exception as e:


        st.error(

            f"Ocurrió un error inesperado: {e}"

        )