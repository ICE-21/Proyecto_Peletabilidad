import pandas as pd
import streamlit as st

from pellet_ai import Catalogos


class Formulario:

    """
    Construye el formulario de ingreso
    de formulaciones.
    """

    def __init__(self, modelo):

        self.modelo = modelo

        self.catalogos = Catalogos()

    # ======================================================
    # TABLA DE INGREDIENTES
    # ======================================================

    def mostrar(self):

        variables = self.modelo.variables()

        tabla = self.catalogos.ingredientes_modelo(
            variables
        )

        tabla = tabla.rename(
            columns={
                "Valor": "Kg"
            }
        )

        # Ordenar alfabéticamente por nombre
        tabla = tabla.sort_values(
            by="Nombre",
            ascending=True,
            ignore_index=True
        )

        st.subheader("Formulación")

        tabla = st.data_editor(

            tabla,

            hide_index=True,

            use_container_width=True,

            num_rows="fixed",

            disabled=["Codigo", "Nombre"]

        )

        return tabla

    # ======================================================
    # CONVERTIR TABLA A FORMATO DEL MODELO
    # ======================================================

    def obtener_formula(
        self,
        tabla,
        peso_bache
    ):

        """
        Convierte Kg ingresados
        a porcentaje para el modelo.
        """

        formula = tabla.copy()

        # Solo ingredientes con cantidad

        formula = formula[
            formula["Kg"] > 0
        ]
        
        # Convertir Kg → %

        formula["Valor"] = (

            formula["Kg"]

            /

            peso_bache

        ) * 100

        # Eliminar columna Kg

        formula = formula.drop(
            columns=["Kg"]
        )

        # Filas -> columnas

        formula = (

            formula

            .set_index("Codigo")["Valor"]

            .to_frame()

            .T

        )

        # Completar variables faltantes

        formula = self.modelo.prepare_formula(
            formula
        )

        return formula