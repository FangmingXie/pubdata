import os
import scanpy as sc

# --- file paths ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(PROJECT_ROOT, 'local_data', 'gao25')
IN_FILE = os.path.join(DATA_DIR, 'DevVIS_scRNA_processed.h5ad')
OUT_FILE = os.path.join(DATA_DIR, 'astrocyte_counts_per_age.txt')

ASTRO_LABEL = 'Astro-TE NN'
SUBCLASS_COL = 'subclass_label'
AGE_COL = 'Age'

# --- load obs only ---
obs = sc.read_h5ad(IN_FILE, backed='r').obs

# --- filter astrocytes ---
astro = obs[obs[SUBCLASS_COL] == ASTRO_LABEL]
counts = astro[AGE_COL].value_counts().sort_index()

# --- write results ---
lines = [
    f'Dataset: DevVIS_scRNA_processed.h5ad',
    f'Astrocyte cell type: {ASTRO_LABEL}',
    f'Total astrocytes: {len(astro)}',
    '',
    f'Astrocyte counts per age ({AGE_COL}):',
]
for age, n in counts.items():
    lines.append(f'  {age}: {n}')

with open(OUT_FILE, 'w') as f:
    f.write('\n'.join(lines) + '\n')
print(f'Saved {OUT_FILE}')
