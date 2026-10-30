"""Check observed fictional runs without changing inputs or evaluator outputs.

Uses Python's standard library. Run from any directory:
    python tests/check_results.py --round r1
This checks structure, arithmetic and cross-run invariants. A separate semantic
review must assess evidence use, counterevidence, deduction ownership and choice.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import re

HERE = Path(__file__).resolve().parent
WEIGHTS = {'quality': 35, 'fit': 20, 'value': 15, 'long_term_cost': 10,
           'after_sales': 10, 'rd_marketing': 5, 'labor': 5}
STATUSES = {'可进入购买决策', '仅适合优先核验', '证据不足，暂不排序', '不符合本次购买条件', '排除购买'}

def check(round_name):
    if not re.fullmatch(r'r[1-9][0-9]*', round_name):
        raise ValueError('Round must be r followed by a positive integer, inside tests/runs.')
    problems, checked, by_fixture = [], [], {}
    rounds = json.loads((HERE / 'rounds.json').read_text(encoding='utf-8')) if (HERE / 'rounds.json').exists() else {}
    round_info = rounds.get(round_name, {})
    fixture_ids = round_info.get('fixture_ids', ['F1', 'F2', 'F3', 'F4', 'F5'])
    if not fixture_ids or len(fixture_ids) != len(set(fixture_ids)) or not set(fixture_ids).issubset({'F1', 'F2', 'F3', 'F4', 'F5'}):
        raise ValueError('Invalid recorded fixture selection')
    def need(condition, description):
        if not condition:
            problems.append(description)
    for fid in fixture_ids:
        fixture_file = HERE / 'fixtures' / (fid + '.json')
        fixture = json.loads(fixture_file.read_text(encoding='utf-8'))
        input_hash = hashlib.sha256(fixture_file.read_bytes()).hexdigest()
        ids = {record['id'] for record in fixture['records']}
        expected_candidates = set(fixture['scenario']['candidates'])
        runs = []
        for suffix in ['A', 'B', 'C']:
            run_id = fid + '-' + suffix
            path = HERE / 'runs' / round_name / (run_id + '.json')
            if not path.exists():
                problems.append(run_id + ': not observed / file missing')
                continue
            try:
                data = json.loads(path.read_text(encoding='utf-8'))
                need(data['fixture_id'] == fid and data['run_id'] == run_id, run_id + ': identity')
                need(data['input_hash'].lower() == input_hash, run_id + ': input hash')
                need(isinstance(data['skill_hash'], str) and len(data['skill_hash']) == 64, run_id + ': skill hash')
                if 'runtime_hash' in round_info:
                    need(data['skill_hash'].lower() == round_info['runtime_hash'], run_id + ': rule snapshot hash')
                if round_info.get('posthoc_calibration'):
                    need(data['execution'].get('calibration_hash') == round_info['calibration_hashes'][fid + '.json'], run_id + ': shared calibration input hash')
                need(all(k in data['execution'] for k in ['date', 'context', 'configuration', 'observed_scope']), run_id + ': execution provenance')
                need(bool(data['anchors']), run_id + ': anchors absent')
                candidates = {c['candidate_id']: c for c in data['candidates']}
                need(set(candidates) == expected_candidates and len(candidates) == len(data['candidates']), run_id + ': candidates')
                for cid, candidate in candidates.items():
                    label = run_id + '/' + cid
                    dims = candidate['dimensions']
                    need(set(dims) == set(WEIGHTS), label + ': dimension coverage')
                    for key, weight in WEIGHTS.items():
                        dim = dims[key]
                        score = dim['score']
                        need(dim['weight'] == weight, label + '/' + key + ': weight')
                        need(score is None or (isinstance(score, (int, float)) and not isinstance(score, bool) and math.isfinite(score) and 0 <= score <= 10), label + '/' + key + ': score bounds')
                        need(isinstance(dim['reason'], str) and bool(dim['reason']), label + '/' + key + ': reason')
                        need(set(dim['evidence_ids']).issubset(ids), label + '/' + key + ': unknown evidence id')
                        need(score is None or bool(dim['evidence_ids']), label + '/' + key + ': unsupported numeric score')
                        need('evidence_state' in dim, label + '/' + key + ': evidence state')
                    need(candidate['purchase_status'] in STATUSES, label + ': purchase status')
                    need(bool(candidate['status_reason']), label + ': status reason')
                    for item in candidate['safety']:
                        need(item['state'] in ['通过', '待核', '不满足', '不适用'], label + ': safety state')
                        need(set(item['evidence_ids']).issubset(ids), label + ': safety evidence')
                    for event in candidate['negative_events']:
                        need(event['primary_dimension'] in WEIGHTS, label + ': deduction dimension')
                        need(set(event['evidence_ids']).issubset(ids), label + ': deduction evidence')
                        need(bool(event['reason']) and 'other_consequences' in event, label + ': deduction reason/scope')
                        before, after = event['before'], event['after']
                        need(all(v is None or (isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) and 0 <= v <= 10) for v in (before, after)), label + ': deduction values')
                        if before is not None and after is not None:
                            need(after <= before, label + ': deduction direction')
                    agg = candidate['aggregate']
                    included = agg['included_dimensions']
                    need(len(included) == len(set(included)) and set(included).issubset(WEIGHTS), label + ': aggregate dimensions')
                    if agg['kind'] in ['complete', 'partial']:
                        need(all(dims[k]['score'] is not None for k in included), label + ': unknown included in aggregate')
                        if all(dims[k]['score'] is not None for k in included):
                            total = sum(dims[k]['score'] * WEIGHTS[k] / 10 for k in included)
                            denominator = sum(WEIGHTS[k] for k in included)
                            need(isinstance(agg['numerator'], (int, float)) and abs(agg['numerator'] - total) < 1e-7, label + ': arithmetic')
                            need(agg['denominator'] == denominator, label + ': original denominator')
                        need(agg['kind'] != 'complete' or set(included) == set(WEIGHTS), label + ': incomplete total called complete')
                    else:
                        need(agg['kind'] == 'not_scored', label + ': aggregate kind')
                need('reason' in data['comparison'] and 'unresolved' in data['comparison'], run_id + ': comparison explanation')
                data['_candidates'] = candidates
                runs.append(data)
                checked.append(run_id)
            except (ValueError, KeyError, TypeError) as error:
                problems.append(run_id + ': malformed output: ' + str(error))
        by_fixture[fid] = runs
        if len(runs) != 3:
            continue
        need(len({r['skill_hash'] for r in runs}) == 1, fid + ': different rule inputs')
        for cid in expected_candidates:
            if not all(cid in r['_candidates'] for r in runs):
                continue
            candidates = [r['_candidates'][cid] for r in runs]
            need(len({c['purchase_status'] for c in candidates}) == 1, fid + '/' + cid + ': purchase-status disagreement')
            safety_maps = [{s['item']: s['state'] for s in c['safety']} for c in candidates]
            common_items = set.intersection(*(set(s) for s in safety_maps))
            for item in common_items:
                need(len({s[item] for s in safety_maps}) == 1, fid + '/' + cid + '/' + item + ': safety disagreement')
            for key in WEIGHTS:
                scores = [c['dimensions'][key]['score'] for c in candidates]
                if all(x is None for x in scores):
                    continue
                if any(x is None for x in scores):
                    problems.append(fid + '/' + cid + '/' + key + ': numeric/N-A scope disagreement')
                else:
                    need(max(scores) - min(scores) <= 1 + 1e-7, fid + '/' + cid + '/' + key + ': drift over 1/10')
            totals = [c['aggregate']['numerator'] for c in candidates if c['aggregate']['kind'] == 'complete']
            if len(totals) == 3:
                need(max(totals) - min(totals) <= 5 + 1e-7, fid + '/' + cid + ': total drift over 5/100')
        if fid == 'F3':
            expected = {'F3-A': (42, 55), 'F3-B': (42.5, 55), 'F3-C': (18, 20)}
            for r in runs:
                for cid, (num, den) in expected.items():
                    agg = r['_candidates'][cid]['aggregate']
                    need(agg['numerator'] == num and agg['denominator'] == den, r['run_id'] + '/' + cid + ': fixed-anchor calculation')
        if fid == 'F4':
            expected = {'F4-A': '仅适合优先核验', 'F4-B': '排除购买', 'F4-C': '可进入购买决策'}
            for r in runs:
                for cid, status in expected.items():
                    need(r['_candidates'][cid]['purchase_status'] == status, r['run_id'] + '/' + cid + ': fixed safety/status invariant')
        if fid == 'F5':
            for r in runs:
                for cid in expected_candidates:
                    candidate = r['_candidates'][cid]
                    need(candidate['purchase_status'] == '可进入购买决策', r['run_id'] + '/' + cid + ': purchase invariant')
                    need(candidate['aggregate']['kind'] == 'complete', r['run_id'] + '/' + cid + ': complete-score coverage')
    expected_runs = len(fixture_ids) * 3
    result = {'round': round_name, 'fixture_ids': fixture_ids, 'observed_runs': len(checked), 'expected_runs': expected_runs,
              'machine_checks': 'passed' if not problems and len(checked) == expected_runs else 'failed_or_incomplete',
              'problems': problems, 'semantic_review': 'separate_required',
              'scope': 'fictional materials only; no real product or client-invocation claim'}
    output = HERE / 'runs' / round_name / 'machine-check.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=True))
    return not problems and len(checked) == expected_runs

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--round', default='r1')
    args = parser.parse_args()
    raise SystemExit(0 if check(args.round) else 1)
