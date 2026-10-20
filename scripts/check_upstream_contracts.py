#!/usr/bin/env python3
"""Read-only producer/consumer contract check against explicitly supplied clones.

Usage: python scripts/check_upstream_contracts.py --source research-hub=/path/to/repo
Supply all five repositories. This never installs plugins or invokes an AI host.
Add --accepted-source to bind local Git identity and bounded relevant files to
the reviewed snapshot. See docs/accepted-source-verification.md for limits.
"""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
from pathlib import PurePosixPath
import re
import subprocess
import sys

import yaml

try:
    from . import check_marketplace_consistency as consistency
    from .check_skill_health import _frontmatter_name
except ImportError:
    import check_marketplace_consistency as consistency
    from check_skill_health import _frontmatter_name


SNAPSHOT = Path(__file__).resolve().parents[1] / "test-corpus/integration/upstream-contracts.json"


class GitUnavailable(RuntimeError):
    pass


def _git(root: Path, *arguments: str) -> bytes:
    # No lazy object fetching, replace-object interpretation, fsmonitor hook or
    # optional index refresh. Never execute a shell or alter repository config.
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    env.update(GIT_OPTIONAL_LOCKS="0", GIT_TERMINAL_PROMPT="0")
    try:
        result = subprocess.run(
            ["git", "--no-lazy-fetch", "--no-replace-objects", "--literal-pathspecs",
             "-c", "core.fsmonitor=false", "-C", str(root), *arguments],
            env=env, capture_output=True, timeout=10, check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise GitUnavailable(type(exc).__name__) from exc
    if result.returncode:
        raise GitUnavailable("Git metadata/object unavailable (or Git lacks --no-lazy-fetch)")
    return result.stdout


def _relative_path(value: str) -> str:
    if (not isinstance(value, str) or value in ("", ".") or "\\" in value or ":" in value
            or "\0" in value or str(PurePosixPath(value)) != value
            or PurePosixPath(value).is_absolute() or ".." in PurePosixPath(value).parts):
        raise ValueError("invalid relevant repository-relative path")
    return value


def _accepted_source(root: Path, repository: dict, skills: list[dict], plugin: dict) -> dict:
    result = {"repository": repository["repo_url"], "status": "unavailable",
              "reviewed_commit": repository.get("commit"), "reviewed_tree": repository.get("tree"),
              "head_commit": None, "head_tree": None, "files_checked": 0, "findings": []}
    findings = result["findings"]
    try:
        for key in ("commit", "tree"):
            if not isinstance(repository.get(key), str) or not re.fullmatch(r"[0-9a-f]{40}", repository[key]):
                raise ValueError("reviewed commit and tree must be full SHA-1 object identities")
        if repository.get("plugin") != {key: plugin[key] for key in ("name", "version")}:
            raise ValueError("reviewed manifest identity differs from the current catalog")
        expected_skills = [{key: skill[key] for key in ("name", "directory")} for skill in skills]
        if repository.get("skills") != expected_skills:
            raise ValueError("reviewed skill paths differ from the current catalog")
        shared = repository.get("shared_references")
        if not isinstance(shared, list) or len(shared) > 32 or len(set(shared)) != len(shared):
            raise ValueError("shared_references must be an explicit unique list of at most 32 paths")
        paths = [".claude-plugin/plugin.json", *(s["directory"] + "/SKILL.md" for s in skills), *shared]
        paths = list(dict.fromkeys(_relative_path(path) for path in paths))
        if Path(_git(root, "rev-parse", "--show-toplevel").decode().strip()).resolve() != root.resolve():
            raise GitUnavailable("supplied source is not the Git worktree root")
        head, tree = _git(root, "rev-parse", "HEAD", "HEAD^{tree}").decode().splitlines()
        result.update(head_commit=head, head_tree=tree)
        if head != repository["commit"]:
            findings.append("HEAD differs from reviewed snapshot; same version is insufficient")
        if tree != repository["tree"]:
            findings.append("HEAD tree differs from reviewed snapshot")
        # Inspect objects/index without refreshing worktree content. git status
        # and diff can execute configured clean/process filters in a local clone.
        reviewed_entries = {}
        for entry in _git(root, "ls-tree", "-r", "-z", repository["commit"], "--", *paths).split(b"\0"):
            if entry:
                metadata, name = entry.split(b"\t", 1)
                mode, kind, oid = metadata.split()
                reviewed_entries[name] = (mode, kind, oid)
        index = _git(root, "ls-files", "--stage", "-z", "--", *paths)
        expected_index = {}
        for relative in paths:
            name = relative.encode("utf-8")
            entry = reviewed_entries.get(name)
            if entry is None or entry[0] not in (b"100644", b"100755") or entry[1] != b"blob":
                findings.append(f"{relative}: reviewed regular-file blob missing")
                continue
            expected_index[name] = (entry[0], entry[2], b"0")
        actual_index = {}
        for entry in index.split(b"\0"):
            if entry:
                metadata, name = entry.split(b"\t", 1)
                mode, oid, stage = metadata.split()
                actual_index.setdefault(name, []).append((mode, oid, stage))
        if actual_index != {name: [entry] for name, entry in expected_index.items()}:
            findings.append("relevant index paths are dirty or unmerged")
        for relative in paths:
            path = root / relative
            if not path.resolve().is_relative_to(root.resolve()) or path.is_symlink():
                findings.append(f"{relative}: relevant path escapes root or is linked")
                continue
            try:
                actual = path.read_bytes()
            except OSError:
                findings.append(f"{relative}: required file missing or unreadable")
                continue
            # Read reviewed blobs directly: no clean filters or executable
            # attributes. This also detects edits hidden by assume-unchanged.
            entry = reviewed_entries.get(relative.encode("utf-8"))
            if entry is None or entry[1] != b"blob":
                continue
            expected = _git(root, "cat-file", "blob", entry[2].decode("ascii"))
            if actual.replace(b"\r\n", b"\n") != expected.replace(b"\r\n", b"\n"):
                findings.append(f"{relative}: dirty content differs from reviewed blob")
            if os.name != "nt" and bool(path.stat().st_mode & 0o111) != (entry[0] == b"100755"):
                findings.append(f"{relative}: dirty executable mode differs from reviewed tree")
            result["files_checked"] += 1
        # Reject concurrent checkout/index changes observed during this read.
        if _git(root, "rev-parse", "HEAD", "HEAD^{tree}").decode().splitlines() != [head, tree]:
            findings.append("Git identity changed during verification")
        if _git(root, "ls-files", "--stage", "-z", "--", *paths) != index:
            findings.append("relevant Git index changed during verification")
        result["status"] = "fail" if findings else "pass"
    except (ValueError, TypeError) as exc:
        findings.append(str(exc))
        result["status"] = "fail"
    except GitUnavailable as exc:
        findings.append(str(exc))
        result["status"] = "fail" if result["head_commit"] and findings[:-1] else "unavailable"
    return result


def check_sources(catalog: dict, marketplace: dict, sources: dict[str, Path], *, accepted_snapshot: dict | None = None) -> dict:
    findings = consistency.check_skill_paths_and_refs(catalog, marketplace)
    checked = 0
    for plugin in marketplace["plugins"]:
        repo_url = consistency._normalize_repo(plugin["source"]["url"])
        slug = repo_url.rsplit("/", 1)[1]
        if slug not in sources:
            findings.append(f"{slug}: source clone was not supplied")
            continue
        root = sources[slug].resolve()
        manifest_path = root / ".claude-plugin/plugin.json"
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            for key in ("name", "version"):
                if manifest.get(key) != plugin[key]:
                    findings.append(f"{slug}: manifest {key} {manifest.get(key)!r} differs from catalog {plugin[key]!r}")
        except (OSError, ValueError) as exc:
            findings.append(f"{slug}: manifest unreadable ({type(exc).__name__})")
            continue
        for family in catalog["families"]:
            for skill in family["skills"]:
                if consistency._normalize_repo(skill["repo_url"]) != repo_url:
                    continue
                path = (root / skill["directory"] / "SKILL.md").resolve()
                if not path.is_relative_to(root):
                    findings.append(f"{skill['name']}: skill path escapes source root")
                    continue
                try:
                    name = _frontmatter_name(path.read_text(encoding="utf-8"))
                    if name != skill["name"]:
                        findings.append(f"{skill['name']}: frontmatter identity is {name!r}")
                    checked += 1
                except OSError as exc:
                    findings.append(f"{skill['name']}: SKILL.md unreadable ({type(exc).__name__})")
    report = {"status": "pass" if not findings else "fail", "skills_checked": checked,
              "verification_scope": "source-layout-and-manifest; host loading unverified", "findings": findings}
    if accepted_snapshot is not None:
        results = []
        if not isinstance(accepted_snapshot, dict) or not isinstance(accepted_snapshot.get("repositories"), list):
            report.update(status="fail", findings=findings + ["reviewed snapshot repositories must be a list"])
            return report
        rows = accepted_snapshot["repositories"]
        if not all(isinstance(row, dict) for row in rows):
            report.update(status="fail", findings=findings + ["invalid reviewed repository contract"])
            return report
        for plugin in marketplace["plugins"]:
            repo = consistency._normalize_repo(plugin["source"]["url"])
            slug = repo.rsplit("/", 1)[1]
            matching = [r for r in rows if consistency._normalize_repo(r.get("repo_url", "")) == repo]
            if len(matching) != 1:
                findings.append(f"{slug}: one reviewed repository contract is required")
                continue
            if slug not in sources:
                continue
            skills = [s for f in catalog["families"] for s in f["skills"]
                      if consistency._normalize_repo(s["repo_url"]) == repo]
            results.append(_accepted_source(sources[slug].resolve(), matching[0], skills, plugin))
        statuses = {r["status"] for r in results}
        report.update(
            status="fail" if findings or "fail" in statuses else "unavailable" if "unavailable" in statuses else "pass",
            verification_scope="accepted-source identity and bounded relevant text (CRLF/LF equivalent); live models, host loading, runtime capability and scientific quality unverified",
            snapshot_checked_on=accepted_snapshot.get("checked_on"),
            accepted_sources=results,
        )
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", action="append", default=[], metavar="REPO=PATH")
    parser.add_argument("--accepted-source", action="store_true",
                        help="verify exact reviewed commit/tree and bounded relevant files; requires local Git metadata")
    args = parser.parse_args()
    sources = {}
    for entry in args.source:
        slug, sep, local = entry.partition("=")
        if not sep or not slug or not local or slug in sources:
            parser.error("each --source must be a unique REPO=PATH")
        sources[slug] = Path(local)
    catalog, marketplace = consistency._load()
    expected = {consistency._normalize_repo(p["source"]["url"]).rsplit("/", 1)[1] for p in marketplace["plugins"]}
    if sources.keys() - expected:
        parser.error("unknown source repositories: " + ", ".join(sorted(sources.keys() - expected)))
    snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8")) if args.accepted_source else None
    report = check_sources(catalog, marketplace, sources, accepted_snapshot=snapshot)
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
