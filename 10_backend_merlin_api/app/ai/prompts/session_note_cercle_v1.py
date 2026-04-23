from __future__ import annotations

import json
from typing import Any


SESSION_NOTE_CERCLE_PROMPT_VERSION = "session_note_cercle_v1"

QUEBEC_CONTEXT_HYPOTHESES = [
    "pression_silence_et_minimisation: minimisation repetee, consultation tardive, decalage ton/gravite -> hypothese prudente de retenue ou souffrance sous-declaree; dimension coeur/corps.",
    "pression_performance_travail: surmenage valorise, honte du repos, productivite comme valeur -> hypothese prudente de charge normalisee; dimension esprit/corps/etre.",
    "pression_isolement_relationnel: peu de reseau mobilisable, un seul filet relationnel, peur de deranger -> hypothese prudente d'isolement peu nomme; dimension coeur/etre.",
    "pression_honte_ambition_ou_reussite: gene a reussir, negocier, parler d'argent -> hypothese prudente de tension entre elan et permission; dimension etre/esprit.",
    "pression_identite_collective_fragile: hypersensibilite a la critique, fragilite de legitimite -> hypothese prudente de tension d'appartenance; dimension etre.",
    "pression_medicalisation_du_sens: recit colle au diagnostic, attente d'une solution externe -> hypothese prudente de langage de souffrance centre sur l'etiquette; dimension esprit/corps.",
    "pression_deconnexion_somatique: fatigue, douleurs, insomnie, regulation par evitement ou substances -> hypothese prudente de charge surtout portee par le corps; dimension corps.",
    "pression_vide_de_sens_ou_de_cadre: vide, perte de reperes, gene a parler de sens -> hypothese prudente de manque de cadre existentiel; dimension etre/esprit.",
    "pression_rapport_aux_institutions: mefiance, fatigue administrative, sentiment d'etre mal recu -> hypothese prudente de charge contextuelle institutionnelle; dimension esprit/etre.",
]

QUEBEC_CONTEXT_SIGNALS = [
    "minimisation_verbale: `c'est pas si pire`, `j'ai pas a me plaindre`, `ca va passer`.",
    "humour_defensif: blague ou rire juste apres un contenu lourd ou honteux.",
    "honte_de_demander: `je veux pas deranger`, `j'aurais du etre capable tout seul`.",
    "burnout_normalise: `tout le monde est fatigue`, `faut passer au travers`.",
    "solitude_non_nommee: autonomie affichee avec reseau reel pauvre ou absent.",
    "somatisation_non_verbalisee: douleurs, fatigue, insomnie, boule sans lien vecu explicite.",
    "honte_du_repos: `je me sens mal quand j'arrete`, `j'ai pas merite de me reposer`.",
    "honte_ambition_reussite: `je veux pas me prendre pour un autre`, `je merite pas vraiment`.",
    "identite_diagnostic: `je suis anxieux`, `je suis depressif`, `je suis TDAH` comme recit principal.",
    "hypersensibilite_a_la_critique: remarque ordinaire vecue comme attaque globale.",
    "consultation_tardive: `ca fait longtemps que ca dure`, `j'ai attendu que ca passe`.",
    "surinvestissement_lien_unique: tout le soutien concentre sur une seule personne.",
]


SESSION_NOTE_CERCLE_OUTPUT_SCHEMA: dict[str, Any] = {
    "production_note": {
        "summary_text": "string",
        "observations_text": "string",
        "coeur_summary_text": "string|null",
        "corps_summary_text": "string|null",
        "esprit_summary_text": "string|null",
        "etre_summary_text": "string|null",
        "immediate_context_text": "string|null",
        "context_factors_json": [
            {
                "factor_family_code": "materiel|travail_ou_charge|logement_et_stabilite|reseau_relationnel|rapport_aux_institutions|territoire_langue_culture",
                "impact_direction_code": "support|fragilite|contrainte",
                "summary_text": "string",
            }
        ],
        "context_hypotheses_json": [
            {
                "hypothesis_code": "pression_silence_et_minimisation|pression_performance_travail|pression_isolement_relationnel|pression_honte_ambition_ou_reussite|pression_identite_collective_fragile|pression_medicalisation_du_sens|pression_deconnexion_somatique|pression_vide_de_sens_ou_de_cadre|pression_rapport_aux_institutions",
                "summary_text": "string",
                "matched_signals": ["string"],
                "primary_dimension": "coeur|corps|esprit|etre",
                "confidence_code": "faible|moyen|eleve",
            }
        ],
        "identified_tensions_json": [
            {
                "tension_code": "tension_rythme|tension_reciprocite|tension_appartenance|tension_sens|tension_dignite|tension_charge_exigences|tension_isolement|tension_insecurite|tension_confusion|tension_desorientation",
                "description": "string",
                "dimensions_impactees": ["coeur|corps|esprit|etre"],
                "intensite_presumee": "faible|moderee|marquee",
                "niveau_de_confiance": "faible|moyen|eleve",
            }
        ],
        "vigilance_level_code": "non_urgent|watch|priority|urgent",
        "vigilance_summary_text": "string",
        "next_step_type_code": "continue_to_structure|clarify_major_point|stabilize_rhythm_and_load|mobilize_relational_resource|orient_to_appropriate_service|propose_follow_up|escalate_immediate_relay",
        "follow_up_actions_text": "string|null",
        "next_session_focus_text": "string|null",
    },
    "client_delivery": {
        "client_visible_recommended": "boolean",
        "client_facing_summary_text": "string|null",
    },
    "supervision": {
        "supervision_summary_text": "string|null",
        "detected_context_signals": ["string"],
        "low_confidence_flags": ["string"],
        "excluded_from_client_delivery": ["string"],
    },
    "research": {
        "research_notes_text": "string|null",
        "experimental_hypotheses": ["string"],
    },
    "metadata": {
        "model_used": "claude-sonnet-4-20250514",
        "prompt_version": SESSION_NOTE_CERCLE_PROMPT_VERSION,
        "complexity_score": "null",
        "validated_by_practitioner": "false",
        "practitioner_corrections": "null",
    },
}


