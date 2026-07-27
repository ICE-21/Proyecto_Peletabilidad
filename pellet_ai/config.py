"""
Configuración general del proyecto PelletAI
"""

from pathlib import Path


# ============================================================
# RUTAS
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = ROOT / "datos"

MODEL_PATH = ROOT / "modelos"

VERSION_PATH = MODEL_PATH / "versiones"

LOG_PATH = ROOT / "logs"


# ============================================================
# DATOS DEL PROYECTO
# ============================================================

# Variable objetivo del modelo

TARGET = "%Alimentador"


# Familias de productos a analizar
# Equivalente a:
# familias = ["T"] en el notebook original

FAMILIAS = ["T"]


# Rango de Batch utilizado en el entrenamiento

BATCH_MIN = 11

BATCH_MAX = 101



# ============================================================
# COLUMNAS DEL DATASET
# ============================================================

# Columnas que no entran al modelo

DROP_COLUMNS = [

    # Variables identificadoras
    "Codigo",
    "Batch",

    # Ingredientes excluidos del modelo
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
# ENTRENAMIENTO
# ============================================================

RANDOM_STATE = 42

TEST_SIZE = 0.20



# ============================================================
# CATBOOST
# ============================================================

CATBOOST_PARAMS = {

    "iterations":300,

    "learning_rate":0.05,

    "depth":4,

    "l2_leaf_reg":10,

    "border_count":64,

    "loss_function":"RMSE",

    "verbose":False,

    "random_seed":RANDOM_STATE

}
