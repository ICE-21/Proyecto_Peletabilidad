"""
Analizador de retroalimentación PelletAI.

Evalúa el desempeño del modelo
con resultados reales de producción.
"""


import pandas as pd

from .config import DATA_PATH



class FeedbackAnalyzer:


    def __init__(self):

        self.archivo = (
            DATA_PATH /
            "feedback.xlsx"
        )

        self.df = None



    # ========================================================
    # CARGAR DATOS
    # ========================================================

    def cargar(self):


        if not self.archivo.exists():

            raise FileNotFoundError(

                "No existe feedback.xlsx"

            )


        self.df = pd.read_excel(

            self.archivo

        )


        return self.df





    # ========================================================
    # RESUMEN GENERAL
    # ========================================================

    def resumen(self):


        if self.df is None:

            self.cargar()



        if self.df.empty:


            return {

                "lotes_registrados": 0,

                "error_promedio": 0,

                "error_abs_promedio": 0,

                "error_maximo": 0,

                "error_minimo": 0

            }



        return {


            "lotes_registrados":

                len(self.df),



            "error_promedio":

                self.df["Error"].mean(),



            "error_abs_promedio":

                self.df["Error"]
                .abs()
                .mean(),



            "error_maximo":

                self.df["Error"].max(),



            "error_minimo":

                self.df["Error"].min()


        }





    # ========================================================
    # SESGO DEL MODELO
    # ========================================================

    def sesgo(self):


        if self.df is None:

            self.cargar()



        if self.df.empty:


            return {

                "bias": 0,

                "interpretacion":

                    "No existen datos suficientes."

            }



        promedio = (

            self.df["Error"]
            .mean()

        )



        if promedio > 0:


            mensaje = (

                f"El modelo subestima "
                f"{promedio:.2f}% en promedio."

            )


        else:


            mensaje = (

                f"El modelo sobreestima "
                f"{abs(promedio):.2f}% en promedio."

            )



        return {


            "bias": promedio,


            "interpretacion": mensaje


        }


    # ========================================================
    # DECISIÓN DE REENTRENAMIENTO
    # ========================================================

    def necesita_reentrenamiento(

        self,

        minimo_lotes=50,

        max_error=5

    ):


        datos = self.resumen()



        return (

            datos["lotes_registrados"]

            >=

            minimo_lotes


            and


            datos["error_abs_promedio"]

            >

            max_error

        )
        
    # ========================================================
    # DATOS PARA GRÁFICOS
    # ========================================================

    def datos_graficos(self):


        if self.df is None:

            self.cargar()


        if self.df.empty:

            return pd.DataFrame()



        columnas = [

            "Fecha",

            "Prediccion",

            "Resultado_Real",

            "Error"

        ]


        return self.df[columnas]
    
        # ========================================================
    # EVOLUCIÓN DEL ERROR
    # ========================================================

    def evolucion_error(self):


        if self.df is None:

            self.cargar()


        if self.df.empty:

            return pd.DataFrame()



        datos = self.df.copy()


        datos["Fecha"] = pd.to_datetime(

            datos["Fecha"]

        )


        datos = datos.sort_values(

            by="Fecha"

        )


        datos["Error_Absoluto"] = (

            datos["Error"]
            .abs()

        )


        return datos[
            [
                "Fecha",
                "Error",
                "Error_Absoluto"
            ]
        ]
        
            # ========================================================
    # PRECISIÓN OPERACIONAL
    # ========================================================

    def precision_operacional(

        self,

        tolerancia=5

    ):


        if self.df is None:

            self.cargar()



        if self.df.empty:

            return {

                "total":0,

                "aciertos":0,

                "precision":0

            }



        datos = self.df.copy()



        datos["Error_Abs"] = (

            datos["Error"]
            .abs()

        )



        aciertos = (

            datos["Error_Abs"]

            <=

            tolerancia

        ).sum()



        total = len(datos)



        precision = (

            aciertos / total * 100

        )



        return {


            "total":

                total,


            "aciertos":

                aciertos,


            "precision":

                precision


        }