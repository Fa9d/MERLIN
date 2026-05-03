import urllib.request, json, sys

payload = {
    "email": "testclient01@fa9.quebec",
    "password": "TestMerlin1",
    "first_name_or_alias": "ClientTest",
    "is_adult_confirmed": True
}

data = json.dumps(payload).encode()
req = urllib.request.Request(
    "http://localhost:8000/v1/register/client",
    data,
    {"Content-Type": "application/json"},
    method="POST"
)

try:
    r = urllib.request.urlopen(req)
    print("STATUS:", r.status)
    print("BODY:", r.read().decode())
except urllib.error.HTTPError as e:
    print("HTTP ERROR:", e.code)
    print("BODY:", e.read().decode())
except Exception as e:
    print("ERROR:", type(e).__name__, str(e))
