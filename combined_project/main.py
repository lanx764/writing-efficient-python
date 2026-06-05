import requests

response = requests.get(
    "https://reqres.in/api/users",
    params={"page": 1},
    headers={"x-api-key": "your_key_here"}  # temporary hardcode just for this inspection step
)

print(response.json())