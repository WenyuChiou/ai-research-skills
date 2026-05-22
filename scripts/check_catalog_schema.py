#!/usr/bin/env python3
"""Validate catalog/skills.yml against schema/skills.schema.json.

Run from the repo root:

    python scripts/check_catalog_schema.py

Exits non-zero on any validation error with a specific JSON-pointer
path showing where in the YAML the problem is.

Designed to be called from CI alongside
`scripts/check_marketplace_consistency.py`. Adds the catalog
schema-driven validation layer to complement the
`tests/test_catalog.py` structural checks (which are about
content invariants like 15 skills total, not field-level shape).

Requires: pyyaml + jsonschema. Both already in the CI install step
after this commit. Locally:

    pip install pyyaml jsonschema
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "catalog" / "skills.yml"
SCHEMA_PATH = ROOT / "schema" / "skills.schema.json"


def _format_error(err) -> str:
    """jsonschema error -> human-readable single line.

    err.absolute_path is a deque like ['families', 0, 'skills', 2, 'verified_on'].
    Render as JSON-pointer-ish: families[0].skills[2].verified_on.
    """
    parts = []
    for p in err.absolute_path:
        if isinstance(p, int):
            parts[-1] = parts[-1] + f"[{p}]"
        else:
            parts.append(str(p))
    where = ".".join(parts) if parts else "<root>"
    return f"  {where}: {err.message}"


def main() -> int:
    if not SCHEMA_PATH.exists():
        print(f"error: schema not found at {SCHEMA_PATH}", file=sys.stderr)
        return 2
    if not CATALOG_PATH.exists():
        print(f"error: catalog not found at {CATALOG_PATH}", file=sys.stderr)
        return 2

    with SCHEMA_PATH.open(encoding="utf-8") as f:
        schema = json.load(f)
    with CATALOG_PATH.open(encoding="utf-8") as f:
        catalog = yaml.safe_load(f)

    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(catalog), key=lambda e: list(e.absolute_path))

    if errors:
        print(
            f"catalog schema check FAILED ({len(errors)} error{'s' if len(errors) != 1 else ''}):",
            file=sys.stderr,
        )
        for err in errors:
            print(_format_error(err), file=sys.stderr)
        return 1

    n_families = len(catalog.get("families", []))
    n_skills = sum(len(f.get("skills", [])) for f in catalog.get("families", []))
    print(
        f"catalog schema check OK ({n_families} families, {n_skills} skills)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
