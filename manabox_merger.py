import sys
import pandas as pd
import tkinter as tk
from tkinter import filedialog


GROUPING_COLUMNS = [
    'Name', 'Set code', 'Collector number', 'Language',
    'Foil', 'Condition', 'Purchase price currency', 'Altered', 'Scryfall ID'
]

NUMERIC_COLUMNS = ['Quantity', 'Purchase price']

MISSING_DEFAULTS = {
    'Altered': 'No',
    'Collector number': 'Unknown',
    'Foil': 'normal',
    'Condition': 'mint',
    'Scryfall ID': 'unknown',
}


def main() -> None:
    root = tk.Tk()
    root.withdraw()
    csv_file = filedialog.askopenfilename(
        title="Select CSV file to merge",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    root.destroy()

    if not csv_file:
        print("No file selected. Exiting...")
        sys.exit()

    try:
        df = pd.read_csv(csv_file, header=0)

        
        df[NUMERIC_COLUMNS] = (
            df[NUMERIC_COLUMNS]
            .apply(pd.to_numeric, errors='coerce')
            .fillna(0)
        )

        df.fillna(value=MISSING_DEFAULTS, inplace=True)

        original_quantity = df['Quantity'].sum()
        print(f"Original: {len(df)} entries, {original_quantity} total cards")

        merged_df = df.groupby(GROUPING_COLUMNS, as_index=False).agg(
            Quantity=('Quantity', 'sum'),
            **{'Purchase price': ('Purchase price', 'mean')}
        )

        merged_quantity = merged_df['Quantity'].sum()
        print(f"Merged: {len(merged_df)} entries, {merged_quantity} total cards")

        if original_quantity == merged_quantity:
            print("Merge successful!")
            merged_df.to_csv('manabox_inventory_merged.csv', index=False)
            print("Saved to 'manabox_inventory_merged.csv'")
        else:
            print("Quantity mismatch - merge failed!")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()