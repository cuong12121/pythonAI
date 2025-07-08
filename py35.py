
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

# import redis
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





# so_trang = count_pdf_pages(input_file)

input_file = os.path.join(current_dir, 't46.pdf')


text = pdf_to_text(input_file,14)

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
	pattern = r'[A-Za-z0-9]{4,5}-[A-Za-z]{2}-\d{2}-[A-Za-z]{3}'

	matches = re.findall(pattern, text_no_breaks)

	matches =list(dict.fromkeys(matches))

	print(text_no_breaks)

	exit()

	




exit()

# Đường dẫn đến file PDF
pdf_path = input_file
i=0
# indexpage = i+1
indexpage =1
# Bước 1: Đọc chỉ trang 116 (số bắt đầu từ 1)
pages = convert_from_path(pdf_path, dpi=600, first_page=indexpage, last_page=indexpage)

# Bước 2: Lấy trang 116 ra (chỉ có 1 phần tử)


# Bước 3: Chuyển PIL → NumPy → OpenCV (BGR)

page = pages[0].convert('RGB')  # page là ảnh kiểu PIL

# Cắt vùng tương ứng với gray[3800:5500, 170:340]
cropped = page  # (x1, y1, x2, y2)



# Cắt vùng tương ứng với gray[3800:5500, 170:340]
# cropped = cropped.crop((170, 3800, 340, 5500))  # (x1, y1, x2, y2)




# gray = cv2.threshold(cropped, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]


custom_config = r'--oem 3 --psm 6'

# Load ảnh và apply nhận dạng bằng Tesseract OCR
text = pytesseract.image_to_string(cropped,config=custom_config, lang='vie-best2')

# Tìm đoạn sau cụm 'phân tiên loại 1'
match = re.search(r'phân tiên\s+loại\s*(.*)', text, flags=re.IGNORECASE | re.DOTALL)
if match:

	after_ordersn = match.group(1).strip()

	# Xoá mọi thứ sau dấu |
	cleaned_text = re.sub(r'\|.*', '', after_ordersn)

	cleaned_text = re.sub(r'\b\d+\s', '', cleaned_text)
	cleaned_text = re.sub(r"[^a-zA-Z0-9\- ]", "", cleaned_text)

	pattern = r'\b[A-Za-z0-9]{4,5}\s*-\s*[A-Za-z]{2}\s*-\s*\d{2}\b'

	clean_text = cleaned_text.replace('\n', ' ').replace('\r', ' ')

	skusss = re.findall(pattern, clean_text)
	skusss = [s.replace(" ", "") for s in skusss]

	rs = skusss

	# Print the results
	print(clean_text)
else:
    print("Không tìm thấy OrderSN.")

exit()

# Tìm SKU theo định dạng bạn đưa: dạng mã có cấu trúc nhóm chữ-số phân cách bằng dấu gạch ngang
match = re.search(r'\b(?:\w+-){4}\w+\b', text)
if match:
    sku = match.group()
    print("SKU tìm được:", sku)
else:
    print("Không tìm thấy SKU")

# lines = [line.strip() for line in text.split('\n') if line.strip()]

# # Kiểm tra dòng 2 (chỉ khi có ít nhất 2 dòng)
# # if len(lines) >= 2:
# #     line2 = lines[1]

# #     if len(line2) >= 2 and line2[3] == '0':
# #         text = pytesseract.image_to_string(cropped,config=custom_config, lang='eng')
   

# skuss = re.sub(r'[^A-Za-z0-9]+', '-', text)

# skuss1 = skuss.replace('SKU', '')

# skuss1 = skuss1.replace('SKU-','')

# pattern = r'\b[A-Za-z0-9]{4,5}\s*-\s*[A-Za-z]{2}\s*-\s*\d{2}\b'

# clean_text = skuss1.replace('\n', ' ').replace('\r', ' ')

# skusss = re.findall(pattern, clean_text)
# skusss = [s.replace(" ", "") for s in skusss]

# rs = skusss
# print(text)
