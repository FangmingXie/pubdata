import os
import scanpy as sc

# --- file paths ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(PROJECT_ROOT, 'local_data', 'jorstad23_human')
IN_FILE = os.path.join(DATA_DIR, 'orig', 'jorstad23_human_v1.h5ad')
OUT_FILE = os.path.join(DATA_DIR, 'jorstad23_human_WithinArea_L23IT.h5ad')

adata = sc.read_h5ad(IN_FILE, backed='r')
print(f'Loaded (backed): {adata}')

mask = (
    (adata.obs['WithinArea_subclass'] == 'L2/3 IT') &
    (adata.obs['Source'] != 'lein_10x_layer5_only')
)
adata_sub = adata[mask].to_memory()
print(f'Subset (WithinArea_subclass==L2/3 IT, Source!=lein_10x_layer5_only): {adata_sub}')

adata_sub.write_h5ad(OUT_FILE)
print(f'Saved {OUT_FILE}')
