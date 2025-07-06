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

preprocess = "blur" 

image_path = 'cropped_page119.png'

image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
if preprocess == "thresh":
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
elif preprocess == "blur":
    gray = cv2.medianBlur(gray, 5)

# Lưu ảnh trong ổ cứng như file tạm để có thể apply OCR
temp_filename = "temp.tiff"


cv2.imwrite(temp_filename, gray)

custom_config = r'--oem 3 --psm 6'
from PIL import Image
# Load ảnh và apply nhận dạng bằng Tesseract OCR
text = pytesseract.image_to_string(Image.open(temp_filename),config=custom_config, lang='eng-best+vie')
print(text)