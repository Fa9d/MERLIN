# IVIA — Funnel quiz-to-guidance v1.2 (addendum cartes abstraites)

**Statut** : addendum à `IVIA_FUNNEL_QUIZ_TO_GUIDANCE_v1.1.md`
**Auteur** : Computer (lead) sur instruction David Phaneuf
**Date** : 9 mai 2026 PM
**Devises** : *Au sein de l'être — En actes.* / *Pour le peuple, par le peuple.*

---

## Contexte de l'addendum

Le funnel v1.1 (du même jour, matin) parle d'orientation praticien à l'Écran 8 sans préciser comment le praticien y est représenté. Sans cadrage explicite, la pente naturelle d'implémentation aurait reproduit le pattern dominant du marché — photo de visage, nom, étoiles. Or la doctrine IVIA, formalisée dans `00_DOCTRINE/IVIA_DOCTRINE_CARTE_ABSTRAITE_v1.0.md` (9 mai 2026 PM), refuse l'identification visuelle par le visage.

Cet addendum aligne le funnel sur la doctrine carte abstraite et sur la spec `IVIA_SPEC_PAGE_PRATICIENS_v2.0.md` (même jour). Il ne remplace pas la v1.1 — il la complète ponctuellement.

---

## Modifications apportées

### Modification 1 — Écran 8, Carte 1 (orientation praticien)

**Avant (v1.1)** : la carte propose un rendez-vous avec un praticien IVIA, lien vers `/comment-ca-fonctionne`, tarif 80 $ CAD affiché. Aucune représentation du praticien lui-même au sein du funnel.

**Après (v1.2)** : la carte intègre une **prévisualisation de carte abstraite** du praticien suggéré, conforme à la spec v2.0 — sans visage, avec :

