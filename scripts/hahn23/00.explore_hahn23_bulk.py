import os
import pandas as pd

# --- file paths ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(PROJECT_ROOT, 'local_data', 'hahn23')
IN_FILE = os.path.join(DATA_DIR, 'orig', 'GSE212336_BulkSeq_Counttable.txt.gz')
OUT_FILE = os.path.join(DATA_DIR, 'readme.txt')

# --- load count table ---
df = pd.read_csv(IN_FILE, sep='\t', index_col=0)
n_genes, n_samples = df.shape
print(f'Genes: {n_genes}')
print(f'Samples: {n_samples}')
print(f'Columns (first 5): {df.columns[:5].tolist()}')

# --- parse tissue from sample names: BulkSeq_[tissue]_[rep] ---
tissues = pd.Series([col.split('_')[1] for col in df.columns], name='tissue')
tissue_counts = tissues.value_counts().sort_index()

lines = []
lines.append(f'Dataset: GSE212336_BulkSeq_Counttable.txt.gz')
lines.append(f'Genes: {n_genes}')
lines.append(f'Samples: {n_samples}')
lines.append('')
lines.append(f'Unique tissues: {len(tissue_counts)}')
for tissue, n in tissue_counts.items():
    lines.append(f'  {tissue}: {n}')
lines.append('')
lines.append('All samples:')
for col in df.columns:
    lines.append(f'  {col}')

# --- write results ---
with open(OUT_FILE, 'w') as f:
    f.write('\n'.join(lines) + '\n')
print(f'\nSaved {OUT_FILE}')
