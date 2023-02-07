from ppocronnx.predict_system import TextSystem
import cv2
import time

ocr = TextSystem()
# single line
start = time.time()
img = cv2.imread("D:/Application/keqing/yas-train-main/test.png")
result = ocr.ocr_lines([img, img, img, img, img, img, img, img, img])
end = time.time()
print(end - start)
print(result)

# multiline
start = time.time()
img = cv2.imread('test/test_img/bag_all.png')
result = ocr.detect_and_ocr(img)
end = time.time()
print(end - start)
for item in result:
    print(item.ocr_text)