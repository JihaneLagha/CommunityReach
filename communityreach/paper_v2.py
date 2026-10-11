"""Literal specialization of Du, Li & Wang (2024), Algorithm 1, to budgeted coverage.

The marginal-value oracle is the cardinality of newly covered beneficiary IDs.
Paper lines 8-14 select the globally highest-density remaining item BEFORE
checking its affordability; unaffordable items are discarded rather than
filtered out before selection.
"""
from itertools import combinations
from .core import Result, _result, validate


def paper_algorithm_1(items, budget):
    """Return the paper's two-branch Algorithm 1 (coverage objective)."""
    validate(items, budget)

    # S1: best affordable subset of cardinality at most two (paper lines 3-7).
    s1 = []
    best_value = 0
    for size in (1, 2):
        for subset in combinations(items, size):
            if sum(a.cost for a in subset) > budget:
                continue
            value = len(set().union(*(a.people for a in subset)))
            if value > best_value:  # paper uses strict improvement
                s1, best_value = list(subset), value

    # S2: choose highest marginal gain / cost from ALL remaining items,
    # then accept only if within budget; remove in either case (lines 8-14).
    remaining = list(items)
    s2 = []
    covered = set()
    spent = 0
    trace = []
    while remaining:
        # Ratio comparison uses integer cross multiplication to avoid floating error.
        best_index = 0
        best_gain = len(remaining[0].people - covered)
        best_cost = remaining[0].cost
        for i in range(1, len(remaining)):
            candidate = remaining[i]
            gain = len(candidate.people - covered)
            if gain * best_cost > best_gain * candidate.cost:
                best_index, best_gain, best_cost = i, gain, candidate.cost
        choice = remaining.pop(best_index)
        if spent + choice.cost <= budget:
            gain = len(choice.people - covered)
            covered.update(choice.people)
            spent += choice.cost
            s2.append(choice)
            trace.append({'activity': choice.name, 'cost': choice.cost,
                          'new_people': gain, 'cumulative_covered': len(covered),
                          'budget_used': spent})

    # Paper lines 15-20: choose S1 when equal.
    r1 = _result('Paper Algorithm 1: pair branch', s1, [])
    r2 = _result('Paper Algorithm 1: density branch', s2, trace)
    winner = r1 if r1.covered >= r2.covered else r2
    return Result('Du et al. (2024) Algorithm 1 — literal implementation',
                  winner.chosen, winner.cost, winner.covered, winner.people,
                  [{'branch': 'best_at_most_two', 'covered': r1.covered,
                    'chosen': r1.chosen},
                   {'branch': 'paper_density', 'covered': r2.covered,
                    'chosen': r2.chosen}] + winner.trace)
