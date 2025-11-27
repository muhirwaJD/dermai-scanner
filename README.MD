# DermAI Scanner 🔬

A machine learning-powered skin condition analysis application built with Streamlit and TensorFlow. This app helps identify potential skin conditions through image analysis.

## Video Demo

Watch the complete project walkthrough and demonstration:  
**[YouTube Demo](https://youtu.be/nnhMq1QnuOo)**

## Features

- Image-based skin condition analysis
- Powered by TensorFlow and Keras
- Interactive visualizations with matplotlib and seaborn
- RESTful API with FastAPI
- User-friendly web interface with Streamlit
- Performance testing with Locust

## Prerequisites

- Python 3.10.14
- macOS (for tensorflow-metal support) or other OS (remove tensorflow-metal from requirements)
- pyenv (recommended for Python version management)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/muhirwaJD/dermai-scanner.git
cd dermai-scanner
```

### 2. Set up Python environment

If you're using pyenv:

```bash
pyenv install 3.10.14
pyenv local 3.10.14
```

### 3. Create a virtual environment

```bash
python -m venv test
```

### 4. Activate the virtual environment

```bash
source test/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

**Note:** If you're not on macOS with Apple Silicon, remove `tensorflow-metal==1.2.0` from `requirements.txt` before installing.

## Usage

### Running the Streamlit App

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

### Running the API Server

```bash
uvicorn api:app --reload
```

The API will be available at `http://localhost:8000`

### Running Performance Tests with Locust

Create a `locustfile.py` in the project root, then run:

```bash
# With web UI
locust -f locustfile.py --host=http://localhost:8501

# Headless mode (50 users, 5/sec spawn rate, 2 min duration)
locust -f locustfile.py --host=http://localhost:8501 --users 50 --spawn-rate 5 --run-time 2m --headless
```

Access the Locust web interface at `http://localhost:8089` to configure users and view real-time performance metrics.

### Running Tests

```bash
pytest
```

## Project Structure

```
dermai-scanner/
├── app.py              # Main Streamlit application
├── locustfile.py       # Performance tests (optional)
├── requirements.txt    # Python dependencies
├── test/              # Virtual environment
├── models/            # Trained ML models (not in repo)
├── data/              # Training/test data (not in repo)
└── .gitignore         # Git ignore rules
```

## Configuration

- **Model Files:** Place your trained model files in the `models/` directory
- **Data:** Training and testing data should be placed in the `data/` directory
- Both directories are git-ignored for security and size reasons

## Technologies Used

- **Frontend:** Streamlit 1.51.0
- **ML Framework:** TensorFlow 2.16.2, Keras 3.12.0
- **API:** FastAPI 0.122.0
- **Data Processing:** Pandas 2.3.3, NumPy 1.26.4
- **Visualization:** Matplotlib 3.10.7, Seaborn 0.13.2
- **Testing:** pytest 9.0.1
- **Performance Testing:** Locust 2.42.5

## Hardware Acceleration

This project supports Apple Silicon GPU acceleration via `tensorflow-metal`. If you're on a different platform, you may need to adjust the TensorFlow installation.

## Troubleshooting

### Virtual Environment Issues

If you encounter issues with the virtual environment after renaming the project folder, recreate it:

```bash
rm -rf test
python -m venv test
source test/bin/activate
pip install -r requirements.txt
```

### Streamlit Command Not Found

Use the full Python path:
```bash
/path/to/your/project/test/bin/python -m streamlit run app.py
```

### TensorFlow Metal Issues

If you're on macOS but encounter metal-related errors:
1. Ensure you have macOS 12.0+ 
2. Update Xcode Command Line Tools: `xcode-select --install`
3. Try reinstalling: `pip uninstall tensorflow-metal && pip install tensorflow-metal==1.2.0`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Add your license here]

## Disclaimer

⚠️ **Medical Disclaimer:** This application is for educational and informational purposes only. It is not intended to be a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.

## Contact

[Add your contact information or links here]

## Acknowledgments

- TensorFlow team for the ML framework
- Streamlit for the amazing web app framework
- HAM10000 dataset contributors