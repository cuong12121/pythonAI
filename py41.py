import os
import re
import cv2
import pytesseract
import sys
import io
# import redis
import json
import requests
import numpy as np
from PIL import Image
from wand.image import Image
from wand.color import Color
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

def count_pdf_pages(input_file):
    with Image(filename=input_file) as img:
        return len(img.sequence)

def cut_image(input_file,page):
    # phần cắt ảnh thành 3 ảnh để check
    with Image(filename=f'{input_file}[{page}]', resolution=(300, 300)) as img:
        # Convert to grayscale
        img.transform_colorspace('gray')
        
        for _ in range(1):
            img.contrast()
        
        # Enhance image
        img.modulate(brightness=500, saturation=500, hue=500)
        
        
        with img.clone() as img3:    
            img.transform_colorspace('gray')  # Convert to grayscale

            for _ in range(1):
                img.contrast()  # Increase contrast

            img.modulate(brightness=500, saturation=500, hue=500)  # Enhance image

            img.sharpen(radius=1, sigma=1)  # Sharpen image

            x = 82
            y = 1900
            width = 90
            height = 1000
            img.crop(x, y, width=width, height=height)
            
            # Set output format to PNG
            img.format = 'png'
            
           

           
            output_file ='cropped1170.png'
            img.save(filename=output_file)        

count =count_pdf_pages('t45.pdf')
# for i in range(1):
cut_image('t45.pdf',33)
# image_path = 'cropped1170.png'  # hoặc đường dẫn đầy đủ nếu nằm ngoài thư mục chạy

# image = cv2.imread(image_path)

# text = pytesseract.image_to_string(image, config='--oem 3 --psm 6',lang='vie')



# # Bước 1: Lấy phần sau đoạn "phân tiền\nloại"
# match = re.search(r"phân tiền\s*loại\s*(.*)", text, re.DOTALL | re.IGNORECASE)

# if match:
#     after_text = match.group(1).strip()
  
#     print(after_text,flush=True)
    #     # Bước 2: Tìm tất cả phần trước dấu '-' trong từng dòng
    #     results = re.findall(r"^(.*?)-", after_text, re.MULTILINE)
        
    #     # In kết quả
    #     for idx, item in enumerate(results, 1):
    #         print(item.strip())
    # else:
    #     print("Không tìm thấy đoạn 'phan tién\\nloai'")




