# Hướng dẫn chạy
# python tesseract_ocr.py --image image1.png
from PIL import Image
import pytesseract
import argparse
import cv2
import os

""" Ảnh nên được xử lý trước như khử nhiễu, chuyển về đen trắng... sẽ cho kết quả tốt hơn đới với Tesseract """
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to the input image")
ap.add_argument("-p", "--preprocess", type=str, default="thresh", help="kind of image pre-processing")
args = vars(ap.parse_args())

# Đọc ảnh và convert về grayscale
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
# Kiểm tra xem có chuyển về ảnh đen trắng 
if args["preprocess"] == "thresh":
	_, gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)		# trả về 2 tham số threshold và image
 
# Có blur không
elif args["preprocess"] == "blur":
	gray = cv2.medianBlur(gray, 3)	# tham số thứ hai là kernel size, giảm salt và pepper noise

# Lưu ảnh trong ổ cứng như file tạm để có thể apply OCR
filename = "{}.png".format(os.getpid())		# os.getpid() method in Python is used to get the process ID of the current process, trả về 1 số nguyên
cv2.imwrite(filename, gray)		# ghi ảnh gray vào filename

custom_config = r'--oem 3 --psm 6'

# Load ảnh và apply nhận dạng bằng Tesseract OCR
text = pytesseract.image_to_string(Image.open(filename),config=custom_config, lang='vie')	# có nhiều ngông ngữ thì trong lang các ngôn ngữ cách nhau bằng dấu  +
""" Cần chú ý các chế độ nhận diện được điều chỉnh bằng config """

# Thực hiện chuyển đổi xong thì xóa ảnh tạm
os.remove(filename)

# In dòng chữ nhận dạng được
print(text)
 
# Hiển thị ảnh ban đầu, ảnh đã được pre-processing
# cv2.imshow("Image", image)
# cv2.imshow("Output", gray)
# cv2.waitKey(0)