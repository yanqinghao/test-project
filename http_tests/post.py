import requests

url = "http://localhost:8080/train"

data = {"path": "/data/engine", "label": "engine"}

r = requests.post(url, data=data)

print(r.content)
