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
import requests
# import redis
import json
import time
from PIL import Image
from wand.image import Image
from wand.color import Color

sys.stdout.reconfigure(encoding='utf-8')

current_dir = os.path.dirname(os.path.abspath(__file__))
# so_trang = count_pdf_pages(input_file)

input_file = os.path.join(current_dir, 't46.pdf')
# output_file = os.path.join(current_dir, 'cropped1169.png')

def count_pdf_pages(input_file):
    with Image(filename=input_file) as img:
        return len(img.sequence)

def cut2(input_file):

	# Đường dẫn đến file PDF
	pdf_path = input_file

	array = []

	so_trang = count_pdf_pages(input_file)
	dem=0 
	for i in range(so_trang):
		indexpage = i+1
		
		# Bước 1: Đọc chỉ trang 116 (số bắt đầu từ 1)
		pages = convert_from_path(pdf_path, dpi=600, first_page=indexpage, last_page=indexpage)

		# Bước 2: Lấy trang 116 ra (chỉ có 1 phần tử)
		page = pages[0]  # dạng PIL.Image

		# Bước 3: Chuyển PIL → NumPy → OpenCV (BGR)
		open_cv_image = np.array(page.convert('RGB'))
		

		gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
		gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

		# Bước 4: Cắt vùng theo tọa độ [y1:y2, x1:x2]
		# Ví dụ: cắt vùng từ dòng 100 đến 400 và cột 200 đến 600
		cropped = gray[3800:5500, 170:340]  # vì 82+88=170

		
		 
		# if preprocess == "thresh":
		#     gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
		# elif preprocess == "blur":
		#     gray = cv2.medianBlur(gray, 5)

		custom_config = r'--oem 3 --psm 6'

		# from PIL import Image
		# Load ảnh và apply nhận dạng bằng Tesseract OCR
		text = pytesseract.image_to_string(cropped,config=custom_config, lang='vie-best2')

		# lines = [line.strip() for line in text.split('\n') if line.strip()]

		# # Kiểm tra dòng 2 (chỉ khi có ít nhất 2 dòng)
		# if len(lines) >= 2:
		#     line2 = lines[1]

		#     if len(line2) >= 2 and line2[3] == '0':
		#         text = pytesseract.image_to_string(cropped,config=custom_config, lang='eng')

		skuss = re.sub(r'[^A-Za-z0-9]+', '-', text)

		skuss1 = skuss.replace('SKU', '')

		skuss1 = skuss1.replace('SKU-','')

		pattern = r'\b[A-Za-z0-9]{4,5}\s*-\s*[A-Za-z]{2}\s*-\s*\d{2}\b'

		clean_text = skuss1.replace('\n', ' ').replace('\r', ' ')

		skusss = re.findall(pattern, clean_text)
		skusss = [s.replace(" ", "") for s in skusss]

		rs = skusss

		print(text)

		exit()
	    
		array.append({
	        'sku': rs
	    }) 
		dem += 1

		print(dem, flush=True)
	return array
array  = cut2(input_file)
orders_json = json.dumps(array)
print(orders_json)

