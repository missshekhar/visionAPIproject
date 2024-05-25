from flask import Flask, render_template, request, jsonify, url_for
from google.cloud import vision
import os
import cv2
import logging
import tempfile

app = Flask(__name__)

# Paste your API key in place of "API_KEY"!!!
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "API_KEY"

def segment_image(image_path):
    try:
        image = cv2.imread(image_path)

        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        _, segmented_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)

        segmented_image_path = "static/segmented_image.jpg"
        cv2.imwrite(segmented_image_path, segmented_image)

        return segmented_image_path
    except Exception as e:
        logging.error(f"Error during image segmentation: {e}")
        return None

def format_ocr_results(text_annotations):
    
    if text_annotations:
        first_description = text_annotations[0].description
        return first_description.replace("\n", "<br>")
    else:
        return "No text to extract found."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_image():
    try:
        if "image" not in request.files:
            logging.error("No file uploaded")
            return jsonify({"error": "No file uploaded"}), 400

        image_file = request.files["image"]

        with tempfile.NamedTemporaryFile(delete=False) as temp_image_file:
            temp_image_path = temp_image_file.name
            image_file.save(temp_image_path)

        # OCR
        client = vision.ImageAnnotatorClient()
        with open(temp_image_path, 'rb') as image_file:
            image_content = image_file.read()
        image = vision.Image(content=image_content)
        text_response = client.text_detection(image=image)
        extracted_text = format_ocr_results(text_response.text_annotations)

        os.unlink(temp_image_path)

        image = vision.Image(content=image_content)
        label_response = client.label_detection(image=image)
        labels = [label.description for label in label_response.label_annotations]

        face_response = client.face_detection(image=image)
        faces = face_response.face_annotations

        landmark_response = client.landmark_detection(image=image)
        landmarks = [landmark.description for landmark in landmark_response.landmark_annotations]

        logo_response = client.logo_detection(image=image)
        logos = [logo.description for logo in logo_response.logo_annotations]

        properties_response = client.image_properties(image=image)
        dominant_colors = properties_response.image_properties_annotation.dominant_colors.colors
        colors = [{'color': (color.color.red, color.color.green, color.color.blue), 'score': color.score} for color in dominant_colors]

        # Segmentation
        uploaded_image_path = "static/uploaded_image.jpg"
        with open(uploaded_image_path, 'wb') as uploaded_image_file:
            uploaded_image_file.write(image_content)
        segmented_image_path = segment_image(uploaded_image_path)

        if not segmented_image_path:
            logging.error("Image segmentation failed")
            return jsonify({"error": "Image segmentation failed"}), 500

        description = f"The image contains: {', '.join(labels)}.<br>"
        
        if faces:
            num_faces = len(faces)
            description += f"{num_faces} face(s) detected.<br>"

            for i, face in enumerate(faces):
                description += f"Face {i+1}:<br>"

                headwear_status = "not wearing" if face.headwear_likelihood >= 1 else "wearing"
                description += f"The person is {headwear_status} headwear.<br>"

                frontal_gaze = "not looking straight" if abs(face.pan_angle) >= 15 else "looking straight"
                description += f"The person is {frontal_gaze}.<br>"

                eyes_visibility = "not visible" if face.under_exposed_likelihood >= 3 else "visible"
                description += f"The person's eyes are {eyes_visibility}.<br>"

                glasses_status = "not wearing" if face.under_exposed_likelihood >= 1 else "wearing"
                description += f"The person is {glasses_status} glasses.<br>"

        if landmarks:
            description += f"Landmarks identified: {', '.join(landmarks)}.<br>"
        if logos:
            description += f"Logos detected: {', '.join(logos)}.<br>"
        if dominant_colors:
            colors_description = ', '.join([f"rgb({c['color'][0]}, {c['color'][1]}, {c['color'][2]}) with a score of {c['score']:.2f}" for c in colors])
            description += f"Dominant colors are: {colors_description}.<br>"

        # Prepare data
        analysis_results = {
            "description": description,
            "extracted_text": extracted_text,
            "segmented_image": url_for('static', filename='segmented_image.jpg')
        }
        
        return jsonify(analysis_results)

    except Exception as e:
        logging.error(f"Error during image upload and analysis: {e}")
        return jsonify({"error": "Something went wrong"}), 500

if __name__ == "__main__":
    app.run(debug=True)
