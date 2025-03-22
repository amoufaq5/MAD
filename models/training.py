import os
import numpy as np
import tensorflow as tf
from multimodal_model import build_multimodal_model

def load_synthetic_data(num_samples=200):
    """
    Replace with real data loading from your preprocessed text,
    annotated images, and numeric blood data.
    """
    # Example text data: integer-encoded sequences of length 100
    text_data = np.random.randint(0, 10000, (num_samples, 100))
    
    # Example image data: 224x224 RGB
    image_data = np.random.rand(num_samples, 224, 224, 3).astype(np.float32)
    
    # Example blood data: vector of length 10
    blood_data = np.random.rand(num_samples, 10).astype(np.float32)
    
    # Example labels: 10 diseases
    labels = np.random.randint(0, 10, (num_samples,))
    labels_onehot = tf.keras.utils.to_categorical(labels, num_classes=10)
    
    return {
        "text_input": text_data,
        "image_input": image_data,
        "blood_input": blood_data
    }, labels_onehot

def train_model():
    model = build_multimodal_model(num_diseases=10)
    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

    X, y = load_synthetic_data()
    model.fit(X, y, epochs=5, batch_size=8, validation_split=0.2)
    
    os.makedirs("models", exist_ok=True)
    model.save("models/diagnosis_model.h5")
    print("Model trained and saved at models/diagnosis_model.h5")

if __name__ == "__main__":
    train_model()
