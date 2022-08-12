'''截图、图像识别、文字处理、分数计算'''

from PIL import Image, ImageGrab
import pytesseract
import re
# import time

# 角色面板截图坐标x,y,w,h
# position = (1820, 422, 364, 152)
# 背包面板截图坐标x,y,w,h
x, y, w, h = (1684, 560, 350, 168)

# 角色有效词条
valuables = {
    # 风
    '鹿野院平藏': {'生命值': 0, '攻击力': 0.75, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0.75, '元素充能效率': 0},
    '旅行者-风': {'生命值': 0, '攻击力': 0.75, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0.75, '元素充能效率': 0.55},
    '枫原万叶': {'生命值': 0, '攻击力': 0.75, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 1, '元素充能效率': 0.55},
    '温迪': {'生命值': 0, '攻击力': 0.75, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0.75, '元素充能效率': 0.55},
    '琴': {'生命值': 0, '攻击力': 0.75, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0, '元素充能效率': 0.55},
    '魈': {'生命值': 0, '攻击力': 0.75, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0, '元素充能效率': 0.55},
    '早柚': {'生命值': 0, '攻击力': 0.5, '防御力': 0, '暴击率': 0.5, '暴击伤害': 0.5, '元素精通': 1, '元素充能效率': 0.55},
    '砂糖': {'生命值': 0, '攻击力': 0.75, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 1, '元素充能效率': 0.55},

    # 火
    '托马': {'生命值': 1, '攻击力': 0.5, '防御力': 0, '暴击率': 0.5, '暴击伤害': 0.5, '元素精通': 0, '元素充能效率': 0.9},
    '胡桃': {'生命值': 0.8, '攻击力': 0.5, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0.75, '元素充能效率': 0},
    '宵宫': {'生命值': 0, '攻击力': 0.75, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0.75, '元素充能效率': 0},
    '可莉': {'生命值': 0, '攻击力': 0.75, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0.75, '元素充能效率': 0},
    '迪卢克': {'生命值': 0, '攻击力': 0.75, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0.75, '元素充能效率': 0},
    '班尼特': {'生命值': 1, '攻击力': 0.5, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0, '元素充能效率': 0.55},
    '安柏': {'生命值': 0, '攻击力': 0.75, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0.75, '元素充能效率': 0},
    '香菱': {'生命值': 0, '攻击力': 0.75, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0.75, '元素充能效率': 0.55},
    '辛焱': {'生命值': 0, '攻击力': 0.75, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0, '元素充能效率': 0},
    '烟绯': {'生命值': 0, '攻击力': 0.75, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0.75, '元素充能效率': 0},

    # 水
    '夜兰': {'生命值': 0.8, '攻击力': 0, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0, '元素充能效率': 0.55},
    '神里绫人': {'生命值': 0.5, '攻击力': 0.75, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0, '元素充能效率': 0},
    '达达利亚': {'生命值': 0, '攻击力': 0.75, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0.75, '元素充能效率': 0},
    '珊瑚宫心海': {'生命值': 1, '攻击力': 0.5, '防御力': 0, '暴击率': 0, '暴击伤害': 0, '元素精通': 0, '元素充能效率': 0.55},
    '莫娜': {'生命值': 0, '攻击力': 0.75, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0.75, '元素充能效率': 0.75},
    '行秋': {'生命值': 0, '攻击力': 0.75, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0, '元素充能效率': 0.55},
    '芭芭拉': {'生命值': 1, '攻击力': 0.5, '防御力': 0, '暴击率': 0.5, '暴击伤害': 0.5, '元素精通': 0, '元素充能效率': 0.55},

    # 冰
    '申鹤': {'生命值': 0, '攻击力': 1, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0, '元素充能效率': 0.55},
    '优菈': {'生命值': 0, '攻击力': 0.75, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0, '元素充能效率': 0.55},
    '埃洛伊': {'生命值': 0, '攻击力': 0.75, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0, '元素充能效率': 0},
    '神里绫华': {'生命值': 0, '攻击力': 0.75, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0, '元素充能效率': 0},
    '七七': {'生命值': 0, '攻击力': 1, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0, '元素充能效率': 0.55},
    '甘雨': {'生命值': 0, '攻击力': 0.75, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0.75, '元素充能效率': 0},
    '迪奥娜': {'生命值': 1, '攻击力': 0.5, '防御力': 0, '暴击率': 0.5, '暴击伤害': 0.5, '元素精通': 0, '元素充能效率': 0.9},
    '重云': {'生命值': 0, '攻击力': 0.75, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0.75, '元素充能效率': 0.55},
    '罗莎莉亚': {'生命值': 0, '攻击力': 0.75, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0, '元素充能效率': 0},
    '凯亚': {'生命值': 0, '攻击力': 0.75, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0, '元素充能效率': 0},

    # 雷
    '九岐忍': {'生命值': 1, '攻击力': 0, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0.75, '元素充能效率': 0.55},
    '旅行者-雷': {'生命值': 0, '攻击力': 0.75, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0, '元素充能效率': 0.55},
    '八重神子': {'生命值': 0, '攻击力': 0.75, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0.75, '元素充能效率': 0.55},
    '雷电将军': {'生命值': 0, '攻击力': 0.75, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0, '元素充能效率': 0.9},
    '刻晴': {'生命值': 0, '攻击力': 0.75, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0, '元素充能效率': 0},
    '九条裟罗': {'生命值': 0, '攻击力': 0.75, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0, '元素充能效率': 0.55},
    '菲谢尔': {'生命值': 0, '攻击力': 0.75, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0, '元素充能效率': 0},
    '丽莎': {'生命值': 0, '攻击力': 0.75, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0.75, '元素充能效率': 0},
    '雷泽': {'生命值': 0, '攻击力': 0.75, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0, '元素充能效率': 0},
    '北斗': {'生命值': 0, '攻击力': 0.75, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0.75, '元素充能效率': 0.55},

    # 岩
    '旅行者-岩': {'生命值': 0, '攻击力': 0.75, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0, '元素充能效率': 0.55},
    '云堇': {'生命值': 0, '攻击力': 0, '防御力': 1, '暴击率': 0.5, '暴击伤害': 0.5, '元素精通': 0, '元素充能效率': 0.9},
    '荒泷一斗': {'生命值': 0, '攻击力': 0.5, '防御力': 1, '暴击率': 1, '暴击伤害': 1, '元素精通': 0, '元素充能效率': 0.3},
    '五郎': {'生命值': 0, '攻击力': 0.5, '防御力': 1, '暴击率': 0.5, '暴击伤害': 0.5, '元素精通': 0, '元素充能效率': 0.9},
    '阿贝多': {'生命值': 0, '攻击力': 0, '防御力': 1, '暴击率': 1, '暴击伤害': 1, '元素精通': 0, '元素充能效率': 0},
    '钟离': {'生命值': 0.8, '攻击力': 0.75, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0, '元素充能效率': 0.55},
    '凝光': {'生命值': 0, '攻击力': 0.75, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0, '元素充能效率': 0},
    '诺艾尔': {'生命值': 0, '攻击力': 0.5, '防御力': 1, '暴击率': 1, '暴击伤害': 1, '元素精通': 0, '元素充能效率': 0.55},
}

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
character = ''
txt = pytesseract.image_to_string(Image.open('test/test_img/example.png'), lang = 'chi_sim')

