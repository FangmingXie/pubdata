"""
Survey local_data/ and write a markdown table of datasets to docs/datasets.md.
Description is pulled from the first README found, or inferred from directory contents.
"""
import os
import textwrap

LOCAL_DATA_DIR = "local_data"
OUTPUT_FILE = "docs/datasets.md"

README_NAMES = {"readme.txt", "readme.md", "readme"}

def get_description(dataset_dir):
    """Return a one-line description from a README if present, else a file-list summary."""
    for fname in os.listdir(dataset_dir):
        if fname.lower() in README_NAMES:
            with open(os.path.join(dataset_dir, fname)) as f:
                first_line = f.readline().strip()
                if first_line:
                    return textwrap.shorten(first_line, width=80)

    # Fallback: summarize file extensions present
    exts = set()
    for root, _, files in os.walk(dataset_dir):
        for f in files:
            ext = os.path.splitext(f)[1]
            if ext:
                exts.add(ext.lstrip("."))
    if exts:
        return "Files: " + ", ".join(sorted(exts))
    return ""


def main():
    entries = sorted(
        d for d in os.listdir(LOCAL_DATA_DIR)
        if os.path.isdir(os.path.join(LOCAL_DATA_DIR, d))
    )

    rows = []
    for name in entries:
        desc = get_description(os.path.join(LOCAL_DATA_DIR, name))
        rows.append((name, desc))

    lines = [
        "# Datasets",
        "",
        "| Dataset | Description |",
        "| ------- | ----------- |",
    ]
    for name, desc in rows:
        lines.append(f"| {name} | {desc} |")
    lines.append("")

    with open(OUTPUT_FILE, "w") as f:
        f.write("\n".join(lines))

    print(f"Written {len(rows)} datasets to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
