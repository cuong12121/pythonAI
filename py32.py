# Hướng dẫn chạy
# python tesseract_ocr.py --image image1.png
from PIL import Image
import pytesseract
import argparse
import cv2
import os

""" Ảnh nên được xử lý trước như khử nhiễu, chuyển về đen trắng... sẽ cho kết quả tốt hơn đới với Tesseract """
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=True, help="path to the input image")
# ap.add_argument("-p", "--preprocess", type=str, default="thresh", help="kind of image pre-processing")
# args = vars(ap.parse_args())
image_path = "cropped_page116.png"          # ← ảnh của bạn
preprocess = "thresh" 

# Đọc ảnh và convert về grayscale
image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
if preprocess == "thresh":
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
elif preprocess == "blur":
    gray = cv2.medianBlur(gray, 3)

# Lưu ảnh trong ổ cứng như file tạm để có thể apply OCR
temp_filename = "temp.png"
cv2.imwrite(temp_filename, gray)

custom_config = r'--oem 3 --psm 6'

# Load ảnh và apply nhận dạng bằng Tesseract OCR
text = pytesseract.image_to_string(Image.open(temp_filename),config=custom_config, lang='vie')	# có nhiều ngông ngữ thì trong lang các ngôn ngữ cách nhau bằng dấu  +
""" Cần chú ý các chế độ nhận diện được điều chỉnh bằng config """

# Thực hiện chuyển đổi xong thì xóa ảnh tạm
os.remove(temp_filename)

# In dòng chữ nhận dạng được
print(text)
 
# Hiển thị ảnh ban đầu, ảnh đã được pre-processing
# cv2.imshow("Image", image)
# cv2.imshow("Output", gray)
# cv2.waitKey(0)