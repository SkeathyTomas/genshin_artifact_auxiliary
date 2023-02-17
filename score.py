'''计算圣遗物评分'''

# 基础词条系数
coefficient = {
    '暴击率': 2,
    '暴击伤害': 1,
    '攻击力百分比': 1.331429,
    '生命值百分比': 1.331429,
    '防御力百分比': 1.066362,
    '攻击力': 0.199146,
    '生命值': 0.012995,
    '防御力': 0.162676,
    '元素精通': 0.332857,
    '元素充能效率': 1.197943
}

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

def cal_score(ocr_result, config):
    '''计算圣遗物评分
    参数：
        ocr_result: ocr识别结果字典dict
            {'防御力': 23.0, '元素充能效率': 5.8, '暴击伤害': 5.4}
        config: 角色配置dict
            {'生命值': 0, '攻击力': 0.75, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0, '元素充能效率': 0}
    返回：
        scores: 每个词条单独的评分列表list
            [0.0, 6.3, 5.4, 0.0]
        round(sums, 1): 总分float
            11.7
    '''
        
    scores = []
    powerupArray = []
    sums = 0
    for key, value in ocr_result.items():
        
        # 兼容角色配置未区分百分比的情况
        if key == '生命值百分比' or  key == '攻击力百分比' or key == '防御力百分比':
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
    
    print(scores, round(sums, 1), '\n')
    return scores, round(sums, 1), powerupArray