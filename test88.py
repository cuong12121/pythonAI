from PIL import Image

# Mở ảnh
img = Image.open('cropped1169.png')

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
cropped_img.save('cropped_image.png')
