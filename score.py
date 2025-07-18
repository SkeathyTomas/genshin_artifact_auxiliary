'''计算圣遗物评分、词条数、词条强化次数'''

import json
from doc import coefficient_path  # 导入 coefficient_path

# 平均单词条数值
average = {
    '暴击率': 3.3,
    '暴击伤害': 6.6,
    '攻击力百分比': 4.975,
    '生命值百分比': 4.975,
    '防御力百分比': 6.2,
    '攻击力': 16.75,
    '生命值': 254,
    '防御力': 19.75,
    '元素精通': 19.75,
    '元素充能效率': 5.5
}

# 基础词条系数动态加载
def load_coefficient():
    with open(coefficient_path, "r", encoding = 'utf-8') as f:
        return json.load(f)
coefficient = load_coefficient()

def cal_score(ocr_result_sub, config):
    '''计算圣遗物评分、词条数、词条强化次数
    参数：
        ocr_result_sub: ocr识别结果中副词条dict
            {'防御力': 23.0, '元素充能效率': 5.8, '暴击伤害': 5.4}
        config: 角色配置dict
            {'生命值': 0, '攻击力': 0.75, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0, '元素充能效率': 0}
    返回：
        scores: 每个词条单独的评分列表list
            [0.0, 6.3, 5.4, 0.0]
        round(sums, 1): 总分float
            11.7
        owerupArray: 强化次数列表list
            [0, 1, 2, 1]
        round(entriesSum, 1): 有效词条数float
            4.5
    '''
    
    scores = []
    powerupArray = []
    sums = 0
    entriesSum = 0
    for key, value in ocr_result_sub.items():
        
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

        # 计算强化次数
        try:
            powerup = round(value / average[key]) - 1
        except:
            powerup = 0
        powerupArray.append(powerup)

        # 计算有效词条数量
        if key_s in config and config[key_s]>0 :
            entries = value / average[key]
            # print(key, entries)
            entriesSum += entries
    
    print(scores, round(sums, 1), powerupArray, round(entriesSum, 1))
    return scores, round(sums, 1), powerupArray, round(entriesSum, 1)