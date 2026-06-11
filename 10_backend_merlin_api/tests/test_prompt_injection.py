"""ROD-TEST-001-A / J1 : test_prompt_injection_validation

Verifie que les 3 prompts METH charges par prompt_loader contiennent
exactement le contenu attendu d'apres leur specification.

Resultats attendus :
  METH-001 : 9 hypotheses de pression (lignes '- pression_' sans backticks)
  METH-002 : 12 signaux contextuels (lignes '- mot_: ' format cle:valeur)
  METH-003 : contient 'Tu es MERLIN'

Type : Unitaire - zero dependance externe.
Lancer : pytest tests/test_prompt_injection.py -v
"""

from app.ai.prompt_loader import load_prompt


class TestPromptInjectionValidation:

    def test_meth001_loaded_and_non_empty(self) -> None:
        """METH-001 doit etre charge et non vide."""
        content = load_prompt("METH-001")
        assert content, "METH-001 est vide ou non charge"
        assert len(content) > 100, "METH-001 semble trop court"

    def test_meth001_contains_9_hypotheses(self) -> None:
        """METH-001 doit contenir exactement 9 hypotheses de pression."""
        content = load_prompt("METH-001")
        hypotheses = [
            line for line in content.splitlines()
            if line.strip().startswith("- pression_")
        ]
        assert len(hypotheses) == 9, (
            f"METH-001 doit contenir 9 hypotheses de pression, "
            f"trouve : {len(hypotheses)}\n"
            f"Lignes detectees : {hypotheses}"
        )

    def test_meth001_hypothesis_codes_present(self) -> None:
        """METH-001 doit contenir les codes d'hypotheses canoniques."""
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
            assert code in content, f"Code manquant dans METH-001 : {code}"

    def test_meth002_loaded_and_non_empty(self) -> None:
        """METH-002 doit etre charge et non vide."""
        content = load_prompt("METH-002")
        assert content, "METH-002 est vide ou non charge"
        assert len(content) > 100, "METH-002 semble trop court"

    def test_meth002_contains_12_signals(self) -> None:
        """METH-002 doit contenir exactement 12 signaux contextuels."""
        content = load_prompt("METH-002")
        # Les signaux sont au format '- code_signal: description' (cle snake_case suivie de ':')
        import re
        signals = [
            line for line in content.splitlines()
            if re.match(r'^- [a-z][a-z0-9_]+:', line.strip())
        ]
        assert len(signals) == 12, (
            f"METH-002 doit contenir 12 signaux, "
            f"trouve : {len(signals)}\n"
            f"Lignes detectees : {signals}"
        )

    def test_meth002_signal_codes_present(self) -> None:
        """METH-002 doit contenir les codes de signaux canoniques."""
        content = load_prompt("METH-002")
        expected_codes = [
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
        for code in expected_codes:
            assert code in content, f"Code de signal manquant dans METH-002 : {code}"

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
