import os
import scanpy as sc

# --- file paths ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(PROJECT_ROOT, 'local_data', 'gao25')
IN_FILE = os.path.join(DATA_DIR, 'DevVIS_scRNA_processed.h5ad')
OUT_FILE = os.path.join(DATA_DIR, 'README.txt')

# --- load obs only ---
obs = sc.read_h5ad(IN_FILE, backed='r').obs
print(f'Cells: {len(obs)}')
print(f'Obs columns: {list(obs.columns)}')

# --- identify subclass and age columns ---
subclass_col = next((c for c in obs.columns if 'subclass' in c.lower()), None)
age_col = next((c for c in obs.columns if 'age' in c.lower()), None)

print(f'\nSubclass column: {subclass_col}')
print(f'Age column: {age_col}')

lines = []
lines.append(f'Dataset: DevVIS_scRNA_processed.h5ad')
lines.append(f'Cells: {len(obs)}')
lines.append(f'Obs columns: {list(obs.columns)}')
lines.append('')

if subclass_col:
    counts = obs[subclass_col].value_counts().sort_index()
    lines.append(f'Unique cell types ({subclass_col}): {len(counts)}')
    for ct, n in counts.items():
        lines.append(f'  {ct}: {n}')
else:
    lines.append('No subclass column found.')
lines.append('')

if age_col:
    counts = obs[age_col].value_counts().sort_index()
    lines.append(f'Unique developmental ages ({age_col}): {len(counts)}')
    for age, n in counts.items():
        lines.append(f'  {age}: {n}')
else:
    lines.append('No age column found.')

# --- write results ---
with open(OUT_FILE, 'w') as f:
    f.write('\n'.join(lines) + '\n')
print(f'\nSaved {OUT_FILE}')
