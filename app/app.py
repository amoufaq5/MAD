from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import os

app = Flask(__name__)

# Load model
MODEL_PATH = os.path.join("models", "diagnosis_model.h5")
model = tf.keras.models.load_model(MODEL_PATH)

# Example disease mapping
DISEASE_LABELS = {
    0: "common cold",
    1: "pneumonia",
    2: "bronchitis",
    3: "influenza",
    4: "herpes",
    5: "covid",
    6: "hepatitis b",
    7: "chlamydia",
    8: "chicken pox",
    9: "other"
}

SEVERE_DISEASES = {"pneumonia", "covid", "hepatitis b"}

# Sample function to handle tokenization/encoding of text
def preprocess_text(text, max_length=100):
    # Very simplistic: convert chars to integer, pad/truncate
    # Replace with a real tokenizer in production
    tokens = [ord(c) % 10000 for c in text.lower() if c.isalnum() or c.isspace()]
    tokens = tokens[:max_length]
    if len(tokens) < max_length:
        tokens += [0]*(max_length - len(tokens))
    return np.array(tokens)

@app.route("/collect_info", methods=["POST"])
def collect_info():
    """
    A sample endpoint demonstrating how you might collect
    ASMETHOD data. In a real app, you'd store these in a DB
    or session to help refine diagnosis questions dynamically.
    """
    data = request.json
    # Just echoing it back as demonstration
    # Fields might be: age, medication, time persisting, etc.
    return jsonify({
        "message": "ASMETHOD data received",
        "data": data
    })

@app.route("/diagnose", methods=["POST"])
def diagnose():
    """
    Expects JSON of the form:
    {
      "text": "patient complaint ...",
      "image": [...],
      "blood": [...]
    }
    """
    body = request.json
    text_data = body.get("text", "")
    image_data = body.get("image", [])
    blood_data = body.get("blood", [])

    # Preprocess text
    text_input = preprocess_text(text_data)
    text_input = np.expand_dims(text_input, axis=0)

    # Convert image and blood data to numpy arrays (ensure correct shape)
    image_data = np.array(image_data, dtype=np.float32)
    if image_data.ndim == 3:
        # Insert batch dimension
        image_data = np.expand_dims(image_data, axis=0)
    elif image_data.ndim == 4:
        pass  # Already batched
    else:
        # If no image, create dummy array
        image_data = np.zeros((1, 224, 224, 3), dtype=np.float32)

    blood_data = np.array(blood_data, dtype=np.float32)
    if blood_data.ndim == 1:
        blood_data = np.expand_dims(blood_data, axis=0)

    # Model inference
    prediction = model.predict({
        "text_input": text_input,
        "image_input": image_data,
        "blood_input": blood_data
    })
    diagnosis_idx = int(np.argmax(prediction, axis=1)[0])
    diagnosis = DISEASE_LABELS.get(diagnosis_idx, "unknown")

    # Simple severity check
    if diagnosis in SEVERE_DISEASES:
        recommendation = "Refer to a doctor immediately."
    else:
        recommendation = "Recommend over-the-counter medication and rest."

    return jsonify({
        "diagnosis": diagnosis,
        "recommendation": recommendation,
        "confidence_scores": prediction[0].tolist()
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
