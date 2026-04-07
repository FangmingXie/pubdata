# Plan: Explore gao25 Cell Metadata

## Context
The user wants to inspect cell metadata from `local_data/gao25/DevVIS_scRNA_processed.h5ad` — specifically unique cell types at the subclass level and developmental ages — without loading the full data matrix. Results should be saved to `local_data/gao25/README.txt`.

## Approach

### New script: `scripts/gao25/00.explore_gao25_scRNA.py`

Follow patterns from `scripts/morcom26/00.subset_EN_L2_3.py`:
- Capitalize file path variables at the top
- Use `sc.read_h5ad(FILE, backed='r').obs` to load only cell metadata
- Print all `obs` column names first to identify the right columns for "subclass" and "age"
- Report unique values for the relevant columns
- Write results to `local_data/gao25/README.txt`

### Script logic
1. Load only `.obs` metadata via `sc.read_h5ad(IN_FILE, backed='r').obs`
2. Print all column names so the user can see what's available
3. Identify and report unique cell types (subclass-level column — likely named something like `subclass`, `cell_type_subclass`, etc.) and developmental ages (likely `age`, `developmental_age`, etc.)
4. Write a summary to `README.txt` with:
   - Number of cells
   - All obs columns
   - Unique subclass values (sorted, with counts)
   - Unique developmental age values (sorted, with counts)

## Critical files
- **New**: `scripts/gao25/00.explore_gao25_scRNA.py`
- **Output**: `local_data/gao25/README.txt`
- **Input**: `local_data/gao25/DevVIS_scRNA_processed.h5ad`
- **Reference pattern**: `scripts/morcom26/00.subset_EN_L2_3.py`

## Verification
Run the script with:
```bash
conda run -n pubdata python scripts/gao25/00.explore_gao25_scRNA.py
```
Check that `local_data/gao25/README.txt` is created with cell type and age summaries.
