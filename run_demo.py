import argparse
from communityreach import read_activities,greedy,paper_inspired,exact
p=argparse.ArgumentParser(description='CommunityReach allocation demonstration')
p.add_argument('--csv',default='data/sample_activities.csv')
p.add_argument('--budget',type=int,default=1000)
a=p.parse_args(); items=read_activities(a.csv)
for result in [paper_inspired(items,a.budget),greedy(items,a.budget,'density'),greedy(items,a.budget,'gain'),exact(items,a.budget)]:
 print(f'{result.algorithm}: people={result.covered}, cost={result.cost}, selected={list(result.chosen)}')
