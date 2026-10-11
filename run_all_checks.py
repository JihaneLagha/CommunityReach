"""Run local correctness, dataset and reference checks with Python standard library."""
import subprocess
import sys
from communityreach.io import read_activities
from communityreach.paper_v2 import paper_algorithm_1
from communityreach.budget_aware import budget_aware


def main():
    tests = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v'])
    if tests.returncode:
        return tests.returncode
    items = read_activities('data/humanitarian_aid_40_activities.csv')
    assert len(items) == 40
    expected = {3500: (346, 3500), 6500: (440, 6450), 10000: (480, 9630)}
    for budget, (coverage, spent) in expected.items():
        v2 = paper_algorithm_1(items, budget)
        bac = budget_aware(items, budget)
        assert (v2.covered, v2.cost) == (coverage, spent), (budget, v2.covered, v2.cost)
        assert bac.covered >= v2.covered and bac.cost <= budget
        print(f'PASS budget={budget}: V2 coverage={v2.covered}, spent={v2.cost}; BAC={bac.covered}, {bac.cost}')
    print('All code and humanitarian reference checks passed.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
