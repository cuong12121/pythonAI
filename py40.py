
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
import fitz

import redis
import json
import time
from PIL import Image
from wand.image import Image
from wand.color import Color

sys.stdout.reconfigure(encoding='utf-8')

current_dir = os.path.dirname(os.path.abspath(__file__))

def pdf_to_text(pdf_path, page):
	index = page-1
	doc = fitz.open(pdf_path)
	text = ""
	page1 = doc[index]  # Trang 1 = index 0
	text = page1.get_text()
	return text
def count_pdf_pages(input_file):
    with Image(filename=input_file) as img:
        return len(img.sequence)




def cut2(input_file):
	so_trang = count_pdf_pages(input_file)
	array = []
	dem=0 
	for k in range(so_trang):
		dem += 1
		text = pdf_to_text(input_file,dem)

		lines = text.splitlines()

		# Tìm dòng bắt đầu từ "Phân loại hàng" đến dòng chứa "tiền"
		start_index = None
		for i in range(len(lines)):
		    if "Phân loại hàng" in lines[i]:
		        if i + 1 < len(lines) and "tiền" in lines[i + 1]:
		            start_index = i + 2  # dữ liệu bắt đầu từ dòng sau
		            break

		# Lấy phần text sau đoạn đó
		if start_index is not None:
			remaining_text = "\n".join(lines[start_index:])

		    # Xóa dòng chỉ chứa số 1 đến 9
			cleaned_text = re.sub(r'^\s*[1-9]\s*$', '', remaining_text, flags=re.MULTILINE)

			# Xóa các dòng trống còn lại sau khi xóa
			cleaned_text = re.sub(r'\n+', '\n', cleaned_text).strip()

		    # Bỏ xuống dòng giữa các phần mã
			text_no_breaks = cleaned_text.replace('\n', '')



			# Regex nhận dạng SKU dạng: 650J-NA-00-UPS-00-001
			pattern = r'[A-Za-z0-9]{4}-[a-zA-Z]{2}-\d{2}-[A-Za-z]{3}'

			matches = re.findall(pattern, text_no_breaks)

			rs =list(dict.fromkeys(matches))
			
			array.append({
		        'sku': rs
		    }) 
			

			print(dem, flush=True)

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
