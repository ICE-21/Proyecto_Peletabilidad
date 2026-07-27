from catboost import CatBoostRegressor


class PelletAI:

    def __init__(self):

        self.modelo = None

        self.metricas = {}

        self.variables = []

        self.X_train = None

        self.X_test = None

        self.y_train = None

        self.y_test = None

  from sklearn.model_selection import train_test_split

from .config import *

import pandas as pd

    def preparar_datos(self, df):

        df = df[df["Codigo"].str.startswith(tuple(FAMILIAS), na=False)].copy()

        X = df.drop(columns=[TARGET])

        y = df[TARGET]

        self.variables = list(X.columns)

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(

            X,

            y,

            test_size=TEST_SIZE,

            random_state=RANDOM_STATE

        )

        return self

    def entrenar(self):

        self.modelo = CatBoostRegressor(

            **CATBOOST_PARAMS

        )

        self.modelo.fit(

            self.X_train,

            self.y_train

        )

        return self
