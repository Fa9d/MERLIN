# Délivrabilité des courriels IVIA — SPF / DKIM / DMARC (OVH)

**But** : qu'IVIA envoie ses courriels (magic link, notifications, rappels) **From
`noreply@ivia.quebec`**, authentifiés (SPF + DKIM alignés) et couverts par DMARC — pour
ne pas tomber en spam et arrêter de transiter par `fa9.quebec`.

## État constaté (2026-06-21)

| Élément | État |
|---|---|
| From réel du backend | ❌ `david@fa9.quebec` (devrait être `noreply@ivia.quebec`) |
| SMTP | OVH `ssl0.ovh.net:465` (SSL) |
| `ivia.quebec` SPF | ✅ `v=spf1 include:mx.ovh.com ~all` |
| `ivia.quebec` MX | ✅ OVH |
| `ivia.quebec` DKIM | ❌ absent |
| `_dmarc.ivia.quebec` | ❌ absent |
| Réception | toutes les adresses redirigent vers `davidphaneuf@gmail.com` |

> Rappel : une **redirection (alias)** ne gère que la **réception**. Pour **envoyer**
> « au nom de » une adresse avec DKIM, il faut une **vraie boîte SMTP** (pas un alias).

## Procédure (checklist)

- [ ] **1. Boîte d'envoi OVH** — créer une **vraie boîte** `noreply@ivia.quebec`
      (OVH → Email → MX Plan, gratuit avec le domaine). Pas un alias.
- [ ] **2. Redirection** — rediriger l'entrant de `noreply@ivia.quebec` vers
      `davidphaneuf@gmail.com` (cohérent avec le reste).
- [ ] **3. DKIM** — OVH → Email → onglet DKIM → **activer** pour `ivia.quebec`.
      OVH publie automatiquement le(s) sélecteur(s) `ovhmoXXXX._domainkey.ivia.quebec`.
      *(À faire AVANT de changer le From, sinon délivrabilité dégradée.)*
- [ ] **4. DMARC** — ajouter au DNS de `ivia.quebec` un TXT :
      - **Nom/hôte** : `_dmarc`
      - **Valeur** :
        ```
        v=DMARC1; p=none; rua=mailto:dmarc@ivia.quebec; ruf=mailto:dmarc@ivia.quebec; fo=1; adkim=r; aspf=r; pct=100
        ```
      - (`dmarc@ivia.quebec` peut être un alias qui redirige vers Gmail.)
- [ ] **5. Backend** — dans `/opt/merlin/.env.prod` :
      ```
      SMTP_FROM_EMAIL=noreply@ivia.quebec
      SMTP_FROM_NAME=IVIA
      SMTP_USERNAME=noreply@ivia.quebec
      SMTP_PASSWORD=<mot de passe de la boîte OVH>
      ```
      puis redémarrer l'API : `make restart` (ou `prod-up.sh`).
- [ ] **6. Test** — envoyer un courriel test (ex. magic link vers `davidphaneuf@gmail.com`)
      et vérifier dans Gmail : *Afficher l'original* → **SPF: PASS · DKIM: PASS · DMARC: PASS**,
      tous alignés sur `ivia.quebec`.

## Durcissement (après quelques jours de `p=none` sans surprise)

1. `p=none` → `p=quarantine; pct=25` puis `pct=100`.
2. Puis `p=reject` quand tous les envois légitimes passent → protège `ivia.quebec`
   contre l'usurpation.

## Vérifications (depuis le VPS)

```bash
dig +short TXT ivia.quebec
dig +short TXT _dmarc.ivia.quebec
dig +short TXT ovhmo1._domainkey.ivia.quebec   # selecteur exact donné par OVH
```

## Note `fa9.quebec`

Tant que le From reste `fa9.quebec`, les rapports DMARC `fa9.quebec` continuent
(c'est sain — DKIM `fa9.quebec` passe). Ils cesseront d'être liés à IVIA dès l'étape 5.
