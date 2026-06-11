"""ROD-TEST-001-A / J1 : test_prompt_injection_validation

Verifie la chaine d'injection des donnees de reference METH :
  - METH-001/002 (v1.1) ne dupliquent plus les listes : ils pointent vers les
    referentiels vivants (00_DOCTRINE/referentiels/), source d'autorite unique ;
  - les constantes injectees (QUEBEC_CONTEXT_HYPOTHESES / SIGNALS) sont rendues
    depuis le registre : 9 hypotheses de pression, 12 signaux contextuels ;
  - METH-003 : contient 'Tu es MERLIN'.

Type : Unitaire - zero dependance externe (ni DB ni API).
Lancer : pytest tests/test_prompt_injection.py -v
"""

from app.ai.prompt_loader import load_prompt
from app.ai.prompts.session_note_cercle_v1 import (
    QUEBEC_CONTEXT_HYPOTHESES,
    QUEBEC_CONTEXT_SIGNALS,
)
from app.referentiels import get_codes


class TestPromptInjectionValidation:

    def test_meth001_loaded_and_non_empty(self) -> None:
        """METH-001 doit etre charge et non vide."""
        content = load_prompt("METH-001")
        assert content, "METH-001 est vide ou non charge"
        assert len(content) > 100, "METH-001 semble trop court"

    def test_meth001_delegue_au_referentiel(self) -> None:
        """METH-001 v1.1 doit pointer vers le referentiel sans dupliquer la liste."""
        content = load_prompt("METH-001")
        assert "pressions_societales.v1.yaml" in content, (
            "METH-001 doit referencer le referentiel pressions_societales"
        )
        duplicated = [
            line for line in content.splitlines()
            if line.strip().startswith("- pression_")
        ]
        assert not duplicated, (
            f"METH-001 ne doit plus dupliquer les hypotheses, trouve : {duplicated}"
        )

    def test_hypotheses_rendues_depuis_registre(self) -> None:
        """Les 9 hypotheses injectees viennent du registre, codes canoniques en tete."""
        assert len(QUEBEC_CONTEXT_HYPOTHESES) == 9, (
            f"9 hypotheses attendues, trouve : {len(QUEBEC_CONTEXT_HYPOTHESES)}"
        )
        codes = get_codes("pressions_societales")
        expected_codes = [
            "pression_silence_et_minimisation",
            "pression_performance_travail",
            "pression_isolement_relationnel",
            "pression_honte_ambition_ou_reussite",
            "pression_identite_collective_fragile",
            "pression_medicalisation_du_sens",
            "pression_deconnexion_somatique",
            "pression_vide_de_sens_ou_de_cadre",
            "pression_rapport_aux_institutions",
        ]
        assert codes == expected_codes, f"Codes du referentiel inattendus : {codes}"
        for code, rendered in zip(expected_codes, QUEBEC_CONTEXT_HYPOTHESES):
            assert rendered.startswith(f"{code}:"), (
                f"Hypothese rendue sans son code en tete : {rendered}"
            )

    def test_meth002_loaded_and_non_empty(self) -> None:
        """METH-002 doit etre charge et non vide."""
        content = load_prompt("METH-002")
        assert content, "METH-002 est vide ou non charge"
        assert len(content) > 100, "METH-002 semble trop court"

    def test_meth002_delegue_au_referentiel(self) -> None:
        """METH-002 v1.1 doit pointer vers le referentiel sans dupliquer la liste."""
        content = load_prompt("METH-002")
        assert "signaux_contextuels.v1.yaml" in content, (
            "METH-002 doit referencer le referentiel signaux_contextuels"
        )

    def test_signaux_rendus_depuis_registre(self) -> None:
        """Les 12 signaux injectes viennent du registre, codes canoniques presents."""
        assert len(QUEBEC_CONTEXT_SIGNALS) == 12, (
            f"12 signaux attendus, trouve : {len(QUEBEC_CONTEXT_SIGNALS)}"
        )
        expected_codes = [
            "minimisation_verbale",
            "humour_defensif",
            "honte_de_demander",
            "burnout_normalise",
            "solitude_non_nommee",
            "somatisation_non_verbalisee",
            "honte_du_repos",
            "honte_ambition_reussite",
            "identite_diagnostic",
            "hypersensibilite_a_la_critique",
            "consultation_tardive",
            "surinvestissement_lien_unique",
        ]
        assert get_codes("signaux_contextuels") == expected_codes
        for code, rendered in zip(expected_codes, QUEBEC_CONTEXT_SIGNALS):
            assert rendered.startswith(f"{code}:"), (
                f"Signal rendu sans son code en tete : {rendered}"
            )

    def test_meth003_loaded_and_non_empty(self) -> None:
        """METH-003 doit etre charge et non vide."""
        content = load_prompt("METH-003")
        assert content, "METH-003 est vide ou non charge"
        assert len(content) > 50, "METH-003 semble trop court"

    def test_meth003_contains_tu_es_merlin(self) -> None:
        """METH-003 doit contenir la directive 'Tu es MERLIN'."""
        content = load_prompt("METH-003")
        assert "Tu es MERLIN" in content, (
            "METH-003 doit contenir 'Tu es MERLIN' comme directive systeme"
        )

    def test_meth003_contains_moteur_documentaire(self) -> None:
        """METH-003 doit decrire le role documentaire de MERLIN."""
        content = load_prompt("METH-003")
        assert "documentaire" in content.lower() or "session" in content.lower(), (
            "METH-003 doit mentionner le role documentaire ou de session"
        )

    def test_all_meth_prompts_have_nonempty_body(self) -> None:
        """Tous les prompts METH doivent avoir un body non vide."""
        for prompt_id in ["METH-001", "METH-002", "METH-003"]:
            content = load_prompt(prompt_id)
            assert content and len(content.strip()) > 0, (
                f"{prompt_id} retourne un contenu vide"
            )
