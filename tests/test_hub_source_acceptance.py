import copy
import hashlib
import json
from pathlib import Path
from scripts import check_manifest_observations as guard

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))

def test_hub_bounded_acceptance_and_observation_history():
    snapshot = read('test-corpus/integration/upstream-contracts.json')
    history = read('test-corpus/integration/hub-source-acceptance-history.json')
    marketplace = read('.claude-plugin/marketplace.json')
    observations = read('test-corpus/integration/manifest-observations.json')
    hub = next(r for r in snapshot['repositories'] if r['repo_url'].endswith('/research-hub'))
    review = history['current_hub_source_review']
    assert snapshot['checked_on'] == '2026-10-19'
    assert history['previous_accepted_hub']['commit'] == '7e046383368d85acb8dfbf0d734ecaaae335cf0a'
    assert history['previous_accepted_hub']['plugin']['version'] == '0.5.4'
    assert history['previous_hub_manifest_observation']['plugin']['version'] == '0.5.10'
    assert hub['commit'] == review['commit'] == '773650343f638295f96d0fb53bebf145a30e86c7'
    assert hub['tree'] == review['tree'] == '84406c080df5ea50ad9acf16ec685f7537779f64'
    assert len(hub['skills']) == 12 and len(set(hub['shared_references'])) == 12
    assert set(read('test-corpus/integration/native-reader-future-contract.json')['candidate_dependencies']).issubset(hub['shared_references'])
    assert hub['plugin'] == review['plugin'] == {'name': 'research-workspace', 'version': '0.5.20'}
    raw = review['manifest_text'].encode('utf-8')
    assert hashlib.sha256(raw).hexdigest() == review['manifest_sha256']
    assert hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == review['manifest_blob'] == '57cd467d7401d44997bfca3844b379de540c300e'
    assert {k: json.loads(raw)[k] for k in ('name', 'version')} == hub['plugin']
    prior = history['prior_hub_source_reviews'][0]
    assert prior['commit'] == '4d83b8b772da5fbb232272aa2829573c3c05b45e'
    assert prior['tree'] == '0bb138414ccd5fea465d808cee8ad4760b22c533'
    assert prior['plugin'] == {'name': 'research-workspace', 'version': '0.5.14'}
    prior_raw = prior['manifest_text'].encode('utf-8')
    assert hashlib.sha256(prior_raw).hexdigest() == prior['manifest_sha256']
    assert hashlib.sha1(b'blob ' + str(len(prior_raw)).encode() + b'\0' + prior_raw).hexdigest() == prior['manifest_blob'] == 'a97e15ab29d2a7d714deb66434c28421516f77de'
    previous = history['prior_hub_source_reviews'][-1]
    assert previous['commit'] == 'c1ab382e1bc4bfdb1d5df6a230d1ab4509a50d2a'
    assert previous['tree'] == 'd0de196c2b3f20bd486eb3700dd4eb10207c3941'
    assert previous['plugin'] == {'name': 'research-workspace', 'version': '0.5.18'}
    previous_raw = previous['manifest_text'].encode('utf-8')
    assert hashlib.sha256(previous_raw).hexdigest() == previous['manifest_sha256']
    assert hashlib.sha1(b'blob ' + str(len(previous_raw)).encode() + b'\0' + previous_raw).hexdigest() == previous['manifest_blob'] == '4182acbe3a04b00e814f5cdbba8f87018b60cef0'
    assert guard.validate(marketplace, snapshot, observations) == []
    stale = copy.deepcopy(observations)
    stale['observations'].append(history['previous_hub_manifest_observation'])
    assert any('unexpected repository or unchanged accepted version' in e for e in guard.validate(marketplace, snapshot, stale))


def test_hub_source_review_date_is_scoped_consistently():
    snapshot = read('test-corpus/integration/upstream-contracts.json')
    review = read('test-corpus/integration/hub-source-acceptance-history.json')['current_hub_source_review']
    assert review['reviewed_on'] == '2026-10-28'
    assert 'research-hub accepted 0.5.20 identity and bounded 25-path source review refreshed on 2026-10-28' in snapshot['verification_scope']
    for suffix in ('', '.zh-TW'):
        text = (ROOT / f'docs/system-assessment{suffix}.md').read_text(encoding='utf-8')
        intro = text.split('## ', 1)[0]
        assert '2026-10-03' in intro and '2026-10-28' in intro
        assert 'research-hub' in intro and '25' in intro
        assert 'runtime' in intro and 'catalog' in intro.lower()
