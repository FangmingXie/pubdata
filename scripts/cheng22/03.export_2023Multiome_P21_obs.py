import os
import scanpy as sc

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(PROJECT_ROOT, 'local_data', 'cheng22_yoo25')
IN_FILE = os.path.join(DATA_DIR, 'orig', 'superdupermegaRNA_hasraw.h5ad')
OUT_FILE = os.path.join(DATA_DIR, 'superdupermegaRNA_yoo25_AllSubclasses_P21_obs.tsv')

STUDY = '2023 Multiome'
AGE = 'P21'

adata = sc.read_h5ad(IN_FILE, backed='r')
print(f'Loaded (backed): {adata}')

obs = adata.obs
mask = (obs['Study'] == STUDY) & (obs['Age'] == AGE)
obs_sub = obs[mask]
print(f'Subset (Study=={STUDY!r}, Age=={AGE!r}): {len(obs_sub)} cells')

obs_sub.to_csv(OUT_FILE, sep='\t')
print(f'Saved {OUT_FILE}')
