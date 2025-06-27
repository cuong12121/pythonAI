import os
import re
import cv2
import pytesseract
import sys
import io
import time
import numpy as np
import gc
from pdf2image import convert_from_path

# import redis
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
        # scale = 4
        # new_width = img.width * scale
        # new_height = img.height * scale
        # img.resize(new_width, new_height)

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
def cut2(filepath):

    # Đường dẫn đến file PDF
    pdf_path = filepath
    array = {}

    
      # Đường dẫn đến file PDF
    pdf_path = filepath

    # Bước 1: Đọc chỉ trang 116 (số bắt đầu từ 1)
    pages = convert_from_path(pdf_path, dpi=300, first_page=116, last_page=116)

    # Bước 2: Lấy trang 116 ra (chỉ có 1 phần tử)
    page = pages[0]  # dạng PIL.Image

    # Bước 3: Chuyển PIL → NumPy → OpenCV (BGR)
    open_cv_image = np.array(page.convert('RGB'))
    img = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)

    # Bước 4: Cắt vùng theo tọa độ [y1:y2, x1:x2]
    # Ví dụ: cắt vùng từ dòng 100 đến 400 và cột 200 đến 600
    cropped = img[1900:2900, 82:170]  # vì 82+88=170


    cv2.imwrite("cropped_page116.png", cropped)

    text = pytesseract.image_to_string(cropped, config='--oem 3 --psm 6', lang="eng+vie")

    skuss = re.sub(r"[^a-zA-Z0-9\- ]", "", text)

    skuss = skuss.replace('SKU', '')

    pattern = r'\b[A-Za-z0-9]{4}\s*-\s*[A-Za-z]{2}\s*-\s*\d{2}\b'

    clean_text = skuss.replace('\n', ' ').replace('\r', ' ')

    skusss = re.findall(pattern, clean_text)

    if not skusss:
        rs = skuss
    else:
        rs = skusss

    array.append({
        'sku': rs
    }) 
            
    return(array)   


def sku(output_file):
     # Load ảnh
    img = cv2.imread(output_file)

    # open_cv_image = np.array(output_file.convert('RGB'))

    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # B3: Làm nét + threshold (giúp OCR chuẩn hơn)
    sharpen_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened = cv2.filter2D(gray, -1, sharpen_kernel)
    _, thresh = cv2.threshold(sharpened, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # B4: OCR với Tesseract
    custom_config = r'--oem 3 --psm 6'

    result = pytesseract.image_to_string(img, config=custom_config)
    return result 
array = cut2(input_file)

# cut(input_file, output_file,116)  
# skus = sku(output_file) 
# skuss = re.sub(r"[^a-zA-Z0-9\- ]", "", skus)


# skuss = skuss.replace('SKU', '')

# pattern = r'\b[A-Za-z0-9]{4}\s*-\s*[A-Za-z]{2}\s*-\s*\d{2}\b'


# clean_text = skuss.replace('\n', ' ').replace('\r', ' ')

# skusss = re.findall(pattern, clean_text)
# if not skusss:
#     rs = skuss
# else:
#     rs = skusss



# array.append({
#     'sku': rs
# }) 



# for i in range(so_trang):
#     cut(input_file, output_file,i)  
#     skus = sku(output_file) 
#     skuss = re.sub(r"[^a-zA-Z0-9\- ]", "", skus)


#     skuss = skuss.replace('SKU', '')

#     pattern = r'\b[A-Za-z0-9]{4}\s*-\s*[A-Za-z]{2}\s*-\s*\d{2}\b'


#     clean_text = skuss.replace('\n', ' ').replace('\r', ' ')

#     skusss = re.findall(pattern, clean_text)
#     if not skusss:
#         rs = skuss
#     else:
#         rs = skusss



#     array.append({
#         'sku': rs
#     }) 




# r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

# key_name = "orders:data_sku_1"

# # Nếu key tồn tại thì xóa


# Ghi dữ liệu mới
orders_json = json.dumps(array)
# r.set(key_name, orders_json)

print(orders_json)

