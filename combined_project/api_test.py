import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

response = requests.get(
    os.getenv("API_URL"),
    params={"page": 1},
    headers={"x-api-key": os.getenv("API_KEY")}
)

print(response.status_code)
print(json.dumps(response.json(), indent=4))