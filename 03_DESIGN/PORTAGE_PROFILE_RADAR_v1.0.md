# Portage de ProfileRadar — React legacy → statique exposable

**Version** : 1.0 — 2026-06-25
**Statut** : portage réalisé (version statique prête), **non mis en prod** (non lié au site).
**Contexte** : la prod est le site statique `ivia_site_v2` ; le React vit dans le Next.js
legacy (`09_app_ivia_merlin`), non servi.

---

## 1. Audit du composant actuel
`09_app_ivia_merlin/src/components/ProfileRadar.tsx` :
- **Forces** : radar **SVG natif** (aucune lib de chart), animation rAF (easeOutCubic),
  5 couches, superposition client/praticien, props `profileA/profileB/activeLayer/onLayerChange`.
- **Liens framework** : React 19 (`useState/useEffect/useMemo/useRef`), JSX, TypeScript,
  directive `"use client"`, classes Tailwind. → **non exécutable hors Next.js**.
- **Risque d'exposition** : un radar **représente des scores** ; en surface **client** cela
  heurte **B3** (pas de scores bruts). À réserver à une **surface interne** (praticien) ou à
  concevoir une variante client revue.

## 2. Dépendances à retirer
| Retiré | Remplacé par |
|---|---|
| React + hooks | Web Component natif (`customElements`) + état d'instance |
| JSX / TSX / TypeScript | JS vanilla + DOM/SVG (`createElementNS`) |
| `"use client"` / Next.js | aucun build, `<script>` simple |
| (classes Tailwind) | CSS injecté + **variables d'ambiance** (`var(--forest-deep)`, `--accent-2`, `--bdr`, `--muted`, `--surface`) avec repli clair |
| (aucune lib chart) | déjà du SVG → **rien à retirer** |

## 3. Version statique cible (livrée)
- `ivia_site_v2/shared/profile-radar.js` — **`<ivia-profile-radar>`** (Web Component, 0 dépendance).
  - Propriétés JS : `profileA`, `profileB`, `activeLayer` ; attribut `active-layer`, `label-a/b`.
  - Événement : `layer-change` (`e.detail.layer`).
  - Thémable Signature/Doux via les tokens `ivia-espace.css` (repli clair si absents).
- `ivia_site_v2/design-system/profile-radar-demo.html` — démo autonome **non liée** (Signature/Doux),
  vérifiée au navigateur (2 ambiances, toggle des 5 couches, overlay, 0 erreur console).

## 4. Plan de portage (ordonné)
1. ✅ Extraire la logique pure (config couches, normalisation, géométrie polaire) — framework‑agnostique.
2. ✅ Encapsuler en Web Component (light DOM pour hériter des tokens d'ambiance).
3. ✅ Réimplémenter l'animation en rAF + **respect `prefers-reduced-motion`**.
4. ✅ Accessibilité : `role="img"` + `<title>/<desc>`, onglets `role=tab` + **navigation clavier** (←/→), légende.
5. ✅ Démo autonome + vérification visuelle (Signature/Doux).
6. ⏸️ (le jour de l'ouverture) Décider de la **surface** : interne (praticien) par défaut ; si client,
   variante revue (B3) + passage `profiling_safety_suite_v1`.
7. ⏸️ Brancher sur de **vraies données** (via les routes internes du câblage) — **non fait** ici.

## 5. Contraintes tenues
- **Accessibilité** : SVG `role=img` + titre/description ; onglets clavier ←/→ + `aria-selected` ;
  légende textuelle ; respect de `prefers-reduced-motion` (animation désactivée si demandé) ;
  cibles tactiles ≥ ~32 px.
- **Sobriété sémantique** : libellés d'axes neutres (préférences/tendances), aucun terme clinique.
- **Non‑diagnostic** : `<desc>` indique explicitement « Visualisation de tendances ; ce n'est pas un
  diagnostic » ; aucun chiffre/score affiché (seulement des formes) ; surface **interne** par défaut.

## 6. Ce qui n'est PAS fait (volontaire)
- **Aucune mise en prod** : le composant et la démo ne sont liés à **aucune** page publique.
- Aucune donnée réelle branchée ; aucune variante client validée.
- Le React legacy (`ProfileRadar.tsx`) est **conservé** (référence) — non supprimé.

## 7. Fichiers
- `ivia_site_v2/shared/profile-radar.js` (nouveau)
- `ivia_site_v2/design-system/profile-radar-demo.html` (nouveau, non lié)
- `09_app_ivia_merlin/src/components/ProfileRadar.tsx` (conservé, legacy)
