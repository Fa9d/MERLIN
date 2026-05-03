import json, urllib.request
r = urllib.request.urlopen("http://localhost:8000/api/v1/openapi.json")
paths = json.loads(r.read())["paths"]
for p in paths:
    if "register" in p or "booking" in p or "verify" in p or "client" in p:
        print(p, list(paths[p].keys()))
