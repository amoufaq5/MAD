# data_scraping/compile_datasets.py
import pandas as pd
import os
from datetime import datetime
from tqdm import tqdm

def quality_score(row):
    score = 0
    if len(str(row.get("content", ""))) > 200:
        score += 1
    if row.get("title") and len(row["title"]) > 10:
        score += 1
    if row.get("symptoms"): score += 1
    if row.get("medication"): score += 1
    if row.get("disease"): score += 1
    return score

def compile_csvs():
    raw_dir = "data/raw"
    compiled_path = "data/compiled_dataset.csv"
    os.makedirs("data", exist_ok=True)

    all_files = [f for f in os.listdir(raw_dir) if f.endswith(".csv")]
    dfs = []
    for file in tqdm(all_files, desc="Compiling datasets"):
        df = pd.read_csv(os.path.join(raw_dir, file))
        df["timestamp"] = datetime.now().isoformat()
        df["source_file"] = file

        df["entity_counts"] = 0  # placeholder
        df["quality_score"] = df.apply(quality_score, axis=1)

        dfs.append(df)

    compiled_df = pd.concat(dfs, ignore_index=True)
    compiled_df = compiled_df[compiled_df["quality_score"] >= 3]  # Filter weak entries
    compiled_df.drop_duplicates(inplace=True)
    compiled_df.to_csv(compiled_path, index=False)
    print(f"✔️ Compiled dataset saved to {compiled_path}")

if __name__ == "__main__":
    compile_csvs()
