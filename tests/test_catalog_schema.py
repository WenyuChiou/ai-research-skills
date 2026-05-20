"""Pytest covering schema/skills.schema.json + the live catalog.

Two layers:

1. **Positive**: the live `catalog/skills.yml` validates clean against
   the schema. (Same check as `scripts/check_catalog_schema.py`, run
   here in CI so a `pytest tests/ -q` alone catches schema regressions.)
2. **Negative**: ad-hoc mutations of a valid catalog are rejected. This
   guards the schema itself — if someone weakens it (e.g. removes a
   `required` field) the negative tests start passing inputs that should
   fail, and these tests flip red.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "catalog" / "skills.yml"
SCHEMA_PATH = ROOT / "schema" / "skills.schema.json"


@pytest.fixture(scope="module")
def schema() -> dict:
    with SCHEMA_PATH.open(encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def catalog() -> dict:
    with CATALOG_PATH.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


@pytest.fixture
def validator(schema):
    return Draft202012Validator(schema)


def test_schema_itself_is_valid_draft_2020_12(schema):
    """The schema must itself conform to the meta-schema; otherwise the
    validator silently misbehaves."""
    Draft202012Validator.check_schema(schema)


def test_live_catalog_validates(validator, catalog):
    errors = list(validator.iter_errors(catalog))
    assert not errors, (
        "live catalog/skills.yml has schema errors:\n"
        + "\n".join(f"  {list(e.absolute_path)}: {e.message}" for e in errors)
    )


# ---------------------------------------------------------------------------
# Negative cases — each guards a specific schema rule we care about
# ---------------------------------------------------------------------------


def test_missing_top_level_version_fails(validator, catalog):
    bad = copy.deepcopy(catalog)
    del bad["version"]
    assert list(validator.iter_errors(bad)), "schema must require top-level 'version'"


def test_invalid_updated_date_format_fails(validator, catalog):
    bad = copy.deepcopy(catalog)
    bad["updated"] = "May 19, 2026"  # not YYYY-MM-DD
    assert list(validator.iter_errors(bad)), "schema must enforce ISO date on 'updated'"


def test_unknown_top_level_field_fails(validator, catalog):
    bad = copy.deepcopy(catalog)
    bad["totally_new_field"] = "drift"
    assert list(validator.iter_errors(bad)), (
        "schema must reject unknown top-level fields (additionalProperties: false)"
    )


def test_skill_missing_verification_status_fails(validator, catalog):
    bad = copy.deepcopy(catalog)
    del bad["families"][0]["skills"][0]["verification_status"]
    assert list(validator.iter_errors(bad)), "verification_status must be required"


def test_skill_invalid_verification_status_fails(validator, catalog):
    bad = copy.deepcopy(catalog)
    bad["families"][0]["skills"][0]["verification_status"] = "ok-ish"
    assert list(validator.iter_errors(bad)), (
        "verification_status must be restricted to the documented enum"
    )


def test_skill_invalid_verification_tier_fails(validator, catalog):
    bad = copy.deepcopy(catalog)
    bad["families"][0]["skills"][0]["verification_tier"] = "S+"
    assert list(validator.iter_errors(bad)), (
        "verification_tier must be restricted to T1 / T2 / T3"
    )


def test_skill_url_must_point_at_skill_md(validator, catalog):
    bad = copy.deepcopy(catalog)
    bad["families"][0]["skills"][0]["skill_url"] = "https://github.com/x/y/blob/main/README.md"
    assert list(validator.iter_errors(bad)), (
        "skill_url must end at SKILL.md (the schema's regex pattern)"
    )


def test_repo_url_must_be_github(validator, catalog):
    bad = copy.deepcopy(catalog)
    bad["families"][0]["skills"][0]["repo_url"] = "https://gitlab.com/x/y"
    assert list(validator.iter_errors(bad)), (
        "repo_url must be a github.com URL per the schema regex"
    )


def test_verified_on_must_be_iso_date(validator, catalog):
    bad = copy.deepcopy(catalog)
    bad["families"][0]["skills"][0]["verified_on"] = "yesterday"
    assert list(validator.iter_errors(bad)), "verified_on must match YYYY-MM-DD"


def test_install_commands_cannot_be_empty(validator, catalog):
    bad = copy.deepcopy(catalog)
    bad["families"][0]["install"]["commands"] = []
    assert list(validator.iter_errors(bad)), "install.commands must be non-empty"


def test_family_id_must_be_slug(validator, catalog):
    bad = copy.deepcopy(catalog)
    bad["families"][0]["id"] = "Research Workspace"  # has space + uppercase
    assert list(validator.iter_errors(bad)), "family.id must match the slug pattern"


def test_skill_name_must_be_slug(validator, catalog):
    bad = copy.deepcopy(catalog)
    bad["families"][0]["skills"][0]["name"] = "Research Hub"  # has space + uppercase
    assert list(validator.iter_errors(bad)), "skill.name must match the slug pattern"
