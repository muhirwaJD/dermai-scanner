"""Model loading utilities for the product recommendation system."""
import os
from pathlib import Path
import streamlit as st  # type: ignore
import tensorflow as tf
import tensorflow.keras as keras # pylint: disable=import-error,no-name-in-module

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

tf.config.set_visible_devices([], 'GPU')

MODELS = Path("models/original_models")

@st.cache_resource
def recreate_model_architecture(): # type: ignore
    """Recreate the exact model architecture from the notebook"""
    SIZE = 224

    base_model = keras.applications.EfficientNetB0(
        include_top=False,
        weights='imagenet',
        input_shape=(SIZE, SIZE, 3)
    )

    base_model.trainable = False

    model = keras.Sequential([
        base_model,
        keras.layers.GlobalAveragePooling2D(),
        keras.layers.BatchNormalization(),
        keras.layers.Dropout(0.4),
        keras.layers.Dense(256, activation='relu'),
        keras.layers.BatchNormalization(),
        keras.layers.Dropout(0.4),
        keras.layers.Dense(7, activation='softmax')
    ], name='SkinCancerClassifier')

    return model

@st.cache_resource
def load_face_model():
    """Load face model by recreating architecture and loading weights"""
    skin_model_path = MODELS / "Skin_Cancer_Model_v1.keras"

    if not skin_model_path.exists():
        st.error("Skin cancer model does not exist.")
        return None

    st.success("Skin cancer model found.")

    try:
        with st.spinner("Loading skin cancer model..."):
            # Recreate the model architecture
            model = recreate_model_architecture()
            # Load the trained weights
            model.load_weights(str(skin_model_path))

            # model = tf.keras.models.load_model(str(skin_model_path))

            st.success("✅ Model loaded successfully!")
        return model
    except FileNotFoundError as e:
        st.error(f"Failed to load skin cancer model: {e}")
        return None
