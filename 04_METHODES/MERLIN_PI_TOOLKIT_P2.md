# MERLIN — Intégration `pi` toolkit (LLM unifiée) — Roadmap P2

**Version**: v1.0 — 2026-05-15  
**Horizon**: Phase 2 — M12 à M24  
**Statut**: veille technologique — pas en production

---

## Qu'est-ce que `pi` (syntaix.ai)

`pi` est un toolkit Python de couche d'abstraction multi-LLM permettant de router
des requêtes vers plusieurs fournisseurs (Anthropic, OpenAI, Mistral, vLLM local)
avec une interface unifiée. Il vise à :

- Remplacer les appels hardcodés au SDK Anthropic par un client agnostique.
- Activer le fallback automatique (Claude → GPT-4.1 → modèle local) selon disponibilité/coût.
- Préparer la route vers l'inférence locale avec **vLLM** (M18-M24).

---

## Pertinence pour MERLIN

| Scénario | Pertinence | Horizon |
|----------|-----------|---------|
| Pipeline post-séance (Deepgram → GPT → Claude) | ✅ Élevée — unifie le routing | M12 |
| Fallback automatique si quota Anthropic atteint | ✅ Élevée — résilience opérationnelle | M12 |
| Inférence locale (vLLM) pour données sensibles | ✅ Stratégique — données au Québec | M18-M24 |
| Dev tooling (CLI) pour tests de prompts | ✅ Utile maintenant en sandbox | Sandbox |
| Intégration en production P1 | ❌ Hors scope — risques dépendance | — |

---

## Architecture cible P2

```
app/services/llm_client.py       # Nouveau : client pi unifié
├── provider: "anthropic"        # P1 (par défaut)
├── provider: "openai"           # Fallback
└── provider: "vllm_local"       # P2 M18 (inférence locale OVH)
```

Le pipeline actuel (`generate_session_summary_job`) appelle directement le SDK
Anthropic. En P2, il appellera `llm_client.py` avec un `provider` configurable
via variable d'environnement (`LLM_PROVIDER=anthropic|openai|vllm`).

---

## Règles d'adoption (héritées de la politique laboratoire §7)

- Ne **pas** installer `pi` ou tout package syntaix.ai en production avant validation sandbox complète.
- Toute expérimentation dans `docs/labs/pi-toolkit-poc/` (worktree ou container isolé).
- POC obligatoire : tester le routing fallback sur au moins 100 appels simulés avec les prompts MERLIN.
- La couche `pi` ne doit **jamais** router des données client vers un service tiers non encadré (Loi 25, LPRPDE).
- L'activation vLLM local est conditionnelle à une analyse de conformité données complète.

---

## Prérequis avant activation

1. **Audit de conformité** : vérifier que `pi` ne loggue pas les payloads vers des serveurs externes.
2. **Tests d'évaluation** : passer la safety_suite_v1 sur le pipeline avec `pi` activé (score ≥ 0.85 sur les 10 catégories).
3. **Infrastructure** : RAM et GPU disponibles sur le VPS OVH pour vLLM (>= 24 Go VRAM pour Mistral 7B).
4. **Contrat fournisseur** : si `pi` devient dépendance → analyse juridique du ToS syntaix.ai.

---

## Références

- Repo source : `https://github.com/syntaix-ai/pi` (lire en lecture seule, ne pas forker en prod)
- vLLM : `https://github.com/vllm-project/vllm`
- Politique laboratoire MERLIN : `CLAUDE.md §7`
- Safety suite : `managed_agents/evals/safety_suite_v1.yaml`

---

## Prochaine action

> **M12** : Créer `docs/labs/pi-toolkit-poc/` et tester le routing Claude → GPT-4.1-mini
> sur 50 appels de `generate_session_summary_job` en sandbox isolé.
> Documenter les latences, coûts, et conformité payload dans `05_JOURNAUX/`.
