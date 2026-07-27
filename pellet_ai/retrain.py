"""
Módulo de reentrenamiento PelletAI

Gestiona la unión de datos históricos
con nuevos datos obtenidos por feedback.
"""


import pandas as pd

from .config import DATA_PATH



class Retrainer:


    def __init__(self):

        self.historico = None

        self.feedback = None



    # ========================================================
    # CARGAR DATA
    # ========================================================

    def load_data(self):

        """
        Carga histórico original
        y datos nuevos.
        """


        archivo_historico = (
            DATA_PATH /
            "lotes_peletizado.xlsx"
        )


        archivo_feedback = (
            DATA_PATH /
            "feedback.xlsx"
        )


        self.historico = pd.read_excel(
            archivo_historico
        )


        self.feedback = pd.read_excel(
            archivo_feedback
        )


        return (
            self.historico,
            self.feedback
        )



    # ========================================================
    # LIMPIAR FEEDBACK
    # ========================================================

    def clean_feedback(self):

        """
        Deja feedback con las mismas
        columnas del entrenamiento.
        """


        columnas_eliminar = [

            "fecha",

            "prediccion",

            "error"

        ]


        self.feedback = self.feedback.drop(

            columns=columnas_eliminar,

            errors="ignore"

        )


        return self.feedback



    # ========================================================
    # UNIFICAR DATASETS
    # ========================================================

    def combine(self):

        """
        Une histórico + nuevos lotes.
        """


        if self.historico is None:

            self.load_data()



        self.clean_feedback()



        combinado = pd.concat(

            [

                self.historico,

                self.feedback

            ],

            ignore_index=True

        )


        return combinado
