"""Dermatology Skin Cancer Classifier App"""
from pathlib import Path
import streamlit as st
# import tensorflow as tf
import tensorflow.keras as keras # pylint: disable=import-error,no-name-in-module
from PIL import Image
import numpy as np
import pandas as pd
from utils.load_model import load_face_model

# Class names for skin cancer
CLASS_NAMES = ['akiec', 'bcc', 'bkl', 'df', 'mel', 'nv', 'vasc']
st.title("Dermatology Skin Cancer Classifier")

# Sidebar for navigation
page = st.sidebar.selectbox("Navigation", ["Dashboard","Prediction", "Retrain"])

with st.sidebar:
    st.markdown("## About")
    st.markdown(
        """
        This application allows users to upload skin
        lesion images for classification using a pre-trained model.
        Users can also retrain the model with new data and view model performance metrics.
        """
    )

    st.markdown("---")

    model = load_face_model()


if page == "Dashboard":

    # # Model metrics
    # col1, col2, col3 = st.columns(3)
    # with col1:
    #     st.metric("Model Uptime", "99.8%", "↑ 0.2%")
    # with col2:
    #     st.metric("Total Predictions", "1,234", "↑ 45")
    # with col3:
    #     st.metric("Avg Confidence", "87.3%", "↑ 2.1%")

    # st.markdown("---")

    # Data visualizations
    st.subheader("Dataset Insights")

    # Load training data (you'll need to export metadata from your notebook)
    try:
        from src.visualization import (
            load_training_data,
            plot_class_distribution,
            plot_age_distribution,
            plot_localization_distribution
        )

        df = load_training_data()

        if df is not None:
            # Visualization 1: Class Distribution
            with st.expander("Class Distribution Details"):
                st.write("""
                Shows how balanced/imbalanced the 
                dataset is across different skin cancer types.
                """)
                plot_class_distribution(df)
            # Visualization 2: Age Distribution
            with st.expander("Patient Age Distribution Details"):
                st.write("Most skin cancers occur in older adults (50-70 years).")
                plot_age_distribution(df)
            # Visualization 3: Body Location
            with st.expander("Lesion Locations Details"):
                st.write("Back and lower extremities are the most common locations.")
                plot_localization_distribution(df)
        else:
            st.warning("Training data not found. Please add metadata.csv to notebook/ folder.")

    except Warning as e:
        st.error(f"Error loading visualizations: {e}")


elif page == "Prediction":
    st.subheader("Single Image Prediction")

    # Initialize sessions state
    if 'selected_image' not in st.session_state:
        st.session_state.selected_image = None

    uploaded_file = st.file_uploader("Upload a skin lesion image", type=['jpg', 'png', 'jpeg'])

    # Option 2: Use sample image
    st.write("**OR try a sample image:**")
    sample_dir = Path("sample_images")
    if sample_dir.exists():
        sample_classes = [d.name for d in sample_dir.iterdir() if d.is_dir()]
        selected_class = st.selectbox("Select class", sample_classes)

        class_images = list((sample_dir / selected_class).glob("*.jpg"))
        if class_images:
            selected_sample = st.selectbox("Select image", [img.name for img in class_images])
            if st.button("Use this sample"):
                st.session_state.selected_image = sample_dir / selected_class / selected_sample
                st.rerun()

    image_to_predict = uploaded_file if uploaded_file else st.session_state.selected_image


    if image_to_predict:
        # Display image
        if isinstance(image_to_predict, Path):
            image = Image.open(image_to_predict)
        else:
            image = Image.open(image_to_predict)

        # Convert to RGB if grayscale
        if image.mode != 'RGB':
            image = image.convert('RGB')

        st.image(image, caption="Uploaded Image", width="stretch")

        # Preprocess
        img_array = np.array(image.resize((224, 224)))
        img_array = keras.applications.efficientnet.preprocess_input(img_array)
        img_array = np.expand_dims(img_array, axis=0)

        # Predict
        if st.button("🔍 Predict"):
            predictions = model.predict(img_array)
            predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
            confidence = np.max(predictions[0]) * 100

            st.success(f"**Prediction:** {predicted_class}")
            st.info(f"**Confidence:** {confidence:.2f}%")

            # Show all probabilities
            prob_df = pd.DataFrame({"Class": CLASS_NAMES, "Probability": predictions[0] * 100
                                    }).sort_values(by="Probability", ascending=False)
            st.bar_chart(prob_df.set_index("Class"))

elif page == "Retrain":
    st.subheader("Retrain Model")

    # Class selection
    selected_class = st.selectbox("Select class for uploaded images", CLASS_NAMES,
    format_func=lambda x: {
        'akiec': 'Actinic Keratoses (akiec)',
        'bcc': 'Basal Cell Carcinoma (bcc)',
        'bkl': 'Benign Keratosis-like Lesions (bkl)',
        'df': 'Dermatofibroma (df)',
        'mel': 'Melanoma (mel)',
        'nv': 'Melanocytic Nevi (nv)',
        'vasc': 'Vascular Lesions (vasc)'
    }[x])

    uploaded_files = st.file_uploader(
        f"Upload {selected_class} images", 
        type=['jpg', 'png', 'jpeg'],
        accept_multiple_files=True,
        help="You can upload multiple images at once."
    )

    if uploaded_files:
        st.write(f"Uploaded {len(uploaded_files)} files")

        # Preview uploaded files
        col1, col2, col3 = st.columns(3)
        for i, file in enumerate(uploaded_files[:6]):
            with [col1, col2, col3][i % 3]:
                image = Image.open(file)
                st.image(image, caption=f"{selected_class}_{i:04d}.jpg", width=150)

        # Retrain button
        if st.button("Retrain Model"):
            from src.retrain import save_uploaded_files, retrain_model

            with st.spinner("Saving uploaded files..."):
                class_counts = save_uploaded_files(uploaded_files, selected_class)
                st.success(f"Files saved: {class_counts[selected_class]} images for class '{selected_class}'.")

            with st.spinner("Retraining model... This may take a few minutes."):
                try:
                    new_model_path, metadata = retrain_model('data/retrain', epochs=5)

                    st.success("Model retrained successfully!")
                    st.json(metadata)

                    # Show improvement
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Training Accuracy", f"{metadata['training_accuracy']:.2%}")
                    with col2:
                        st.metric("Validation Accuracy", f"{metadata['validation_accuracy']:.2%}")

                except Warning as e:
                    st.error(f"❌ Retraining failed: {e}")
