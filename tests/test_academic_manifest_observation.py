"""Cache observation regression; no source acceptance or host execution."""
import copy
import hashlib
import json
from pathlib import Path

import pytest
from scripts import check_manifest_observations as guard
from scripts import check_skill_health as health

ROOT = Path(__file__).resolve().parents[1]
REPO = 'https://github.com/WenyuChiou/academic-writing-skills'


def inputs():
    return tuple(json.loads((ROOT / path).read_text(encoding='utf-8')) for path in (
        '.claude-plugin/marketplace.json',
        'test-corpus/integration/upstream-contracts.json',
        'test-corpus/integration/manifest-observations.json'))


def academic(observed):
    return next(row for row in observed['observations'] if row['repo_url'] == REPO)


def test_academic_cache_observation_keeps_historical_acceptance():
    market, snapshot, observed = inputs()
    record = academic(observed)
    source = next(row for row in snapshot['repositories'] if row['repo_url'] == REPO)
    plugin = next(row for row in market['plugins'] if row['name'] == 'academic-writing-skills')
    assert snapshot['checked_on'] == '2026-10-19'
    assert source['plugin']['version'] == '1.3.24'
    assert plugin['version'] == record['plugin']['version'] == '1.4.1'
    assert plugin['source']['ref'] == source['default_branch'] == record['ref'] == 'main'
    assert record['commit'] == 'e776ceb893fb719d2f48ca2a8b3e8004264b57ff'
    assert record['tree'] == '1bdea4e95a371f4d79031bccb7ad2ec0a27cb684'
    raw = record['manifest_text'].encode('utf-8')
    assert hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == record['manifest_blob'] == 'c16f4e3135541019aeacaeb85c791078be45da2c'
    assert len(source['skills']) == 2
    assert guard.validate(market, snapshot, observed) == []


@pytest.mark.parametrize('fault', ['missing', 'duplicate', 'tampered', 'wrong-source', 'wrong-ref', 'wrong-version', 'wrong-name'])
def test_academic_cache_observation_fails_closed(fault):
    market, snapshot, observed = inputs()
    record = academic(observed)
    if fault == 'missing':
        observed['observations'].remove(record)
    elif fault == 'duplicate':
        observed['observations'].append(copy.deepcopy(record))
    elif fault == 'tampered':
        record['manifest_text'] += ' '
    elif fault == 'wrong-source':
        record['repo_url'] = 'https://github.com/other/academic-writing-skills'
    elif fault == 'wrong-ref':
        record['ref'] = 'master'
    elif fault == 'wrong-version':
        record['plugin']['version'] = '1.3.24'
    else:
        record['plugin']['name'] = 'paper-review'
    assert guard.validate(market, snapshot, observed)


@pytest.mark.parametrize('version,drifts', [('1.4.0', True), ('1.4.1', False)])
def test_academic_version_health_detects_old_cache(version, drifts, monkeypatch, tmp_path):
    """Actual recorded manifest, synthetic metadata/SKILL responses for isolation."""
    market, _, observed = inputs()
    plugin = next(row for row in market['plugins'] if row['name'] == 'academic-writing-skills')
    plugin['version'] = version
    path = tmp_path / 'marketplace.json'
    path.write_text(json.dumps(market), encoding='utf-8')
    monkeypatch.setattr(health, 'MARKETPLACE', path)
    catalog = health.yaml.safe_load(health.CATALOG.read_text(encoding='utf-8'))
    skills = [s for family in catalog['families'] for s in family['skills']]
    refs = {p['source']['url'].removesuffix('.git'): p['source']['ref'] for p in market['plugins']}
    monkeypatch.setattr(health, '_request_json', lambda url: {
        'archived': False, 'default_branch': refs[url.replace('https://api.github.com/repos/', 'https://github.com/')]})
    responses = {health._raw_skill_url(s['skill_url']): '---\nname: '+s['name']+'\n---\n' for s in skills}
    for p in market['plugins']:
        repo = p['source']['url'].removesuffix('.git')
        responses[health._raw_repo_file_url(repo, p['source']['ref'], '.claude-plugin/plugin.json')] = (
            academic(observed)['manifest_text'] if repo == REPO else json.dumps({k:p[k] for k in ('name','version')}))
    monkeypatch.setattr(health, '_request_text', responses.__getitem__)
    report = health.run_checks()
    findings = [f for f in report['findings'] if f['check'] == 'plugin_version_drift' and f['target'] == 'academic-writing-skills']
    assert bool(findings) is drifts
    assert len(report['findings']) == int(drifts)
