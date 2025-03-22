# File: data/preprocessing.py
import os
import logging
import re
import nltk

logging.basicConfig(
    filename='preprocessing.log',
    filemode='a',
    format='%(asctime)s [%(levelname)s] %(message)s',
    level=logging.INFO
)

def basic_clean_text(text):
    # Remove non-alphanumeric characters
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    # Lowercase
    text = text.lower()
    return text

def tokenize_text(text):
    # Use nltk for tokenization
    tokens = nltk.word_tokenize(text)
    return tokens

def process_raw_files(raw_dir, output_dir):
    nltk.download('punkt', quiet=True)  # Ensure NLTK data is available
    os.makedirs(output_dir, exist_ok=True)
    
    for fname in os.listdir(raw_dir):
        if fname.endswith(".txt"):
            path = os.path.join(raw_dir, fname)
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
            cleaned = basic_clean_text(text)
            tokens = tokenize_text(cleaned)
            
            # Write tokens to a processed file
            out_path = os.path.join(output_dir, fname.replace(".txt", "_tokens.txt"))
            with open(out_path, "w", encoding="utf-8") as f_out:
                f_out.write(" ".join(tokens))
            
            logging.info(f"Processed {fname} -> {out_path}")

if __name__ == "__main__":
    raw_directory = "data/raw"
    preprocessed_directory = "data/preprocessed"
    process_raw_files(raw_directory, preprocessed_directory)
