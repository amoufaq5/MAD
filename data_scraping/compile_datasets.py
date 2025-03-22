# data_scraping/compile_datasets.py
import pandas as pd
import os
import spacy
from datetime import datetime
from tqdm import tqdm

# Load spaCy model (medical model)
nlp = spacy.load("en_core_web_sm")


def extract_entities(text):
    doc = nlp(text)
    symptoms = []
    medications = []
    diseases = []
    for ent in doc.ents:
        label = ent.label_.lower()
        if label in ["disease", "condition"]:
            diseases.append(ent.text)
        elif label in ["drug", "medication"]:
            medications.append(ent.text)
        elif label in ["symptom", "sign"]:
            symptoms.append(ent.text)
    return list(set(symptoms)), list(set(medications)), list(set(diseases))

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

        # Fill missing fields using SpaCy
        for i, row in df.iterrows():
            content = str(row.get("content", ""))
            if not content.strip(): continue
            symptoms, meds, diseases = extract_entities(content)

            if not row.get("symptoms") and symptoms:
                df.at[i, "symptoms"] = ", ".join(symptoms)
            if not row.get("medication") and meds:
                df.at[i, "medication"] = ", ".join(meds)
            if not row.get("disease") and diseases:
                df.at[i, "disease"] = ", ".join(diseases)

            df.at[i, "entity_counts"] = len(symptoms) + len(meds) + len(diseases)
            df.at[i, "quality_score"] = quality_score(df.loc[i])

        dfs.append(df)

    compiled_df = pd.concat(dfs, ignore_index=True)
    compiled_df = compiled_df[compiled_df["quality_score"] >= 3]  # Filter weak entries
    compiled_df.drop_duplicates(inplace=True)
    compiled_df.to_csv(compiled_path, index=False)
    print(f"✔️ Compiled dataset saved to {compiled_path}")

if __name__ == "__main__":
    compile_csvs()
