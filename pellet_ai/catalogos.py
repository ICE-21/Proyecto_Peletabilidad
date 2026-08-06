import pandas as pd

from .config import DATA_PATH


class Catalogos:

    """
    Maneja todos los catálogos
    utilizados por PelletAI.
    """

    def __init__(self):

        self.ruta = DATA_PATH / "catalogos"


    # ==============================================
    # INGREDIENTES
    # ==============================================

    def ingredientes(self):

        archivo = self.ruta / "ingredientes.xlsx"

        return pd.read_excel(archivo)


    # ==============================================
    # SOLO VARIABLES DEL MODELO
    # ==============================================

    def ingredientes_modelo(self, variables):

        ingredientes = self.ingredientes()

        ingredientes = ingredientes[
            ingredientes["Codigo"].isin(variables)
        ]

        ingredientes = ingredientes.copy()

        ingredientes["Valor"] = 0.0

        ingredientes = ingredientes[
            [
                "Nombre",
                "Valor",
                "Codigo"
            ]
        ]

        return ingredientes
        # ==============================================
    # BUSCAR NOMBRE POR CODIGO
    # ==============================================

    def nombre(self, codigo):

        ingredientes = self.ingredientes()


        resultado = ingredientes[
            ingredientes["Codigo"] == codigo
        ]


        if len(resultado) > 0:

            return resultado.iloc[0]["Nombre"]


        return codigo