'''个人数据另外储存'''

import json, os, shutil

folder = os.path.expanduser('~/Documents')
folder = folder + '/keqing'
character_path = folder + '/character.json'
archive_path = folder + '/archive.json'
mona_path = folder + '/mona.json'
coefficient_path = folder + '/coefficient.json'

# 创建存档文件
def create_archieve():
    with open(archive_path, 'w', encoding = 'utf-8') as fp:
            artifacts = {'背包':{}, '角色': {}}
            json.dump(artifacts, fp, ensure_ascii = False)

# 创建词条配置文件
def create_coefficient():
    with open(coefficient_path, 'w', encoding = 'utf-8') as fp:
        coefficient = {"暴击率": 2.0,
                       "暴击伤害": 1.0,
                       "攻击力百分比": 1.33,
                       "生命值百分比": 1.33,
                       "防御力百分比": 1.06,
                       "攻击力": 0.199,
                       "生命值": 0.01716,
                       "防御力": 0.2211,
                       "元素精通": 0.33,
                       "元素充能效率": 1.1979}
        json.dump(coefficient, fp, ensure_ascii = False)

# 数据文件夹存在则更新、补充相关配置文件
if os.path.exists(folder):
    # 角色配置不存在就复制一份，存在进行对比，有新角色添加则增量更新
    if not os.path.exists(character_path):
        shutil.copy('src/character.json', character_path)
    else:
        with open('src/character.json', 'r', encoding = 'utf-8') as fp:
            default = json.load(fp)
        with open(character_path, 'r', encoding = 'utf-8') as fp:
            user = json.load(fp)
        diff = default.keys() - user.keys()
        if diff != set():
            for item in diff:
                user[item] = default[item]
            with open(character_path, 'w', encoding = 'utf-8') as fp:
                json.dump(user, fp, ensure_ascii = False)
    
    # 
    if not os.path.exists(archive_path):
        create_archieve()
    # 
    if not os.path.exists(coefficient_path):
        create_coefficient()

# 数据文件夹不存在则新建文件夹并复制、新建相关数据文件
else:
    os.makedirs(folder)
    shutil.copy('src/character.json', character_path)
    create_archieve()
    create_coefficient()
