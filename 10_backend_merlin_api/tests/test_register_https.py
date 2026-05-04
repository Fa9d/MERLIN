import urllib.request, json, ssl

ctx = ssl.create_default_context()

payload = {
    "email": "testclient01@fa9.quebec",
    "password": "TestMerlin1!",
    "display_name": "Client Test"
}

data = json.dumps(payload).encode()
req = urllib.request.Request(
    "https://api.ivia.quebec/api/v1/register/client",
    data,
    {"Content-Type": "application/json"},
    method="POST"
)

try:
    r = urllib.request.urlopen(req, context=ctx)
    print("STATUS:", r.status)
    print("BODY:", r.read().decode())
except urllib.error.HTTPError as e:
    print("HTTP ERROR:", e.code)
    print("BODY:", e.read().decode())
except Exception as e:
    print("ERROR:", type(e).__name__, str(e))
