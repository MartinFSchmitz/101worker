import requests
import json

data = open('input.json').read()

headers = {'content-type': 'application/json'}

r = requests.post("http://localhost:5000/services/worker/contribution", data=data, headers=headers)

print r.text

