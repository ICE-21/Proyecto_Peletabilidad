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
    MODEL_PATH,
    VERSION_PATH
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

    # ========================================================
    # PREPARAR FÓRMULA
    # ========================================================

    def prepare_formula(self, formula):

        """
        Prepara una formulación para que tenga exactamente
        las mismas variables utilizadas durante el entrenamiento.
        """

        if not isinstance(formula, pd.DataFrame):

            raise TypeError(
                "La fórmula debe ser un DataFrame de pandas."
            )


        ruta_variables = MODEL_PATH / "variables.pkl"


        if not ruta_variables.exists():

            raise FileNotFoundError(
                "No existe variables.pkl. Debe entrenar o cargar un modelo."
            )


        with open(
            ruta_variables,
            "rb"
        ) as f:

            variables = pickle.load(f)


        formula = formula.reindex(

            columns=variables,

            fill_value=0

        )


        return formula

    # ========================================================
    # SHAP DE UNA FORMULACIÓN
    # ========================================================

    def _formula_shap(self, formula):

        """
        Calcula los valores SHAP para una formulación.
        """

        explainer = shap.Explainer(

            self.modelo,

            self.X_train

        )

        shap_values = explainer(

            formula

        )

        return shap_values

    # ========================================================
    # TOP VARIABLES SHAP
    # ========================================================

    def _top_shap(self, formula, top=5):

        """
        Obtiene las variables con mayor impacto SHAP.
        """

        shap_values = self._formula_shap(formula)

        explicacion = pd.DataFrame({

            "Ingrediente": formula.columns,

            "Impacto": shap_values.values[0]

        })

        explicacion["Impacto_abs"] = (
            explicacion["Impacto"].abs()
        )

        explicacion = explicacion.sort_values(

            "Impacto_abs",

            ascending=False

        )

        positivos = explicacion[
            explicacion["Impacto"] > 0
        ].head(top)

        negativos = explicacion[
            explicacion["Impacto"] < 0
        ].head(top)

        return positivos, negativos
        

    # ========================================================
    # PREDICCIÓN DE FORMULACIÓN
    # ========================================================

    def predict_formula(self, formula):

        """
        Predice el % Alimentador de una nueva formulación.
        """

        if self.modelo is None:

            raise Exception(
                "Debe cargar o entrenar un modelo antes de predecir."
            )


        # Preparar fórmula
        formula = self.prepare_formula(formula)


        # Predicción
        prediccion = self.modelo.predict(formula)


        return float(prediccion[0])

    # ========================================================
    # SEMÁFORO DE PELETABILIDAD
    # ========================================================

    def semaforo(self, valor):

        """
        Clasifica el % Alimentador esperado.
        """

        if valor >= 60:

            return "🟢 Excelente"

        elif valor >= 55:

            return "🟡 Bueno"

        elif valor >= 50:

            return "🟠 Riesgo moderado"

        else:

            return "🔴 Bajo rendimiento"

    # ========================================================
    # REPORTE COMPLETO DE PREDICCIÓN
    # ========================================================

    def predict_report(self, formula, top=5):

        """
        Genera un reporte completo de una formulación.
        """

        if self.modelo is None:

            raise Exception(
                "Debe cargar o entrenar un modelo."
            )


        # Preparar fórmula
        formula = self.prepare_formula(formula)


        # Predicción
        prediccion = self.predict_formula(formula)


        # Semáforo
        estado = self.semaforo(prediccion)


        # SHAP
        positivos, negativos = self._top_shap(
            formula,
            top=top
        )


        reporte = {

    "prediccion": round(prediccion, 2),

    "semaforo": estado,

    "formula": formula,

    "top_positivos": positivos.to_dict(
        orient="records"
    ),

    "top_negativos": negativos.to_dict(
        orient="records"
    )

    }


        return reporte
        # ========================================================
    # GUARDAR VERSION DEL MODELO
    # ========================================================

    def save_version(self):

        """
        Guarda una copia histórica
        del modelo entrenado.
        """

        if self.modelo is None:

            raise Exception(
                "No existe modelo entrenado."
            )


        VERSION_PATH.mkdir(
            exist_ok=True
        )


        fecha = datetime.now().strftime(
            "%Y%m%d_%H%M"
        )


        nombre = (
            f"modelo_{fecha}.cbm"
        )


        ruta = VERSION_PATH / nombre


        self.modelo.save_model(

            str(ruta)

        )


        return str(ruta)
        # ========================================================
    # PROMOVER MODELO GANADOR
    # ========================================================

    def promote_model(self):

        """
        Copia el modelo ganador
        como modelo_actual.
        """

        if self.modelo is None:

            raise Exception(
                "No existe modelo entrenado."
            )


        destino = (
            MODEL_PATH /
            "modelo_actual.cbm"
        )


        self.modelo.save_model(

            str(destino)

        )


        return str(destino)

