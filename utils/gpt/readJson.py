import json

f = open('resp.json')
d = json.load(f)

print(d["choices"][0]["message"]["content"])

def validateJSON(jsonData):
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True