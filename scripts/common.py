import scanpy as sc


def subset_h5ad(in_file, out_file, col, values=None, pattern=None):
    """Load h5ad in backed mode, subset by obs column, save result.

    Args:
        in_file: path to input h5ad
        out_file: path to output h5ad
        col: obs column name to filter on
        values: single value or list of values to keep
        pattern: regex pattern to match against col (used if values is None)
    """
    adata = sc.read_h5ad(in_file, backed='r')
    print(f'Loaded (backed): {adata}')

    if pattern is not None:
        mask = adata.obs[col].str.contains(pattern, regex=True)
        label = f'{col} ~ "{pattern}"'
    else:
        if isinstance(values, str):
            values = [values]
        mask = adata.obs[col].isin(values)
        label = f'{col} in {values}'

    adata_sub = adata[mask].to_memory()
    print(f'Subset ({label}): {adata_sub}')

    adata_sub.write_h5ad(out_file)
    print(f'Saved {out_file}')
