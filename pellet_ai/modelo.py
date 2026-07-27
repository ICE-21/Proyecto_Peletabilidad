"""
Modelo predictivo PelletAI

Encapsula entrenamiento, evaluación
e interpretación del modelo CatBoost.
"""


import numpy as np
import pandas as pd
import shap
import json
import pickle

from datetime import datetime


from catboost import CatBoostRegressor


from sklearn.model_selection import (
    train_test_split,
    RepeatedKFold,
    cross_val_score
)


from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


from .config import (
    CATBOOST_PARAMS,
    TEST_SIZE,
    RANDOM_STATE,
    MODEL_PATH
)



class PelletAI:


    def __init__(self):

        self.modelo = None

        self.metrics = {}

        self.X_train = None
        self.X_test = None

        self.y_train = None
        self.y_test = None



    # ========================================================
    # ENTRENAMIENTO
    # ========================================================

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



    # ========================================================
    # EVALUACIÓN
    # ========================================================

    def evaluate(self):

        """
        Calcula métricas del modelo
        """


        if self.modelo is None:

            raise Exception(
                "El modelo no ha sido entrenado."
            )


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



    # ========================================================
    # VALIDACIÓN CRUZADA
    # ========================================================

    def cross_validate(self, X, y):

        """
        Validación cruzada del modelo
        """


        modelo_cv = CatBoostRegressor(

            **CATBOOST_PARAMS

        )


        cv = RepeatedKFold(

            n_splits=5,

            n_repeats=2,

            random_state=RANDOM_STATE

        )


        scores = cross_val_score(

            modelo_cv,

            X,

            y,

            cv=cv,

            scoring="r2"

        )


        resultado = {

            "scores": scores,

            "mean_r2": scores.mean(),

            "std_r2": scores.std()

        }


        return resultado



    # ========================================================
    # IMPORTANCIA DE VARIABLES
    # ========================================================

    def feature_importance(self, X):

        """
        Calcula importancia de variables
        según CatBoost
        """


        importancia = pd.DataFrame({

            "Variable": X.columns,

            "Importancia": self.modelo.feature_importances_

        })


        importancia = importancia.sort_values(

            "Importancia",

            ascending=False

        )


        return importancia



    # ========================================================
    # EXPLICABILIDAD SHAP
    # ========================================================

    def explain(self, X):

        """
        Genera valores SHAP
        """


        if self.modelo is None:

            raise Exception(
                "El modelo no ha sido entrenado."
            )


        explainer = shap.Explainer(

            self.modelo,

            self.X_train

        )


        shap_values = explainer(

            X

        )


        return shap_values



    # ========================================================
    # PREDICCIÓN
    # ========================================================

    def predict(self, X):

        """
        Predice nuevas formulaciones
        """


        if self.modelo is None:

            raise Exception(

                "El modelo no ha sido entrenado."

            )


        return self.modelo.predict(X)



    # ========================================================
    # GUARDAR MODELO
    # ========================================================

    def save(self, X):

        """
        Guarda modelo entrenado,
        variables utilizadas y metadata
        """


        if self.modelo is None:

            raise Exception(

                "No existe un modelo entrenado."

            )


        if not self.metrics:

            self.evaluate()



        MODEL_PATH.mkdir(

            exist_ok=True

        )



        # -----------------------------
        # Guardar modelo CatBoost
        # -----------------------------


        self.modelo.save_model(

            str(

                MODEL_PATH / "modelo_actual.cbm"

            )

        )



        # -----------------------------
        # Guardar variables
        # -----------------------------


        with open(

            str(

                MODEL_PATH / "variables.pkl"

            ),

            "wb"

        ) as f:


            pickle.dump(

                list(X.columns),

                f

            )



        # -----------------------------
        # Metadata
        # -----------------------------


        metadata = {


            "fecha_entrenamiento":

                datetime.now().strftime(

                    "%Y-%m-%d %H:%M"

                ),


            "n_registros":

                len(X),


            "n_variables":

                len(X.columns),


            "MAE":

                float(self.metrics["MAE"]),


            "RMSE":

                float(self.metrics["RMSE"]),


            "R2":

                float(self.metrics["R2"])

        }



        with open(

            str(

                MODEL_PATH / "metadata.json"

            ),

            "w"

        ) as f:


            json.dump(

                metadata,

                f,

                indent=4

            )



        return metadata

    # ========================================================
    # CARGAR MODELO
    # ========================================================

    def load(self):

        """
        Carga un modelo CatBoost previamente guardado
        """

        ruta_modelo = MODEL_PATH / "modelo_actual.cbm"


        if not ruta_modelo.exists():

            raise FileNotFoundError(
                "No existe un modelo guardado."
            )


        self.modelo = CatBoostRegressor()


        self.modelo.load_model(

            str(ruta_modelo)

        )


        return self.modelo
