import pytesseract
import cv2
import sys
import io
import pytesseract

# Bắt lỗi encode khi print
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


# Đường dẫn ảnh bảng
image_path = 'no_border.png'  # hoặc đường dẫn đầy đủ nếu nằm ngoài thư mục chạy

# Đọc ảnh
image = cv2.imread(image_path)



# Chuyển sang ảnh xám
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Nhị phân ảnh (đen trắng)
_, thresh = cv2.threshold(gray, 150, 256, cv2.THRESH_BINARY_INV)

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

print(numbers)
