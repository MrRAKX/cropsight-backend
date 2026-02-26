from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from ai_engine import analyze_image

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return "Cropsight Backend Running"

@app.route("/upload-crop", methods=["POST"])
def upload_crop():
    crop_type = request.form.get("crop_type")
    file = request.files["image"]
    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    result = analyze_image(file_path, crop_type)
    
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)