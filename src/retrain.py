"""Model retraining pipeline"""
# import os
import shutil
from pathlib import Path
from datetime import datetime
import json
import streamlit as st
import tensorflow.keras as keras  # pylint: disable=import-error,no-name-in-module
from tensorflow.keras.preprocessing.image import ImageDataGenerator # pylint: disable=import-error,no-name-in-module
from tensorflow.keras.applications.efficientnet import preprocess_input # pylint: disable=import-error,no-name-in-module
from utils.load_model import recreate_model_architecture

def save_uploaded_files(uploaded_files, selected_class, save_dir='data/retrain'):
    """
    Save uploaded files organized by class
    
    Args:
        uploaded_files: List of uploaded files from Streamlit
        save_dir: Directory to save files
        
    Returns:
        Dictionary with class counts
    """
    save_path = Path(save_dir)
    save_path.mkdir(parents=True, exist_ok=True)

    # IMPORTANT: Create ALL 7 class folders (even if empty)
    # This ensures the data generator uses categorical mode correctly
    all_classes = ['akiec', 'bcc', 'bkl', 'df', 'mel', 'nv', 'vasc']
    
    for class_name in all_classes:
        class_folder = save_path / class_name
        class_folder.mkdir(exist_ok=True)
        
        # Clear existing files in this class folder
        if class_folder.exists():
            for file in class_folder.glob('*'):
                if file.is_file():
                    file.unlink()

    # Save uploaded files to the selected class folder
    class_dir = save_path / selected_class
    class_counts = {selected_class: 0}

    for i, uploaded_file in enumerate(uploaded_files):
        # Get file extension
        original_filename = uploaded_file.name
        extension = Path(original_filename).suffix

        # Create unique filename with class prefix
        new_filename = f"{selected_class}_img_{i+1}{extension}"

        # Save file
        file_path = class_dir / new_filename
        with open(file_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())

        class_counts[selected_class] = class_counts.get(selected_class, 0) + 1
    
    return class_counts

def create_data_generators(data_dir, img_size=224, batch_size=32):
    """Create training and validation data generators"""

    datagen = ImageDataGenerator(
        preprocessing_function=preprocess_input,
        validation_split=0.2,
        rotation_range=20,
        width_shift_range=0.1,
        height_shift_range=0.1,
        horizontal_flip=True,
        zoom_range=0.1
    )

    train_generator = datagen.flow_from_directory(
        data_dir,
        target_size=(img_size, img_size),
        batch_size=batch_size,
        class_mode='categorical',
        subset='training'
    )

    val_generator = datagen.flow_from_directory(
        data_dir,
        target_size=(img_size, img_size),
        batch_size=batch_size,
        class_mode='categorical',
        subset='validation'
    )

    return train_generator, val_generator

def retrain_model(data_dir, base_model_path='models/Skin_Cancer_Model_v1.keras', epochs=5):
    """
    Retrain model with new data
    
    Args:
        data_dir: Directory containing new training data
        base_model_path: Path to pre-trained model
        epochs: Number of training epochs
        
    Returns:
        Tuple of (new_model_path, metadata)
    """
    print("Recreating model architecture...")
    model = recreate_model_architecture()


    # Try to load pre-trained weights
    weights_file = Path('weights/weights.weights.h5')

    try:
        if weights_file.exists():
            print(f"Loading weights from {weights_file}...")
            model.load_weights(str(weights_file))
        else:
            print("⚠️ Weights file not found, using ImageNet weights")

    except Exception as e:
        print(f"⚠️ Error loading weights: {e}")

    # Create data generators
    print("Creating data generators...")
    train_gen, val_gen = create_data_generators(data_dir)

    # Compile model
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.0001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    # Train
    print(f"Retraining for {epochs} epochs...")
    history = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=epochs,
        verbose=1
    )

    # Save new model
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_model_path = f'models/retrained_models/skin_cancer_model_{timestamp}.keras'
    model.save(new_model_path)

    # Save metadata
    metadata = {
        'timestamp': timestamp,
        'base_model': base_model_path,
        'new_model': new_model_path,
        'epochs': epochs,
        'training_accuracy': float(history.history['accuracy'][-1]),
        'validation_accuracy': float(history.history['val_accuracy'][-1]),
        'training_loss': float(history.history['loss'][-1]),
        'validation_loss': float(history.history['val_loss'][-1])
    }

    # Append to log
    log_path = Path('models/retraining_log.json')
    with open(log_path, 'a') as f:
        json.dump(metadata, f)
        f.write('\n')

    print(f"✅ Model saved to: {new_model_path}")
    print(f"✅ Training accuracy: {metadata['training_accuracy']:.2%}")
    print(f"✅ Validation accuracy: {metadata['validation_accuracy']:.2%}")

    return new_model_path, metadata
