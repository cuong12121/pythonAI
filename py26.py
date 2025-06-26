from pdf2image import convert_from_path
import pytesseract
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(current_dir, 't3.pdf')
poppler_path = r"C:xampp\poppler\Library\bin"  # đổi lại đúng theo thư mục bạn giải nén


pdf_path = input_file

# Chuyển PDF sang ảnh (mỗi trang là một ảnh)
images = convert_from_path(pdf_path, dpi=300)

# Đọc chữ từ ảnh bằng Tesseract OCR
text = ""
for i, img in enumerate(images):
    custom_config = r'--oem 3 --psm 6'
    page_text = pytesseract.image_to_string(img, lang='vie+eng')  # dùng vie nếu là tiếng Việt
    text += f"\n--- PAGE {i+1} ---\n{page_text}"
print(text)    