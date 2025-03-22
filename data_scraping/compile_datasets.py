# data_scraping/compile_datasets.py
import pandas as pd
import os
from datetime import datetime

def compile_csvs():
    raw_dir = "data/raw"
    compiled_path = "data/compiled_dataset.csv"
    os.makedirs("data", exist_ok=True)

    all_files = [f for f in os.listdir(raw_dir) if f.endswith(".csv")]
    dfs = []
    for file in all_files:
        df = pd.read_csv(os.path.join(raw_dir, file))
        df["timestamp"] = datetime.now().isoformat()
        df["source_file"] = file
        dfs.append(df)

    compiled_df = pd.concat(dfs, ignore_index=True)
    compiled_df.drop_duplicates(inplace=True)
    compiled_df.to_csv(compiled_path, index=False)
    print(f"Compiled dataset saved to {compiled_path}")

if __name__ == "__main__":
    compile_csvs()
