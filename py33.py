import easyocr
import sys
sys.stdout.reconfigure(encoding='utf-8')

reader = easyocr.Reader(['en', 'vi'])  # Hỗ trợ tiếng Anh và tiếng Việt
results = reader.readtext('cropped_page116.png')

for bbox, text, conf in results:
    print(f"{text} (confidence: {conf:.2f})")