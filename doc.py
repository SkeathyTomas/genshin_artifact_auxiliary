'''个人数据另外储存'''
import json, os, shutil

username = os.getlogin()
folder = 'C:/Users/' + username + '/Documents/keqing'
character_path = folder + '/character.json'
archive_path = folder + '/archive.json'

if os.path.exists(folder):
    if not os.path.exists(character_path):
        shutil.copy('src/character.json', character_path)
    if not os.path.exists(archive_path):
        with open(archive_path, 'w', encoding = 'utf-8') as fp:
            artifacts = {'背包':{}, '角色': {}}
            json.dump(artifacts, fp, ensure_ascii = False)
else:
    os.mkdir(folder)
    shutil.copy('src/character.json', character_path)
    with open(archive_path, 'w', encoding = 'utf-8') as fp:
        artifacts = {'背包':{}, '角色': {}}
        json.dump(artifacts, fp, ensure_ascii = False)