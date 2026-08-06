"""
Construcción del dataset para aprendizaje continuo.

Combina:
- Datos históricos
- Simulaciones realizadas
- Feedback real de producción
"""


import pandas as pd

import json


from .config import DATA_PATH

from .data import DataManager

from .historial import Historial

from .feedback import FeedbackManager



class DatasetFeedback:


    def __init__(self):

        self.historial = Historial()

        self.feedback = FeedbackManager()



    # ==================================================
    # CREAR DATASET HISTÓRICO
    # ==================================================

    def datos_base(self):


        data = DataManager()


        X, y = data.get_training_data()


        df = X.copy()


        df["Resultado_Real"] = y.values


        return df



    # ==================================================
    # CREAR DATOS CORREGIDOS
    # ==================================================

    def datos_feedback(self):


        historial = self.historial.cargar()


        feedback = self.feedback.cargar()



        if feedback.empty:

            return pd.DataFrame()



        registros = []



        for _, fila in feedback.iterrows():


            id_simulacion = fila["ID_Simulacion"]



            receta = historial[

                historial["ID"]

                ==

                id_simulacion

            ]



            if receta.empty:

                continue



            formula = json.loads(

                receta.iloc[0]["Formula"]

            )



            registro = {}



            for ingrediente, valor in formula.items():

                registro[ingrediente] = valor["Valor"]



            registro["Resultado_Real"] = (

                fila["Resultado_Real"]

            )


            registros.append(

                registro

            )



        return pd.DataFrame(registros)



    # ==================================================
    # DATASET FINAL
    # ==================================================

    def construir(self):


        base = self.datos_base()


        feedback = self.datos_feedback()



        if not feedback.empty:


            base = pd.concat(

                [

                    base,

                    feedback

                ],

                ignore_index=True

            )



        return base