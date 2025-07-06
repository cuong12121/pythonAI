
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

current_dir = os.path.dirname(os.path.abspath(__file__))
# so_trang = count_pdf_pages(input_file)

input_file = os.path.join(current_dir, 't44.pdf')
output_file = os.path.join(current_dir, 'cropped1169.png')

# Đường dẫn đến file PDF
pdf_path = input_file
i=0
# indexpage = i+1
indexpage =2
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

cv2.imwrite("cropped_page119.png", cropped)

print('thành công')