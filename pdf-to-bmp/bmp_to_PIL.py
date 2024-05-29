import cv2
import pytesseract
import re

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    _,image = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    # binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    # binary = cv2.medianBlur(binary, 3)
    
    # coords = cv2.findNonZero(binary)
    # angle = cv2.minAreaRect(coords)[-1]
    # if angle < -45:
    #     angle = -(90 + angle)
    # else:
    #     angle = -angle
    
    # (h, w) = binary.shape[:2]
    # center = (w // 2, h // 2)
    # M = cv2.getRotationMatrix2D(center, angle, 1.0)
    # rotated = cv2.warpAffine(binary, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    
    return image

def extract_text(image):
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(image, config=custom_config)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text

def correct_text(text, sym_spell):
    suggestions = sym_spell.lookup_compound(text, max_edit_distance=2)
    return suggestions[0].term if suggestions else text

if __name__ == "__main__":
    image_path = 'loren-ipsum/loren_ipsum_text_thesis.result.copy-0.jpg'
    # image_path = 'loren-ipsum/loren_ipsum_text_thesis.jpg'

    preprocessed_image = preprocess_image(image_path)
    raw_text = extract_text(preprocessed_image)
    print(raw_text)
    
   
    
