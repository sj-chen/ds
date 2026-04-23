import requests



resp = requests.post("http://192.168.1.49:8085/sso/login",data={"username": "member", "password": "member123"})
print(resp.json(), resp.status_code)