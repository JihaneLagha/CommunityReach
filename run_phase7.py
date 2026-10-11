"""CommunityReach Phase 7: reproducible comparative experiments.
Run from CommunityReach_Project root: python run_phase7.py
No existing project files are overwritten except results/phase7_*.csv.
"""
import csv
import random
import statistics
import time
import tracemalloc
from pathlib import Path

from communityreach.core import Activity, greedy, paper_inspired, exact
from communityreach.paper_v2 import paper_algorithm_1

SIZES = (10, 30, 100, 300)  # Increase only after reviewing timing
SEEDS = (0, 1, 2, 3, 4)
PATTERNS = ('low_overlap', 'high_overlap', 'unequal_costs')
BUDGET_FRACTIONS = (0.10, 0.25)


def make_items(n, seed, pattern):
    rng = random.Random(100000 * seed + n)
    universe_size = max(80, n * (30 if pattern == 'low_overlap' else 3))
    universe = [f'person_{i}' for i in range(universe_size)]
    items = []
    for i in range(n):
        cost = (rng.choice((10, 12, 15, 25, 50, 100, 250))
                if pattern == 'unequal_costs' else rng.randint(20, 100))
        count = rng.randint(5, 20)
        # A high-overlap universe increases repeated beneficiaries.
        people = frozenset(rng.sample(universe, min(count, universe_size)))
        items.append(Activity(f'activity_{i:05d}', cost, people))
    return items


def measured(call, items, budget):
    tracemalloc.start()
    begin = time.perf_counter()
    try:
        output = call(items, budget)
    finally:
        elapsed = (time.perf_counter() - begin) * 1000
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
    assert output.cost <= budget, f'{output.algorithm} exceeded budget'
    names = set(output.chosen)
    assert len(names) == len(output.chosen), 'duplicate selected projects'
    selected = [a for a in items if a.name in names]
    assert len(selected) == len(names), 'unknown selected project'
    assert sum(a.cost for a in selected) == output.cost, 'cost mismatch'
    assert len(set().union(*(a.people for a in selected))) == output.covered if selected else output.covered == 0, 'coverage mismatch'
    return output, elapsed, peak / 1024


def main():
    runs = []
    methods = [
        ('paper_v2', paper_algorithm_1),
        ('original_v1', paper_inspired),
        ('greedy_density', lambda items, budget: greedy(items, budget, 'density')),
        ('greedy_gain', lambda items, budget: greedy(items, budget, 'gain')),
    ]
    for n in SIZES:
        for pattern in PATTERNS:
            for seed in SEEDS:
                items = make_items(n, seed, pattern)
                total_cost = sum(a.cost for a in items)
                for fraction in BUDGET_FRACTIONS:
                    budget = max(1, round(total_cost * fraction))
                    # Exact optimum only for small, feasible instances.
                    sample_methods = methods + ([('exact', exact)] if n <= 10 else [])
                    outputs = {}
                    for name, method in sample_methods:
                        result, elapsed, peak = measured(method, items, budget)
                        outputs[name] = result
                        runs.append(dict(n=n, pattern=pattern, seed=seed,
                                         budget_fraction=fraction, budget=budget,
                                         algorithm=name, coverage=result.covered,
                                         spent=result.cost,
                                         remaining=budget-result.cost,
                                         selected=len(result.chosen),
                                         runtime_ms=round(elapsed, 4),
                                         peak_traced_kib=round(peak, 2)))
                    if 'exact' in outputs:
                        optimum = outputs['exact'].covered
                        assert all(r.covered <= optimum for r in outputs.values()), 'result exceeds exact optimum'
        print(f'Finished n={n}: {len(runs)} total rows', flush=True)

    target = Path('results')
    target.mkdir(exist_ok=True)
    raw = target / 'phase7_raw.csv'
    with raw.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=runs[0].keys())
        writer.writeheader()
        writer.writerows(runs)

    grouped = {}
    for r in runs:
        key = (r['n'], r['pattern'], r['budget_fraction'], r['algorithm'])
        grouped.setdefault(key, []).append(r)
    summary_rows = []
    for (n, pattern, fraction, algorithm), block in sorted(grouped.items()):
        summary_rows.append(dict(n=n, pattern=pattern, budget_fraction=fraction,
                                 algorithm=algorithm, runs=len(block),
                                 mean_coverage=round(statistics.mean(r['coverage'] for r in block), 3),
                                 mean_spent=round(statistics.mean(r['spent'] for r in block), 3),
                                 mean_runtime_ms=round(statistics.mean(r['runtime_ms'] for r in block), 3),
                                 median_runtime_ms=round(statistics.median(r['runtime_ms'] for r in block), 3),
                                 mean_peak_traced_kib=round(statistics.mean(r['peak_traced_kib'] for r in block), 3)))
    summary = target / 'phase7_summary.csv'
    with summary.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=summary_rows[0].keys())
        writer.writeheader()
        writer.writerows(summary_rows)
    print(f'Completed {len(runs)} benchmark runs.')
    print(f'Saved {raw} and {summary}')
    print('Note: measured runtime includes tracemalloc overhead; peak memory excludes input construction.')


if __name__ == '__main__':
    main()
