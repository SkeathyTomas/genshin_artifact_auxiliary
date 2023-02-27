'''图像识别、文字处理，考虑多种ocr方式'''

from PIL import ImageGrab, Image
import re

def ppocr(x, y, w, h):
    '''返回使用paddle ocr引擎识别及处理结果
    参数：
        x：截图坐标x
        y：截图坐标y
        w：截图宽度w
        h：截图高度h
    返回：
        basic：主词条等基本信息list
            名称，部位，主属性，数值，等级
            ['雷云之笼', '时之沙', '攻击力', '46.6%', '+20']
        result：副词条属性dict
            key：词条属性（含百分比差异说明）
            value；词条数值
            如：{'防御力': 23.0, '元素充能效率': 5.8, '暴击伤害': 5.4}
    '''
    from ppocronnx.predict_system import TextSystem
    import cv2

    # 截屏与ocr识别
    img = ImageGrab.grab(bbox = (x, y, x + w, y + h))
    img.save('src/grab.png')
    img = cv2.imread('src/grab.png')
    # img = cv2.imread('test/test_img/character_all.png') # 本地测试用图片
    ocr = TextSystem()
    result = ocr.detect_and_ocr(img)

    # 千位符（含误识别的.）兼容
    pattern_thou = '\d\.\d{3}|\d\,\d{3}'
    txt = [re.sub(pattern_thou, item.ocr_text.replace(',', '').replace('.', ''), item.ocr_text) for item in result]
    print(txt)

    name = txt[0]
    parts = txt[1]
    main_name = txt[2]
    main_digit = txt[3]
    lvl = txt[4]
    basic = [name, parts, main_name, main_digit, lvl]

    # 中文和数字正则
    pattern_chinese = '[\u4e00-\u9fa5]+'
    pattern_digit = '\d+(\.\d+)?'

    result = {}
    for item in txt[-4:]:
        try:
            # 词条名称
            name = re.findall(pattern_chinese, item)
            name = name[0]
            # 数值
            digit = float(re.search(pattern_digit, item).group())
            # 兼容千位符
            if digit < 2:
                digit *= 1000
            if name in '暴击率':
                result['暴击率'] = digit
            elif name in '暴击伤害':
                result['暴击伤害'] = digit
            elif name in '元素精通':
                result['元素精通'] = digit
            elif name in '攻击力' and '%' in item:
                result['攻击力百分比'] = digit
            elif name in '攻击力':
                result['攻击力'] = digit
            elif name in '生命值' and '%' in item:
                result['生命值百分比'] = digit
            elif name in '生命值':
                result['生命值'] = digit
            elif name in '防御力' and '%' in item:
                result['防御力百分比'] = digit
            elif name in '防御力':
                result['防御力'] = digit
            elif name in '元素充能效率':
                result['元素充能效率'] = digit
            else:
                result[item] = 0
        except:
            result[item] = 0
    
    print(basic, result)
    return basic, result

if __name__ == '__main__':
    # 截图坐标
    x, y, w, h = (1808, 277, 377, 714) # 副词条
    # x, y, w, h = (1948, 200, 360, 70) # 圣遗物名称

    # ocr测试
    import time
    start = time.time()
    # tesseract_ocr(x, y, w, h)
    ppocr(x, y, w, h)
    end = time.time()
    print(end - start)
    
    # import score
    # print(score.cal_score(tesseract_ocr(x, y, w, h), '雷电将军'))