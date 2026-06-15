# Carte d'état des outils IVIA — classe chaque page du site selon sa source de données.
# REEL    : appelle l'API réelle (api.js) sans mock
# MIXTE   : appelle l'API réelle ET garde un repli mock
# FICTIF  : n'utilise que des données mock (getMock*/buildMock*)
# STATIQUE: page de contenu, aucune donnée dynamique
#
# Sortie : tableau Markdown sur stdout (sert de base au benchmark « connecter au réel »).
import re
import glob
import os

ROOT = "C:/MERLIN/ivia_site_v2"

REAL_FNS = [
    "apiLogin", "apiRegisterClient", "apiVerifyEmail", "apiMe", "apiSetPassword",
    "bookingCheckout", "pilotBook", "getMyClient", "getMyBookings", "getMyJournal",
    "createMyJournalEntry", "uploadMyRecording", "getMyRecordings", "createExpressSession",
    "getExpressSession", "uploadExpressRecording", "listPraticiens", "getAvailableSlots",
    "getMySchedule", "createScheduleBlock", "updateScheduleBlock", "deleteScheduleBlock",
    "getMyExceptions", "createScheduleException", "deleteScheduleException",
    "holdSlot", "confirmSlot", "cancelSlot",
]
MOCK_RE = re.compile(r"\b(getMock[A-Za-z]+|buildMock[A-Za-z]+)\s*\(")
REAL_RE = re.compile(r"\b(" + "|".join(REAL_FNS) + r")\s*\(")


def classify(path):
    s = open(path, encoding="utf-8").read()
    real = sorted(set(REAL_RE.findall(s)))
    mock = sorted(set(m[0] if isinstance(m, tuple) else m for m in MOCK_RE.findall(s)))
    has_api = "shared/api.js" in s
    if real and mock:
        verdict = "MIXTE"
    elif real:
        verdict = "REEL"
    elif mock:
        verdict = "FICTIF"
    else:
        verdict = "STATIQUE"
    return verdict, real, mock, has_api


rows = []
for path in sorted(glob.glob(ROOT + "/**/*.html", recursive=True)):
    rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
    if rel.startswith(("design-system/", "src/")):
        continue
    verdict, real, mock, has_api = classify(path)
    rows.append((rel, verdict, real, mock))

order = {"REEL": 0, "MIXTE": 1, "FICTIF": 2, "STATIQUE": 3}
rows.sort(key=lambda r: (r[0].split("/")[0], order[r[1]], r[0]))

print("| Page | État | API réelle utilisée | Mock restant |")
print("|------|------|---------------------|--------------|")
for rel, verdict, real, mock in rows:
    print(f"| `{rel}` | {verdict} | {', '.join(real) or '—'} | {', '.join(mock) or '—'} |")

from collections import Counter
c = Counter(r[1] for r in rows)
print()
print(f"**{len(rows)} pages** — RÉEL {c['REEL']} · MIXTE {c['MIXTE']} · FICTIF {c['FICTIF']} · STATIQUE {c['STATIQUE']}")