# 截图与ocr识别
def ocr(x, y, w, h):
    # time.sleep(0.2)
    # 可能未安装ocr引擎
    try:
        img = ImageGrab.grab(bbox = (x, y, x + w, y + h))
        txt = pytesseract.image_to_string(img, lang = 'chi_sim')
        print(txt)
        return txt
    except:
        print('未安装tesseract引擎或中文简体语言包')

# 文字处理与分数计算
def cal_score(txt, character):
    txt = txt.replace(' ', '')

    # 一些误识别兼容
    txt = txt.replace('仿', '伤')
    txt = txt.replace('传', '伤')
    txt = txt.replace('传', '伤')
    txt = txt.replace('政', '功')
    txt = txt.replace('宇', '击')
    txt = txt.replace('出', '击')
    txt = txt.replace('宠', '害')
    txt = txt.replace('宓', '害')
    txt = txt.replace('演', '爆')
    txt = txt.replace('宏', '素')

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
            # 词条名称
            name = re.findall(pattern_chinese, item)
            name = name[0]
            # 数值
            digit = float(re.search(pattern_digit, item).group())
            # 识别可能出错，词条不在表中
            try:
                if '%' in item:
                    score += digit * coefficient[name][0] * valuable[name]
                    print(name, digit, '%', score)
                else:
                    score += digit * coefficient[name][1] * valuable[name]
                    print(name, digit, score)
            except:
                print(name + ' 词条名称识别有误！')
    
    return round(score, 1)

def main(character, x, y, w, h):
    print(character)
    txt = ocr(x, y, w, h)
    score = cal_score(txt, character)
    return score

if __name__ == '__main__':
    main(character, x, y, w, h)