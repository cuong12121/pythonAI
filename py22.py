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
input_file = os.path.join(current_dir, 't33.pdf')
output_file = os.path.join(current_dir, 'cropped1169.png')

input_file3 = os.path.join(current_dir, 'file3.png')
cut_image(input_file, 29)  


# Đường dẫn ảnh bảng
image_path = 'file3.png'  # hoặc đường dẫn đầy đủ nếu nằm ngoài thư mục chạy

img = cv2.imread(image_path)

# Chuyển sang ảnh xám
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Nhị phân hóa để tìm đường viền
_, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

# Dò đường kẻ bằng morphology
kernel_h = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
kernel_v = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
horizontal = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel_h)
vertical = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel_v)
lines = cv2.bitwise_or(horizontal, vertical)

# Mask xóa viền
mask = cv2.bitwise_not(lines)
no_border = cv2.bitwise_and(img, img, mask=mask)
no_border[mask == 0] = [255, 255, 255]  # chuyển viền về trắng

# Resize to giúp OCR chính xác hơn
resized = cv2.resize(no_border, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
gray2 = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

# Dùng pytesseract đọc số
custom_config = r'--oem 3 --psm 6 outputbase digits'
text = pytesseract.image_to_string(gray2, config=custom_config)

print("Kết quả OCR:", text.strip())