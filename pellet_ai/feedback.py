"""
Módulo encargado de registrar resultados reales
de producción para aprendizaje continuo.
"""


import pandas as pd

from pathlib import Path

from datetime import datetime


from .config import DATA_PATH



class FeedbackManager:


    def __init__(self):

        self.path = DATA_PATH / "feedback.xlsx"



    # ========================================================
    # GUARDAR RESULTADO REAL
    # ========================================================

    def save_result(
        self,
        formula,
        prediccion,
        real
    ):

        """
        Guarda una predicción junto
        con el resultado real obtenido.
        """


        registro = formula.copy()


        registro["fecha"] = (
            datetime.now()
            .strftime("%Y-%m-%d %H:%M")
        )


        registro["prediccion"] = prediccion


        registro["real"] = real


        registro["error"] = (
            real - prediccion
        )


        registro = pd.DataFrame([registro])


        # Si ya existe historial,
        # agregar nuevo registro

        if self.path.exists():

            historial = pd.read_excel(
                self.path
            )


            historial = pd.concat(
                [
                    historial,
                    registro
                ],
                ignore_index=True
            )


        else:

            historial = registro



        historial.to_excel(

            self.path,

            index=False

        )


        return historial
