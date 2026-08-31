#!/usr/bin/env python3
"""Report-only live health smoke for active catalog skills.

Checks source repository lifecycle, remote plugin manifests/versions/default
refs, SKILL.md reachability/frontmatter identity, and HITL metadata invariants.
It never installs skills, invokes paid services, changes remote state, or
prints credentials.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog" / "skills.yml"
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
USER_AGENT = "ai-research-skills-health/1.0"


def _request_json(url: str) -> dict:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": USER_AGENT}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=20) as response:
        return json.load(response)


def _request_text(url: str) -> str:
    headers = {
        "Accept": "application/vnd.github.raw+json",
        "User-Agent": USER_AGENT,
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=20) as response:
        return response.read(262_144).decode("utf-8", errors="replace")


def _github_api_url(repo_url: str) -> str:
    match = re.fullmatch(r"https://github\.com/([^/]+)/([^/]+)/?", repo_url)
    if not match:
        raise ValueError(f"unsupported repo URL: {repo_url}")
    return f"https://api.github.com/repos/{match.group(1)}/{match.group(2)}"


def _raw_skill_url(skill_url: str) -> str:
    repo_url, ref, path = _skill_url_parts(skill_url)
    return _raw_repo_file_url(repo_url, ref, path)


def _frontmatter_name(text: str) -> str | None:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    try:
        closing = next(index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration:
        return None
    try:
        frontmatter = yaml.safe_load("\n".join(lines[1:closing]))
    except yaml.YAMLError:
        return None
    if not isinstance(frontmatter, dict) or not isinstance(frontmatter.get("name"), str):
        return None
    return frontmatter["name"].strip()


def _raw_repo_file_url(repo_url: str, ref: str, path: str) -> str:
    api_url = _github_api_url(repo_url)
    encoded_path = urllib.parse.quote(path, safe="/")
    encoded_ref = urllib.parse.quote(ref, safe="")
    return f"{api_url}/contents/{encoded_path}?ref={encoded_ref}"


def _repo_url_from_source(source_url: str) -> str:
    if not source_url.startswith("https://github.com/") or not source_url.endswith(".git"):
        raise ValueError(f"unsupported plugin source URL: {source_url}")
    return source_url[:-4]


def _skill_url_parts(skill_url: str) -> tuple[str, str, str]:
    match = re.fullmatch(r"(https://github\.com/[^/]+/[^/]+)/blob/([^/]+)/(.+)", skill_url)
    if not match:
        raise ValueError(f"unsupported skill URL: {skill_url}")
    return match.group(1), match.group(2), match.group(3)


def _fetch_severity(exc: Exception) -> str:
    return "error" if isinstance(exc, urllib.error.HTTPError) and exc.code == 404 else "warning"


def run_checks() -> dict:
    catalog = yaml.safe_load(CATALOG.read_text(encoding="utf-8"))
    marketplace = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
    findings: list[dict[str, str]] = []
    skills = [skill for family in catalog["families"] for skill in family["skills"]]
    repo_metadata: dict[str, dict] = {}

    for repo_url in sorted({skill["repo_url"] for skill in skills}):
        try:
            metadata = _request_json(_github_api_url(repo_url))
            repo_metadata[repo_url] = metadata
            if metadata.get("archived"):
                findings.append({"severity": "error", "check": "repo_archived", "target": repo_url})
        except (OSError, ValueError, urllib.error.URLError, json.JSONDecodeError) as exc:
            findings.append({"severity": "warning", "check": "repo_metadata", "target": repo_url, "detail": type(exc).__name__})

    for plugin in marketplace["plugins"]:
        try:
            source = plugin["source"]
            repo_url = _repo_url_from_source(source["url"])
            ref = source["ref"]
            if repo_url not in {skill["repo_url"] for skill in skills}:
                findings.append({"severity": "error", "check": "plugin_catalog_repo", "target": plugin["name"]})
            metadata = repo_metadata.get(repo_url)
            if metadata and metadata.get("default_branch") != ref:
                findings.append({
                    "severity": "error",
                    "check": "plugin_default_ref",
                    "target": plugin["name"],
                    "detail": f"marketplace={ref!r} source={metadata.get('default_branch')!r}",
                })
            manifest_text = _request_text(_raw_repo_file_url(repo_url, ref, ".claude-plugin/plugin.json"))
            manifest = json.loads(manifest_text)
            if manifest.get("name") != plugin["name"]:
                findings.append({
                    "severity": "error",
                    "check": "plugin_manifest_name",
                    "target": plugin["name"],
                    "detail": f"source={manifest.get('name')!r}",
                })
            if manifest.get("version") != plugin["version"]:
                findings.append({
                    "severity": "error",
                    "check": "plugin_version_drift",
                    "target": plugin["name"],
                    "detail": f"marketplace={plugin['version']!r} source={manifest.get('version')!r}",
                })
        except (KeyError, TypeError, ValueError, OSError, urllib.error.URLError, json.JSONDecodeError) as exc:
            findings.append({
                "severity": _fetch_severity(exc),
                "check": "plugin_manifest_fetch",
                "target": plugin.get("name", "<unknown>"),
                "detail": type(exc).__name__,
            })

    for skill in skills:
        try:
            url_repo, url_ref, _ = _skill_url_parts(skill["skill_url"])
            if url_repo != skill["repo_url"]:
                findings.append({"severity": "error", "check": "skill_repo_ref", "target": skill["name"]})
            metadata = repo_metadata.get(skill["repo_url"])
            if metadata and metadata.get("default_branch") != url_ref:
                findings.append({
                    "severity": "error",
                    "check": "skill_default_ref",
                    "target": skill["name"],
                    "detail": f"catalog={url_ref!r} source={metadata.get('default_branch')!r}",
                })
            text = _request_text(_raw_skill_url(skill["skill_url"]))
            actual_name = _frontmatter_name(text)
            if actual_name != skill["name"]:
                findings.append({
                    "severity": "error",
                    "check": "frontmatter_name",
                    "target": skill["name"],
                    "detail": f"source={actual_name!r}",
                })
        except (OSError, ValueError, urllib.error.URLError) as exc:
            findings.append({"severity": _fetch_severity(exc), "check": "skill_fetch", "target": skill["name"], "detail": type(exc).__name__})

        if skill["lifecycle_status"] != "active":
            findings.append({"severity": "error", "check": "lifecycle", "target": skill["name"]})
        if skill["mutation_class"] in {"mixed", "external-write"} and not skill["human_gates"]:
            findings.append({"severity": "error", "check": "missing_human_gate", "target": skill["name"]})

    return {
        "catalog_version": catalog["version"],
        "skills_checked": len(skills),
        "repositories_checked": len({skill["repo_url"] for skill in skills}),
        "status": "pass" if not findings else "needs_human_review",
        "findings": findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Live report-only skill health smoke")
    parser.add_argument("--strict", action="store_true", help="exit 1 when findings exist")
    parser.add_argument("--json-output", type=Path, help="write the complete report to this path")
    args = parser.parse_args()

    report = run_checks()
    rendered = json.dumps(report, indent=2, ensure_ascii=False)
    print(rendered)
    if args.json_output:
        args.json_output.write_text(rendered + "\n", encoding="utf-8")
    return 1 if args.strict and report["findings"] else 0


if __name__ == "__main__":
    sys.exit(main())