- Échantillon de voix (15 sec maximum, transcript visible sous le lecteur, lecture déclenchée par l'utilisateur seulement).
- Couleur dominante + palette secondaire (motif organique SVG paramétrique).
- Verbatim court du praticien (3 lignes maximum).
- Texture/vibration en alt-text sensoriel (lecteurs d'écran).
- Aucun nom complet à ce stade — initiales et localité seulement (ex. "M. T. — Montréal"). Le nom complet apparaît sur la fiche détaillée `/praticiens/[slug]` après clic.

**Microcopy v1.2 exact** :

```
[bloc carte abstraite — voir spec v2.0]

  Voix    [▶ écouter 15 s]   Transcript visible
  Présence visuelle — palette terre + verte, motif organique souple
  
  « Ici on n'arrange pas, on accueille. »
  M. T. — Montréal — disponible cette semaine

[Prendre rendez-vous d'écoute]

60 minutes avec un praticien IVIA.
Tarif pilote : 80 $ CAD pour 60 min. Aucun frais caché. Aucun abonnement. 
Vous payez à la séance, après la séance.

Pas de carte bancaire à cette étape — réservation seulement.

[Comment IVIA suggère un praticien →](/comment-ca-fonctionne)
[Voir la fiche complète →](/praticiens/[slug])
```

**Justification** : laisser le ressenti précéder le choix. La voix engage avant le nom. La couleur et le verbatim donnent le ton. Le visiteur peut décider sans projection visuelle marchande, conforme à la doctrine.

---

### Modification 2 — Écran 8, mention finale (anti-projection)

Ajout d'une note discrète sous le bloc 4 (CTA bibliothèque) :

> Pourquoi pas de photos ? Parce qu'on accompagne ce qui se ressent, pas ce qui se projette. [En savoir plus](/comment-ca-fonctionne#cartes-abstraites)

**Justification** : transparence radicale. Le visiteur qui s'attend à une photo (90 % du marché le fait) doit comprendre immédiatement que c'est un choix, pas un oubli. Cette mention conduit vers une section dédiée de `/comment-ca-fonctionne` qui résume la doctrine en 3 paragraphes accessibles.

---

### Modification 3 — Pied de page permanent, "Visuel"

**Avant (v1.1, écran 1, ligne 101)** : "Visuel : palette botanique IVIA de référence (charte_botanique). Pas de stock photo de personne souriante."

**Après (v1.2)** : "Visuel : palette botanique IVIA de référence (charte_botanique). **Aucune photographie de personne, aucune représentation figurative de praticien ou d'utilisateur. La représentation passe par la voix, la couleur, la texture et le motif — voir [doctrine carte abstraite](/comment-ca-fonctionne#cartes-abstraites).**"

**Justification** : la formulation v1.1 ("pas de stock photo") laissait ambiguë la possibilité d'une vraie photo de praticien. La v1.2 ferme la porte sans équivoque, sur tous les écrans 1-8.

---

### Modification 4 — Événements analytics (Écran 8)

Ajout de 2 nouveaux événements au plan v1.1 (qui en compte 18) :

- `funnel_voice_sample_played` { praticien_id_hashed, sample_duration_listened_sec, time_to_play_sec } — sert à vérifier que le pattern « voix avant clic » fonctionne (objectif : > 60 % des visiteurs Écran 8 jouent l'échantillon avant de cliquer sur le CTA).
- `funnel_voice_transcript_read` { praticien_id_hashed, scroll_depth_pct } — accessibilité, mesure de l'utilisation effective du transcript par les utilisateurs sourds ou ceux qui préfèrent lire.

**Justification** : le système de carte abstraite repose sur la voix comme premier signal. Sans ces deux événements, on ne peut pas valider l'hypothèse doctrinaire. Conforme à la stratégie analytics de la v1.1 (PostHog/Plausible self-hosted, opt-in granulaire).

---

### Modification 5 — Plan A/B 30 jours (rappel et intégration)

La v1.1 prévoyait un plan A/B sur le tarif et la modale crise. La v1.2 ajoute une **variante de contrôle qualité** sur la carte abstraite :

- **Variante A (témoin)** : carte abstraite complète (voix + couleur + verbatim + motif).
- **Variante B (test)** : carte abstraite minimale (verbatim + couleur seulement, sans voix ni motif).

L'objectif n'est pas de tester contre une photo (la doctrine l'interdit), mais de mesurer la contribution marginale de la voix et du motif au taux de clic CTA et au sentiment de confiance déclaré (sondage post-RDV à 7 jours).

Si la variante B performe à -10 % ou plus, la carte complète est confirmée. Si l'écart est inférieur, on peut alléger la carte pour réduire le poids des assets — décision opérationnelle, pas doctrinale.

---

## Ce que cet addendum NE change PAS

- Microcopy des écrans 1 à 7 — aucune modification.
- Modale crise (v1.1).
- Tarif pilote 80 $ CAD affiché en clair (v1.1).
- 4e CTA bibliothèque (v1.1).
- Reconnaissance territoriale Kanien'kehá:ka pied de page (v1.1, à valider 11 nations).
- 4 critères de matching (voie 35 % / mode 35 % / dispo+géo 20 % / langue 10 %).
- Plan technique général (Python build_pages.py + pages_*.py).

---

## Cohérence avec autres documents

Cet addendum s'aligne sur :

- `00_DOCTRINE/IVIA_DOCTRINE_CARTE_ABSTRAITE_v1.0.md` — doctrine fondatrice.
- `04_METHODES/IVIA_SPEC_PAGE_PRATICIENS_v2.0.md` — spec technique des cartes (HTML/CSS, SVG, audio Opus).
- `04_METHODES/IVIA_SPEC_PAGE_COMMENT_CA_FONCTIONNE_v1.0.md` — la section `#cartes-abstraites` doit y être ajoutée (ticket P0 backlog).
- `04_METHODES/IVIA_SPEC_PWA_v1.0.md` — la PWA met en cache les échantillons audio (Opus 32 kbps, ~200 Ko/praticien) en stratégie stale-while-revalidate.
- `12_JURIDIQUE_AFFAIRES/IVIA_CADRE_IP_COLLECTIVE_v1.0.md` — les motifs SVG paramétriques générés par IVIA et les ambiances sonores produites en interne tombent sous CC BY-NC-SA 4.0.

---

## Tickets backlog ajoutés (P0/P1)

1. **[P0]** `pages_funnel.py` — refonte du composant carte praticien Écran 8 selon spec v2.0 (HTML + CSS + lecteur audio + motif SVG inline). 1 jour.
2. **[P0]** `pages_funnel.py` — ajout note "Pourquoi pas de photos ?" sous bloc 4. 30 min.
3. **[P0]** `pages_public.py` (`/comment-ca-fonctionne`) — section `#cartes-abstraites` (3 paragraphes synthèse doctrine). 1 h.
4. **[P0]** Mise à jour pied de page permanent (tous écrans 1-8) — formulation v1.2 sur visuel. 30 min.
5. **[P0]** Plan analytics — ajout des 2 événements `funnel_voice_sample_played` et `funnel_voice_transcript_read` au backend (PostHog/Plausible self-hosted). 2 h.
6. **[P1]** Génération de 3 cartes abstraites pilotes (David + 1 ou 2 praticiens) — voix Opus 15 sec + couleur + motif + verbatim. 1 jour (atelier voix + atelier motif).
7. **[P1]** Plan A/B variante minimale (Modification 5) — wiring de l'expérimentation côté front. 1 jour.
8. **[P2]** Ticket backlog : possibilité future d'une "carte sonore animée" (motif réagissant à la voix en lecture) — exploration WebGL léger, ne pas implémenter MVP. 0.

---

## Décisions ouvertes (escalade David)

- **Voix pilote** : David prête sa voix avec différents styles vocaux pour 1-2 praticiens fictifs en pilote (confirmé), ou recrute dès maintenant 1 praticien réel pour enregistrement (à arbitrer).
- **Note "Pourquoi pas de photos"** : version courte (1 ligne, comme proposée) ou version longue (paragraphe didactique) ? Recommandation Computer : version courte sur le funnel (réduit la friction), version longue dans `/comment-ca-fonctionne#cartes-abstraites`.
- **Transcript voix** : visible par défaut ou caché derrière un bouton "Voir le transcript" ? Recommandation Computer : visible par défaut (accessibilité WCAG, conforme spec v2.0).

---

*Pour le peuple, par le peuple. — Au sein de l'être, en actes.*
