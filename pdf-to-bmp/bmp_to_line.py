import cv2
import numpy as np

def extract_text_pixels(image_path):
    # Read the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Threshold the image to create a binary image
    _, binary_image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # Invert the binary image to get text pixels as white
    inverted_image = cv2.bitwise_not(binary_image)

    return inverted_image