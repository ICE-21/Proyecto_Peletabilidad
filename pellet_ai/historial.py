"""
Gestión del historial de predicciones PelletAI.

Registra las simulaciones realizadas,
sus fórmulas y resultados estimados.
"""


import pandas as pd

from datetime import datetime

from .config import DATA_PATH



class Historial:


    def __init__(self):

        self.archivo = (

            DATA_PATH /

            "historial_predicciones.xlsx"

        )



    # ==============================================
    # GUARDAR PREDICCIÓN
    # ==============================================

    def guardar(

        self,

        formula,

        prediccion,

        semaforo,

        nombre="Sin nombre"

    ):


        # ------------------------------------------
        # Cargar historial existente
        # ------------------------------------------

        if self.archivo.exists():


            antiguo = pd.read_excel(

                self.archivo

            )


            if antiguo.empty:


                siguiente_id = 1


            else:


                siguiente_id = (

                    antiguo["ID"].max()

                    +

                    1

                )


        else:


            antiguo = pd.DataFrame()


            siguiente_id = 1



        # ------------------------------------------
        # Nuevo registro
        # ------------------------------------------

        nuevo = pd.DataFrame({


            "ID": [

                siguiente_id

            ],


            "Fecha": [

                datetime.now()

            ],


            "Nombre": [

                nombre

            ],


            "Prediccion": [

                prediccion

            ],


            "Semaforo": [

                semaforo

            ],


            "Formula": [

                formula.to_json()

            ]

        })



        # ------------------------------------------
        # Unificar
        # ------------------------------------------

        historial = pd.concat(

            [

                antiguo,

                nuevo

            ],

            ignore_index=True

        )



        # ------------------------------------------
        # Guardar
        # ------------------------------------------

        historial.to_excel(

            self.archivo,

            index=False

        )


        return historial





    # ==============================================
    # CARGAR HISTORIAL
    # ==============================================

    def cargar(self):


        if self.archivo.exists():


            return pd.read_excel(

                self.archivo

            )


        return pd.DataFrame()





    # ==============================================
    # OBTENER SIMULACIÓN POR ID
    # ==============================================

    def obtener(

        self,

        id_simulacion

    ):


        df = self.cargar()



        if df.empty:


            return None



        registro = df[

            df["ID"]

            ==

            id_simulacion

        ]



        if registro.empty:


            return None



        return registro.iloc[0]





    # ==============================================
    # LISTA DE SIMULACIONES
    # ==============================================

    def lista(self):


        df = self.cargar()



        if df.empty:


            return []



        return df[

            [

                "ID",

                "Nombre",

                "Fecha"

            ]

        ]





    # ==============================================
    # RESUMEN HISTORIAL
    # ==============================================

    def resumen(self):


        df = self.cargar()



        if df.empty:


            return {


                "total": 0,


                "promedio": 0,


                "maximo": 0,


                "minimo": 0


            }



        return {


            "total":

                len(df),



            "promedio":

                df["Prediccion"].mean(),



            "maximo":

                df["Prediccion"].max(),



            "minimo":

                df["Prediccion"].min()

        }





    # ==============================================
    # ÚLTIMO ID
    # ==============================================

    def ultimo_id(self):


        df = self.cargar()



        if df.empty:


            return 0



        return int(

            df["ID"].max()

        )