import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import subset_h5ad

# --- file paths ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(PROJECT_ROOT, 'local_data', 'gao25')
IN_FILE = os.path.join(DATA_DIR, 'DevVIS_scRNA_processed.h5ad')
OUT_FILE = os.path.join(DATA_DIR, 'DevVIS_scRNA_IT_CTX_Glut.h5ad')

subset_h5ad(IN_FILE, OUT_FILE, col='subclass_label', pattern=r'IT CTX Glut')
