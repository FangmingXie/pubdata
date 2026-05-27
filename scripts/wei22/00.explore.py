"""
Explore metadata of wei22_macaque_v1 dataset (E-MTAB-10459).
Outputs a summary to readme.txt.
"""
import pandas as pd

# Input files
BARCODE_CSV  = "/data/qlyu/project/pubdata/local_data/wei22_macaque_v1/FM_V1_133454_barcode.csv"
GENE_CSV     = "/data/qlyu/project/pubdata/local_data/wei22_macaque_v1/FM_V1_133454_gene.csv"
MTX_FILE     = "/data/qlyu/project/pubdata/local_data/wei22_macaque_v1/FM_V1_133454.mtx"
PATCH_CELL   = "/data/qlyu/project/pubdata/local_data/wei22_macaque_v1/PatchSeq_cell.csv"
PATCH_COUNT  = "/data/qlyu/project/pubdata/local_data/wei22_macaque_v1/PatchSeq_count.csv"
PATCH_GENE   = "/data/qlyu/project/pubdata/local_data/wei22_macaque_v1/PatchSeq_gene.csv"

# Output
README       = "/data/qlyu/project/pubdata/local_data/wei22_macaque_v1/readme.txt"

# --- snRNA-seq (FM_V1) ---
cells = pd.read_csv(BARCODE_CSV, index_col=0)
genes = pd.read_csv(GENE_CSV, index_col=0)

# MTX dimensions from header line 3
with open(MTX_FILE) as f:
    f.readline()  # %%MatrixMarket
    f.readline()  # %
    mtx_dims = f.readline().split()
mtx_ncells, mtx_ngenes, mtx_nnz = int(mtx_dims[0]), int(mtx_dims[1]), int(mtx_dims[2])

# --- PatchSeq ---
with open(PATCH_COUNT) as f:
    header = f.readline()
patch_cells = [c for c in header.strip().split(",") if c != "gene"]
patch_genes = pd.read_csv(PATCH_GENE, header=None, names=["gene"])

lines = []
lines.append("=" * 60)
lines.append("Dataset: wei22_macaque_v1 (E-MTAB-10459)")
lines.append("Species: Macaca fascicularis (macaque), V1 cortex")
lines.append("=" * 60)

lines.append("\n--- snRNA-seq (FM_V1_133454) ---")
lines.append(f"Cells:  {len(cells):,}  (MTX dim: {mtx_ncells:,})")
lines.append(f"Genes:  {len(genes):,}  (MTX dim: {mtx_ngenes:,})")
lines.append(f"NNZ entries in MTX: {mtx_nnz:,}")

lines.append("\nSamples (MonkeyID) and cell counts:")
for monkey, cnt in cells["MonkeyID"].value_counts().sort_index().items():
    lines.append(f"  {monkey}: {cnt:,}")

lines.append("\nAge distribution:")
for age, cnt in cells["age"].value_counts().sort_index().items():
    lines.append(f"  {age}: {cnt:,}")

lines.append("\nSex distribution:")
for sex, cnt in cells["sex"].value_counts().items():
    lines.append(f"  {sex}: {cnt:,}")

lines.append("\nClass (broad cell type):")
for cls, cnt in cells["class"].value_counts().items():
    lines.append(f"  {cls}: {cnt:,}")

lines.append("\nSubclass_1:")
for sub, cnt in cells["subclass_1"].value_counts().items():
    lines.append(f"  {sub}: {cnt:,}")

lines.append("\nSubclass_2:")
for sub, cnt in cells["subclass_2"].value_counts().items():
    lines.append(f"  {sub}: {cnt:,}")

lines.append(f"\nCell labels (fine types): {cells['cell_label'].nunique()} unique")
for lbl, cnt in cells["cell_label"].value_counts().items():
    lines.append(f"  {lbl}: {cnt:,}")

lines.append("\n--- PatchSeq ---")
lines.append(f"Cells: {len(patch_cells)}")
lines.append(f"Cell IDs: {', '.join(patch_cells)}")
lines.append(f"Genes: {len(patch_genes):,}")

output = "\n".join(lines) + "\n"
print(output)
with open(README, "w") as f:
    f.write(output)

print(f"\nSaved to {README}")
