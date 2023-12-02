import json

f = open('resp.json')
d = json.load(f)

print(d["choices"][0]["message"]["content"])