'''图像识别、文字处理，考虑多种ocr方式'''

from PIL import Image, ImageGrab
import pytesseract
import re

def tesseract_ocr(x, y, w, h):
    '''返回使用tesseract ocr引擎识别及处理结果
    参数：
        x：截图坐标x
        y：截图坐标y
        w：截图宽度w
        h：截图高度h
    返回：
        result：字典
            key：词条属性（含百分比差异说明）
            value；词条数值
            如：{'防御力': 23.0, '元素充能效率': 5.8, '暴击伤害': 5.4}
    '''
    img = ImageGrab.grab(bbox = (x, y, x + w, y + h))
    img.save('src/grab.png')
    try:
        txt = pytesseract.image_to_string(img, lang = 'chi_sim')
    except:
        txt = ''
        print('未检测到tesseract ocr引擎或中文语言包，请下载with-tesseract版本或手动安装引擎及语言包')
    
    # 本地图片测试用
    # txt = pytesseract.image_to_string(Image.open('test/test_img/example.png'), lang = 'chi_sim')
    # 纯数字单行测试
    # txt = pytesseract.image_to_string(Image.open('test/test_img/1.png'), lang = 'eng', config='--psm 13 --oem 1 -c tessedit_char_whitelist=0123456789.')
    txt = txt.replace(' ', '')

    # 一些误识别兼容
    txt = txt.replace(':', '.')
    txt = txt.replace('+1986', '+986')
    txt = txt.replace('完', '充')
    txt = txt.replace('为', '力')

    # 中文和数字正则
    pattern_chinese = '[\u4e00-\u9fa5]+'
    pattern_digit = '\d+(\.\d+)?'

    # 逐行识别
    line = txt.splitlines()
    result = {}
    for item in line:
        if item != '':
            print(item)
            try:
                # 词条名称
                name = re.findall(pattern_chinese, item)
                name = name[0]
                # 数值
                digit = float(re.search(pattern_digit, item).group())
                if name == '暴击率':
                    result['暴击率'] = digit
                elif name == '暴击伤害':
                    result['暴击伤害'] = digit
                elif name == '元素精通':
                    result['元素精通'] = digit
                elif name == '攻击力' and '%' in item:
                    result['攻击力百分比'] = digit
                elif name == '攻击力':
                    result['攻击力'] = digit
                elif name == '生命值' and '%' in item:
                    result['生命值百分比'] = digit
                elif name == '生命值':
                    result['生命值'] = digit
                elif name == '防御力' and '%' in item:
                    result['防御力百分比'] = digit
                elif name == '防御力':
                    result['防御力'] = digit
                elif name == '元素充能效率':
                    result['元素充能效率'] = digit
                else:
                    result[item] = 0
            except:
                result[item] = 0
    
    print(result)
    return result

def yas_ocr():
    import numpy as np
    import json 
    import onnxruntime as rt

    img = Image.open('test/test_img/example.png')
    img = img.crop((0, 0, 184, 32))
    sess = rt.InferenceSession('model_training.onnx')
    
    # data = json.dumps({'data': np.asarray(img)})
    # data = np.array(json.loads(data)['data']).astype('float32')

    input_name = sess.get_inputs()[0].name
    label_name = sess.get_outputs()[0].name
    out = sess.run([label_name], {input_name: np.array(img).astype(np.float32)})
    print(out)

if __name__ == '__main__':
    # 截图坐标
    x, y, w, h = (1684, 560, 350, 168) 
    # tesseract_ocr(x, y, w, h)
    # yas_ocr()
    import score
    print(score.cal_score(tesseract_ocr(x, y, w, h), '雷电将军'))