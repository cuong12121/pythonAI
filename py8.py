import os
import re
import cv2
import pytesseract
import sys
import io
import redis
import json
import numpy as np
from PIL import Image
from wand.image import Image
from wand.color import Color
sys.stdout.reconfigure(encoding='utf-8')



# Define file paths (equivalent to __DIR__ in PHP)
current_dir = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(current_dir, 'cropped1169.png')
input_file = os.path.join(current_dir, 't18.pdf')

def count_pdf_pages(input_file):
    with Image(filename=input_file) as img:
        return len(img.sequence)


so_trang = count_pdf_pages(input_file)
# print(f"Số trang PDF: {so_trang}")

def cut_image(input_file,page):
    # phần cắt ảnh thành 3 ảnh để check
    with Image(filename=f'{input_file}[{page}]', resolution=(300, 300)) as img:
        # Convert to grayscale
        img.transform_colorspace('gray')
        
        for _ in range(3):
            img.contrast()
        
        # Enhance image
        img.modulate(brightness=100, saturation=100, hue=100)
        
        # Sharpen image
        img.sharpen(radius=2, sigma=1)

        # -------- Cắt ảnh 1 --------
        with img.clone() as img1:
            x = 82
            y = 1900
            width = 88
            height = 1000
            img1.crop(x, y, width=width, height=height)
            img1.format = 'png'
            img1.save(filename='file1.png')

        # -------- Cắt ảnh 2 --------
        with img.clone() as img2:
            x1 = 500
            y1 = 130
            width1 = 650
            height1 = 150
            img2.crop(x1, y1, width=width1, height=height1)
            img2.format = 'png'
            img2.save(filename='file2.png')
        with img.clone() as img3:    
            img.transform_colorspace('gray')  # Convert to grayscale

            for _ in range(3):
                img.contrast()  # Increase contrast

            img.modulate(brightness=200, saturation=200, hue=200)  # Enhance image

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
            x_pct = 0.349
            y_pct = 0.54
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

def sku(input_file):
   

    

    # Chỉ định đường dẫn Tesseract nếu cần
    # pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    # Load ảnh
    image = cv2.imread(input_file)  # thay bằng đường dẫn ảnh của bạn

    # Chuyển sang xám
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Làm nét và threshold nhẹ (tùy ảnh)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # OCR chỉ lấy số
    custom_config = r'--oem 3 --psm 6'
    result = pytesseract.image_to_string(image, config=custom_config, lang='vie')  # nếu có tiếng Việt
    return result   




def tracking(input_file):
    # sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    # Chỉ định đường dẫn Tesseract nếu cần
    # pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    # Load ảnh
    image = cv2.imread(input_file)  # thay bằng đường dẫn ảnh của bạn

    # Chuyển sang xám
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Làm nét và threshold nhẹ (tùy ảnh)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # OCR chỉ lấy số
    custom_config = r'--oem 3 --psm 6'
    result = pytesseract.image_to_string(image, config=custom_config, lang='vie')  # nếu có tiếng Việt
    return result
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
    custom_config = r'--oem 3 --psm 6 outputbase digits'
    result = pytesseract.image_to_string(thresh, config=custom_config)
    return result



input_file1 = os.path.join(current_dir, 'file1.png')
input_file2 = os.path.join(current_dir, 'file2.png')
input_file3 = os.path.join(current_dir, 'file3.png')

# sku = sku(input_file1)
array = []

def extract_ma_van_don(text):
    match = re.search(r'Mã vận đơn[.: ]+\s*([A-Z0-9]+)', text)
    return match.group(1) if match else ""

#phần chạy code
for i in range(so_trang): 
    # print(i)
    cut_image(input_file,i)
    
    trackings= tracking(input_file2)
    
    value = extract_ma_van_don(text)


    ma_don_hang = re.search(r'Mã đơn hàng[.: ]+\s*([A-Z0-9]+)', trackings)

   

    arrayvd = [value, ma_don_hang.group(1)]


    quantitys = quantity(input_file3)
    skus =sku(input_file1)

    pattern = r'\b[A-Za-z0-9]{4}\s*-\s*[A-Za-z]{2}\s*-\s*\d{2}\s*-\s*[A-Za-z]{3}\b'

    clean_text = skus.replace('\n', ' ').replace('\r', ' ')

    skuss = re.findall(pattern, clean_text)

    array.append({
        'sku': skus,
        'tracking': arrayvd,
        'quantity': quantitys
    })

# # image = cv2.imread(input_file2)


# Kết nối Redis


r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

key_name = "orders:data"

# Nếu key tồn tại thì xóa


# Ghi dữ liệu mới
orders_json = json.dumps(array)
r.set(key_name, orders_json)
       
