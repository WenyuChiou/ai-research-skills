from __future__ import annotations

from pathlib import Path
import copy

import pytest
import yaml

from scripts.catalog_v3_view import build_v3_view


ROOT = Path(__file__).resolve().parents[1]


def test_v3_view_preserves_core_and_omits_extensions():
    source = ROOT / "catalog" / "skills.yml"
    current = yaml.safe_load(source.read_text(encoding="utf-8"))
    legacy = build_v3_view(source)
    assert legacy["version"] == 3
    assert "extensions" not in legacy
    assert legacy["families"] == current["families"]
    assert sum(len(family["skills"]) for family in legacy["families"]) == 17


@pytest.mark.parametrize(
    "mutator",
    [
        lambda data: data.pop("families"),
        lambda data: data.__setitem__("families", "not-a-list"),
        lambda data: data["families"][0].pop("skills"),
    ],
)
def test_v3_view_fails_closed_on_malformed_v4(tmp_path, mutator):
    source = yaml.safe_load((ROOT / "catalog/skills.yml").read_text(encoding="utf-8"))
    bad = copy.deepcopy(source)
    mutator(bad)
    path = tmp_path / "bad.yml"
    path.write_text(yaml.safe_dump(bad, sort_keys=False), encoding="utf-8")
    with pytest.raises(ValueError, match="invalid v4 source catalog"):
        build_v3_view(path)
