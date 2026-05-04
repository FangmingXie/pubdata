import os
import scanpy as sc

# --- file paths ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(PROJECT_ROOT, 'local_data', 'cheng22_yoo25')
IN_FILE = os.path.join(DATA_DIR, 'orig', 'superdupermegaRNA_hasraw.h5ad')
OUT_FILE = os.path.join(DATA_DIR, 'README.txt')

# --- load obs only ---
obs = sc.read_h5ad(IN_FILE, backed='r').obs
print(f'Cells: {len(obs)}')
print(f'Obs columns: {list(obs.columns)}')

# --- identify subclass, condition, and study columns ---
subclass_col = next((c for c in obs.columns if 'subclass' in c.lower()), None)
condition_col = next((c for c in obs.columns if 'condition' in c.lower()), None)
study_col = next((c for c in obs.columns if 'study' in c.lower()), None)

print(f'\nSubclass column: {subclass_col}')
print(f'Condition column: {condition_col}')
print(f'Study column: {study_col}')

lines = []
lines.append('NOTE: CELLS WITH STUDY == NaN ARE TREATED AS "2022 RNA" (P28+ AGES HAVE NO STUDY LABEL).')
lines.append('')
lines.append(f'Dataset: superdupermegaRNA_hasraw.h5ad')
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

if condition_col:
    counts = obs[condition_col].value_counts().sort_index()
    lines.append(f'Unique conditions ({condition_col}): {len(counts)}')
    for cond, n in counts.items():
        lines.append(f'  {cond}: {n}')
else:
    lines.append('No condition column found.')
lines.append('')

if study_col:
    counts = obs[study_col].value_counts().sort_index()
    lines.append(f'Unique studies ({study_col}): {len(counts)}')
    for study, n in counts.items():
        lines.append(f'  {study}: {n}')
else:
    lines.append('No study column found.')

# --- write results ---
with open(OUT_FILE, 'w') as f:
    f.write('\n'.join(lines) + '\n')
print(f'\nSaved {OUT_FILE}')
