"""
=========================================================
        Cấu hình hệ thống - Đường dẫn thư mục
=========================================================
"""

from pathlib import Path

# =========================
ROOT_DIR = Path(__file__).resolve().parent.parent
# =========================
DATA_DIR = ROOT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
# =========================
MODEL_DIR = ROOT_DIR / "model"
SRC_DIR = ROOT_DIR / "src"
# =========================
JUPYTER_DIR = ROOT_DIR / "notebooks"