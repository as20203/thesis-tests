import cv2
import pytesseract
from PIL import Image, ImageEnhance
import numpy as np

def preprocess_image(image_path):
    # Read the image using OpenCV
    image = cv2.imread(image_path)

    # Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply sharpening filter
    kernel = np.array([[0, -1, 0], 
                       [-1, 5,-1], 
                       [0, -1, 0]])
    sharpened_image = cv2.filter2D(gray_image, -1, kernel)

    # Apply adaptive thresholding to get a binary image
    binary_image = cv2.adaptiveThreshold(sharpened_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # Invert the image to get black text on white background
    inverted_image = cv2.bitwise_not(binary_image)

    # Apply morphological operations
    kernel = np.ones((1, 1), np.uint8)
    processed_image = cv2.morphologyEx(inverted_image, cv2.MORPH_CLOSE, kernel)

    # Save the processed image for debugging (optional)
    cv2.imwrite("processed_image.png", processed_image)

    return processed_image

# Path to the image
image_path = 'loren-ipsum/loren_ipsum_scan.jpg'

# Preprocess the image
preprocessed_image = preprocess_image(image_path)

# Convert the OpenCV image to PIL format
pil_image = Image.fromarray(preprocessed_image)

# Enhance the image contrast
enhancer = ImageEnhance.Contrast(pil_image)
enhanced_image = enhancer.enhance(2)

# Use pytesseract to do OCR on the preprocessed image
custom_config = r'--oem 3 --psm 6'
text = pytesseract.image_to_string(enhanced_image, config=custom_config)

# Print the extracted text
print(text)