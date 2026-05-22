import os
import pandas as pd

# --- file paths ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(PROJECT_ROOT, 'local_data', 'hahn23')
IN_FILE = os.path.join(DATA_DIR, 'orig', 'GSE212336_BulkSeq_Counttable.txt.gz')
META_FILE = os.path.join(DATA_DIR, 'hahn23_mouse_metadata.tsv')
OUT_FILE = os.path.join(DATA_DIR, 'hahn23_vis_bulk.parquet')

# --- load data and metadata ---
df = pd.read_csv(IN_FILE, sep='\t', index_col=0)
meta = pd.read_csv(META_FILE, sep='\t', index_col='Mouse_ID')

# --- subset vis samples ---
vis_cols = [c for c in df.columns if '_vis_' in c]
df_vis = df[vis_cols]
print(f'Vis samples: {df_vis.shape[1]}')

# --- rename columns: BulkSeq_vis_[n] -> [age]_[sex]_[n]ID ---
def rename_col(col):
    mouse_id = col.split('_')[-1] + 'ID'
    row = meta.loc[mouse_id]
    return f'{row["Age"]}_{row["Sex"]}_{mouse_id}'

df_vis.columns = [rename_col(c) for c in vis_cols]

# --- sort columns: increasing age, Female before Male, increasing ID ---
age_order = {a: i for i, a in enumerate(sorted(meta['Age'].unique(), key=lambda a: int(a.replace('mo', ''))))}
def col_sort_key(col):
    age, sex, mid = col.split('_')
    return (age_order[age], 0 if sex == 'Female' else 1, int(mid.replace('ID', '')))

df_vis = df_vis[sorted(df_vis.columns, key=col_sort_key)]
print(f'Columns (first 5): {df_vis.columns[:5].tolist()}')

# --- save ---
df_vis.to_parquet(OUT_FILE)
print(f'Saved {OUT_FILE}')
