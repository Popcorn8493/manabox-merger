# Manabox Inventory Merger

Merge duplicate rows in a Manabox CSV export into a single consolidated inventory. Quantities are summed, and purchase price is averaged per unique card variant.

## Requirements

- Python 3.9+
- Pandas

## Setup (Windows - Command Prompt)

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
```

## Setup (Linux/Unix)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run (Terminal)

```bash
python manabox_merger.py
```

- Choose your Manabox CSV in the file dialog.
- The merged file is written as `manabox_inventory_merged.csv` in this folder.

## Required CSV columns

The script expects these columns to be present:
`Name`, `Set code`, `Collector number`, `Language`, `Foil`, `Condition`, `Purchase price currency`, `Altered`, `Scryfall ID`, `Quantity`, `Purchase price`.

## What it does

- Coerces `Quantity` and `Purchase price` to numbers (non-numeric becomes 0).
- Fills missing values for: `Altered` → "No", `Collector number` → "Unknown", `Foil` → "normal", `Condition` → "mint", `Scryfall ID` → "unknown".
- Groups by card identity fields and:
  - Sums `Quantity`
  - Averages `Purchase price`
