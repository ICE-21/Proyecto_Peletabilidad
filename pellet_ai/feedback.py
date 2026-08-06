"""
Módulo encargado de registrar resultados reales
de producción para aprendizaje continuo.
"""


import pandas as pd

from datetime import datetime

from .config import DATA_PATH



class FeedbackManager:


    def __init__(self):

        self.archivo = (
            DATA_PATH /
            "feedback.xlsx"
        )



    # ========================================================
    # GUARDAR RESULTADO REAL
    # ========================================================

    def guardar(
        self,
        id_simulacion,
        prediccion,
        resultado_real,
        observacion=""
    ):

        """
        Guarda el resultado real obtenido
        asociado a una simulación existente.
        """


        # ----------------------------------------------------
        # EVITAR DUPLICADOS
        # ----------------------------------------------------

        if self.existe_feedback(id_simulacion):

            raise ValueError(

                f"Ya existe feedback para la simulación {id_simulacion}"

            )



        # ----------------------------------------------------
        # CALCULAR ERROR
        # ----------------------------------------------------

        error = (

            resultado_real - prediccion

        )



        nuevo = pd.DataFrame({

            "ID_Simulacion": [

                int(id_simulacion)

            ],

            "Fecha": [

                datetime.now()

            ],

            "Prediccion": [

                prediccion

            ],

            "Resultado_Real": [

                resultado_real

            ],

            "Error": [

                error

            ],

            "Observacion": [

                observacion

            ]

        })



        # ----------------------------------------------------
        # AGREGAR AL HISTORIAL EXISTENTE
        # ----------------------------------------------------

        if self.archivo.exists():


            antiguo = pd.read_excel(

                self.archivo

            )


            historial = pd.concat(

                [

                    antiguo,

                    nuevo

                ],

                ignore_index=True

            )


        else:


            historial = nuevo



        # ----------------------------------------------------
        # GUARDAR ARCHIVO
        # ----------------------------------------------------

        historial.to_excel(

            self.archivo,

            index=False

        )


        return historial





    # ========================================================
    # CARGAR FEEDBACK
    # ========================================================

    def cargar(self):


        if self.archivo.exists():

            return pd.read_excel(

                self.archivo

            )


        return pd.DataFrame()





    # ========================================================
    # VALIDAR SI YA EXISTE FEEDBACK
    # ========================================================

    def existe_feedback(

        self,

        id_simulacion

    ):


        datos = self.cargar()


        if datos.empty:

            return False



        if "ID_Simulacion" not in datos.columns:

            return False



        datos["ID_Simulacion"] = pd.to_numeric(

            datos["ID_Simulacion"],

            errors="coerce"

        )



        id_simulacion = int(id_simulacion)



        return (

            id_simulacion

            in

            datos["ID_Simulacion"]
            .dropna()
            .astype(int)
            .values

        )