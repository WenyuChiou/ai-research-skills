---
name: Broken link / stale URL
about: A SKILL.md URL or doc reference 404s or points at the wrong path.
title: "[broken-link] "
labels: documentation
---

## Where's the broken link?

- File: `<README.md / docs/X.md / catalog/skills.yml / .claude-plugin/marketplace.json>`
- Line / section:
- The broken URL: `<paste>`
- Status: `404 / wrong content / redirects to wrong place / other`

## Where should it point?

- Correct URL (if you know it):

## Why is it broken?

(check any that apply)

- [ ] Upstream repo renamed a directory (catalog hasn't synced)
- [ ] Branch name changed (e.g. `master` → `main`)
- [ ] File deleted upstream
- [ ] Typo in the original link
- [ ] Don't know

## Catalog ↔ upstream sync

If this looks like a catalog-vs-upstream drift, mention which upstream
repo you noticed the actual file at, so the fix can update both ends.
