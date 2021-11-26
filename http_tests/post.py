import requests

url = "https://sp.xuelangyun.com/proxr/shanglu/61812/14747c80420911eca21d75a6433baa8f/8899/checkCode"

data = {"code": "111111"}

r = requests.post(url, json=data)

print(r.content)
