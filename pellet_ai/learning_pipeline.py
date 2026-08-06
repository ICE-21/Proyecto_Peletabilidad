"""
Pipeline de aprendizaje continuo PelletAI.

Coordina:

Feedback
    ↓
Entrenamiento candidato
    ↓
Comparación modelos
    ↓
Registro histórico
    ↓
Aceptación/Rechazo
    ↓
Actualización modelo activo
"""


from datetime import datetime


from .feedback import FeedbackManager

from .trainer import Trainer

from .model_compare import ModelComparator

from .model_registry import ModelRegistry

from .modelo_manager import ModeloManager

from .config import MODEL_SELECTION




class LearningPipeline:



    def __init__(self):


        self.feedback = FeedbackManager()

        self.trainer = Trainer()

        self.comparator = ModelComparator()

        self.registry = ModelRegistry()

        self.manager = ModeloManager()




    # =====================================================
    # CONTAR FEEDBACK
    # =====================================================

    def cantidad_feedback(self):


        datos = self.feedback.cargar()


        return len(datos)





    # =====================================================
    # EJECUTAR CICLO COMPLETO
    # =====================================================

    def ejecutar(self):


        cantidad = self.cantidad_feedback()



        # =================================================
        # VALIDAR DATOS
        # =================================================


        if cantidad < MODEL_SELECTION["MIN_FEEDBACK"]:


            return {


                "estado":

                    "ESPERANDO_DATOS",



                "feedback_actual":

                    cantidad,



                "feedback_necesario":

                    MODEL_SELECTION["MIN_FEEDBACK"],



                "mensaje":

                    "No existen suficientes resultados reales."

            }





        try:



            # =================================================
            # ENTRENAR MODELO CANDIDATO
            # =================================================


            modelo, metricas_entrenamiento = (

                self.trainer.entrenar()

            )





            # =================================================
            # COMPARAR MODELOS
            # =================================================


            resultado = (

                self.comparator.decidir()

            )



            decision = resultado["decision"]





            # =================================================
            # REGISTRAR EVALUACIÓN
            # =================================================


            self.registry.registrar(

                metricas=resultado["metricas"],

                decision=decision,

                score=resultado["score"],

                motivo=resultado["motivo"],

                registros=cantidad

            )





            # =================================================
            # ACEPTAR MODELO
            # =================================================


            if decision == "ACEPTAR":



                respaldo = (

                    self.registry.activar_candidato()

                )



                self.manager.actualizar_metadata(

                    resultado["metricas"]["nuevo"],

                    origen="aprendizaje_continuo"

                )



                return {


                    "estado":

                        "MODELO_ACTUALIZADO",



                    "fecha":

                        datetime.now(),



                    "respaldo":

                        str(respaldo),



                    "comparacion":

                        resultado

                }





            # =================================================
            # RECHAZAR MODELO
            # =================================================


            return {


                "estado":

                    "MODELO_MANTENIDO",



                "fecha":

                    datetime.now(),



                "comparacion":

                    resultado

            }





        except Exception as error:



            return {


                "estado":

                    "ERROR_PIPELINE",



                "mensaje":

                    str(error)

            }