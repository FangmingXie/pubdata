import os
import scanpy as sc

# --- file paths ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(PROJECT_ROOT, 'local_data', 'jorstad23_human')
IN_FILE = os.path.join(DATA_DIR, 'orig', 'jorstad23_human_v1.h5ad')
OUT_FILE = os.path.join(DATA_DIR, 'README.txt')

# --- load (backed) ---
adata = sc.read_h5ad(IN_FILE, backed='r')
obs = adata.obs
print(f'Shape: {adata.shape}')
print(f'Obs columns: {list(obs.columns)}')
print(f'Var columns: {list(adata.var.columns)}')
print(f'Uns keys: {list(adata.uns.keys())}')
print(f'Obsm keys: {list(adata.obsm.keys())}')

# --- key columns to report ---
KEY_COLS = [
    'Class',
    'CrossArea_subclass',
    'WithinArea_subclass',
    'Region',
    'Layer',
    'Source',
    'sex',
    'development_stage',
]

lines = []
lines.append('Dataset: jorstad23_human_v1.h5ad')
lines.append(f'Shape: {adata.shape[0]} cells x {adata.shape[1]} genes')
lines.append(f'Obs columns: {list(obs.columns)}')
lines.append('')

for col in KEY_COLS:
    counts = obs[col].value_counts().sort_index()
    lines.append(f'Unique {col}: {len(counts)}')
    for val, n in counts.items():
        lines.append(f'  {val}: {n}')
    lines.append('')

with open(OUT_FILE, 'w') as f:
    f.write('\n'.join(lines) + '\n')
print(f'\nSaved {OUT_FILE}')
