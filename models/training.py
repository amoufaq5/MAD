# models/training.py
import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from multimodal_model import build_multimodal_model

def load_text_data_from_excel(excel_file="data/aggregated.xlsx", max_length=100):
    """Loads content from Excel, tokenizes, and returns numeric sequences + disease labels."""
    df = pd.read_excel(excel_file)

    # Minimal cleaning for demonstration
    texts = df["content"].astype(str).tolist()
    diseases = df["disease"].astype(str).tolist()

    # Convert disease text to a label index. 
    # This is naive: just picking the first disease found in the cell, or labeling 'other'
    disease_map = {
        "common cold": 0, "pneumonia": 1, "bronchitis": 2, "influenza": 3,
        "herpes": 4, "covid": 5, "hepatitis b": 6, "chlamydia": 7, "chicken pox": 8
    }

    labels = []
    for d in diseases:
        # Find which label matches
        found = None
        for key in disease_map.keys():
            if key in d.lower():
                found = disease_map[key]
                break
        if found is not None:
            labels.append(found)
        else:
            # treat as "other" or just pick the first if multiple
            labels.append(np.random.randint(0, 9))  # random fallback

    tokenizer = Tokenizer(num_words=5000, oov_token="<OOV>")
    tokenizer.fit_on_texts(texts)
    sequences = tokenizer.texts_to_sequences(texts)
    padded_sequences = pad_sequences(sequences, maxlen=max_length, padding='post', truncating='post')

    return padded_sequences, np.array(labels), tokenizer

def load_dummy_image_data(num_samples, image_shape=(224,224,3)):
    """Generate random image data for demonstration."""
    return np.random.rand(num_samples, *image_shape)

def load_dummy_blood_data(num_samples, num_features=10):
    """Generate random blood test data for demonstration."""
    return np.random.rand(num_samples, num_features)

def train_model():
    # Load text data
    text_data, label_data, tokenizer = load_text_data_from_excel()
    num_samples = text_data.shape[0]

    # Create dummy images and blood data
    image_data = load_dummy_image_data(num_samples)
    blood_data = load_dummy_blood_data(num_samples)

    # Build and compile the model
    model = build_multimodal_model()
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

    # Train
    model.fit(
        x={
            "text_input": text_data,
            "image_input": image_data,
            "blood_input": blood_data
        },
        y=label_data,
        batch_size=8,
        epochs=5
    )

    os.makedirs("models", exist_ok=True)
    model_path = os.path.join("models", "diagnosis_model.h5")
    model.save(model_path)
    print(f"Model trained and saved to {model_path}")

if __name__ == "__main__":
    train_model()
