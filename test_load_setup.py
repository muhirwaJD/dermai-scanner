"""Quick test script for API and Locust"""
import subprocess
import time
import requests
import sys
from pathlib import Path

print("🧪 Testing Load Testing Setup")
print("=" * 60)

# Test 1: Check if API dependencies are installed
print("\n1️⃣ Checking dependencies...")
try:
    import fastapi
    import uvicorn
    import locust
    print("✅ All dependencies installed")
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    sys.exit(1)

# Test 2: Start API server
print("\n2️⃣ Starting API server...")
python_path = "/Users/muhirwa/Desktop/projects/test/test/bin/python"
api_process = subprocess.Popen(
    [python_path, "-m", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

# Wait for server to start
print("⏳ Waiting for server...")
for i in range(10):
    time.sleep(1)
    try:
        response = requests.get("http://localhost:8000/health", timeout=2)
        if response.status_code == 200:
            print(f"✅ API server is running!")
            print(f"   Response: {response.json()}")
            break
    except requests.exceptions.ConnectionError:
        print(f"   Attempt {i+1}/10...")
else:
    print("❌ API server failed to start")
    api_process.kill()
    sys.exit(1)

# Test 3: Test prediction endpoint with sample image
print("\n3️⃣ Testing /predict endpoint...")
sample_dir = Path("sample_images")
if sample_dir.exists():
    # Find first image
    for class_dir in sample_dir.iterdir():
        if class_dir.is_dir():
            images = list(class_dir.glob("*.jpg"))
            if images:
                test_image = images[0]
                print(f"   Using test image: {test_image}")
                
                with open(test_image, 'rb') as f:
                    files = {'file': (test_image.name, f, 'image/jpeg')}
                    response = requests.post("http://localhost:8000/predict", files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ Prediction successful!")
                    print(f"   Class: {result['predicted_class']}")
                    print(f"   Confidence: {result['confidence']:.2%}")
                else:
                    print(f"❌ Prediction failed: {response.status_code}")
                break

# Test 4: Check Locust file
print("\n4️⃣ Checking locustfile.py...")
if Path("locustfile.py").exists():
    print("✅ locustfile.py exists")
else:
    print("❌ locustfile.py not found")

# Instructions
print("\n" + "=" * 60)
print("📊 NEXT STEPS FOR LOAD TESTING:")
print("=" * 60)
print("\n1. API is running on http://localhost:8000")
print("\n2. Open a NEW terminal and run:")
print("   cd /Users/muhirwa/Desktop/projects/test")
print("   /Users/muhirwa/Desktop/projects/test/test/bin/python -m locust --host=http://localhost:8000")
print("\n3. Open browser: http://localhost:8089")
print("\n4. Start test with:")
print("   - Number of users: 10")
print("   - Spawn rate: 2")
print("\n5. When done, press Ctrl+C here to stop the API")
print("=" * 60)

# Keep API running
try:
    print("\n⏸️  API is running. Press Ctrl+C to stop...")
    api_process.wait()
except KeyboardInterrupt:
    print("\n\n🛑 Stopping API server...")
    api_process.terminate()
    api_process.wait()
    print("✅ Done!")
