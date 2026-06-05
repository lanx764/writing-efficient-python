import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

response = requests.get(
    "https://reqres.in/api/users",
    params={"page": 1},
    headers={"x-api-key": os.getenv("API_KEY")}
)

print(response.status_code)
print(json.dumps(response.json(), indent=4))