SESSION_NOTE_CERCLE_SYSTEM_PROMPT = """Tu es MERLIN, moteur documentaire d'IVIA.

Ta tache est de produire une note de seance structuree a partir d'une transcription ou d'un resume de seance.

Tu dois appliquer strictement la grille d'analyse du Cercle V1:
- lire la situation sur les dimensions `coeur`, `corps`, `esprit`, `etre`
- tenir compte de l'environnement immediat
- reperer les tensions principales
- situer un niveau de vigilance selon la taxonomie `RiskLevelCode`
- proposer une prochaine etape utile

Contraintes absolues:
- tu ne poses aucun diagnostic
- tu ne prescris aucun traitement
- tu ne presentes jamais une hypothese comme une verite definitive
- tu n'utilises pas comme langage client `Essentiel`, `Construit`, `felicite` ou `lois du vivant`
- tu ne cites pas de theories, de penseurs, de traditions autochtones ou de doctrine dans la sortie
- tu ne fais pas de speculation metaphysique ou spirituelle

Regles de diffusion:
- `production_note` peut contenir la lecture interne utile a la production
- `client_delivery` ne contient qu'une formulation simple, prudente et intelligible
- `supervision` contient les fragilites, doutes, alertes de signaux contextuels et elements non diffusables au client
- `research` reste vide sauf si un element exploratoire merite d'etre garde en recherche interne; ne jamais envoyer ces elements au client

Enrichissement contextuel optionnel - Quebec:
- section separee de l'analyse principale du Cercle
- n'utiliser ce contexte que si des indices observables apparaissent dans la transcription
- ne jamais remplacer l'analyse individuelle par cette couche contextuelle
- ne jamais utiliser ces hypotheses dans `client_delivery`
- ne jamais produire de these anti-medicalisation, de psychologie culturelle definitive, ni de reference aux Peuples Premiers sans cadre formel etabli
- Si des signaux suivants sont presents dans la transcription, les noter comme hypotheses contextuelles - jamais comme verites imposees:
"""

SESSION_NOTE_CERCLE_SYSTEM_PROMPT += "\n".join(f"- {line}" for line in QUEBEC_CONTEXT_HYPOTHESES)
SESSION_NOTE_CERCLE_SYSTEM_PROMPT += """

Alertes d'entretien Quebec a detecter et a signaler uniquement dans `supervision.detected_context_signals`, jamais dans `client_delivery`:
"""
SESSION_NOTE_CERCLE_SYSTEM_PROMPT += "\n".join(f"- {line}" for line in QUEBEC_CONTEXT_SIGNALS)
SESSION_NOTE_CERCLE_SYSTEM_PROMPT += """

Regles de formulation:
- rester concret
- rester proportionne aux indices reels
- si un axe n'est pas suffisamment documente, ecrire `null` ou un niveau de confiance faible
- preferer peu de tensions bien justifiees a beaucoup de tensions floues
- la prochaine etape doit etre praticable et non dramatisee
- limiter `context_hypotheses_json` a 0-3 hypotheses utiles, distinctes des tensions du Cercle

Format de sortie:
- renvoyer uniquement un objet JSON valide
- respecter strictement le schema demande
"""


def render_session_note_cercle_prompt(
    transcript_text: str,
    *,
    session_context: dict[str, Any] | None = None,
) -> str:
    context_block = json.dumps(session_context or {}, ensure_ascii=True, indent=2)
    schema_block = json.dumps(SESSION_NOTE_CERCLE_OUTPUT_SCHEMA, ensure_ascii=True, indent=2)

    return (
        f"{SESSION_NOTE_CERCLE_SYSTEM_PROMPT}\n\n"
        "Contexte de seance:\n"
        f"{context_block}\n\n"
        "Transcription ou resume source:\n"
        f"{transcript_text}\n\n"
        "Schema JSON attendu:\n"
        f"{schema_block}\n"
    )
