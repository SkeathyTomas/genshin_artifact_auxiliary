import requests

response = requests.get('https://api.github.com/repos/SkeathyTomas/genshin_artifact_auxiliary/releases/latest')
print(response.json()['tag_name'])