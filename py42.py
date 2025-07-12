from paddleocr import PaddleOCR

# Khởi tạo PaddleOCR với ngôn ngữ tiếng Việt
ocr = PaddleOCR(use_angle_cls=True, lang='vi')

# Thay 'image.png' bằng đường dẫn tới hình ảnh của bạn
image_path = 'cropped1170.png'
result = ocr.ocr(image_path, cls=True)

# In kết quả nhận diện
for line in result[0]:
    print(line[1][0])