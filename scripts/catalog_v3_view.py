"""Emit a deterministic catalog-v3 compatibility view from catalog v4."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]


V4_SCHEMA = ROOT / "schema" / "skills.schema.json"
V3_SCHEMA = ROOT / "schema" / "skills-v3.schema.json"


def _validate(data: dict, schema_path: Path, label: str) -> None:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    errors = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(data),
        key=lambda error: list(error.absolute_path),
    )
    if errors:
        details = "; ".join(f"{list(error.absolute_path)}: {error.message}" for error in errors)
        raise ValueError(f"invalid {label} catalog: {details}")


def build_v3_view(source: Path) -> dict:
    data = yaml.safe_load(source.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("invalid v4 catalog: document must be an object")
    _validate(data, V4_SCHEMA, "v4 source")
    view = dict(data)
    view["version"] = 3
    view.pop("extensions", None)
    _validate(view, V3_SCHEMA, "v3 compatibility")
    return view


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=ROOT / "catalog" / "skills.yml")
    args = parser.parse_args()
    print(yaml.safe_dump(build_v3_view(args.catalog), sort_keys=False, allow_unicode=True), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
