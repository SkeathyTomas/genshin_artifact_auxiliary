'''计算圣遗物评分'''

import json

# 基础词条系数
coefficient = {
    '暴击率': 2,
    '暴击伤害': 1,
    '元素精通': 0.33,
    '攻击力百分比': 1.33,
    '攻击力': 0.2,
    '生命值百分比': 1.33,
    '生命值': 0.02,
    '防御力百分比': 1.06,
    '防御力': 0.22,
    '元素充能效率': 1.2
}

def cal_score(ocr_result, character):
    '''计算圣遗物评分
    参数：
        ocr_result: ocr识别结果字典dict
            {'防御力': 23.0, '元素充能效率': 5.8, '暴击伤害': 5.4}
        character: 角色字符串
            '旅行者-风'
    返回：
        scores: 每个词条单独的评分列表list
            [0.0, 6.3, 5.4, 0.0]
        round(sums, 1): 总分float
            11.7
    '''

    # 获取角色配置，角色未输入或输入错误则取攻击双爆
    try:
        with open('src/character.json', 'r', encoding = 'UTF-8') as f:
            characters = json.load(f)
        config = characters[character]
    except:
        config = {'生命值': 0, '攻击力': 0.75, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0, '元素充能效率': 0}
    
    scores = []
    sums = 0
    for key, value in ocr_result.items():
        
        # 兼容角色配置未区分百分比的情况
        if key == '生命值百分比' or key == '攻击力百分比' or key == '防御力百分比':
            key_s = key[:3]
        else:
            key_s = key
        
        # key值存在误识别情况，则判定为0
        try:
            score = round(value * config[key_s] * coefficient[key], 1)
        except:
            score = 0
        scores.append(score)
        sums += score
    
    print(scores, round(sums, 1), '\n')
    return scores, round(sums, 1)