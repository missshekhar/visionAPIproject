# Vision API Project

This project is a web application that performs image analysis using the Google Cloud Vision API. It allows users to upload images and receive detailed analysis, including text detection, label detection, face detection, landmark detection, logo detection, and image properties detection. Additionally, it performs basic image segmentation using OpenCV.

## Features

- Image upload and analysis via a web interface.
- Optical Character Recognition (OCR) to extract text from images.
- Detection of labels, faces, landmarks, logos, and image properties.
- Basic image segmentation.
- Display of analysis results in a user-friendly format.

## Requirements

- Python 3.x
- Flask
- OpenCV
- Google Cloud Vision API

## Installation

1. **Clone the repository**:
   ```
   git clone https://github.com/missshekhar/visionAPIproject.git
   cd visionAPIproject
   ```
2. **Create virtual environment**:
   ```
   python -m venv env
   env\Scripts\activate   <- on Windows
   ```
3. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```
4. **Set up Google Cloud credentials**
   ```
   export GOOGLE_APPLICATION_CREDENTIALS="YOUR_API.json"
   ```
   
## Usage

1. **Run the Flask application**:
   ```
   python app.py
   ```
2. **Access the application**:.
   - Open a web browser and navigate to http://localhost:5000
3. **Upload an image**:.
   - Use the provided form to upload an image.
   - View the analysis results displayed on the webpage.

## Project Structure

- app.py: Main application file containing the Flask app and routes.
- requirements.txt: List of Python dependencies.
- templates/: Folder containing HTML templates.
- index.html: Main template for the web interface.
- static/: Folder containing static assets such as CSS, JavaScript, and images.
- style.css: CSS file for styling the web interface.
- script.js: JavaScript file for handling frontend interactions.
- .gitignore: File specifying which files and directories to ignore in version control.