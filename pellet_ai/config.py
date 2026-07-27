"""
Configuración general del proyecto
"""

from pathlib import Path

#====================================================
# CARPETAS DEL PROYECTO
#====================================================

ROOT = Path(__file__).resolve().parent.parent

DATOS = ROOT / "datos"

MODELOS = ROOT / "modelos"

LOGS = ROOT / "logs"

#====================================================
# MODELO
#====================================================

RANDOM_STATE = 42

TEST_SIZE = 0.20

TARGET = "%Alimentador"

FAMILIAS = ["T3"]

#====================================================
# CATBOOST
#====================================================

CATBOOST_PARAMS = {

    "iterations":800,

    "learning_rate":0.01,

    "depth":5,

    "l2_leaf_reg":1,

    "border_count":128,

    "loss_function":"RMSE",

    "verbose":False,

    "random_seed":RANDOM_STATE

}
