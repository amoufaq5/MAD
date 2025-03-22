import tensorflow as tf
from multimodal_model import build_multimodal_model
import numpy as np

def load_data():
    # Dummy data for demonstration—replace with actual preprocessing of scraped and annotated datasets.
    num_samples = 100
    text_data = np.random.randint(10000, size=(num_samples, 100))  # tokenized text
    image_data = np.random.rand(num_samples, 224, 224, 3)            # image data
    blood_data = np.random.rand(num_samples, 10)                     # blood test values
    labels = tf.keras.utils.to_categorical(np.random.randint(10, size=(num_samples,)), num_classes=10)
    return {"text_input": text_data, "image_input": image_data, "blood_input": blood_data}, labels

def train_model():
    model = build_multimodal_model()
    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
    X, y = load_data()
    model.fit(X, y, epochs=5, batch_size=8)
    model.save("models/diagnosis_model.h5")
    print("Model trained and saved.")

if __name__ == "__main__":
    train_model()
