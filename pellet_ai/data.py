"""
Módulo encargado de leer y validar datos
"""

import pandas as pd


class DataManager:

    def __init__(self):

        self.df = None

    def load_excel(self, path):

        self.df = pd.read_excel(path)

        return self.df

    def info(self):

        return self.df.info()

    def describe(self):

        return self.df.describe()

    def null_values(self):

        return self.df.isnull().sum()

    def duplicated(self):

        return self.df.duplicated().sum()
