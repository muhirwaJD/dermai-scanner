"""Extract weights from existing model for retraining"""
from load_model import recreate_model_architecture

# Recreate the architecture
print("Recreating model architecture...")
model = recreate_model_architecture()

# Load the weights from the .keras file
print("Loading weights from Skin_Cancer_Model_v1.keras...")
model.load_weights('models/original_models/Skin_Cancer_Model_v1.keras')

# Save just the weights
weights_path = 'weights/weights.weights.h5'
print(f"Saving weights to {weights_path}...")
model.save_weights(weights_path)

print(f"✅ Weights extracted successfully!")
print(f"📁 Saved to: {weights_path}")
print("\nNow you can use these weights for retraining!")
