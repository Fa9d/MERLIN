"""ROD-TEST-001-A / J1 : test_prompt_injection_validation

Verifie que les 3 prompts METH charges par prompt_loader contiennent
exactement le contenu attendu d'apres leur specification.

Resultats attendus :
  METH-001 : 9 hypotheses de pression (lignes '- `pression_')
  METH-002 : 12 signaux contextuels (lignes '* ' ou '- ' en section donnees)
  METH-003 : contient 'Tu es MERLIN'

Type : Unitaire — zero dependance externe.
Lancer : pytest tests/test_prompt_injection.py -v
"""
from __future__ import annotations

import pytest

from app.ai.prompt_loader import load_prompt


class TestPromptInjectionValidation:
    """Verifie l'integrite du contenu des prompts METH charges."""

    def test_meth001_loaded_and_non_empty(self) -> None:
        """METH-001 se charge sans erreur et retourne du contenu."""
        content = load_prompt("METH-001")
        assert isinstance(content, str), "METH-001 doit retourner une chaine"
        assert len(content.strip()) > 50, "METH-001 ne doit pas etre vide ou trivial"

    def test_meth001_contains_9_hypotheses(self) -> None:
        """METH-001 doit contenir exactement 9 hypotheses de pression."""
        content = load_prompt("METH-001")
        # Chaque hypothese commence par '- `pression_' dans la section donnees
        hypotheses = [
            line for line in content.splitlines()
            if line.strip().startswith("- `pression_")
        ]
        assert len(hypotheses) == 9, (
            f"METH-001 doit contenir 9 hypotheses de pression, "
            f"trouve : {len(hypotheses)}\n"
            f"Lignes detectees : {hypotheses}"
        )

    def test_meth001_hypothesis_codes_present(self) -> None:
        """Les 9 codes d'hypothese specifiques doivent etre presents dans METH-001."""
        content = load_prompt("METH-001")
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
        for code in expected_codes:
            assert code in content, (
                f"Code hypothese manquant dans METH-001 : {code}"
            )

    def test_meth002_loaded_and_non_empty(self) -> None:
        """METH-002 se charge sans erreur et retourne du contenu."""
        content = load_prompt("METH-002")
        assert isinstance(content, str)
        assert len(content.strip()) > 50

    def test_meth002_contains_12_signals(self) -> None:
        """METH-002 doit contenir exactement 12 signaux contextuels."""
        content = load_prompt("METH-002")
        # Chaque signal commence par '* ' ou '- ' suivi d'un code_signal:
        # ex: '* minimisation_verbale: ...' ou '- minimisation_verbale: ...'
        import re
        signal_lines = [
            line for line in content.splitlines()
            if re.match(r'^[\*\-]\s+`?\w+`?:', line.strip())
        ]
        assert len(signal_lines) == 12, (
            f"METH-002 doit contenir 12 signaux, "
            f"trouve : {len(signal_lines)}\n"
            f"Lignes detectees : {signal_lines}"
        )

    def test_meth002_signal_codes_present(self) -> None:
        """Les 12 codes de signaux specifiques doivent etre presents dans METH-002."""
        content = load_prompt("METH-002")
        expected_signals = [
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
        for signal in expected_signals:
            assert signal in content, (
                f"Code signal manquant dans METH-002 : {signal}"
            )

    def test_meth003_loaded_and_non_empty(self) -> None:
        """METH-003 se charge sans erreur et retourne du contenu."""
        content = load_prompt("METH-003")
        assert isinstance(content, str)
        assert len(content.strip()) > 50

    def test_meth003_contains_tu_es_merlin(self) -> None:
        """METH-003 doit contenir la phrase d'identite 'Tu es MERLIN'."""
        content = load_prompt("METH-003")
        assert "Tu es MERLIN" in content, (
            "METH-003 doit contenir la phrase d'identite 'Tu es MERLIN'. "
            "Le persona moteur MERLIN doit etre explicitement declare."
        )

    def test_meth003_contains_moteur_documentaire(self) -> None:
        """METH-003 doit mentionner 'moteur documentaire' (role du systeme)."""
        content = load_prompt("METH-003")
        assert "moteur documentaire" in content, (
            "METH-003 doit decrire le role 'moteur documentaire d IVIA'."
        )

    def test_all_meth_prompts_have_nonempty_body(self) -> None:
        """Tous les prompts METH doivent avoir un corps non vide apres le frontmatter."""
        for prompt_id in ("METH-001", "METH-002", "METH-003"):
            content = load_prompt(prompt_id)
            # Le loader extrait deja le corps apres le frontmatter YAML
            assert content.strip(), (
                f"{prompt_id} : le corps apres frontmatter ne doit pas etre vide"
            )
            # Pas de frontmatter residuel dans le corps
            assert not content.strip().startswith("---"), (
                f"{prompt_id} : le corps ne doit pas commencer par '---' "
                f"(frontmatter non retire par le loader)"
            )
