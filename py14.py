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



# Define file paths (equivalent to __DIR__ in PHP)
current_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(current_dir, 't37.pdf')
output_file = os.path.join(current_dir, 'cropped1169.png')

array =[]


def count_pdf_pages(input_file):
    with Image(filename=input_file) as img:
        return len(img.sequence)


so_trang = count_pdf_pages(input_file)
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
        # scale = 3
        # new_width = img.width * scale
        # new_height = img.height * scale
        # img.resize(new_width, new_height)

        # # 3. Enhance màu sắc (tăng sáng, đậm màu, chỉnh màu)
        # img.modulate(brightness=200, saturation=200, hue=100)

        # # 4. Làm nét ảnh (sharpen)
        # # img.sharpen(radius=1, sigma=7)

        # # 5. (Tùy chọn) chuyển ảnh về grayscale để OCR dễ hơn
        # img.type = 'grayscale'

       
        # Set output format to PNG
        img.format = 'png'
        
        # Save the output
        img.save(filename=output_file)
def sku(output_file):
     # Load ảnh
    image = cv2.imread(output_file)  # thay bằng đường dẫn ảnh của bạn

    # Chuyển sang xám
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Làm nét và threshold nhẹ (tùy ảnh)
    # gray = cv2.bilateralFilter(gray, 11, 17, 17)
    # _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # OCR chỉ lấy số
    custom_config = r'--oem 3 --psm 11'
    result = pytesseract.image_to_string(image, config=custom_config, lang='vie+eng')  # nếu có tiếng Việt
    return result 


for i in range(so_trang):
    cut(input_file, output_file,i)  
    skus = sku(output_file) 

    pattern = r'\b[A-Za-z0-9]{4}\s*-\s*[A-Za-z]{2}\s*-\s*\d{2}\s*-\s*[A-Za-z]{3}\b'

    clean_text = skus.replace('\n', ' ').replace('\r', ' ')

    skuss = re.findall(pattern, clean_text)
    time.sleep(6)  
  
    array.append({
        'sku': skuss
    }) 

    print('đã chạy xong trang'{i})

r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

key_name = "orders:data_sku_1"

# Nếu key tồn tại thì xóa


# Ghi dữ liệu mới
orders_json = json.dumps(array)
r.set(key_name, orders_json)

