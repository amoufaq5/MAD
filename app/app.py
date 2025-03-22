# app/app.py
from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf
import os

app = Flask(__name__)

# Load the trained model
MODEL_PATH = os.path.join("models", "diagnosis_model.h5")
model = tf.keras.models.load_model(MODEL_PATH)

disease_labels = [
    "common cold", "pneumonia", "bronchitis", "influenza",
    "herpes", "covid", "hepatitis b", "chlamydia", "chicken pox"
]

def simple_text_preprocess(text, tokenizer, max_length=100):
    # Minimal example, in real usage, ensure tokenizer is loaded from your training environment
    sequences = tokenizer.texts_to_sequences([text])
    padded = tf.keras.preprocessing.sequence.pad_sequences(sequences, maxlen=max_length, padding='post', truncating='post')
    return padded

@app.route("/diagnose", methods=["POST"])
def diagnose():
    data = request.json
    text_input = data.get("text", "")
    image_input = data.get("image", [])
    blood_input = data.get("blood", [])

    # For demonstration, we do a dummy approach to text:
    # In practice, load your trained tokenizer from disk and use the same method you used during training
    # If you want to keep it consistent with training, you'd pickle or save the tokenizer object
    # For now, let's do a random approach
    text_array = np.random.randint(5000, size=(1,100))

    # Convert image_input / blood_input to np array
    image_array = np.array(image_input, dtype="float32").reshape((1,224,224,3)) if image_input else np.random.rand(1,224,224,3)
    blood_array = np.array(blood_input, dtype="float32").reshape((1,10)) if blood_input else np.random.rand(1,10)

    # Predict
    prediction = model.predict({
        "text_input": text_array,
        "image_input": image_array,
        "blood_input": blood_array
    })
    disease_idx = int(np.argmax(prediction, axis=1)[0])
    diagnosis = disease_labels[disease_idx]

    # Simple severity logic
    severe = ["pneumonia", "covid", "hepatitis b", "chlamydia"]
    if diagnosis in severe:
        recommendation = "Refer to a doctor (severe case)."
    else:
        recommendation = "Recommend OTC medication and rest."

    return jsonify({"diagnosis": diagnosis, "recommendation": recommendation})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
