"""
Configuración general del proyecto PelletAI
"""

from pathlib import Path


# ============================================================
# RUTAS DEL PROYECTO
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = ROOT / "datos"

MODEL_PATH = ROOT / "modelos"

VERSION_PATH = MODEL_PATH / "versiones"

LOG_PATH = ROOT / "logs"


# ============================================================
# ARCHIVOS DEL MODELO
# ============================================================

MODELO_ACTUAL = (
    MODEL_PATH /
    "modelo_actual.cbm"
)

MODELO_CANDIDATO = (
    MODEL_PATH /
    "modelo_candidato.cbm"
)


# ============================================================
# DATOS DEL PROYECTO
# ============================================================

# Variable objetivo

TARGET = "%Alimentador"


# Familias de productos utilizadas

FAMILIAS = ["T"]


# Rango de Batch utilizado

BATCH_MIN = 11

BATCH_MAX = 101


# ============================================================
# COLUMNAS EXCLUIDAS DEL MODELO
# ============================================================

DROP_COLUMNS = [

    # Identificación
    "Codigo",
    "Batch",

    # Ingredientes descartados
    "M82076IB",
    "M80822IA",
    "M80710IB",
    "M80032NB",
    "M70202IB",
    "M60013NB",
    "M60000NA",
    "M51012NB",
    "M51003IB",
    "M50805MB",
    "M50802MB",
    "M50701NA",
    "M50536MB",
    "M50534MB",
    "M50523MAT",
    "M50522MA",
    "M50504MA",
    "M50231LB",
    "M50113MB",
    "M50009MB",
    "M40715NB",
    "M40662MB",
    "M40602IA",
    "M40141LA",
    "M40031LA",
    "M40002QA",
    "M10302MA",
    "M10301MA",
    "M080006"

]


# ============================================================
# PARÁMETROS DE ENTRENAMIENTO
# ============================================================

RANDOM_STATE = 42

TEST_SIZE = 0.20


# ============================================================
# PARÁMETROS CATBOOST
# ============================================================

CATBOOST_PARAMS = {

    "iterations": 300,

    "learning_rate": 0.05,

    "depth": 4,

    "l2_leaf_reg": 10,

    "border_count": 64,

    "loss_function": "RMSE",

    "verbose": False,

    "random_seed": RANDOM_STATE

}


# ============================================================
# REGLAS DE SELECCIÓN DEL MODELO
# ============================================================

MODEL_SELECTION = {

    # --------------------------------------------------------
    # Cantidad mínima de feedbacks
    # antes de permitir un reentrenamiento
    # --------------------------------------------------------

    "MIN_FEEDBACK": 30,


    # --------------------------------------------------------
    # Mejora mínima requerida
    # (% respecto al modelo actual)
    # --------------------------------------------------------

    "MIN_MAE_IMPROVEMENT": 1.5,

    "MIN_RMSE_IMPROVEMENT": 1.5,


    # --------------------------------------------------------
    # Incremento mínimo aceptado
    # del coeficiente R²
    # --------------------------------------------------------

    "MIN_R2_IMPROVEMENT": 0.01,


    # --------------------------------------------------------
    # Puntaje mínimo para aceptar
    # un nuevo modelo
    # (0 - 100)
    # --------------------------------------------------------

    "MIN_GLOBAL_SCORE": 70,


    # --------------------------------------------------------
    # Ponderación de métricas
    # La suma debe ser 100
    # --------------------------------------------------------

    "WEIGHTS": {

        "MAE": 45,

        "RMSE": 30,

        "R2": 25

    }

}


# ============================================================
# VERSIONADO DE MODELOS
# ============================================================

# Cantidad máxima de modelos históricos
# que se conservarán automáticamente.

MAX_VERSION_HISTORY = 50