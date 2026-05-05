from __future__ import annotations

from pathlib import Path

import pytest

from app.ai import prompt_loader
from app.ai.prompt_loader import PromptNotFoundError, load_prompt


@pytest.fixture(autouse=True)
def clear_prompt_cache() -> None:
    prompt_loader._PROMPT_CACHE.clear()


def test_load_prompt_existing_returns_non_empty_string(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    prompts_root = tmp_path / "11_PROMPTS"
    prompts_root.mkdir()
    prompt_file = prompts_root / "02_METH" / "METH-001-quebec-context-hypotheses-v1.md"
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text("---\nid: TEST\n---\n\n- ligne 1\n", encoding="utf-8")

    monkeypatch.setattr(prompt_loader, "_PROMPT_PATHS", {"METH-001": "02_METH/METH-001-quebec-context-hypotheses-v1.md"})
    monkeypatch.setattr(prompt_loader, "_prompts_root", lambda: prompts_root)

    content = load_prompt("METH-001")

    assert isinstance(content, str)
    assert content.strip() != ""
    assert "ligne 1" in content


def test_load_prompt_missing_raises_prompt_not_found() -> None:
    with pytest.raises(PromptNotFoundError):
        load_prompt("METH-999")


def test_load_prompt_uses_cache(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    prompts_root = tmp_path / "11_PROMPTS"
    prompts_root.mkdir()
    prompt_file = prompts_root / "02_METH" / "METH-001-quebec-context-hypotheses-v1.md"
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text("---\nid: TEST\n---\n\n- cache test\n", encoding="utf-8")

    monkeypatch.setattr(prompt_loader, "_PROMPT_PATHS", {"METH-001": "02_METH/METH-001-quebec-context-hypotheses-v1.md"})
    monkeypatch.setattr(prompt_loader, "_prompts_root", lambda: prompts_root)

    read_count = {"calls": 0}

    def fake_reader(path: Path) -> str:
        read_count["calls"] += 1
        return path.read_text(encoding="utf-8")

    monkeypatch.setattr(prompt_loader, "_read_prompt_file", fake_reader)

    first = load_prompt("METH-001")
    second = load_prompt("METH-001")

    assert first == second
    assert read_count["calls"] == 1
