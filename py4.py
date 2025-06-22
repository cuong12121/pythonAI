import cv2
import numpy as np
import pytesseract
import os
import io
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))

output_file = os.path.join(current_dir, 'cropped_image.png')

# Load the image
image = cv2.imread(output_file)

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to reduce noise
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Detect edges using Canny
edges = cv2.Canny(blurred, 50, 150)

# Find lines using Hough Transform
lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)

# Create a white mask
mask = np.ones(image.shape[:2], dtype=np.uint8) * 255

# Draw lines on the mask (remove borders)
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(mask, (x1, y1), (x2, y2), 0, 3)

# Apply mask to remove borders on the original image
result = image.copy()
result[mask == 0] = [255, 255, 255]  # Replace borders with white

# Perform OCR to detect text
ocr_result = pytesseract.image_to_data(result, output_type=pytesseract.Output.DICT)

# Create a mask for letters
text_mask = np.ones(result.shape[:2], dtype=np.uint8) * 255

# Iterate through OCR results
for i, text in enumerate(ocr_result['text']):
    if text.strip():  # Check if text is not empty
        # Check if the text contains only letters (no numbers)
        if text.isalpha():  # Only letters
            x, y, w, h = ocr_result['left'][i], ocr_result['top'][i], ocr_result['width'][i], ocr_result['height'][i]
            # Draw a white rectangle over the letters
            cv2.rectangle(text_mask, (x, y), (x + w, y + h), 0, -1)

# Apply text mask to remove letters
result[text_mask == 0] = [255, 255, 255]  # Replace letters with white

# Save or display the result
cv2.imwrite('result_no_letters.png', result)

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


# Load ảnh
image = cv2.imread('result_no_letters.png')  # thay bằng đường dẫn ảnh của bạn

# Chuyển sang xám
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Làm nét và threshold nhẹ (tùy ảnh)
gray = cv2.bilateralFilter(gray, 11, 17, 17)
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# OCR chỉ lấy số
custom_config = r'--oem 3 --psm 6 outputbase digits'
result = pytesseract.image_to_string(thresh, config=custom_config)

print(result)
# cv2.imshow('Result', result)
# cv2.waitKey(0)
# cv2.destroyAllWindows()