"""Locust load testing for Skin Cancer Classifier API"""
from locust import HttpUser, task, between
import random
from pathlib import Path

class SkinCancerUser(HttpUser):
    """Simulates a user making predictions on the API"""

    # Wait 1-3 seconds between requests (simulating real user behavior)
    wait_time = between(1, 3)

    def on_start(self):
        """Called when a simulated user starts"""
        # Load sample images for testing
        self.sample_images = []
        sample_dir = Path("sample_images")

        if sample_dir.exists():
            # Collect all sample images
            for class_dir in sample_dir.iterdir():
                if class_dir.is_dir():
                    for img in class_dir.glob("*.jpg"):
                        self.sample_images.append(img)

        if not self.sample_images:
            print("⚠️ No sample images found. Create sample_images/ directory with test images.")

    @task(3)
    def predict_image(self):
        """Make a prediction (most common task - weight=3)"""
        if not self.sample_images:
            return

        # Randomly select an image
        image_path = random.choice(self.sample_images)

        with open(image_path, 'rb') as f:
            files = {'file': (image_path.name, f, 'image/jpeg')}
            response = self.client.post("/predict", files=files)

            if response.status_code == 200:
                data = response.json()
                # Optionally validate response structure
                assert 'predicted_class' in data
                assert 'confidence' in data
    
    @task(1)
    def health_check(self):
        """Check API health (less frequent - weight=1)"""
        self.client.get("/health")

    @task(1)
    def get_classes(self):
        """Get available classes (less frequent - weight=1)"""
        self.client.get("/classes")
