"""
Módulo encargado de leer y preparar datos
"""

import pandas as pd

from .config import (
    DATA_PATH,
    TARGET,
    FAMILIAS,
    BATCH_MIN,
    BATCH_MAX,
    DROP_COLUMNS
)


class DataManager:


    def __init__(self):

        self.df = None



    # ========================================================
    # CARGA DATASET
    # ========================================================

    def load_excel(self, filename="lotes_peletizado.xlsx"):

        path = DATA_PATH / filename

        self.df = pd.read_excel(path)

        return self.df



    # ========================================================
    # LIMPIEZA INICIAL
    # ========================================================

    def clean(self):

        self.df["Codigo"] = (
            self.df["Codigo"]
            .astype(str)
            .str.strip()
        )


        self.df["Batch"] = pd.to_numeric(
            self.df["Batch"],
            errors="coerce"
        )


        return self.df



    # ========================================================
    # FILTRO DE PRODUCTOS
    # ========================================================

    def filter_data(self):


        self.df = self.df[
            (
                self.df["Codigo"]
                .str.startswith(
                    tuple(FAMILIAS),
                    na=False
                )
            )
            &
            (
                self.df["Batch"] >= BATCH_MIN
            )
            &
            (
                self.df["Batch"] <= BATCH_MAX
            )
        ].copy()


        return self.df



    # ========================================================
    # PREPARAR VARIABLES MODELO
    # ========================================================

    def prepare_training_data(self):


        X = self.df.drop(
            columns=[TARGET] + DROP_COLUMNS,
            errors="ignore"
        )


        # eliminar columnas constantes

        constantes = X.columns[
            X.nunique() <= 1
        ]


        if len(constantes) > 0:

            X = X.drop(
                columns=constantes
            )


        y = self.df[TARGET]


        return X, y



    # ========================================================
    # VALIDACIONES BÁSICAS
    # ========================================================

    def describe(self):

        return self.df.describe()



    def null_values(self):

        return self.df.isnull().sum()



    def duplicated(self):

        return self.df.duplicated().sum()
