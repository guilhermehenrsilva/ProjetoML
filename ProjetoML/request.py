import requests

url = 'http://localhost:5000/api'

data = {
    "gender": 0,
    "age": 25,
    "height": 175,
    "weight": 80,
    "family_history": 1,
    "fcvc": 2,
    "ncp": 3,
    "caec": 1,
    "ch2o": 2,
    "faf": 1,
    "tue": 2,
    "calc": 0,
    "mtrans": 1
}

r = requests.post(url, json=data)
print(r.json())
