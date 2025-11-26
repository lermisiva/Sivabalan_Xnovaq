import requests 
url = "https://api.github.com/users/lermisiva"
response = requests.get(url)
data = response.json()
print(data["login"])
# git is a open source api