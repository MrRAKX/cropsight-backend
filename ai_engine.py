import cv2
import numpy as np
import pandas as pd


def analyze_image(image_path, crop_type):
    image = cv2.imread(image_path)

    if image is None:
        return {"error": "Invalid image file"}

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # -------- BLUR DETECTION --------
    blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()

    # We DO NOT reject image anymore
    blur_warning = blur_score < 5   # only warning

    # -------- BRIGHTNESS SCORE --------
    brightness = np.mean(gray)

    # Normalize brightness (0–100)
    brightness_score = min(brightness / 255 * 100, 100)

    # -------- COLOR SCORE --------
    # More red = better for tomato
    b, g, r = cv2.split(image)

    red_mean = np.mean(r)
    green_mean = np.mean(g)

    color_score = (red_mean / 255) * 100

    # -------- SIZE SCORE --------
    height, width = image.shape[:2]
    size_score = min((height * width) / (500 * 500) * 100, 100)

    # -------- FINAL QUALITY SCORE --------
    quality_score = (
        (color_score * 0.4) +
        (brightness_score * 0.3) +
        (size_score * 0.3)
    )

    # -------- GRADE --------
    if quality_score > 80:
        grade = "A"
        multiplier = 1.2
    elif quality_score > 60:
        grade = "B"
        multiplier = 1.0
    else:
        grade = "C"
        multiplier = 0.8

    # -------- LOAD MANDI PRICE --------
    try:
        data = pd.read_csv("mandi_price.csv")
        row = data[data["crop"] == crop_type]

        if row.empty:
            base_price = 20  # default fallback
        else:
            base_price = float(row["base_price"].values[0])

    except Exception:
        base_price = 20  # fallback if CSV fails

    predicted_price = base_price * multiplier

    return {
        "quality_score": round(float(quality_score), 2),
        "grade": grade,
        "predicted_price": round(float(predicted_price), 2),
        "blur_score": round(float(blur_score), 2),
        "blur_warning": blur_warning
    }