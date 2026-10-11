"""CommunityReach Phase 9: controlled evaluation of budget-aware candidate selection.
Run from CommunityReach_Project: python run_phase9.py
No changes to app.py, core.py, or paper_v2.py.
"""
import csv
import random
import statistics
import time
from pathlib import Path

from communityreach.core import Activity, greedy, paper_inspired
from communityreach.paper_v2 import paper_algorithm_1

SIZES = (10, 30, 100, 300)
SEEDS = range(5)
SCENARIOS = ("low_overlap", "high_overlap", "unequal_cost")
BUDGET_FRACTIONS = (0.15, 0.35)


def make_instance(n, seed, scenario):
    rng = random.Random(19991 + seed + n * 37 + SCENARIOS.index(scenario) * 100003)
    universe = max(50, n * 10) if scenario != "high_overlap" else max(20, n // 2)
    items = []
    for i in range(n):
        cost = rng.randint(10, 100) if scenario != "unequal_cost" else (rng.randint(10, 30) if rng.random() < .8 else rng.randint(250, 600))
        size = min(universe, rng.randint(8, 25))
        ids = frozenset(f"P{j}" for j in rng.sample(range(universe), size))
        items.append(Activity(f"Project_{i:05d}", cost, ids))
    return items


def time_call(fn):
    start = time.perf_counter()
    result = fn()
    return result, (time.perf_counter() - start) * 1000


def run():
    rows = []
    for n in SIZES:
        for scenario in SCENARIOS:
            for seed in SEEDS:
                items = make_instance(n, seed, scenario)
                total = sum(a.cost for a in items)
                all_people = set().union(*(a.people for a in items))
                for fraction in BUDGET_FRACTIONS:
                    budget = max(1, round(total * fraction))
                    candidates = {}
                    timings = {}
                    for key, fn in (
                        ("v2", lambda: paper_algorithm_1(items, budget)),
                        ("v1", lambda: paper_inspired(items, budget)),
                        ("density", lambda: greedy(items, budget, 'density')),
                        ("gain", lambda: greedy(items, budget, 'gain')),
                    ):
                        candidates[key], timings[key] = time_call(fn)
                    # BAC: pick greatest coverage, then least expense, over all four candidates.
                    chosen_key = min(candidates, key=lambda k: (-candidates[k].covered, candidates[k].cost, k))
                    bac = candidates[chosen_key]
                    assert bac.cost <= budget
                    assert bac.covered >= candidates['v2'].covered
                    assert bac.covered >= candidates['density'].covered
                    assert bac.covered == len(bac.people)
                    rows.append({
                        'n': n, 'scenario': scenario, 'seed': seed, 'budget_fraction': fraction,
                        'budget': budget, 'all_possible_people': len(all_people),
                        'v2_covered': candidates['v2'].covered, 'v2_spent': candidates['v2'].cost,
                        'density_covered': candidates['density'].covered, 'density_spent': candidates['density'].cost,
                        'bac_covered': bac.covered, 'bac_spent': bac.cost, 'bac_source': chosen_key,
                        'coverage_gain_vs_v2': bac.covered - candidates['v2'].covered,
                        'coverage_gain_vs_density': bac.covered - candidates['density'].covered,
                        'savings_vs_v2_on_equal_coverage': (candidates['v2'].cost - bac.cost) if bac.covered == candidates['v2'].covered else '',
                        'savings_vs_density_on_equal_coverage': (candidates['density'].cost - bac.cost) if bac.covered == candidates['density'].covered else '',
                        'v2_ms': round(timings['v2'], 4), 'density_ms': round(timings['density'], 4),
                        'bac_total_ms': round(sum(timings.values()), 4),
                    })
        print(f'Finished {n} activities: {len(rows)} scenarios')
    target = Path('results')
    target.mkdir(exist_ok=True)
    out = target / 'phase9_raw.csv'
    with out.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    summary = []
    for n in SIZES:
        r = [x for x in rows if x['n'] == n]
        summary.append({
            'n': n, 'instances': len(r),
            'bac_better_coverage_vs_v2': sum(x['coverage_gain_vs_v2'] > 0 for x in r),
            'bac_equal_coverage_vs_v2': sum(x['coverage_gain_vs_v2'] == 0 for x in r),
            'bac_better_coverage_vs_density': sum(x['coverage_gain_vs_density'] > 0 for x in r),
            'bac_equal_coverage_vs_density': sum(x['coverage_gain_vs_density'] == 0 for x in r),
            'bac_cheaper_same_coverage_vs_v2': sum(x['savings_vs_v2_on_equal_coverage'] != '' and x['savings_vs_v2_on_equal_coverage'] > 0 for x in r),
            'bac_cheaper_same_coverage_vs_density': sum(x['savings_vs_density_on_equal_coverage'] != '' and x['savings_vs_density_on_equal_coverage'] > 0 for x in r),
            'mean_bac_total_ms': round(statistics.mean(x['bac_total_ms'] for x in r), 4),
            'mean_v2_ms': round(statistics.mean(x['v2_ms'] for x in r), 4),
        })
    with (target / 'phase9_summary.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(summary[0]))
        writer.writeheader()
        writer.writerows(summary)
    print(f'Completed {len(rows)} matched instances. Saved {out} and {target / "phase9_summary.csv"}')
    print('Note: BAC here is a four-candidate selector; its runtime includes computing all four candidates.')


if __name__ == '__main__':
    run()
