from paddleocr import PaddleOCR

ocr = PaddleOCR(lang = 'ch')
result = ocr.ocr('test/test_img/bag_all.bag_all.png')
print(result)