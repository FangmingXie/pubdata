import os
import pandas as pd
import anndata as ad
import scipy.sparse as sp

# --- file paths ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(PROJECT_ROOT, 'local_data', 'tran19_retina')
IN_FILE = os.path.join(DATA_DIR, 'GSE133382_AtlasRGCs_CountMatrix.csv.gz')
OUT_FILE = os.path.join(DATA_DIR, 'tran19_retina.h5ad')

# --- load count matrix (genes x cells) ---
print('Loading count matrix...')
df = pd.read_csv(IN_FILE, index_col=0)
print(f'Loaded: {df.shape[0]} genes x {df.shape[1]} cells')

# --- build AnnData (cells x genes) ---
X = sp.csr_matrix(df.values.T)

adata = ad.AnnData(X=X)
adata.obs_names = pd.Index(df.columns)
adata.var_names = pd.Index(df.index)
adata.obs['subtype'] = [c.split('_')[0] for c in df.columns]

print(f'AnnData: {adata}')
print(f'Subtypes:\n{adata.obs["subtype"].value_counts().sort_index()}')

# --- save ---
adata.write_h5ad(OUT_FILE)
print(f'Saved {OUT_FILE}')
