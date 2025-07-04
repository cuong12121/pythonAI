import re

def correct_sku(raw_text):
   

    pattern = r'([0-9OIl]{3}[A-ZOlI])-([A-Z]{2})-(\d{2})-([A-Z]{3})-(\d{2})-(\d{3})'

    matches = re.findall(pattern, raw_text)

    corrected = []

    for part1, part2, part3, part4, part5, part6 in matches:
        # Sửa các lỗi OCR
        digits = part1[:3].replace('I', '1').replace('O', '0')
        letter = part1[3]
        if letter == '1': letter = 'I'
        elif letter == '0': letter = 'O'
        part1_fixed = digits + letter

        part2 = part2.replace('1', 'I').replace('0', 'O')
        part4 = part4.replace('1', 'I').replace('0', 'O')

        part3 = part3.replace('I', '1').replace('O', '0')
        part5 = part5.replace('I', '1').replace('O', '0')
        part6 = part6.replace('I', '1').replace('O', '0')

        sku = f"{part1_fixed}-{part2}-{part3}-{part4}-{part5}-{part6}"
        corrected.append(sku)

    return corrected

code ='150B-MT-00-ABC-00-001'

codes = correct_sku(code)

print(codes)