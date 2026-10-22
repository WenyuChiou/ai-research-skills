"""Offline bilingual documentation guards; no install or live run is exercised."""
from pathlib import Path
import re

import pytest

ROOT = Path(__file__).resolve().parents[1]
ENTRYPOINTS = (
    "README.md", "README.zh-TW.md",
    "docs/researcher-workflow-checklist.md",
    "docs/researcher-workflow-checklist.zh-TW.md",
)
AUTO = 'research-hub auto "agent-based modeling" --max-papers 3 --no-nlm'


def _check_entrypoint(text, path):
    zh = ".zh-TW." in path
    blocks = re.findall(r"```bash\n(.*?)```", text, re.S)
    installs = [block for block in blocks if "pip install research-hub-pipeline" in block]
    assert len(installs) == 1
    assert installs[0].strip().endswith("research-hub doctor")
    assert "research-hub auto" not in installs[0]
    live = next(block for block in blocks if AUTO in block)
    assert "pip install" not in live
    heading = "獨立的 live smoke（非安裝步驟）" if zh else "Separate live smoke (not installation)"
    start = text.index(heading)
    end = text.index(AUTO)
    assert start < end
    warning = text[start:end]
    prefix = "docs/" if path.startswith("README") else ""
    suffix = ".zh-TW" if zh else ""
    assert f"]({prefix}live-run-preflight{suffix}.md)" in warning
    terms = (("只停用 NotebookLM", "不會停用其他網路呼叫", "模型", "寫入", "費用", "授權")
             if zh else ("disables NotebookLM only", "does not disable other network calls",
                         "models", "writes", "cost", "authorization"))
    for term in terms:
        assert term in warning


@pytest.mark.parametrize("path", ENTRYPOINTS)
def test_entrypoint_install_stops_at_doctor_and_live_smoke_is_gated(path):
    _check_entrypoint((ROOT / path).read_text(encoding="utf-8"), path)


@pytest.mark.parametrize("path", ENTRYPOINTS)
def test_rejects_live_command_moved_back_into_install(path):
    text = (ROOT / path).read_text(encoding="utf-8")
    text = text.replace(AUTO + "\n", "").replace("research-hub doctor\n", "research-hub doctor\n" + AUTO + "\n", 1)
    with pytest.raises(AssertionError):
        _check_entrypoint(text, path)


@pytest.mark.parametrize("path", ENTRYPOINTS)
@pytest.mark.parametrize("choice", range(7))
def test_rejects_missing_live_warning_or_preflight_link(path, choice):
    text = (ROOT / path).read_text(encoding="utf-8")
    terms = (("只停用 NotebookLM", "不會停用其他網路呼叫", "模型", "寫入", "費用", "授權", "live-run-preflight.zh-TW.md")
             if ".zh-TW." in path else ("disables NotebookLM only", "does not disable other network calls",
                                        "models", "writes", "cost", "authorization", "live-run-preflight.md"))
    with pytest.raises(AssertionError):
        _check_entrypoint(text.replace(terms[choice], "REMOVED"), path)


def _check_route(text, zh):
    bullet = next(b for b in text.split("\n- ") if b.startswith("`research-hub-multi-ai`"))
    terms = (("只有計畫會呼叫 `research-hub` 時", "`research-hub doctor`", "缺少 Hub 時不要產生 Hub 命令",
              "delegate-only 計畫不需 Hub 即可繼續", "leaf skill", "wrapper 可用", "preflight", "資料、費用與寫入授權檢查")
             if zh else ("only when the plan calls `research-hub`", "`research-hub doctor`", "If Hub is missing, do not emit Hub",
                         "delegate-only plans may proceed without Hub", "leaf skill", "wrapper", "preflight", "data/cost/write permission checks"))
    for term in terms:
        assert term in bullet
    # The previous unconditional joint prerequisite must not coexist with the correction.
    assert ("`research-hub` 與 `research-hub-multi-ai`" if zh else
            "`research-hub` and `research-hub-multi-ai` need") not in text
    return terms


@pytest.mark.parametrize("zh", [False, True])
def test_multi_ai_hub_prerequisite_is_conditional_and_leaves_still_checked(zh):
    path = ROOT / ("docs/install.zh-TW.md" if zh else "docs/install.md")
    text = path.read_text(encoding="utf-8")
    terms = _check_route(text, zh)
    for term in terms:
        with pytest.raises(AssertionError):
            _check_route(text.replace(term, "REMOVED"), zh)
    old = ("`research-hub` 與 `research-hub-multi-ai`" if zh else
           "`research-hub` and `research-hub-multi-ai` need")
    with pytest.raises(AssertionError):
        _check_route(text + "\n- " + old, zh)
