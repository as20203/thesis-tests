import cv2
import pytesseract

# Read the image
image_path = 'loren-ipsum/loren_ipsum_scan.jpg'
image = cv2.imread(image_path)

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to remove noise
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# Apply thresholding to get a binary image
_, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Perform dilation and erosion to remove noise
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
dilated = cv2.dilate(binary, kernel, iterations=1)
eroded = cv2.erode(dilated, kernel, iterations=1)

# Perform edge detection
edges = cv2.Canny(eroded, 100, 200)

# Optionally, resize the image if needed
# resized = cv2.resize(edges, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

# # Deskewing (if necessary)
# coords = cv2.findNonZero(edges)  # Find all non-zero points (text)
# angle = cv2.minAreaRect(coords)[-1]  # Find minimum area rectangle
# if angle < -45:
#     angle = -(90 + angle)
# else:
#     angle = -angle

# (h, w) = edges.shape[:2]
# center = (w // 2, h // 2)
# M = cv2.getRotationMatrix2D(center, angle, 1.0)
# deskewed = cv2.warpAffine(edges, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

# Save or display the preprocessed image (for debugging)
cv2.imwrite('preprocessed_image.png', edges)

data = pytesseract.image_to_data(edges,config='--oem 3 --psm 6', output_type='dict')

print(data)