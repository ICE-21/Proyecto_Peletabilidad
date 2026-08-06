"""
Administrador del ciclo de vida de modelos PelletAI.

Controla:
- respaldo de modelos anteriores
- actualización del modelo activo
- historial de evaluaciones
- trazabilidad de cambios
- evolución del desempeño del modelo
"""


from datetime import datetime

import shutil

import pandas as pd


from .config import (
    MODELO_ACTUAL,
    MODELO_CANDIDATO,
    VERSION_PATH,
    DATA_PATH
)




class ModelRegistry:



    def __init__(self):


        self.historial = (

            DATA_PATH /

            "historial_modelos.xlsx"

        )


        # asegurar carpeta versiones

        VERSION_PATH.mkdir(

            exist_ok=True

        )



    # =====================================================
    # GUARDAR VERSION ACTUAL
    # =====================================================

    def guardar_version_actual(self):


        if not MODELO_ACTUAL.exists():


            return None



        fecha = datetime.now().strftime(

            "%Y%m%d_%H%M%S"

        )



        archivo_version = (

            VERSION_PATH /

            f"modelo_{fecha}.cbm"

        )



        shutil.copy(

            MODELO_ACTUAL,

            archivo_version

        )



        return archivo_version





    # =====================================================
    # PROMOVER MODELO CANDIDATO
    # =====================================================

    def activar_candidato(
        self,
        metricas=None
    ):


        respaldo = (

            self.guardar_version_actual()

        )



        shutil.copy(

            MODELO_CANDIDATO,

            MODELO_ACTUAL

        )



        return {


            "respaldo":

                str(respaldo)
                if respaldo
                else None,



            "actualizado":

                True

        }





    # =====================================================
    # REGISTRAR EVALUACIÓN DE MODELO
    # =====================================================

    def registrar(


        self,


        metricas,


        decision,


        score=None,


        motivo="",


        registros=None,


        variables=None


    ):



        nuevo = pd.DataFrame({


            "Fecha":[

                datetime.now()

            ],



            "Decision":[

                decision

            ],



            "Score":[

                score

            ],



            "Registros":[

                registros

            ],



            "Variables":[

                variables

            ],



            "MAE_actual":[

                metricas["actual"]["MAE"]

            ],



            "MAE_nuevo":[

                metricas["nuevo"]["MAE"]

            ],



            "RMSE_actual":[

                metricas["actual"]["RMSE"]

            ],



            "RMSE_nuevo":[

                metricas["nuevo"]["RMSE"]

            ],



            "R2_actual":[

                metricas["actual"]["R2"]

            ],



            "R2_nuevo":[

                metricas["nuevo"]["R2"]

            ],



            "Motivo":[

                motivo

            ]

        })





        if self.historial.exists():


            antiguo = pd.read_excel(

                self.historial

            )


            datos = pd.concat(

                [

                    antiguo,

                    nuevo

                ],

                ignore_index=True

            )


        else:


            datos = nuevo





        datos.to_excel(

            self.historial,

            index=False

        )



        return datos






    # =====================================================
    # LEER HISTORIAL
    # =====================================================

    def cargar_historial(self):


        if self.historial.exists():


            return pd.read_excel(

                self.historial

            )



        return pd.DataFrame()





    # =====================================================
    # EVOLUCIÓN DEL MODELO
    #
    # Devuelve datos preparados para gráficos:
    #
    # Fecha
    # MAE_actual
    # MAE_nuevo
    # R2_actual
    # R2_nuevo
    #
    # =====================================================

    def evolucion_modelo(self):


        df = self.cargar_historial()



        if df.empty:


            return pd.DataFrame()




        columnas = [

            "Fecha",

            "MAE_actual",

            "MAE_nuevo",

            "R2_actual",

            "R2_nuevo"

        ]



        disponibles = [

            columna

            for columna in columnas

            if columna in df.columns

        ]



        df = df[disponibles].copy()




        if "Fecha" in df.columns:


            df["Fecha"] = pd.to_datetime(

                df["Fecha"]

            )


            df = df.sort_values(

                "Fecha"

            )



        return df