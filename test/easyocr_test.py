import easyocr
import time
start = time.time()
reader = easyocr.Reader(['ch_sim', 'en'])
result = reader.readtext('test/test_img/bag_all.png', detail = 0)
end = time.time()
print(result, end - start)