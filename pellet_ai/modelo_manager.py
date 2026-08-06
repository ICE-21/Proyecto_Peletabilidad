"""
Administrador de modelos PelletAI.

Controla versiones,
metadatos y modelo activo.
"""


from pathlib import Path

import json

import shutil

from datetime import datetime


from .config import DATA_PATH





class ModeloManager:


    def __init__(self):


        self.carpeta_modelos = (

            DATA_PATH.parent /

            "modelos"

        )


        self.modelo_actual = (

            self.carpeta_modelos /

            "modelo_actual.cbm"

        )


        self.metadata = (

            self.carpeta_modelos /

            "metadata.json"

        )


        self.versiones = (

            self.carpeta_modelos /

            "versiones"

        )


        self.versiones.mkdir(

            exist_ok=True

        )





    # ======================================================
    # CREAR VERSION DE MODELO
    # ======================================================

    def guardar_version(

        self,

        nuevo_modelo,

        metricas

    ):


        fecha = (

            datetime.now()

            .strftime("%Y%m%d_%H%M")

        )


        nombre = (

            f"modelo_{fecha}.cbm"

        )


        destino = (

            self.versiones /

            nombre

        )


        shutil.copy(

            nuevo_modelo,

            destino

        )


        return destino





    # ======================================================
    # ACTUALIZAR MODELO ACTUAL
    # ======================================================

    def activar_modelo(
        self,
        modelo_nuevo,
        metricas=None,
        origen="manual"
    ):


        shutil.copy(

            modelo_nuevo,

            self.modelo_actual

        )


        if metricas:


            self.actualizar_metadata(

                metricas,

                origen

            )


        return True





    # ======================================================
    # LEER METADATA
    # ======================================================

    def cargar_metadata(self):


        if not self.metadata.exists():

            return {}


        with open(

            self.metadata,

            "r",

            encoding="utf-8"

        ) as archivo:


            return json.load(archivo)
        
    # ======================================================
    # ACTUALIZAR METADATA
    # ======================================================

    def actualizar_metadata(
        self,
        metricas,
        origen="manual"
    ):


        datos = {


            "modelo_activo":

                "CatBoost",



            "fecha_actualizacion":

                datetime.now()
                .strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),



            "origen":

                origen,



            "metricas":{


                "MAE":

                    metricas.get(
                        "MAE",
                        None
                    ),



                "RMSE":

                    metricas.get(
                        "RMSE",
                        None
                    ),



                "R2":

                    metricas.get(
                        "R2",
                        None
                    )

            }


        }



        with open(

            self.metadata,

            "w",

            encoding="utf-8"

        ) as archivo:


            json.dump(

                datos,

                archivo,

                indent=4

            )



        return datos
    
    
    # ======================================================
    # INFORMACIÓN DEL MODELO ACTUAL
    # ======================================================

    def estado_modelo(self):


        existe = self.modelo_actual.exists()


        metadata = self.cargar_metadata()



        # Compatibilidad con versiones anteriores
        if metadata:


            if "metricas" not in metadata:


                metadata["metricas"] = {


                    "MAE":

                        metadata.get(
                            "MAE",
                            None
                        ),


                    "RMSE":

                        metadata.get(
                            "RMSE",
                            None
                        ),


                    "R2":

                        metadata.get(
                            "R2",
                            None
                        )

                }



        return {


            "existe":

                existe,


            "archivo":

                self.modelo_actual.name,


            "metadata":

                metadata


        }