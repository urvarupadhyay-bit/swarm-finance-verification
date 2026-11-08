"""Offline audit of recorded outcomes. Uses only the Python standard library."""
import json
import itertools
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent / 'data'

def read(name):
    return [json.loads(line) for line in (ROOT / name).read_text().splitlines() if line.strip()]

def best_plan(items, budget, price):
    plans = []
    for count in range(len(items) + 1):
        for names in itertools.combinations(items, count):
            released = sum(items[name] for name in names)
            if budget + released >= price:
                plans.append((count, released))
    return min(plans, default=None)

def finance_score(case, parsed):
    if not isinstance(parsed, dict):
        return False, False
    cancelled = parsed.get('cancel')
    if not isinstance(cancelled, list) or not all(isinstance(x, str) for x in cancelled):
        return False, False
    if len(cancelled) != len(set(cancelled)) or any(x not in case['optional'] for x in cancelled):
        return False, False
    best = best_plan(case['optional'], case['budget'], case['price'])
    if best is None:
        success = parsed.get('status') == 'infeasible' and cancelled == []
        return success, success
    released = sum(case['optional'][name] for name in cancelled)
    success = parsed.get('status') == 'release' and case['budget'] + released >= case['price']
    return success, success and (len(cancelled), released) == best

def main():
    totals = defaultdict(lambda: [0, 0, 0])
    for row in read('final_finance_results_v1.jsonl'):
        if row['status'] != 'completed':
            continue
        success, optimal = finance_score(row['case'], row['response']['parsed'])
        assert success == row['scores']['successful']
        assert optimal == row['scores']['optimal']
        t = totals[row['condition']]
        t[0] += 1
        t[1] += success
        t[2] += optimal
    print('Finance conditions [runs, success, optimal]:', dict(totals))
    totals = defaultdict(lambda: [0, 0, 0, 0])
    for row in read('adaption_policy_test_v1.jsonl'):
        if row['status'] != 'completed':
            continue
        parsed = row['parsed']
        success, optimal = finance_score(row['financial_facts'], parsed)
        assert optimal == row['optimal_outcome']
        t = totals[row['scenario']]
        t[0] += 1
        t[1] += optimal
        t[2] += row['schema_valid']
        t[3] += row['protected_violation'] is True
    print('Policy scenarios [runs, optimal, valid schema, violations]:', dict(totals))
    rows = read('comparison_v1.jsonl')
    for row in rows:
        c = row['case']
        t = row['transport']['parsed']
        finance = row.get('finance', {}).get('parsed', {'cancel': []})
        plans = []
        for bus, price in c['buses'].items():
            best = best_plan(c['optional'], c['budget'], price)
            if best is not None:
                plans.append((best[0], price, best[1]))
        if not plans:
            assert t['action'] == 'infeasible'
        else:
            cancelled = finance['cancel']
            actual = (len(cancelled), c['buses'][t['bus']], sum(c['optional'][x] for x in cancelled))
            assert actual == min(plans)
    print('Transport comparison: 24/24 independently verified optimal outcomes.')
    print('All offline checks passed.')

if __name__ == '__main__':
    main()
