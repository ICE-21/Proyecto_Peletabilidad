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
    Prepara feedback para que tenga
    la misma estructura del entrenamiento.
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


    # Convertir resultado real
    # al nombre de la variable objetivo

    if "real" in self.feedback.columns:

        self.feedback = self.feedback.rename(

            columns={
                "real": "%Alimentador"
            }

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
