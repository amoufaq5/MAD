from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import os

app = Flask(__name__)

# Load the trained model
MODEL_PATH = os.path.join("models", "diagnosis_model.h5")
model = tf.keras.models.load_model(MODEL_PATH)

# Mapping for disease labels (indices should correspond to model output)
disease_labels = {
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

def preprocess_text(text):
    # Dummy tokenization and padding—replace with your actual tokenizer logic.
    tokens = [ord(c) % 10000 for c in text][:100]
    padded = tokens + [0]*(100 - len(tokens))
    return np.array(padded)

@app.route("/diagnose", methods=["POST"])
def diagnose():
    data = request.json
    # Extract text, image, and blood data
    text = data.get("text", "")
    image = np.array(data.get("image", []))
    blood = np.array(data.get("blood", []))
    
    # Preprocess text
    text_input = preprocess_text(text)
    text_input = np.expand_dims(text_input, axis=0)
    
    # Ensure image and blood inputs have batch dimensions
    image_input = np.expand_dims(image, axis=0) if image.ndim == 3 else image
    blood_input = np.expand_dims(blood, axis=0) if blood.ndim == 1 else blood

    # Predict diagnosis
    prediction = model.predict({
        "text_input": text_input,
        "image_input": image_input,
        "blood_input": blood_input
    })
    diagnosis_index = int(np.argmax(prediction, axis=1)[0])
    diagnosis = disease_labels.get(diagnosis_index, "unknown")
    
    # Business logic based on severity (for example, severe diseases require a doctor’s referral)
    severe_diseases = ["pneumonia", "covid", "hepatitis b"]
    if diagnosis in severe_diseases:
        recommendation = "Refer to a doctor immediately."
    else:
        recommendation = "Recommend over-the-counter medication and rest."
    
    return jsonify({"diagnosis": diagnosis, "recommendation": recommendation})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
