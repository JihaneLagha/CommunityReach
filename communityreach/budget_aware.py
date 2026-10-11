"""Cost-aware selector over existing allocation algorithms.

This is an APPLICATION-LEVEL extension, not a new approximation theorem.
The V2 candidate is always included. Selection is lexicographic:
(1) maximize coverage, (2) minimize total cost, (3) deterministic candidate order.
"""
from .core import Result, greedy, paper_inspired, validate
from .paper_v2 import paper_algorithm_1


def budget_aware(items, budget):
    validate(items, budget)
    methods = [
        ('Paper Algorithm 1 (V2)', paper_algorithm_1),
        ('Original prototype (V1)', paper_inspired),
        ('Greedy density', lambda xs, b: greedy(xs, b, 'density')),
        ('Greedy gain', lambda xs, b: greedy(xs, b, 'gain')),
    ]
    candidates = [(label, method(items, budget)) for label, method in methods]
    for label, candidate in candidates:
        if candidate.cost > budget or candidate.cost < 0:
            raise AssertionError(f'{label}: infeasible solution')
    # min with -coverage means highest coverage first, then lowest cost.
    label, winner = min(candidates, key=lambda pair: (-pair[1].covered, pair[1].cost))
    trace = [{
        'candidate': name, 'covered': r.covered, 'cost': r.cost,
        'selected_count': len(r.chosen), 'winner': name == label
    } for name, r in candidates]
    return Result('Budget-Aware CommunityReach (candidate selector)',
                  winner.chosen, winner.cost, winner.covered, winner.people, trace)
