import os
import re
import cv2
import pytesseract
import sys
import io
import redis
import json
import requests
import numpy as np
from PIL import Image
from wand.image import Image
from wand.color import Color
sys.stdout.reconfigure(encoding='utf-8')

def count_pdf_pages(input_file):
    with Image(filename=input_file) as img:
        return len(img.sequence)

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

def convert_quantity_to_array(string):
    text_sau_xoa = re.sub(r'^.*?\n', '', string)

    # Tách các dòng còn lại thành mảng
    lines = text_sau_xoa.splitlines()

    return lines


def quantity(input_file):

    current_dir = os.path.dirname(os.path.abspath(__file__))

    output_file = os.path.join(current_dir, input_file)

    # Load the image
    image = cv2.imread(output_file)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Detect edges using Canny
    edges = cv2.Canny(blurred, 50, 150)

    # Find lines using Hough Transform
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)

    # Create a white mask
    mask = np.ones(image.shape[:2], dtype=np.uint8) * 255

    # Draw lines on the mask (remove borders)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(mask, (x1, y1), (x2, y2), 0, 3)

    # Apply mask to remove borders on the original image
    result = image.copy()
    result[mask == 0] = [255, 255, 255]  # Replace borders with white

    # Perform OCR to detect text
    ocr_result = pytesseract.image_to_data(result, output_type=pytesseract.Output.DICT)

    # Create a mask for letters
    text_mask = np.ones(result.shape[:2], dtype=np.uint8) * 255

    # Iterate through OCR results
    for i, text in enumerate(ocr_result['text']):
        if text.strip():  # Check if text is not empty
            # Check if the text contains only letters (no numbers)
            if text.isalpha():  # Only letters
                x, y, w, h = ocr_result['left'][i], ocr_result['top'][i], ocr_result['width'][i], ocr_result['height'][i]
                # Draw a white rectangle over the letters
                cv2.rectangle(text_mask, (x, y), (x + w, y + h), 0, -1)

    # Apply text mask to remove letters
    result[text_mask == 0] = [255, 255, 255]  # Replace letters with white

    # Save or display the result
    cv2.imwrite('result_no_letters.png', result)

   


    # Load ảnh
    image = cv2.imread('result_no_letters.png')  # thay bằng đường dẫn ảnh của bạn

    # Chuyển sang xám
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Làm nét và threshold nhẹ (tùy ảnh)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # OCR chỉ lấy số
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'
    result = pytesseract.image_to_string(thresh, config=custom_config)
    return result



current_dir = os.path.dirname(os.path.abspath(__file__))



url = "https://drive.dienmayai.com/file_in.php"

response = requests.get(url)

data = response.json()  # Tự động decode JSON thành dict
number =0
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

            input_file3 = os.path.join(current_dir, 'file3.png')
            so_trang = count_pdf_pages(input_file)
            image_path = 'file3.png' 

            # sku = sku(input_file1)
            array = []



            # for i in range(so_trang):
            #     cut_image(input_file, i)  
            #     quantitys = quantity(input_file3) 

            #     array.append({
            #         'quantity':convert_quantity_to_array(quantitys)
            #     }) 

            for i in range(so_trang):
                # Đọc ảnh
                current_dir = os.path.dirname(os.path.abspath(__file__))
                input_file = os.path.join(current_dir, 't38.pdf')
                output_file = os.path.join(current_dir, 'cropped1169.png')

                input_file3 = os.path.join(current_dir, 'file3.png')
                cut_image(input_file, i)  


                # Đường dẫn ảnh bảng
                image_path = 'file3.png'  # hoặc đường dẫn đầy đủ nếu nằm ngoài thư mục chạy

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
                        text = pytesseract.image_to_string(roi, config='--psm 10 -c tessedit_char_whitelist=0123456789',lang='vie').strip()
                        digits = ''.join(filter(str.isdigit, text))
                        if digits:
                            numbers.append(digits)

                # Sắp xếp theo vị trí trên ảnh (từ trên xuống dưới, trái sang phải)
                numbers = sorted(numbers)

                array.append({
                'quantity':numbers
                }) 

               
            r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

            number += 1

            key_name = 'orders:data_quantity_'+str(number)

        
            # Ghi dữ liệu mới
            orders_json = json.dumps(array)
            r.set(key_name, orders_json)