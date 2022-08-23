'''图像识别、文字处理，考虑多种ocr方式'''

from PIL import Image, ImageGrab
import pytesseract
import re

# 截图坐标
x, y, w, h = (1684, 560, 350, 168)

def tesseract_ocr():
    img = ImageGrab.grab(bbox = (x, y, x + w, y + h))
    txt = pytesseract.image_to_string(img, lang = 'chi_sim')

    txt = txt.replace(' ', '')