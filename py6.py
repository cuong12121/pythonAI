import os
import re
import cv2
import pytesseract


import sys
import io
from PIL import Image
from wand.image import Image
from wand.color import Color

# Define file paths (equivalent to __DIR__ in PHP)
current_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(current_dir, 't20.pdf')
output_file = os.path.join(current_dir, 'cropped11698.png')

# Initialize Imagick equivalent
with Image(filename=f'{input_file}[0]', resolution=(300, 300)) as img:
    # Convert to grayscale
    img.transform_colorspace('gray')
    
    for _ in range(3):
        img.contrast()
    
    # Enhance image (similar to enhanceImage in PHP Imagick)
    img.modulate(brightness=300, saturation=300, hue=300)
    
    # Sharpen image (radius=2, sigma=1)
    img.sharpen(radius=2, sigma=1)


    
    # Crop image (x, y, width, height)
    x = 400
    y = 130
    width = 720
    height = 210
    img.crop(x, y, width=width, height=height)
    
    # Set output format to PNG
    img.format = 'png'
    
    # Save the output
    img.save(filename=output_file)

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Chỉ định đường dẫn Tesseract nếu cần
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load ảnh
image = cv2.imread(output_file)  # thay bằng đường dẫn ảnh của bạn

# Chuyển sang xám
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Làm nét và threshold nhẹ (tùy ảnh)
gray = cv2.bilateralFilter(gray, 11, 17, 17)
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# OCR chỉ lấy số
custom_config = r'--oem 3 --psm 6'
result = pytesseract.image_to_string(image, config=custom_config, lang='vie')  # nếu có tiếng Việt

def extract_ma_van_don(text):
    match = re.search(r'Mã vận đơn[.: ]+\s*([A-Z0-9]+)', text)
    return match.group(1) if match else ""

def extract_ma_don_hang(text):
    match = re.search(r'Mã đơn hàng[.: ]+\s*([A-Z0-9]+)', text)
    return match.group(1) if match else ""  


value = extract_ma_van_don(result)


value_ma_don_hang = extract_ma_don_hang(result)



arrayvd = [value, value_ma_don_hang]


print(arrayvd)
