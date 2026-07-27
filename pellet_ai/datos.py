import pandas as pd


class GestorDatos:

    def __init__(self):

        self.df = None

    def cargar_excel(self, ruta):

        self.df = pd.read_excel(ruta)

        print("="*50)
        print("Datos cargados correctamente")
        print("="*50)
        print("Registros :", len(self.df))
        print("Columnas :", len(self.df.columns))

        return self.df

      def informacion(self):

        print(self.df.info())

        return self.df.describe()

    def valores_nulos(self):

        return self.df.isnull().sum()

    def duplicados(self):

        return self.df.duplicated().sum()
