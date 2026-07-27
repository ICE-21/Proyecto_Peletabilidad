"""
Módulo encargado de leer y validar datos
"""

import pandas as pd

from .config import DATA_PATH


class DataManager:

    def __init__(self):

        self.df = None


    def load_excel(self, filename="lotes_peletizado.xlsx"):

        """
        Carga un archivo Excel desde la carpeta datos
        """

        path = DATA_PATH / filename

        self.df = pd.read_excel(path)

        return self.df


    def info(self):

        """
        Información general del dataframe
        """

        return self.df.info()


    def describe(self):

        """
        Estadísticas descriptivas
        """

        return self.df.describe()


    def null_values(self):

        """
        Conteo de valores nulos por columna
        """

        return self.df.isnull().sum()


    def duplicated(self):

        """
        Número de registros duplicados
        """

        return self.df.duplicated().sum()
