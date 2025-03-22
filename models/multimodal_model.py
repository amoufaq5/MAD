# models/multimodal_model.py
import tensorflow as tf
from tensorflow.keras import layers, Model

def build_text_branch(vocab_size=5000, embedding_dim=128, max_length=100):
    text_input = layers.Input(shape=(max_length,), name="text_input")
    x = layers.Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_length)(text_input)
    x = layers.LSTM(64)(x)
    x = layers.Dense(32, activation="relu")(x)
    return text_input, x

def build_image_branch(image_shape=(224,224,3)):
    image_input = layers.Input(shape=image_shape, name="image_input")
    x = layers.Conv2D(32, (3,3), activation="relu")(image_input)
    x = layers.MaxPooling2D()(x)
    x = layers.Conv2D(64, (3,3), activation="relu")(x)
    x = layers.MaxPooling2D()(x)
    x = layers.Flatten()(x)
    x = layers.Dense(64, activation="relu")(x)
    return image_input, x

def build_blood_branch(input_dim=10):
    blood_input = layers.Input(shape=(input_dim,), name="blood_input")
    x = layers.Dense(16, activation="relu")(blood_input)
    x = layers.Dense(16, activation="relu")(x)
    return blood_input, x

def build_multimodal_model():
    text_input, text_out = build_text_branch()
    image_input, image_out = build_image_branch()
    blood_input, blood_out = build_blood_branch()

    # Combine
    combined = layers.concatenate([text_out, image_out, blood_out])
    x = layers.Dense(64, activation="relu")(combined)
    # We assume 9 diseases: cold, pneumonia, bronchitis, influenza, herpes, covid, hep B, chlamydia, chicken pox
    output = layers.Dense(9, activation="softmax", name="diagnosis")(x)
    model = Model(inputs=[text_input, image_input, blood_input], outputs=output)
    return model
