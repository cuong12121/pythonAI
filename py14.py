import os
import re
import cv2
import pytesseract
import sys
import io
import numpy as np
import redis
import json
import time
from PIL import Image
from wand.image import Image
from wand.color import Color
sys.stdout.reconfigure(encoding='utf-8')


def count_pdf_pages(input_file):
    with Image(filename=input_file) as img:
        return len(img.sequence)



# print(f"Số trang PDF: {so_trang}")

# exit()
def cut(input_file, output_file, page):
    # Initialize Imagick equivalent
    with Image(filename=f'{input_file}[{page}]', resolution=(300, 300)) as img:
        # Convert to grayscale
        img.transform_colorspace('gray')
        
        for _ in range(3):
            img.contrast()
        
        # Crop image (x, y, width, height)
        x = 82
        y = 1900
        width = 88
        height = 1000
        img.crop(x, y, width=width, height=height)

        # 2. Resize (phóng to) – scale 2~4 lần là hợp lý
        scale = 4
        new_width = img.width * scale
        new_height = img.height * scale
        img.resize(new_width, new_height)

        # 3. Enhance màu sắc (tăng sáng, đậm màu, chỉnh màu)
        img.modulate(brightness=200, saturation=200, hue=100)

        # 4. Làm nét ảnh (sharpen)
        img.sharpen(radius=1, sigma=2)

        # 5. (Tùy chọn) chuyển ảnh về grayscale để OCR dễ hơn
        img.type = 'grayscale'

       
        # Set output format to PNG
        img.format = 'png'
        
        # Save the output
        img.save(filename=output_file)
def sku(output_file):
     # Load ảnh
    img = cv2.imread(output_file)

    # Resize ảnh để tăng độ chính xác
    scale_percent = 300
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    img = cv2.resize(img, (width, height), interpolation=cv2.INTER_CUBIC)

    # Chuyển ảnh sang trắng đen
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # OCR
    custom_config = r'--oem 3 --psm 6'
    result = pytesseract.image_to_string(thresh, config=custom_config, lang='eng+vie')
    return result 


# Define file paths (equivalent to __DIR__ in PHP)
current_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(current_dir, 't37.pdf')
output_file = os.path.join(current_dir, 'cropped1169.png')

array =[]
so_trang = count_pdf_pages(input_file)

for i in range(so_trang):
    cut(input_file, output_file,i)  
    skus = sku(output_file) 
    skuss = re.sub(r"[^a-zA-Z0-9\- ]", "", skus)


    skuss = skuss.replace('SKU', '')

    pattern = r'\b[A-Za-z0-9]{4}\s*-\s*[A-Za-z]{2}\s*-\s*\d{2}\s*-\s*[A-Za-z]{3}\b'


    clean_text = skuss.replace('\n', ' ').replace('\r', ' ')

    skusss = re.findall(pattern, clean_text)
    if not skusss:
        rs = skuss
    else:
        rs = skusss

    
  
    array.append({
        'sku': rs
    }) 




r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

key_name = "orders:data_sku_1"

# Nếu key tồn tại thì xóa


# Ghi dữ liệu mới
orders_json = json.dumps(array)
r.set(key_name, orders_json)

print('thành công')

