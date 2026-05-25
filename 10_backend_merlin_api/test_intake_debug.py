import urllib.request, json, urllib.error

email = "debug_test3@example.com"
d = json.dumps({
    "first_name_or_alias": "DebugTest3",
    "email": email,
    "is_adult_confirmed": True,
    "consent_terms_accepted": True,
    "primary_need_code": "support",
    "perceived_urgency_code": "non_urgent",
    "support_already_in_place": False
}).encode()

for i in range(2):
    req = urllib.request.Request(
        "http://localhost:8000/api/v1/public/intake/start",
        d,
        {"Content-Type": "application/json"}
    )
    try:
        r = urllib.request.urlopen(req)
        resp = json.loads(r.read().decode())
        print(f"R{i+1} OK: client={resp['client_id'][:8]}")
    except urllib.error.HTTPError as e:
        print(f"R{i+1} ERR: {e.code} {e.read().decode()[:100]}")
