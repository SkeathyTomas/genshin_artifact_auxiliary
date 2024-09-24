import json, doc, copy

def update():
    # 读取存档数据
    with open(doc.archive_path, 'r', encoding='utf-8') as fp:
        keqing_out = json.load(fp)

    # mona格式框架
    mona_out = {'version': '1', 'flower': [], 'feather': [], 'sand': [], 'cup': [], 'head': []}
    mona_basic = {
        "setName": "",
        "position": "",
        "mainTag": {
            "name": "",
            "value": 0
            },
        "normalTags": [],
        "omit": False,
        "level": 20,
        "star": 5,
        "id": 0
        }

    # 映射表
    set_name_map ={'悠古的磐岩': 'archaicPetra', '冰风迷途的勇士': 'blizzardStrayer', '染血的骑士道': 'bloodstainedChivalry', '炽烈的炎之魔女': 'crimsonWitch', '深林的记忆': 'DeepwoodMemories', '来歆余响': 'EchoesOfAnOffering', '绝缘之旗印': 'emblemOfSeveredFate', '乐园遗落之花': 'FlowerOfParadiseLost', '沙上楼阁史话': 'DesertPavilionChronicle', '饰金之梦': 'GildedDreams', '角斗士的终幕礼': 'gladiatorFinale', '黄金剧团': 'GoldenTroupe', '沉沦之心': 'heartOfDepth', '华馆梦醒形骸记': 'huskOfOpulentDreams', '渡过烈火的贤人': 'lavaWalker', '被怜爱的少女': 'maidenBeloved', '逐影猎人': 'MarechausseeHunter', '昔日宗室之仪': 'noblesseOblige', '水仙之梦': 'NymphsDream', '海染砗磲': 'oceanHuedClam', '苍白之火': 'paleFlame', '逆飞的流星': 'retracingBolide', '追忆之注连': 'shimenawaReminiscence', '千岩牢固': 'tenacityOfTheMillelith', '如雷的盛怒': 'thunderingFury', '平息雷鸣的尊者': 'thunderSmoother', '辰砂往生录': 'VermillionHereafter', '翠绿之影': 'viridescentVenerer', '花海甘露之光': 'VourukashasGlow', '流浪大地的乐团': 'wandererTroupe', '昔时之歌': 'SongOfDaysPast', '回声之林夜话': 'NighttimeWhispersInTheEchoingWoods', '谐律异想断章': 'FragmentOfHarmonicWhimsy', '未竟的遐思': 'UnfinishedReverie', '黑曜秘典': 'ObsidianCodex', '烬城勇者绘卷': 'ScrollOfTheHeroOfCinderCity'}
    position_map = {'生之花': 'flower', '死之羽': 'feather', '时之沙': 'sand', '空之杯': 'cup', '理之冠': 'head'}
    main_name_map = {'攻击力': 'attackPercentage','生命值': 'lifePercentage', '防御力': 'defendPercentage', '暴击率': 'critical', '暴击伤害': 'criticalDamage', '治疗加成': 'cureEffect', '元素精通': 'elementalMastery', '元素充能效率': 'recharge', '雷元素伤害加成': 'thunderBonus', '火元素伤害加成': 'fireBonus', '水元素伤害加成': 'waterBonus', '冰元素伤害加成': 'iceBonus', '风元素伤害加成': 'windBonus', '岩元素伤害加成': 'rockBonus', '草元素伤害加成': 'dendroBonus', '物理伤害加成': 'physicalBonus'}
    normal_name_map = {'攻击力': 'attackStatic', '攻击力百分比': 'attackPercentage', '生命值': 'lifeStatic', '生命值百分比': 'lifePercentage', '防御力': 'defendStatic', '防御力百分比': 'defendPercentage', '元素精通': 'elementalMastery', '元素充能效率': 'recharge', '暴击率': 'critical', '暴击伤害': 'criticalDamage'}

    id = 0
    for key, groups in keqing_out['背包'].items():
        # 套装名称
        try:
            mona_basic['setName'] = ('{' + key + '}').format(**set_name_map)
        except:
            mona_basic['setName'] = key

        for items in groups.values():
            # print(items[0], items[1])
            # 部位
            mona_basic['position'] = ('{' + items[0][1] + '}').format(**position_map)

            # 主属性
            if mona_basic['position'] == 'flower':
                mona_basic['mainTag']['name'] = 'lifeStatic'
                mona_basic['mainTag']['value'] = eval(items[0][3])
            elif mona_basic['position'] == 'feather':
                mona_basic['mainTag']['name'] = 'attackStatic'
                mona_basic['mainTag']['value'] = eval(items[0][3])
            else:
                mona_basic['mainTag']['name'] = ('{' + items[0][2] + '}').format(**main_name_map)
                if '%' in items[0][3]:
                    mona_basic['mainTag']['value'] = eval(items[0][3][:-1]) / 100
                else:
                    mona_basic['mainTag']['value'] = eval(items[0][3])

            # 副属性
            mona_basic['normalTags'] = []
            for normal_name, normal_value in items[1].items():
                if normal_name == '攻击力' or normal_name == '防御力' or normal_name == '生命值' or normal_name == '元素精通':
                    normal_value_t = int(normal_value)
                else:
                    normal_value_t = normal_value / 100
                try:
                    mona_basic['normalTags'].append({'name': ('{' + normal_name + '}').format(**normal_name_map), 'value': normal_value_t})
                except:
                    pass
            
            # id
            mona_basic['id'] = id
            id += 1

            # 添加到mona_out中
            mona_out[mona_basic['position']].append(copy.deepcopy(mona_basic))

    with open(doc.mona_path, 'w', encoding = 'utf-8') as fp:
        json.dump(mona_out, fp, ensure_ascii = False)

if __name__ == '__main__':
    update()