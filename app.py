import streamlit as st

st.set_page_config(
    page_title="PelletAI",
    page_icon="🏭",
    layout="wide"
)

st.title("🏭 PelletAI")

st.markdown("""
## Bienvenido

PelletAI es una plataforma para apoyar la operación de la línea de peletizado mediante Inteligencia Artificial.

Desde el menú de la izquierda puedes acceder a:

- 🧪 Predicción de nuevas formulaciones
- 📈 Historial de predicciones
- 🔄 Reentrenamiento del modelo
- 🤖 Administración de modelos
- ⚙️ Configuración
""")

st.info("Seleccione una opción del menú lateral para comenzar.")