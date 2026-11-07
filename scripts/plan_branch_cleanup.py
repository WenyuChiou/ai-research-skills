#!/usr/bin/env python3
"""Report merged remote branch cleanup candidates. Never delete or mutate refs.

Live mode uses only paginated GitHub GET requests through an already configured
gh CLI. --snapshot accepts the same metadata for deterministic offline review.
No apply option exists: a candidate still needs fresh checks and authorization.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
from fnmatch import fnmatchcase
import json
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / ".github" / "branch-cleanup.json"
SHA = re.compile(r"[0-9a-f]{40}")


def timestamp(value: str) -> datetime:
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None:
        raise ValueError("timestamps must include a timezone")
    return result


def validate_config(config: dict) -> None:
    fields = {"repository", "allowed_prefixes", "allowed_pr_authors",
              "keep_patterns", "minimum_age_days"}
    if not isinstance(config, dict) or set(config) != fields:
        raise ValueError("config must contain exactly the documented fields")
    if not isinstance(config["repository"], str) or not re.fullmatch(
        r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", config["repository"]
    ):
        raise ValueError("repository must be owner/name")
    for field in ("allowed_prefixes", "allowed_pr_authors", "keep_patterns"):
        values = config[field]
        if not isinstance(values, list) or any(
            not isinstance(value, str) or not value.strip() for value in values
        ):
            raise ValueError(f"{field} must be a list of nonempty strings")
    if any(not prefix.endswith("/") for prefix in config["allowed_prefixes"]):
        raise ValueError("allowed_prefixes must end in / and are literal prefixes")
    age = config["minimum_age_days"]
    if type(age) is not int or age < 0:
        raise ValueError("minimum_age_days must be a nonnegative integer")


def _get(endpoint: str, *, paginate: bool = False):
    command = ["gh", "api", "--hostname", "github.com", "--method", "GET", endpoint]
    if paginate:
        command += ["--paginate", "--slurp"]
    result = subprocess.run(command, capture_output=True, text=True,
                            check=True, timeout=120)
    value = json.loads(result.stdout)
    if paginate:
        if not isinstance(value, list) or any(not isinstance(page, list) for page in value):
            raise ValueError("expected complete array pages from GitHub")
        return [item for page in value for item in page]
    return value


def collect(repository: str) -> dict:
    """Collect all branches and PRs; any failed request aborts the whole plan."""
    endpoint = f"repos/{repository}"
    repo = _get(endpoint)
    branches = _get(f"{endpoint}/branches?per_page=100", paginate=True)
    pulls = _get(f"{endpoint}/pulls?state=all&per_page=100", paginate=True)
    return {"repository": repo, "branches": branches, "pulls": pulls,
            "complete": True, "captured_at": datetime.now(timezone.utc).isoformat()}


def plan(config: dict, snapshot: dict, *, now: datetime | None = None) -> dict:
    validate_config(config)
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise ValueError("now must include a timezone")
    if not isinstance(snapshot, dict) or snapshot.get("complete") is not True:
        raise ValueError("complete branch and PR pagination is required")
    captured = timestamp(snapshot["captured_at"])
    if captured > now or now - captured > timedelta(hours=24):
        raise ValueError("snapshot must be captured within the last 24 hours, not in the future")
    repo = snapshot["repository"]
    if repo["full_name"] != config["repository"] or not repo.get("default_branch"):
        raise ValueError("snapshot repository/default branch does not match config")
    branches, pulls = snapshot["branches"], snapshot["pulls"]
    if not isinstance(branches, list) or not isinstance(pulls, list):
        raise ValueError("snapshot branches and pulls must be arrays")
    names = [branch["name"] for branch in branches]
    if len(set(names)) != len(names) or repo["default_branch"] not in names:
        raise ValueError("snapshot has duplicate branches or lacks the default branch")
    # Refuse malformed PR metadata rather than silently overlooking an open PR.
    for pr in pulls:
        if pr["state"] not in {"open", "closed"}:
            raise ValueError("invalid PR metadata")
        if not isinstance(pr["head"].get("repo"), (dict, type(None))):
            raise ValueError("invalid PR source repository")
        for side in ("head", "base"):
            if not isinstance(pr[side].get("ref"), str) or not pr[side]["ref"]:
                raise ValueError("PR branch identity is missing")
            source = pr[side].get("repo")
            if side == "base" and source is None:
                raise ValueError("PR base repository identity is missing")
            if source is not None and (not isinstance(source, dict) or not source.get("full_name")):
                raise ValueError("PR repository identity is missing")
    candidates, retained = [], []
    for branch in branches:
        name, sha = branch["name"], branch["commit"]["sha"]
        if not isinstance(sha, str) or not SHA.fullmatch(sha):
            raise ValueError("branch head must be a full commit SHA")
        reason = None
        if name == repo["default_branch"]:
            reason = "default_branch"
        elif branch.get("protected") is not False:
            reason = "protected_or_unknown"
        elif any(fnmatchcase(name, pattern) for pattern in config["keep_patterns"]):
            reason = "keep_pattern"
        elif not any(name.startswith(prefix) for prefix in config["allowed_prefixes"]):
            reason = "prefix_not_allowed"
        related = [pr for pr in pulls if pr["head"]["ref"] == name
                   and (pr["head"].get("repo") or {}).get("full_name") == repo["full_name"]]
        # A deleted/unknown head repository with the same name is ambiguous.
        ambiguous = any(pr["head"]["ref"] == name and not pr["head"].get("repo")
                        for pr in pulls)
        if not reason and (ambiguous or any(pr["state"] == "open" for pr in related)):
            reason = "open_pr_or_unknown_source"
        if not reason and any(pr["state"] == "open" and pr["base"]["ref"] == name
                              and (pr["base"].get("repo") or {}).get("full_name") == repo["full_name"]
                              for pr in pulls):
            reason = "dependent_open_pr"
        if not reason and any(pr["state"] == "closed" and not pr.get("merged_at") for pr in related):
            reason = "closed_unmerged_pr"
        matching = [pr for pr in related if pr["state"] == "closed" and pr.get("merged_at")
                    and pr["head"].get("sha") == sha
                    and pr["base"]["ref"] == repo["default_branch"]
                    and (pr["base"].get("repo") or {}).get("full_name") == repo["full_name"]]
        merged = max(matching, key=lambda pr: timestamp(pr["merged_at"]), default=None)
        if not reason and merged is None:
            reason = "no_merged_pr_at_current_head"
        if not reason and merged["user"]["login"] not in config["allowed_pr_authors"]:
            reason = "pr_author_not_allowed"
        if not reason and now - timestamp(merged["merged_at"]) < timedelta(days=config["minimum_age_days"]):
            reason = "retention_period"
        entry = {"branch": name, "head_sha": sha}
        if reason:
            retained.append({**entry, "reason": reason})
        else:
            candidates.append({**entry, "pr_number": merged["number"],
                               "merged_at": merged["merged_at"],
                               "pr_author": merged["user"]["login"]})
    return {"mode": "report-only", "repository": repo["full_name"],
            "captured_at": snapshot["captured_at"], "generated_at": now.isoformat(),
            "candidates": sorted(candidates, key=lambda row: row["branch"]),
            "retained": sorted(retained, key=lambda row: row["branch"]),
            "deletion_authorized": False,
            "remaining_checks": ["fresh remote head and protections", "other contributors or active work",
                                 "dependent PRs and local worktrees", "explicit cleanup authorization"]}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=CONFIG)
    parser.add_argument("--snapshot", type=Path, help="complete offline GitHub metadata snapshot")
    args = parser.parse_args(argv)
    try:
        config = json.loads(args.config.read_text(encoding="utf-8"))
        validate_config(config)
        snapshot = (json.loads(args.snapshot.read_text(encoding="utf-8"))
                    if args.snapshot else collect(config["repository"]))
        print(json.dumps(plan(config, snapshot), ensure_ascii=False, indent=2))
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError):
        # Do not echo gh stderr, auth details, or untrusted metadata on failure.
        print("Cleanup plan unavailable: invalid/incomplete metadata or GitHub GET failed; no action taken.",
              file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
