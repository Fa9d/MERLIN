# Audit des liens internes du site statique ivia_site_v2.
# Reproduit la resolution nginx : try_files $uri $uri.html $uri/ /404.html
import re
import os
import glob
import sys

ROOT = 'C:/MERLIN/ivia_site_v2'
EXTERNES = ('http', 'mailto:', 'tel:', 'javascript:', 'data:', '#')


def resolu(target: str, page_dir: str):
    t = target.split('#')[0].split('?')[0]
    if not t or target.startswith(EXTERNES):
        return True
    p = ROOT + t if t.startswith('/') else os.path.join(page_dir, t)
    if os.path.exists(p) or os.path.exists(p + '.html'):
        return True
    if os.path.isdir(p) and os.path.exists(os.path.join(p, 'index.html')):
        return True
    return False


pages = glob.glob(ROOT + '/**/*.html', recursive=True)
problemes = []
for page in sorted(pages):
    rel = os.path.relpath(page, ROOT).replace(os.sep, '/')
    if rel.startswith(('design-system/', 'src/')):
        continue  # maquettes / sources non servies
    s = open(page, encoding='utf-8').read()
    refs = re.findall(r'(?:href|src|action)=["\']([^"\']+)["\']', s)
    refs += re.findall(r'location\.(?:href\s*=|replace\()\s*["\']([^"\']+)["\']', s)
    for r in sorted(set(refs)):
        if not resolu(r, os.path.dirname(page)):
            problemes.append(f'{rel}: lien casse -> {r}')

print(f'=== {len(pages)} pages, {len(problemes)} liens casses ===')
for p in problemes:
    print(p)
sys.exit(1 if problemes else 0)
