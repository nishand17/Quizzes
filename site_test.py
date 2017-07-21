import requests
response = requests.get(url='http://localhost:5000/quiz/1/1/', json={"body": "<html>", "relational_id": 1})
print(response.text)