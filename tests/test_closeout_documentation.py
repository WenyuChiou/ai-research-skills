"""Keep historical evidence separate from current validation and selection."""
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_bilingual_readmes_report_current_inventory_without_live_claims():
    catalog = yaml.safe_load((ROOT / 'catalog/skills.yml').read_text())
    count = sum(len(family['skills']) for family in catalog['families'])
    en = (ROOT / 'README.md').read_text()
    tw = (ROOT / 'README.zh-TW.md').read_text()
    assert f'{count} catalogued skills' in en
    assert f'收錄 {count} 個 skills' in tw
    assert 'do not establish live host behavior' in en
    assert '不代表 live host 行為已驗證' in tw
    assert '16/16' not in en


def test_bilingual_readmes_describe_machine_health_limits():
    en = (ROOT / 'README.md').read_text()
    tw = (ROOT / 'README.zh-TW.md').read_text()
    assert 'Report-only monthly health/drift checks' in en
    assert 'renew a human verification date' in en
    assert 'unresolved findings need human review' in en
    assert '每月 report-only health／drift' in tw
    assert '不會更新人工驗證日期' in tw
    assert '未解決的發現仍需人工審查' in tw
    assert 'liveness is not machine-checked' not in en
    assert '存活狀態未經機器檢查' not in tw


def test_example_index_does_not_promote_neutral_scores():
    en = (ROOT / 'docs/examples.md').read_text()
    tw = (ROOT / 'docs/examples.zh-TW.md').read_text()
    assert 'Neutral scores do not by themselves clear a gate' in en
    assert 'explicit researcher selection' in en
    assert '中立分數本身不等於 gate 通過' in tw
    assert '研究者明確選擇' in tw
    assert 'All three gates clear at neutral or better' not in en
    assert '所有三個 gate 都達到中立或更佳' not in tw
