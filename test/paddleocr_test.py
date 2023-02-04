from ppocronnx.predict_system import TextSystem
import cv2
import time

ocr = TextSystem()
# single line
# img = cv2.imread('test/test_img/test_line.png')
# result = ocr.ocr_single_line(img)
# print(result)
start = time.time()
img = cv2.imread('test/test_img/character_all.png')
result = ocr.detect_and_ocr(img)
end = time.time()
print(end - start)
for item in result:
    print(item.ocr_text)