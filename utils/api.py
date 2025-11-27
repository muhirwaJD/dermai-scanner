"""FastAPI wrapper for model serving and load testing"""
import io
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse # import-error
from PIL import Image
import numpy as np
import tensorflow.keras as keras # disable=import-error
from utils.load_model import load_face_model

app = FastAPI(title="Skin Cancer Classifier API")

# Load model at startup
model = None
CLASS_NAMES = ['akiec', 'bcc', 'bkl', 'df', 'mel', 'nv', 'vasc']

@app.on_event("startup")
async def load_model():
    """Load model when API starts"""
    global model
    model = load_face_model()
    print("✅ Model loaded successfully")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Skin Cancer Classifier API is running"}

@app.get("/health")
async def health():
    """Health check for load balancers"""
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Predict skin cancer class from uploaded image
    
    Returns:
        JSON with predicted class, confidence, and all probabilities
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        # Read and preprocess image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Preprocess for EfficientNet
        img_array = np.array(image.resize((224, 224)))
        img_array = keras.applications.efficientnet.preprocess_input(img_array)
        img_array = np.expand_dims(img_array, axis=0)

        # Predict
        predictions = model.predict(img_array, verbose=0)
        predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
        confidence = float(np.max(predictions[0]))

        # All probabilities
        all_predictions = {
            CLASS_NAMES[i]: float(predictions[0][i])
            for i in range(len(CLASS_NAMES))
        }

        return {
            "predicted_class": predicted_class,
            "confidence": confidence,
            "all_predictions": all_predictions
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")

@app.get("/classes")
async def get_classes():
    """Get list of available classes"""
    return {
        "classes": CLASS_NAMES,
        "descriptions": {
            "akiec": "Actinic Keratoses and Intraepithelial Carcinoma",
            "bcc": "Basal Cell Carcinoma",
            "bkl": "Benign Keratosis-like Lesions",
            "df": "Dermatofibroma",
            "mel": "Melanoma",
            "nv": "Melanocytic Nevi",
            "vasc": "Vascular Lesions"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
