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


        # Cambiar nombre del resultado real

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
    # ========================================================
    # COMPARAR MODELOS
    # ========================================================

    def compare_models(
        self,
        metrics_old,
        metrics_new
    ):

        """
        Compara modelo actual contra nuevo modelo.

        Reglas:
        - Menor MAE es mejor
        - Menor RMSE es mejor
        - Mayor R2 es mejor
        """


        mejora_mae = (
            metrics_new["MAE"]
            <
            metrics_old["MAE"]
        )


        mejora_rmse = (
            metrics_new["RMSE"]
            <
            metrics_old["RMSE"]
        )


        mejora_r2 = (
            metrics_new["R2"]
            >
            metrics_old["R2"]
        )


        aprobado = (

            mejora_mae
            and
            mejora_rmse
            and
            mejora_r2

        )


        resultado = {

            "modelo_actual": metrics_old,

            "modelo_nuevo": metrics_new,

            "mejora_MAE": mejora_mae,

            "mejora_RMSE": mejora_rmse,

            "mejora_R2": mejora_r2,

            "aceptar_modelo": aprobado

        }


        return resultado
