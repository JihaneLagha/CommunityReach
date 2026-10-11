import unittest,random
from communityreach import Activity,greedy,paper_inspired,exact,best_pair
class CoverageTests(unittest.TestCase):
 def test_zero_budget(self):
  items=[Activity('a',1,frozenset({'x'}))]
  for alg in (paper_inspired,greedy,exact):self.assertEqual(alg(items,0).covered,0)
 def test_overlap_counts_once(self):
  items=[Activity('a',2,frozenset({'x','y'})),Activity('b',3,frozenset({'x','z'}))]
  self.assertEqual(exact(items,5).covered,3)
 def test_pair_branch(self):
  items=[Activity('a',3,frozenset({'a'})),Activity('b',3,frozenset({'b'})),Activity('c',6,frozenset({'a','b','c'}))]
  self.assertEqual(best_pair(items,6).covered,3)
 def test_random_constraints_against_exact(self):
  rng=random.Random(42)
  for t in range(150):
   n=rng.randint(1,10); universe=[f'p{i}' for i in range(20)]
   items=[Activity(f'a{i}',rng.randint(1,12),frozenset(rng.sample(universe,rng.randint(1,9)))) for i in range(n)]
   b=rng.randint(0,30); optimum=exact(items,b)
   for alg in (greedy,paper_inspired):
    out=alg(items,b)
    self.assertLessEqual(out.cost,b)
    self.assertEqual(out.covered,len(out.people))
    self.assertLessEqual(out.covered,optimum.covered)
    self.assertEqual(out.covered,len(set().union(*(a.people for a in items if a.name in out.chosen))))
   self.assertGreaterEqual(paper_inspired(items,b).covered,greedy(items,b).covered)
 def test_bad_data(self):
  with self.assertRaises(ValueError):exact([Activity('a',0,frozenset())],1)
  with self.assertRaises(ValueError):exact([Activity('a',1,frozenset()),Activity('a',1,frozenset())],2)
if __name__=='__main__': unittest.main()
