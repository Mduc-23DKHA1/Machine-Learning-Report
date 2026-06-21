"""
%run ../setup.py : Chạy file setup.py để thêm root directory vào sys.path
%load_ext autoreload : Tự động load lại thư viện khi code thay đổi
%autoreload 2 : Bật chế độ reload tất cả module khi có sự thay đổi 
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

