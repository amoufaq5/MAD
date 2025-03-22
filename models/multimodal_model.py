import tensorflow as tf
from tensorflow.keras import layers, Model

def build_text_model(vocab_size=10000, embedding_dim=128, max_length=100):
    input_text = layers.Input(shape=(max_length,), name="text_input")
    x = layers.Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_length)(input_text)
    x = layers.LSTM(64)(x)
    x = layers.Dense(32, activation="relu")(x)
    return input_text, x

def build_image_model(input_shape=(224,224,3)):
    input_image = layers.Input(shape=input_shape, name="image_input")
    x = layers.Conv2D(32, (3,3), activation="relu")(input_image)
    x = layers.MaxPooling2D()(x)
    x = layers.Conv2D(64, (3,3), activation="relu")(x)
    x = layers.MaxPooling2D()(x)
    x = layers.Flatten()(x)
    x = layers.Dense(64, activation="relu")(x)
    return input_image, x

def build_blood_test_model(input_dim=10):
    input_blood = layers.Input(shape=(input_dim,), name="blood_input")
    x = layers.Dense(16, activation="relu")(input_blood)
    x = layers.Dense(16, activation="relu")(x)
    return input_blood, x

def build_multimodal_model():
    text_input, text_out = build_text_model()
    image_input, image_out = build_image_model()
    blood_input, blood_out = build_blood_test_model()

    # Combine the modalities
    combined = layers.concatenate([text_out, image_out, blood_out])
    x = layers.Dense(64, activation="relu")(combined)
    # For diagnosis, output probabilities for 10 diseases
    output = layers.Dense(10, activation="softmax", name="diagnosis")(x)
    model = Model(inputs=[text_input, image_input, blood_input], outputs=output)
    return model

if __name__ == "__main__":
    model = build_multimodal_model()
    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
    model.summary()
