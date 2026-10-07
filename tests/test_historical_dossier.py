"""Guard the bounded historical dossier and its synchronized Word exports."""
from hashlib import sha256
import json
from pathlib import Path
import re
from xml.etree import ElementTree as ET
from zipfile import ZipFile

import yaml

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'


def _markdown_text(text):
    lines = []
    for line in text.splitlines():
        if re.fullmatch(r'\s*(?:---+|```.*)\s*', line):
            continue
        if re.fullmatch(r'\s*\|[\s|:\-]+\|\s*', line):
            continue
        line = re.sub(r'^\s*(?:- |\d+\. )', '', line)
        line = re.sub(r'^#{1,6}\s+', '', line)
        lines.append(line.replace('|', ' ').replace('*', '').replace('`', ''))
    return ''.join(''.join(lines).split())


def _docx_text(path):
    with ZipFile(path) as archive:
        body = ET.fromstring(archive.read('word/document.xml'))
    return ''.join(element.text or '' for element in body.iter(W + 't'))


def test_original_yaml_evidence_and_verdicts_are_preserved():
    data = yaml.safe_load((DOCS / 'example-topic-dossier.gaps.yml').read_text())
    assert data['generated'] == '2026-05-22'
    assert data['recall']['unique_papers'] == 435
    assert data['recall']['screen']['retrieved'] == 25
    assert data['recall']['screen']['kept'] == 25
    assert [(g['id'], g['open'], g['verdict']) for g in data['gaps']] == [
        ('G1', 'occupied', 'no-go'), ('G2', 'open', 'conditional-go')]
    # Snapshot every pre-existing field; new interpretation cannot rewrite history.
    original_fields = {key: value for key, value in data.items()
                       if key not in {'record_status', 'interpretation_context'}}
    digest = sha256(json.dumps(original_fields, sort_keys=True,
                              ensure_ascii=False).encode()).hexdigest()
    assert digest == 'dbae4c36a2206bc367dedb965d2540bb354184b8cb684412e09b593113c86284'


def test_yaml_does_not_treat_history_as_current_selection():
    data = yaml.safe_load((DOCS / 'example-topic-dossier.gaps.yml').read_text())
    context = data['interpretation_context']
    assert data['record_status'] == 'historical-screening-example'
    assert context['historical_search_date'] == '2026-05-22'
    assert context['current_status'] == 'unknown'
    assert context['new_search_performed'] is False
    assert context['current_feasibility_verified'] is False
    assert context['researcher_selection']['status'] == 'not-recorded'
    assert context['researcher_selection']['selected_gap_id'] is None
    assert 'must explicitly select' in context['researcher_selection']['requirement']
    assert 'not proof of absence from the wider' in context['bounded_absence']
    assert 'do not mean that a gate passed' in context['neutral_scores'].replace('\n', ' ')


def test_bilingual_dossier_qualifications_and_original_scores():
    en = (DOCS / 'example-topic-dossier.md').read_text()
    tw = (DOCS / 'example-topic-dossier.zh-TW.md').read_text()
    for text in (en, tw):
        assert text.count('2026-05-22') >= 2
        assert '435' in text and '25' in text and '13' in text
        assert text.count('1/5') == 2
        assert text.count('3/5') == 7  # Six historical scores and one interpretation.
        assert 'conditional-go' in text
        for author in ('Kizilkaya', 'Sajja', 'Wang', 'Zhang', 'Ravindran',
                       'Batista', 'Schück', 'Braga', 'Khaki', 'Jiang'):
            assert author in text
    for required in (
        'contribution, and feasibility are therefore **unknown**',
        'No such selection is recorded here',
        'neutral scores do not pass gates or record researcher selection',
        'does not establish absence from the wider literature',
        'cannot\nguarantee complete recall',
    ):
        assert required in en
    for required in ('可行性均為**未知**', '此處未記錄這類選擇',
                     '中立分數不代表通過關卡或研究者已選定主題',
                     '不能證明更廣泛的文獻中不存在此類研究', '不能保證完整召回'):
        assert required in tw
    for removed in ('All three gates clear at neutral', 'No one has tried this',
                    'No paper builds calibrated', 'A full-recall search'):
        assert removed not in en
    for removed in ('三個關卡均以中立評價通過', '未曾有人嘗試過',
                    '尚無論文為社會水文學建立', '全召回檢索'):
        assert removed not in tw


def test_markdown_and_docx_have_complete_text_parity():
    for stem in ('example-topic-dossier', 'example-topic-dossier.zh-TW'):
        markdown = _markdown_text((DOCS / f'{stem}.md').read_text())
        docx = ''.join(_docx_text(DOCS / f'{stem}.docx').split())
        assert docx == markdown, f'{stem}: DOCX must mirror every source paragraph and table'
