import json, base64
from pathlib import Path

#Grab your API key
folder = Path("API-keys")
file = folder / "key.json"
key = json.load(open(file))
print(key)