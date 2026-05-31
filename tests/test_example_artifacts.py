"""Validate the worked-example artifacts the catalog ships in docs/.

The catalog advertises producer↔consumer schema integrity as a differentiator,
but until 1.5.30 it never opened a single example artifact it shipped — which is
how a dangling `linked_claim: C6` (fixed in 1.5.29) reached users. These tests
close that silent-failure surface.
"""
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def _load(name):
    return yaml.safe_load((DOCS / name).read_text(encoding="utf-8"))


def _example_yaml_paths():
    # glob("example-*.yml") already covers the *.gaps.yml files (they end in .yml)
    return sorted(DOCS.glob("example-*.yml"))


def test_all_example_yaml_parses():
    paths = _example_yaml_paths()
    assert paths, "no example-*.yml artifacts found in docs/"
    for p in paths:
        data = yaml.safe_load(p.read_text(encoding="utf-8"))
        assert data is not None, f"{p.name} parsed to None"


def _unresolved_linked_claims(gaps_data, claim_ids):
    """Return [(gap_id, linked_claim), ...] for every non-null linked_claim that
    does not resolve to a known claim id. Null links are honest (no companion
    claims file) and are skipped."""
    bad = []
    for gap in gaps_data.get("gaps", []):
        lc = gap.get("linked_claim")
        if lc is not None and lc not in claim_ids:
            bad.append((gap.get("id"), lc))
    return bad


def test_linked_claims_resolve_or_null():
    """Every non-null `linked_claim` in any gaps.yml must resolve to a claim id
    defined in example-paper-memory-claims.yml. A gaps file with no same-topic
    claims companion uses `linked_claim: null`. This is the regression net for the
    1.5.29 O1 fix (a dangling `linked_claim: C6` had shipped)."""
    claim_ids = {c["id"] for c in _load("example-paper-memory-claims.yml")["claims"]}
    for gaps_path in sorted(DOCS.glob("example-*.gaps.yml")):
        data = yaml.safe_load(gaps_path.read_text(encoding="utf-8"))
        bad = _unresolved_linked_claims(data, claim_ids)
        assert not bad, (
            f"{gaps_path.name}: dangling linked_claim {bad} — not in "
            f"example-paper-memory-claims.yml {sorted(claim_ids)}"
        )


def test_unresolved_linked_claims_both_branches():
    """The shipped fixtures are all-null, so exercise the resolver's positive AND
    negative branches on synthetic data — guarding the logic itself, not the
    current fixtures (which would re-introduce the O1 cross-link if linked)."""
    ids = {"C1", "C2"}
    assert _unresolved_linked_claims({"gaps": [{"id": "G1", "linked_claim": "C1"}]}, ids) == []
    assert _unresolved_linked_claims({"gaps": [{"id": "G1", "linked_claim": "C9"}]}, ids) == [("G1", "C9")]
    assert _unresolved_linked_claims({"gaps": [{"id": "G1", "linked_claim": None}]}, ids) == []


def test_figures_support_real_claims():
    """Every figures[].supports_claims id resolves to a claim id (the
    figure↔claim reciprocity rule the claim-evidence audit relies on)."""
    claim_ids = {c["id"] for c in _load("example-paper-memory-claims.yml")["claims"]}
    for fig in _load("example-paper-memory-figures.yml")["figures"]:
        for cid in fig.get("supports_claims", []):
            assert cid in claim_ids, (
                f"figure {fig.get('id')} supports_claims={cid!r} not in claims "
                f"{sorted(claim_ids)}"
            )


def test_topic_dossier_gaps_have_verdict_and_consumer():
    """The topic-dossier gaps file is the Stage 2 → 3a handoff: it must name its
    downstream_consumer and every gap must carry a non-empty verdict."""
    data = _load("example-topic-dossier.gaps.yml")
    assert data.get("downstream_consumer"), (
        "example-topic-dossier.gaps.yml missing top-level downstream_consumer "
        "(the Stage 3a reader contract)"
    )
    for gap in data.get("gaps", []):
        assert gap.get("verdict"), f"gap {gap.get('id')} missing a verdict"
