# Audit JS : chaque page doit inclure les scripts partages qui definissent
# les fonctions qu'elle appelle (api.js, session.js, mock.js, layout.js).
import re
import os
import glob
import sys

ROOT = 'C:/MERLIN/ivia_site_v2'

# Fonctions definies par chaque script partage
defs = {}
for js in glob.glob(ROOT + '/shared/*.js'):
    nom = os.path.basename(js)
    s = open(js, encoding='utf-8').read()
    fns = set(re.findall(r'(?:^|\n)\s*(?:async\s+)?function\s+(\w+)', s))
    fns |= set(re.findall(r'(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?(?:\(|function)', s))
    fns |= set(re.findall(r'window\.(\w+)\s*=', s))
    defs[nom] = fns

print('--- definitions par script partage ---')
for nom, fns in sorted(defs.items()):
    print(f'{nom}: {", ".join(sorted(fns))}')

problemes = []
for page in sorted(glob.glob(ROOT + '/**/*.html', recursive=True)):
    rel = os.path.relpath(page, ROOT).replace(os.sep, '/')
    if rel.startswith(('design-system/', 'src/')):
        continue
    s = open(page, encoding='utf-8').read()
    inclus = set(re.findall(r'src="/shared/(\w+\.js)', s))
    dispo = set()
    for i in inclus:
        dispo |= defs.get(i, set())
    # fonctions locales definies dans la page elle-meme
    locales = set(re.findall(r'(?:^|\n)\s*(?:async\s+)?function\s+(\w+)', s))
    locales |= set(re.findall(r'(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?(?:\(|function)', s))
    # tous les appels candidats aux fonctions partagees connues
    toutes_partagees = set().union(*defs.values()) if defs else set()
    appels = set(re.findall(r'\b(\w+)\s*\(', s))
    for a in sorted(appels & toutes_partagees):
        if a not in dispo and a not in locales:
            origines = [n for n, f in defs.items() if a in f]
            problemes.append(f'{rel}: appelle {a}() mais n\'inclut pas {"/".join(origines)}')

print(f'\n=== {len(problemes)} problemes JS ===')
for p in problemes:
    print(p)
sys.exit(1 if problemes else 0)
