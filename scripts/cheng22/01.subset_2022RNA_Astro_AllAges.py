import os
import scanpy as sc

# NOTE: CELLS WITH STUDY == NaN ARE TREATED AS "2022 RNA" (P28+ AGES HAVE NO STUDY LABEL).

# --- file paths ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(PROJECT_ROOT, 'local_data', 'cheng22_yoo25')
IN_FILE = os.path.join(DATA_DIR, 'orig', 'superdupermegaRNA_hasraw.h5ad')
OUT_FILE = os.path.join(DATA_DIR, 'superdupermegaRNA_cheng22_Astro_AllAges.h5ad')

STUDY = '2022 RNA'
SUBCLASSES = ['Astro']

# --- load and subset ---
adata = sc.read_h5ad(IN_FILE, backed='r')
print(f'Loaded (backed): {adata}')

# NOTE: CELLS WITH STUDY == NaN ARE TREATED AS "2022 RNA" (P28+ AGES HAVE NO STUDY LABEL).
study_mask = (adata.obs['Study'] == STUDY) | adata.obs['Study'].isna()
mask = study_mask & (adata.obs['Subclass'].isin(SUBCLASSES))
adata_sub = adata[mask].to_memory()
print(f'Subset (Study=={STUDY!r} or NaN, all ages, Subclass in {SUBCLASSES}): {adata_sub}')

adata_sub.write_h5ad(OUT_FILE)
print(f'Saved {OUT_FILE}')
