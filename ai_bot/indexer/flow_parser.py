import cv2
import numpy as np
import pytesseract
from PIL import Image

def detect_shapes_and_arrows(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Preprocessing
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 150)

    # Find contours
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    shapes = []
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.03 * cv2.arcLength(contour, True), True)
        x, y, w, h = cv2.boundingRect(approx)

        shape_type = "unknown"
        if len(approx) == 4:
            aspect_ratio = w / float(h)
            if 0.95 <= aspect_ratio <= 1.05:
                shape_type = "decision"  # Diamond-like
            else:
                shape_type = "process"  # Rectangle
        elif len(approx) > 4:
            shape_type = "start/end"  # Ellipse-like

        # OCR inside shape
        roi = gray[y:y + h, x:x + w]
        text = pytesseract.image_to_string(roi).strip()

        if text:
            shapes.append({
                "type": shape_type,
                "text": text,
                "position": (x, y)
            })

    # Sort shapes top to bottom
    shapes.sort(key=lambda s: s["position"][1])

    return shapes
