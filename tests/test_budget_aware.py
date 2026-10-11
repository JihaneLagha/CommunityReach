import random
import unittest

from communityreach.core import Activity, exact, greedy
from communityreach.paper_v2 import paper_algorithm_1
from communityreach.budget_aware import budget_aware


class BudgetAwareTests(unittest.TestCase):
    def test_known_example_never_worse_than_v2(self):
        items = [
            Activity('A', 90, frozenset({'a','b','c'})),
            Activity('B', 40, frozenset({'a','d'})),
            Activity('C', 40, frozenset({'b','e'})),
            Activity('D', 20, frozenset({'f'})),
        ]
        for budget in (0, 20, 40, 80, 100, 200):
            v2 = paper_algorithm_1(items, budget)
            bac = budget_aware(items, budget)
            self.assertLessEqual(bac.cost, budget)
            self.assertGreaterEqual(bac.covered, v2.covered)
            if bac.covered == v2.covered:
                self.assertLessEqual(bac.cost, v2.cost)

    def test_random_feasibility_and_objective(self):
        for seed in range(30):
            rng = random.Random(seed)
            universe = [f'B{i}' for i in range(20)]
            items = [Activity(f'A{i}', rng.randint(1, 30),
                              frozenset(rng.sample(universe, rng.randint(0, 8))))
                     for i in range(9)]
            budget = rng.randint(0, 75)
            bac = budget_aware(items, budget)
            v2 = paper_algorithm_1(items, budget)
            optimum = exact(items, budget)
            by_name = {a.name: a for a in items}
            selected = [by_name[name] for name in bac.chosen]
            self.assertEqual(bac.cost, sum(a.cost for a in selected))
            self.assertEqual(bac.covered, len(set().union(*(a.people for a in selected))))
            self.assertLessEqual(bac.cost, budget)
            self.assertLessEqual(bac.covered, optimum.covered)
            self.assertGreaterEqual(bac.covered, v2.covered)
            if bac.covered == v2.covered:
                self.assertLessEqual(bac.cost, v2.cost)


if __name__ == '__main__':
    unittest.main()
