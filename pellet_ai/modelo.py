"""
Modelo predictivo PelletAI

Encapsula entrenamiento y evaluación
del modelo CatBoost.
"""


import numpy as np

from catboost import CatBoostRegressor

from sklearn.model_selection import train_test_split

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


from .config import (
    CATBOOST_PARAMS,
    TEST_SIZE,
    RANDOM_STATE
)



class PelletAI:


    def __init__(self):

        self.modelo = None

        self.metrics = {}

        self.X_train = None
        self.X_test = None

        self.y_train = None
        self.y_test = None



    def train(self, X, y):

        """
        Entrena el modelo CatBoost
        """

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(

            X,
            y,

            test_size=TEST_SIZE,

            random_state=RANDOM_STATE

        )


        self.modelo = CatBoostRegressor(
            **CATBOOST_PARAMS
        )


        self.modelo.fit(
            self.X_train,
            self.y_train
        )


        return self.modelo



    def evaluate(self):

        """
        Calcula métricas del modelo
        """

        predicciones = self.modelo.predict(
            self.X_test
        )


        mae = mean_absolute_error(
            self.y_test,
            predicciones
        )


        rmse = np.sqrt(
            mean_squared_error(
                self.y_test,
                predicciones
            )
        )


        r2 = r2_score(
            self.y_test,
            predicciones
        )


        self.metrics = {

            "MAE": mae,

            "RMSE": rmse,

            "R2": r2

        }


        return self.metrics



    def predict(self, X):

        """
        Predice nuevas formulaciones
        """

        return self.modelo.predict(X)
