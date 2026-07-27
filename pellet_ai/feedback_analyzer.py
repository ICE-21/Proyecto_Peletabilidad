"""
Analizador de retroalimentación PelletAI

Evalúa el desempeño del modelo
con los nuevos lotes registrados.
"""


import pandas as pd

from pathlib import Path

from .config import DATA_PATH



class FeedbackAnalyzer:


    def __init__(self):

        self.file = DATA_PATH / "feedback.xlsx"

        self.df = None



    # ========================================================
    # CARGAR DATOS DE FEEDBACK
    # ========================================================

    def load(self):

        """
        Carga los resultados reales registrados.
        """

        if not self.file.exists():

            raise FileNotFoundError(
                "No existe feedback.xlsx"
            )


        self.df = pd.read_excel(
            self.file
        )


        return self.df



    # ========================================================
    # RESUMEN GENERAL
    # ========================================================

    def summary(self):

        """
        Resumen del comportamiento
        del modelo.
        """


        if self.df is None:

            self.load()



        resumen = {


            "lotes_registrados":

                len(self.df),


            "error_promedio":

                self.df["error"].mean(),


            "error_abs_promedio":

                self.df["error"].abs().mean(),


            "error_maximo":

                self.df["error"].max(),


            "error_minimo":

                self.df["error"].min()


        }


        return resumen



    # ========================================================
    # SESGO DEL MODELO
    # ========================================================

    def bias(self):

        """
        Evalúa si el modelo tiende
        a sobreestimar o subestimar.
        """


        promedio = self.df["error"].mean()



        if promedio > 0:

            return (
                "El modelo subestima "
                f"en promedio {promedio:.2f}%"
            )


        else:

            return (
                "El modelo sobreestima "
                f"en promedio {abs(promedio):.2f}%"
            )



    # ========================================================
    # DECISIÓN DE REENTRENAMIENTO
    # ========================================================

    def should_retrain(

        self,

        min_lotes=50,

        max_error=5

    ):

        """
        Define si conviene reentrenar.
        """


        resumen = self.summary()



        if (

            resumen["lotes_registrados"] >= min_lotes

            and

            resumen["error_abs_promedio"] > max_error

        ):

            return True



        return False
