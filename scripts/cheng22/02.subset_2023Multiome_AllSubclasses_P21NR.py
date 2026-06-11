import os
import scanpy as sc

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(PROJECT_ROOT, 'local_data', 'cheng22_yoo25')
IN_FILE = os.path.join(DATA_DIR, 'orig', 'superdupermegaRNA_hasraw.h5ad')
OUT_FILE = os.path.join(DATA_DIR, 'superdupermegaRNA_yoo25_AllSubclasses_P21NR.h5ad')

STUDY = '2023 Multiome'
AGE = 'P21'

adata = sc.read_h5ad(IN_FILE, backed='r')
print(f'Loaded (backed): {adata}')

mask = (adata.obs['Study'] == STUDY) & (adata.obs['Age'] == AGE)
adata_sub = adata[mask].to_memory()
print(f'Subset (Study=={STUDY!r}, Age=={AGE!r}, all subclasses): {adata_sub}')

adata_sub.write_h5ad(OUT_FILE)
print(f'Saved {OUT_FILE}')
