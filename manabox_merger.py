import pandas as pd
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()
csv_file = filedialog.askopenfilename(
    title="Select CSV file to merge",
    filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
)

if not csv_file:
    print("No file selected. Exiting...")
    exit()

try:
    df = pd.read_csv(csv_file, header=0)
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(0)
    df['Purchase price'] = pd.to_numeric(df['Purchase price'], errors='coerce').fillna(0)
    df['Altered'] = df['Altered'].fillna('No')

    original_quantity = df['Quantity'].sum()
    print(f"Original: {len(df)} entries, {original_quantity} total cards")

    grouping_cols = ['Name', 'Set code', 'Collector number', 'Language',
                     'Foil', 'Condition', 'Purchase price currency', 'Altered', 'Scryfall ID']

    merged_df = df.groupby(grouping_cols, as_index=False).agg({
        'Quantity': 'sum',
        'Purchase price': 'mean'
    })

    merged_quantity = merged_df['Quantity'].sum()
    print(f"Merged: {len(merged_df)} entries, {merged_quantity} total cards")

    if original_quantity == merged_quantity:
        print("✓ Merge successful!")
        merged_df.to_csv('manabox_inventory_merged.csv', index=False)
        print(f"Saved to 'manabox_inventory_merged.csv'")
    else:
        print("✕ Quantity mismatch - merge failed!")

except Exception as e:
    print(f"Error: {e}")