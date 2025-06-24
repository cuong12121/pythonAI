import os
import re
import cv2
import pytesseract
import sys
import io
# import redis
import json
import numpy as np
from PIL import Image
from wand.image import Image
from wand.color import Color
sys.stdout.reconfigure(encoding='utf-8')


def cut_image(input_file,page):
    # phần cắt ảnh thành 3 ảnh để check
    with Image(filename=f'{input_file}[{page}]', resolution=(300, 300)) as img:
        # Convert to grayscale
        img.transform_colorspace('gray')
        
        for _ in range(3):
            img.contrast()
        
        # Enhance image
        img.modulate(brightness=300, saturation=300, hue=300)
        
        # Sharpen image
        img.sharpen(radius=2, sigma=1)

        with img.clone() as img3:    
            img.transform_colorspace('gray')  # Convert to grayscale

            for _ in range(3):
                img.contrast()  # Increase contrast

            img.modulate(brightness=300, saturation=300, hue=300)  # Enhance image

            img.sharpen(radius=2, sigma=1)  # Sharpen image

            # Optional crop
            # img.crop(x=860, y=2000, width=80, height=900)

            img.format = 'png'  # Set output format
            img.save(filename=output_file)  # Save image
            from PIL import Image as PILImage

            img = PILImage.open(output_file)
            # img.show()  # hoặc các xử lý tiếp theo
            # Lấy kích thước gốc
            img_width, img_height = img.size

            # Ví dụ: cắt từ 40% chiều ngang và 20% chiều cao,
            # với vùng cắt rộng 30% và cao 50%
            x_pct = 0.3482
            y_pct = 0.57
            width_pct = 0.03
            height_pct = 0.25

            # Tính toán toạ độ cắt
            x = int(x_pct * img_width)
            y = int(y_pct * img_height)
            width = int(width_pct * img_width)
            height = int(height_pct * img_height)

            # Cắt ảnh
            cropped_img = img.crop((x, y, x + width, y + height))

            # Lưu ảnh cắt được
            cropped_img.save('file3.png')

current_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(current_dir, 't32.pdf')
output_file = os.path.join(current_dir, 'cropped1169.png')

input_file3 = os.path.join(current_dir, 'file3.png')
cut_image(input_file, 12)  


# Đường dẫn ảnh bảng
image_path = 'file3.png'  # hoặc đường dẫn đầy đủ nếu nằm ngoài thư mục chạy

# Đọc ảnh
image = cv2.imread(image_path)

# Chuyển sang ảnh xám
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Nhị phân ảnh (đen trắng)
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

# Tìm contours
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Danh sách kết quả
numbers = []

# Vòng lặp qua từng contour
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    if w > 10 and h > 10:  # Lọc những vùng quá nhỏ
        roi = gray[y:y+h, x:x+w]  # Cắt vùng ảnh chứa ký tự
        # Nhận diện ký tự bằng Tesseract (chỉ lấy số)
        text = pytesseract.image_to_string(roi, config='--psm 10 -c tessedit_char_whitelist=0123456789').strip()
        digits = ''.join(filter(str.isdigit, text))
        if digits:
            numbers.append(digits)

# Sắp xếp theo vị trí trên ảnh (từ trên xuống dưới, trái sang phải)
numbers = sorted(numbers)

# In kết quả
print("Tất cả các số trong bảng:", numbers)