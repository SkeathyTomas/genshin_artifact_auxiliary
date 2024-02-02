'''个人数据另外储存'''
import json, os, shutil

folder = os.path.expanduser('~/Documents')
folder = folder + '/keqing'
character_path = folder + '/character.json'
archive_path = folder + '/archive.json'

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
    # 数据存档新建
    if not os.path.exists(archive_path):
        with open(archive_path, 'w', encoding = 'utf-8') as fp:
            artifacts = {'背包':{}, '角色': {}}
            json.dump(artifacts, fp, ensure_ascii = False)

# 数据文件夹不存在则复制、新建相关数据文件
else:
    os.makedirs(folder)
    shutil.copy('src/character.json', character_path)
    with open(archive_path, 'w', encoding = 'utf-8') as fp:
        artifacts = {'背包':{}, '角色': {}}
        json.dump(artifacts, fp, ensure_ascii = False)