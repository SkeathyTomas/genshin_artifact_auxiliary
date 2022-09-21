'''截图、图像识别、文字处理、分数计算'''

from PIL import Image, ImageGrab
import pytesseract
import re
import characters
# import time

# 角色面板截图坐标x,y,w,h
# position = (1820, 422, 364, 152)
# 背包面板截图坐标x,y,w,h
x, y, w, h = (1684, 560, 350, 168)

# 角色有效词条
valuables = characters.config

# 基础系数
coefficient = {
    '暴击率': [2],
    '暴击伤害': [1],
    '元素精通': [0, 0.33],
    '攻击力': [1.33, 0.199],
    '生命值': [1.33, 0.01716],
    '防御力': [1.06, 0.2211],
    '元素充能效率': [1.1979]
}

# 手动调试
# txt = '''. 元 素 充 能 效 率 +6.5%
# . 攻 击 力 +35

# . 暴 击 率 +2.7%

# . 攻 击 力 +22.7%
# '''

# 图片手动识别结果
# character = ''
# txt = pytesseract.image_to_string(Image.open('test/test_img/example.png'), lang = 'chi_sim')

# 截图与ocr识别
def ocr(x, y, w, h):
    # time.sleep(0.2)
    # 可能未安装ocr引擎
    try:
        img = ImageGrab.grab(bbox = (x, y, x + w, y + h))
        # img.save('grab.png')
        txt = pytesseract.image_to_string(img, lang = 'chi_sim')
        print(txt)
        return txt
    except:
        print('未安装tesseract引擎或中文简体语言包')

# 文字处理与分数计算
def cal_score(txt, character):
    txt = txt.replace(' ', '')

    # 一些误识别兼容
    # 部分.1%将%识别为数字的情况
    txt = txt.replace('.1', '.1%')

    txt = txt.replace('仿', '伤')
    txt = txt.replace('传', '伤')
    txt = txt.replace('传', '伤')
    txt = txt.replace('伪', '伤')

    txt = txt.replace('政', '功')
    txt = txt.replace('攸', '功')
    txt = txt.replace('改', '功')

    txt = txt.replace('宇', '击')
    txt = txt.replace('出', '击')
    txt = txt.replace('吉', '击')

    txt = txt.replace('徒', '御')

    txt = txt.replace('宠', '害')
    txt = txt.replace('宓', '害')
    txt = txt.replace('窑', '害')

    txt = txt.replace('演', '暴')
    txt = txt.replace('禀', '暴')
    txt = txt.replace('景', '暴')

    txt = txt.replace('宏', '素')
    txt = txt.replace('泰', '素')

    txt = txt.replace('交', '充')

    line = txt.splitlines()
    pattern_chinese = '[\u4e00-\u9fa5]+'
    pattern_digit = '\d+(\.\d+)?'

    # 角色输入可能出错
    try:
        # 二级系数
        valuable = valuables[character]
    except:
        valuable = {'生命值': 0, '攻击力': 0.75, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0, '元素充能效率': 0}
    
    score = 0
    for item in line:
        if item != '':
            # 识别可能出错，词条不在表中
            try:
                # 词条名称
                name = re.findall(pattern_chinese, item)
                name = name[0]
                # 数值
                digit = float(re.search(pattern_digit, item).group())
                if '%' in item:
                    score += digit * coefficient[name][0] * valuable[name]
                    print(name, digit, '%', score)
                else:
                    score += digit * coefficient[name][1] * valuable[name]
                    print(name, digit, score)
            except:
                print('「' + item + '」词条识别有误！')
    
    return round(score, 1)

def main(character, x, y, w, h):
    print(character)
    txt = ocr(x, y, w, h)
    score = cal_score(txt, character)
    return score

if __name__ == '__main__':
    main(character, x, y, w, h)