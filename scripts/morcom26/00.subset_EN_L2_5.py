import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import subset_h5ad

# --- file paths ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(PROJECT_ROOT, 'local_data', 'morcom26_cux2mice')
IN_FILE = os.path.join(DATA_DIR, 'P26_ENs.h5ad')
OUT_FILE = os.path.join(DATA_DIR, 'P26_EN-L2-3-CTX_EN-L4-5-CTX_EN-L2-mix.h5ad')

CELL_TYPES = ['EN-L2-3-CTX', 'EN-L4-5-CTX', 'EN-L2-mix']

subset_h5ad(IN_FILE, OUT_FILE, col='celltype', values=CELL_TYPES)
