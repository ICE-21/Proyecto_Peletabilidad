"""
Comparador de modelos PelletAI.

Evalúa el desempeño del modelo actual
y del modelo candidato utilizando
el dataset de aprendizaje continuo.
"""


from catboost import CatBoostRegressor


from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


from math import sqrt


from .config import (
    MODELO_ACTUAL,
    MODELO_CANDIDATO,
    MODEL_SELECTION
)


from .dataset_feedback import DatasetFeedback



class ModelComparator:


    def __init__(self):

        self.dataset = DatasetFeedback()



    # =====================================================
    # CARGAR MODELOS
    # =====================================================

    def cargar_modelos(self):


        modelo_actual = CatBoostRegressor()

        modelo_actual.load_model(
            MODELO_ACTUAL
        )


        modelo_nuevo = CatBoostRegressor()

        modelo_nuevo.load_model(
            MODELO_CANDIDATO
        )


        return (
            modelo_actual,
            modelo_nuevo
        )



    # =====================================================
    # CALCULAR MÉTRICAS
    # =====================================================

    def calcular_metricas(
        self,
        y_real,
        predicciones
    ):


        mae = mean_absolute_error(
            y_real,
            predicciones
        )


        rmse = sqrt(

            mean_squared_error(
                y_real,
                predicciones
            )

        )


        r2 = r2_score(
            y_real,
            predicciones
        )


        return {

            "MAE": mae,

            "RMSE": rmse,

            "R2": r2

        }



    # =====================================================
    # CALCULAR MEJORAS %
    # =====================================================

    def calcular_mejoras(

        self,

        actual,

        nuevo

    ):


        mejora_mae = (

            (

                actual["MAE"]

                -

                nuevo["MAE"]

            )

            /

            actual["MAE"]

        ) * 100



        mejora_rmse = (

            (

                actual["RMSE"]

                -

                nuevo["RMSE"]

            )

            /

            actual["RMSE"]

        ) * 100



        mejora_r2 = (

            (

                nuevo["R2"]

                -

                actual["R2"]

            )

            /

            abs(actual["R2"])

        ) * 100



        return {


            "MAE":

                mejora_mae,


            "RMSE":

                mejora_rmse,


            "R2":

                mejora_r2

        }



    # =====================================================
    # SCORE GLOBAL
    # =====================================================

    def calcular_score(

        self,

        mejoras

    ):


        pesos = MODEL_SELECTION["WEIGHTS"]


        score = 0


        detalle = {}



        # MAE

        if mejoras["MAE"] >= MODEL_SELECTION["MIN_MAE_IMPROVEMENT"]:

            score += pesos["MAE"]

            detalle["MAE"] = pesos["MAE"]

        else:

            detalle["MAE"] = 0



        # RMSE

        if mejoras["RMSE"] >= MODEL_SELECTION["MIN_RMSE_IMPROVEMENT"]:

            score += pesos["RMSE"]

            detalle["RMSE"] = pesos["RMSE"]

        else:

            detalle["RMSE"] = 0



        # R2

        if mejoras["R2"] >= MODEL_SELECTION["MIN_R2_IMPROVEMENT"]:

            score += pesos["R2"]

            detalle["R2"] = pesos["R2"]

        else:

            detalle["R2"] = 0



        return {


            "score":

                score,


            "detalle":

                detalle

        }



    # =====================================================
    # EVALUAR MODELOS
    # =====================================================

    def evaluar(self):


        df = self.dataset.construir()


        X = df.drop(

            columns=[
                "Resultado_Real"
            ]

        )


        y = df["Resultado_Real"]



        modelo_actual, modelo_nuevo = (

            self.cargar_modelos()

        )



        pred_actual = modelo_actual.predict(X)


        pred_nuevo = modelo_nuevo.predict(X)



        metricas_actual = self.calcular_metricas(

            y,

            pred_actual

        )


        metricas_nuevo = self.calcular_metricas(

            y,

            pred_nuevo

        )



        mejoras = self.calcular_mejoras(

            metricas_actual,

            metricas_nuevo

        )



        return {


            "actual":

                metricas_actual,


            "nuevo":

                metricas_nuevo,


            "mejoras":

                mejoras

        }



    # =====================================================
    # DECISIÓN FINAL
    # =====================================================

    def decidir(self):


        resultado = self.evaluar()


        mejoras = resultado["mejoras"]


        score = self.calcular_score(

            mejoras

        )



        razones = []



        if mejoras["MAE"] > 0:

            razones.append(

                f"MAE mejora {mejoras['MAE']:.2f}%."

            )

        else:

            razones.append(

                f"MAE empeora {abs(mejoras['MAE']):.2f}%."

            )



        if mejoras["RMSE"] > 0:

            razones.append(

                f"RMSE mejora {mejoras['RMSE']:.2f}%."

            )

        else:

            razones.append(

                f"RMSE empeora {abs(mejoras['RMSE']):.2f}%."

            )



        if mejoras["R2"] > 0:

            razones.append(

                f"R² mejora {mejoras['R2']:.2f}%."

            )

        else:

            razones.append(

                f"R² disminuye {abs(mejoras['R2']):.2f}%."

            )



        aceptar = (

            score["score"]

            >=

            70

        )



        if aceptar:

            decision = "ACEPTAR"

            recomendacion = (

                "El modelo candidato supera "

                "los criterios definidos."

            )

        else:

            decision = "RECHAZAR"

            recomendacion = (

                "Mantener modelo actual."

            )



        return {


            "decision":

                decision,


            "score":

                score["score"],


            "motivo":

                " ".join(razones),


            "recomendacion":

                recomendacion,


            "detalle_score":

                score["detalle"],


            "metricas":

                resultado

        }