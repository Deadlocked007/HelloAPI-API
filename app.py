#flask/bin/python
from flask import Flask, request, jsonify, json
import requests

app = Flask(__name__)
pokeCache = {}

@app.route('/')
def index():
   return "Hello, World!"

@app.route('/pokemon', methods=['GET'])
def pokemon():
    pid = request.args.get('id')
    if not pid:
        return "You need to choose a Pokemon"
    
    if pid in pokeCache.keys():
        return jsonify(pokeCache[pid])

    baseURL = "https://pokeapi.co"
    mainURL = baseURL + "/api/v1/pokemon/" + pid

    info = requests.get(mainURL)
    infoJSON = json.loads(info.text)

    pokeInfo = {'name': infoJSON['name']}
    pokeInfo['attack'] = infoJSON['attack']
    pokeInfo['defense'] = infoJSON['defense']
    pokeInfo['sp_attack'] = infoJSON['sp_atk']
    pokeInfo['sp_defense'] = infoJSON['sp_def']
    pokeInfo['height'] = infoJSON['height']
    pokeInfo['weight'] = infoJSON['weight']
    pokeInfo['id'] = infoJSON['pkdx_id']
    pokeInfo['evolutions'] = infoJSON['evolutions']

    types = []
    typesArray = infoJSON['types']
    for t in typesArray:
        types.append(t['name'])
    pokeInfo['types'] = types

    descriptions = infoJSON['descriptions']
    descriptionInfo = descriptions[len(descriptions) - 1]
    descriptionURL = baseURL + descriptionInfo['resource_uri']
    descriptionJSON = json.loads(requests.get(descriptionURL).text)
    pokeInfo['description'] = descriptionJSON['description']

    sprites = infoJSON['sprites']
    lastSprite = sprites[len(sprites) - 1]
    spriteURL = baseURL + lastSprite['resource_uri']
    spriteJSON = json.loads(requests.get(spriteURL).text)
    pokeInfo['sprite'] = baseURL + spriteJSON['image']

    pokeCache[pid] = pokeInfo
    return jsonify(pokeInfo)


if __name__ == '__main__':
    app.run(debug=True)
