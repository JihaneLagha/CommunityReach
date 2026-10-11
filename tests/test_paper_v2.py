import random
import unittest
from communityreach.core import Activity, exact, paper_inspired
from communityreach.paper_v2 import paper_algorithm_1

class PaperV2Tests(unittest.TestCase):
    def test_paper_branch_and_budget(self):
        items = [Activity('A', 3, frozenset({'a', 'b'})),
                 Activity('B', 2, frozenset({'b', 'c'})),
                 Activity('C', 2, frozenset({'d'}))]
        result = paper_algorithm_1(items, 4)
        self.assertLessEqual(result.cost, 4)
        self.assertEqual(result.covered, len(result.people))
        self.assertEqual(result.covered, 3)

    def test_random_validity_and_exact_upper_bound(self):
        for seed in range(30):
            rng = random.Random(seed)
            items = [Activity('P'+str(i), rng.randint(1, 12),
                              frozenset(str(x) for x in rng.sample(range(25), rng.randint(1, 7))))
                     for i in range(9)]
            budget = 15
            result = paper_algorithm_1(items, budget)
            optimum = exact(items, budget)
            self.assertLessEqual(result.cost, budget)
            self.assertLessEqual(result.covered, optimum.covered)
            names = set(result.chosen)
            selected = [a for a in items if a.name in names]
            self.assertEqual(set(result.people), set().union(*(a.people for a in selected)))

    def test_comparison_with_v1_is_not_assumed_equal(self):
        items = [Activity('Large', 9, frozenset({'a','b','c'})),
                 Activity('Small1', 3, frozenset({'d','e'})),
                 Activity('Small2', 3, frozenset({'f','g'}))]
        for algorithm in (paper_algorithm_1, paper_inspired):
            self.assertLessEqual(algorithm(items, 6).cost, 6)

if __name__ == '__main__':
    unittest.main()
