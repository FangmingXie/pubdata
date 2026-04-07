import os
import scanpy as sc

# --- file paths ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(PROJECT_ROOT, 'local_data', 'morcom26_cux2mice')
IN_FILE = os.path.join(DATA_DIR, 'P26_ENs.h5ad')
OUT_FILE = os.path.join(DATA_DIR, 'README.txt')

# --- load obs only ---
obs = sc.read_h5ad(IN_FILE, backed='r').obs
print(f'Cells: {len(obs)}')
print(f'Obs columns: {list(obs.columns)}')

# --- identify relevant columns ---
subclass_col = next((c for c in obs.columns if 'subclass' in c.lower()), None)
celltype_col = next((c for c in obs.columns if c.lower() == 'celltype'), None) or \
               next((c for c in obs.columns if 'celltype' in c.lower() or 'cell_type' in c.lower()), None)
age_col = next((c for c in obs.columns if 'age' in c.lower()), None)
condition_col = next((c for c in obs.columns if 'condition' in c.lower()), None)

print(f'\nSubclass column: {subclass_col}')
print(f'Celltype column: {celltype_col}')
print(f'Age column: {age_col}')
print(f'Condition column: {condition_col}')

lines = []
lines.append(f'Dataset: P26_ENs.h5ad')
lines.append(f'Cells: {len(obs)}')
lines.append(f'Obs columns: {list(obs.columns)}')
lines.append('')

for label, col in [('cell types (celltype)', celltype_col), ('subclasses (subclass)', subclass_col)]:
    if col:
        counts = obs[col].value_counts().sort_index()
        lines.append(f'Unique {label}: {len(counts)}')
        for ct, n in counts.items():
            lines.append(f'  {ct}: {n}')
        lines.append('')

if age_col:
    counts = obs[age_col].value_counts().sort_index()
    lines.append(f'Unique developmental ages ({age_col}): {len(counts)}')
    for age, n in counts.items():
        lines.append(f'  {age}: {n}')
    lines.append('')
else:
    lines.append('No age column found.')
    lines.append('')

if condition_col:
    counts = obs[condition_col].value_counts().sort_index()
    lines.append(f'Conditions ({condition_col}): {len(counts)}')
    for cond, n in counts.items():
        lines.append(f'  {cond}: {n}')

# --- write results ---
with open(OUT_FILE, 'w') as f:
    f.write('\n'.join(lines) + '\n')
print(f'\nSaved {OUT_FILE}')
