# CLAUDE.md

## Project

A data-processing repository at an early stage. Its only code is a script that cleans raw CSV files. It has no data, tests, dependencies or CI yet.

## Folder structure

```
scripts/
  clean_csv.py    Removes empty rows from every CSV in data/raw/ and writes them to data/clean/
data/             Planned; not yet in the repository
  raw/            Input CSVs, never edited in place
  clean/          Output of scripts/clean_csv.py, regenerated rather than hand-edited
```

## Commands

```bash
python3 scripts/clean_csv.py                          # data/raw/ -> data/clean/
python3 scripts/clean_csv.py --input DIR --output DIR # other folders
```

The script exits with status 1 when the input folder has no CSVs.

## Conventions

- **Python 3, standard library only.** Add a third-party dependency only when needed, and record it in a `requirements.txt` at the same time.
- **Scripts** live in `scripts/`, run from any directory (paths resolve from the repository root), use `argparse` with defaults that match the `data/` layout, and print a one-line summary per file.
- **Data flow is one-way:** read from `data/raw/`, write to `data/clean/`. Never change raw files.
- **CSV handling:** read as UTF-8, accepting a byte-order mark; detect the delimiter; keep the header and all non-empty rows unchanged. A row counts as empty only when every field is blank or whitespace. Output uses `\r\n` line endings, the Python `csv` default.
- **Testing:** there is no test suite. Test changes on small test CSVs in a temporary directory, passing `--input`/`--output`, and do not commit test data to `data/`.
- **Git:** short, imperative commit messages, e.g. "Add CSV cleaning script that removes empty rows".

Update this file when you add folders, dependencies, tests or new conventions.
