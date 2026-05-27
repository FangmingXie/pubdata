import os
import scipy.io
import pandas as pd
import anndata as ad

# --- file paths ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR     = os.path.join(PROJECT_ROOT, 'local_data', 'wei22_macaque_v1')
MTX_FILE     = os.path.join(DATA_DIR, 'FM_V1_133454.mtx')
BARCODE_CSV  = os.path.join(DATA_DIR, 'FM_V1_133454_barcode.csv')
GENE_CSV     = os.path.join(DATA_DIR, 'FM_V1_133454_gene.csv')
OUT_FILE     = os.path.join(DATA_DIR, 'wei22_Exc_L13.h5ad')

CELL_LABEL_PREFIX = 'Exc L1-3'

# --- load ---
print('Loading MTX...')
X = scipy.io.mmread(MTX_FILE).tocsr()  # cells x genes (133454 x 18297)

obs = pd.read_csv(BARCODE_CSV, index_col=0)
var = pd.read_csv(GENE_CSV, index_col=0)

print(f'Full matrix: {X.shape[0]:,} cells x {X.shape[1]:,} genes')

# --- subset ---
mask = obs['cell_label'].str.startswith(CELL_LABEL_PREFIX)
cell_idx = obs.index[mask]
idx = obs.index.get_indexer(cell_idx)

adata = ad.AnnData(X=X[idx], obs=obs.loc[cell_idx].copy(), var=var.copy())
print(f'Subset ({CELL_LABEL_PREFIX!r}): {adata}')
print(adata.obs['cell_label'].value_counts().to_string())

# --- save ---
adata.write_h5ad(OUT_FILE)
print(f'Saved {OUT_FILE}')
