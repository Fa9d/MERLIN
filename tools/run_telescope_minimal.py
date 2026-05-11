#!/usr/bin/env python3
"""Run a minimal Telescope fixture evaluation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover - environment guard
    print("ERROR: PyYAML is required. Install it with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FIXTURE = ROOT / "managed_agents" / "evals" / "fixtures" / "telescope_minimal_fake_run.json"
SUITE_PATH = ROOT / "managed_agents" / "evals" / "vibench_coding_suite_v1.yaml"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return data


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be a mapping: {path}")
    return data


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate_result_shape(result: dict[str, Any], output_schema: dict[str, Any]) -> None:
    missing = sorted(set(output_schema) - set(result))
    if missing:
        raise ValueError(f"result missing required fields: {', '.join(missing)}")

    require(isinstance(result["passed"], bool), "result.passed must be boolean")
    require(isinstance(result["score"], int | float), "result.score must be number")
    require(isinstance(result["prd_coverage"], int | float), "result.prd_coverage must be number")

    for field in ["blocking_bugs", "ux_issues", "regressions", "evidence_refs"]:
        require(isinstance(result[field], list), f"result.{field} must be list")

    require(isinstance(result["summary"], str) and result["summary"], "result.summary must be non-empty string")
    require(
        result["recommended_decision"] in {"pass", "fail", "human_review", "ab_test"},
        "result.recommended_decision must be pass, fail, human_review, or ab_test",
    )


def run_fixture(fixture_path: Path) -> dict[str, Any]:
    suite = load_yaml(SUITE_PATH)
    fixture = load_json(fixture_path)

    require(fixture.get("suite_ref") == suite.get("id"), "fixture.suite_ref must match Telescope suite id")
    mode = fixture.get("mode")
    require(mode in suite.get("test_modes", {}), f"fixture.mode is not declared in suite: {mode}")

    result = fixture.get("result")
    require(isinstance(result, dict), "fixture.result must be an object")
    validate_result_shape(result, suite.get("output_schema", {}))

    minimum_score = suite.get("pass_fail", {}).get("minimum_score", 0)
    passed_gate = bool(result["passed"] and result["score"] >= minimum_score and not result["blocking_bugs"])

    return {
        "run_id": fixture.get("id"),
        "suite_ref": fixture.get("suite_ref"),
        "mode": mode,
        "dataset": fixture.get("input", {}).get("dataset"),
        "score": result["score"],
        "minimum_score": minimum_score,
        "passed_gate": passed_gate,
        "recommended_decision": result["recommended_decision"],
        "summary": result["summary"],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the minimal Telescope fake-data fixture.")
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE, help="Path to the fixture JSON file.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    fixture_path = args.fixture if args.fixture.is_absolute() else ROOT / args.fixture

    try:
        summary = run_fixture(fixture_path)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("OK: Telescope minimal fake-data run completed")
    print(json.dumps(summary, indent=2, ensure_ascii=True))
    return 0 if summary["passed_gate"] else 1


if __name__ == "__main__":
    sys.exit(main())
