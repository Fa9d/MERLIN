import subprocess, re

# 1. Patch docker-compose.prod.yml — ajouter volume ivia_site_v2
dc_path = '/opt/merlin/docker-compose.prod.yml'
dc = open(dc_path).read()

vol_line = '      - ./ivia_site_v2:/var/www/ivia:ro'
anchor   = '      - ./deploy/nginx/nginx.conf:/etc/nginx/conf.d/default.conf:ro'

if vol_line not in dc:
    dc = dc.replace(anchor, anchor + '\n' + vol_line)
    open(dc_path, 'w').write(dc)
    print('[OK] Volume ivia ajouté au docker-compose')
else:
    print('[OK] Volume ivia déjà présent')

# 2. Vérifier que ivia_site_v2 existe sur le VPS
import os
if os.path.isdir('/opt/merlin/ivia_site_v2'):
    count = sum(len(f) for _, _, f in os.walk('/opt/merlin/ivia_site_v2'))
    print(f'[OK] ivia_site_v2 présent — {count} fichiers')
else:
    print('[ERREUR] /opt/merlin/ivia_site_v2 ABSENT — copier le site avant de continuer')

# 3. Stop + rm + start nginx
cmds = [
    'docker compose --env-file /opt/merlin/.env.prod -f /opt/merlin/docker-compose.prod.yml stop nginx',
    'docker compose --env-file /opt/merlin/.env.prod -f /opt/merlin/docker-compose.prod.yml rm -f nginx',
    'docker compose --env-file /opt/merlin/.env.prod -f /opt/merlin/docker-compose.prod.yml up -d --no-deps nginx',
    'docker compose --env-file /opt/merlin/.env.prod -f /opt/merlin/docker-compose.prod.yml logs --tail=6 nginx',
]
for cmd in cmds:
    print(f'\n$ {cmd}')
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd='/opt/merlin')
    print(r.stdout or r.stderr)
