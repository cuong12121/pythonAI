
import os
import re
import cv2
import pytesseract
import sys
import io
import time
import numpy as np
import gc
from pdf2image import convert_from_path
import fitz
import requests
import redis
import json
import time
from PIL import Image
from wand.image import Image
from wand.color import Color

sys.stdout.reconfigure(encoding='utf-8')

current_dir = os.path.dirname(os.path.abspath(__file__))

import pdfplumber

def flatten_text(cell):
    return cell.replace('\n', '').strip() if cell else ''



def extract_sku_and_quantity(pdf_path):
    all_pages = []

    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)

        for i in range(total_pages):
            page = pdf.pages[i]

            text = page.extract_text()
            tables = page.extract_tables()


            # Tìm mã vận đơn
            mvd_match = re.search(r'Mã vận đơn:\s*([A-Z0-9]+)', text)
            # Tìm mã đơn hàng
            order_code_match = re.search(r'Mã đơn hàng:\s*([A-Z0-9]+)', text)

            mvd = mvd_match.group(1) if mvd_match else None
            order_code = order_code_match.group(1) if order_code_match else None


            page_items = []

            for table in tables:
                for row in table:
                    if row and row[0] is not None and '#' in row[0]:
                        header_index = table.index(row)
                        product_rows = table[header_index + 1:]

                        for r in product_rows:
                            if r and r[0] and r[0].strip().isdigit():
                                raw_sku = r[1]
                                raw_qty = r[5]  # cột SL

                                sku = raw_sku.replace('\n', '').strip() if raw_sku else ""
                                sku = sku.upper()
                                try:
                                    quantity = int(raw_qty.replace(',', '').strip()) if raw_qty else 0
                                except:
                                    quantity = 0

                                page_items.append({
                                    "page":i+1,
                                    "mvd": mvd,
                                    "mdh": order_code,
                                    "sku": sku[:10],
                                    "quantity": quantity,
                                    "sku_full": sku,
                                    "sku_full_check":sku[:10]

                                })

            all_pages.append(page_items)

    return all_pages

url = "https://drive.dienmayai.com/file_in.php"

response = requests.get(url)

data = response.json()  # Tự động decode JSON thành dict
number = 0
for item in data:
    save_path = "t38.pdf"

    file_pdf = 'https://dienmayai.com/'+item['file_pdf']

    # Gửi request để tải file
    responses = requests.get(file_pdf)

    print(1)

    if responses.status_code == 200:

        with open(save_path, 'wb') as f:
            f.write(responses.content)
            input_file = os.path.join(current_dir, 't38.pdf')
            

            array  = extract_sku_and_quantity(input_file)

            print(array)

            exit()

            r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)


            number += 1

            key_name = 'orders:data_sku_tracking_code'+str(number)

            # Nếu key tồn tại thì xóa


            # Ghi dữ liệu mới
            orders_json = json.dumps(array)
            r.set(key_name, orders_json)    




