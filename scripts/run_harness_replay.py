"""Replay deterministic research-harness failure fixtures."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def evaluate_case(case: dict) -> dict[str, str]:
    kind = case["kind"]
    data = case["input"]
    if kind == "source_identity":
        titles = {title.strip().casefold() for title in data["observed_titles"]}
        return {"status": "unverified", "reason": "metadata_conflict"} if len(titles) > 1 else {"status": "verified", "reason": "identity_match"}
    if kind == "claim_support":
        return {"status": "accepted", "reason": "supported"} if any(data["support_flags"]) else {"status": "rejected", "reason": "unsupported_claim"}
    if kind == "contradiction":
        return {"status": "preserved", "reason": "opposing_evidence_present"} if data.get("opposing_source_ids") else {"status": "clear", "reason": "no_opposition_recorded"}
    if kind == "provider":
        return {"status": "degraded", "reason": "provider_unavailable"} if data["provider_status"] != "available" else {"status": "available", "reason": "provider_ready"}
    if kind == "untrusted_content":
        return {"status": "filtered", "reason": "untrusted_instruction"} if data.get("contains_instruction") else {"status": "retained", "reason": "content_only"}
    if kind == "decision":
        decision = data["decision"]
        if decision in {"decline", "cancel"}:
            return {"status": "terminal", "reason": "declined" if decision == "decline" else "cancelled"}
        return {"status": "running", "reason": "accepted"}
    if kind == "revision":
        same_hash = data["previous_hash"] == data["proposed_hash"]
        return {"status": "blocked", "reason": "new_hash_required"} if same_hash else {"status": "pending", "reason": "replacement_acceptance_required"}
    if kind == "idempotency":
        duplicate = data["retry_hash"] in set(data["applied_hashes"])
        return {"status": "reconciled", "reason": "duplicate_write_prevented"} if duplicate else {"status": "pending", "reason": "write_not_seen"}
    if kind == "policy":
        exhausted = data["observed"] >= data["limit"]
        return {"status": "stop", "reason": "budget_exhausted"} if exhausted else {"status": "continue", "reason": "within_budget"}
    raise ValueError(f"unknown replay kind: {kind}")


def run_replay(path: Path) -> list[dict]:
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    results = []
    for case in document["cases"]:
        actual = evaluate_case(case)
        results.append({"id": case["id"], "passed": actual == case["expected"], "actual": actual, "expected": case["expected"]})
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, default=ROOT / "test-corpus" / "harness-behavior" / "cases.yml")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    results = run_replay(args.cases)
    if args.json:
        print(json.dumps({"results": results}, ensure_ascii=False, sort_keys=True))
    else:
        for result in results:
            print(f"{'PASS' if result['passed'] else 'FAIL'} {result['id']}")
    return 0 if all(result["passed"] for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
