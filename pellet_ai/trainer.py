"""
Entrenador incremental PelletAI.

Genera un modelo candidato usando:
- Datos históricos
- Feedback real de producción

Guarda:
- modelo_candidato.cbm
- métricas del entrenamiento
"""


from catboost import CatBoostRegressor


from sklearn.model_selection import train_test_split


from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


from math import sqrt


from .config import (
    CATBOOST_PARAMS,
    TEST_SIZE,
    RANDOM_STATE,
    MODELO_CANDIDATO
)


from .dataset_feedback import DatasetFeedback





class Trainer:


    def __init__(self):

        self.dataset_feedback = DatasetFeedback()

        self.modelo_path = MODELO_CANDIDATO



    # ==================================================
    # ENTRENAMIENTO
    # ==================================================

    def entrenar(self):


        df = self.dataset_feedback.construir()



        if len(df) < 30:


            raise ValueError(

                f"Datos insuficientes. "
                f"Actualmente existen {len(df)} registros. "
                "Se requieren mínimo 30."

            )



        X = df.drop(

            columns=[

                "Resultado_Real"

            ]

        )


        y = df[

            "Resultado_Real"

        ]



        X_train, X_test, y_train, y_test = train_test_split(

            X,

            y,

            test_size=TEST_SIZE,

            random_state=RANDOM_STATE

        )



        modelo = CatBoostRegressor(

            **CATBOOST_PARAMS

        )



        modelo.fit(

            X_train,

            y_train

        )



        # ==========================================
        # Evaluación
        # ==========================================


        predicciones = modelo.predict(

            X_test

        )



        metricas = {


            "MAE":

                mean_absolute_error(

                    y_test,

                    predicciones

                ),


            "RMSE":

                sqrt(

                    mean_squared_error(

                        y_test,

                        predicciones

                    )

                ),


            "R2":

                r2_score(

                    y_test,

                    predicciones

                )

        }



        # ==========================================
        # Guardar modelo candidato
        # ==========================================


        modelo.save_model(

            self.modelo_path

        )



        return (

            modelo,

            metricas

        )