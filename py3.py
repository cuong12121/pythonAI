import os
import cv2
import pytesseract
import sys
import io
import numpy as np
from PIL import Image
from wand.image import Image
from wand.color import Color

# Define file paths (equivalent to __DIR__ in PHP)
current_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(current_dir, 't13.pdf')
output_file = os.path.join(current_dir, 'cropped1169.png')

# Initialize Imagick equivalent
with Image(filename=f'{input_file}[0]', resolution=(300, 300)) as img:
    # Convert to grayscale
    img.transform_colorspace('gray')
    
    for _ in range(3):
        img.contrast()
    
    # Enhance image (similar to enhanceImage in PHP Imagick)
    img.modulate(brightness=200, saturation=200, hue=200)
    
    # Sharpen image (radius=2, sigma=1)
    img.sharpen(radius=2, sigma=1)
    
    # # Crop image (x, y, width, height)
    # x = 860
    # y = 2000
    # width = 80
    # height = 900
    # img.crop(x, y, width=width, height=height)
    
    # Set output format to PNG
    img.format = 'png'
    
    # Save the output
    img.save(filename=output_file)

# Mở ảnh


# imgs = Image.open('cropped1169.png')



# # Lấy kích thước gốc
# img_width, img_height = imgs.size

# # Ví dụ: cắt từ 40% chiều ngang và 20% chiều cao,
# # với vùng cắt rộng 30% và cao 50%
# x_pct = 0.4
# y_pct = 0.2
# width_pct = 0.3
# height_pct = 0.5

# # Tính toán toạ độ cắt
# x = int(x_pct * img_width)
# y = int(y_pct * img_height)
# width = int(width_pct * img_width)
# height = int(height_pct * img_height)

# # Cắt ảnh
# cropped_img = imgs.crop((x, y, x + width, y + height))

# # Lưu ảnh cắt được
# cropped_img.save('cropped11_image.jpg')    