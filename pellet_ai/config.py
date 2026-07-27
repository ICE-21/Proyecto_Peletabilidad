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

LOG_PATH = ROOT / "logs"

# ============================================================
# MODELO
# ============================================================

TARGET = "%Alimentador"

FAMILIAS = ["T3"]

RANDOM_STATE = 42

TEST_SIZE = 0.20

# ============================================================
# CATBOOST
# ============================================================

CATBOOST_PARAMS = {

    "iterations":800,

    "learning_rate":0.01,

    "depth":5,

    "l2_leaf_reg":1,

    "border_count":128,

    "loss_function":"RMSE",

    "verbose":False,

    "random_seed":42

}
