import cv2
import numpy as np
import pandas as pd

def analyze_image(image_path, crop_type):
    image = cv2.imread(image_path)
    
    # Blur detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()
    
    if blur_score < 50:
        return {"error": "Image too blurry"}
    
    # Brightness
    brightness = np.mean(gray)
    
    # Color score (red dominance example)
    b, g, r = cv2.split(image)
    color_score = np.mean(r)
    
    # Simple quality score
    quality_score = (color_score * 0.4) + (brightness * 0.3) + (blur_score * 0.3)
    
    # Grade
    if quality_score > 150:
        grade = "A"
        multiplier = 1.2
    elif quality_score > 100:
        grade = "B"
        multiplier = 1.0
    else:
        grade = "C"
        multiplier = 0.8
    
    # Load mandi price
    data = pd.read_csv("mandi_price.csv")
    base_price = data.loc[data["crop"] == crop_type, "base_price"].values[0]
    
    predicted_price = base_price * multiplier
    
    return {
        "quality_score": round(float(quality_score), 2),
        "grade": grade,
        "predicted_price": round(float(predicted_price), 2)
    }