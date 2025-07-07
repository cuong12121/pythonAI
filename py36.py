
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

import redis
import json
import time
from PIL import Image
from wand.image import Image
from wand.color import Color

sys.stdout.reconfigure(encoding='utf-8')

current_dir = os.path.dirname(os.path.abspath(__file__))
# so_trang = count_pdf_pages(input_file)

# input_file = os.path.join(current_dir, 't44.pdf')
# output_file = os.path.join(current_dir, 'cropped1169.png')

def cut2(input_file):

	# Đường dẫn đến file PDF
	pdf_path = input_file

	array = []

	so_trang = count_pdf_pages(input_file)
	    
	    # Đường dẫn đến file PDF
	pdf_path = filepath

	for i in range(so_trang):
		indexpage = i+1
		
		# Bước 1: Đọc chỉ trang 116 (số bắt đầu từ 1)
		pages = convert_from_path(pdf_path, dpi=500, first_page=indexpage, last_page=indexpage)

		# Bước 2: Lấy trang 116 ra (chỉ có 1 phần tử)
		page = pages[0]  # dạng PIL.Image

		# Bước 3: Chuyển PIL → NumPy → OpenCV (BGR)
		open_cv_image = np.array(page.convert('RGB'))
		img = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)

		# Bước 4: Cắt vùng theo tọa độ [y1:y2, x1:x2]
		# Ví dụ: cắt vùng từ dòng 100 đến 400 và cột 200 đến 600
		cropped = img[3350:4500, 130:270]  # vì 82+88=170

		preprocess = "thresh" 


		gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
		 
		if preprocess == "thresh":
		    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
		elif preprocess == "blur":
		    gray = cv2.medianBlur(gray, 5)


		custom_config = r'--oem 3 --psm 6'
		from PIL import Image
		# Load ảnh và apply nhận dạng bằng Tesseract OCR
		text = pytesseract.image_to_string(gray,config=custom_config, lang='eng')

		skuss = re.sub(r'[^A-Za-z0-9]+', '-', text)

	    skuss1 = skuss.replace('SKU', '')

	    skuss1 = skuss1.replace('SKU-', '')      # Xóa 'SKU nếu có dấu gạch'

	    pattern = r'\b[A-Za-z0-9]{4,5}\s*-\s*[A-Za-z]{2}\s*-\s*\d{2}\b'

	    clean_text = skuss1.replace('\n', ' ').replace('\r', ' ')

	    skusss = re.findall(pattern, clean_text)
	    skusss = [s.replace(" ", "") for s in skusss]

	    rs = skusss
	    
	    array.append({
	        'sku': rs
	    }) 
	return array    




url = "https://drive.dienmayai.com/file_in.php"

response = requests.get(url)

data = response.json()  # Tự động decode JSON thành dict
number = 0
for item in data:
    save_path = "t38.pdf"

    file_pdf = 'https://dienmayai.com/'+item['file_pdf']

    # Gửi request để tải file
    responses = requests.get(file_pdf)

    if responses.status_code == 200:

        with open(save_path, 'wb') as f:
            f.write(responses.content)
            input_file = os.path.join(current_dir, 't38.pdf')
            output_file = os.path.join(current_dir, 'cropped1169.png')

            array  = cut2(input_file)

            r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)


            number += 1

            key_name = 'orders:data_sku_'+str(number)

            # Nếu key tồn tại thì xóa


            # Ghi dữ liệu mới
            orders_json = json.dumps(array)
            r.set(key_name, orders_json)


