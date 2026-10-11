"""Budgeted maximum coverage algorithms. Activities have positive integer cost and beneficiary IDs.

The paper-inspired method implements the two branches described in Du, Li & Wang
(2024), Section 2: best affordable subset of size <=2 versus affordable
marginal-coverage-per-cost greedy. The journal's exact figure-level pseudocode
has not been independently verified; do not claim a formal reproduction without
checking the original Algorithm 1 figure and proof assumptions.
"""
from dataclasses import dataclass
from itertools import combinations
from typing import Iterable

@dataclass(frozen=True)
class Activity:
    name: str
    cost: int
    people: frozenset[str]

@dataclass
class Result:
    algorithm: str
    chosen: tuple[str, ...]
    cost: int
    covered: int
    people: frozenset[str]
    trace: list[dict]


def validate(items: list[Activity], budget: int) -> None:
    if not isinstance(budget,int) or isinstance(budget,bool) or budget < 0:
        raise ValueError('Budget must be a nonnegative integer')
    names=[a.name for a in items]
    if len(set(names))!=len(names): raise ValueError('Activity names must be unique')
    if any(not isinstance(a.cost,int) or isinstance(a.cost,bool) or a.cost<=0 for a in items):
        raise ValueError('All activity costs must be positive integers')


def _result(label, selection, trace):
    people=frozenset().union(*(a.people for a in selection)) if selection else frozenset()
    return Result(label,tuple(a.name for a in selection),sum(a.cost for a in selection),len(people),people,trace)


def greedy(items: list[Activity], budget: int, mode='density') -> Result:
    validate(items,budget)
    if mode not in ('density','gain','cheapest'):raise ValueError('Unknown greedy mode')
    remaining=list(items); chosen=[]; covered=set(); spent=0; trace=[]
    while True:
        feasible=[a for a in remaining if a.cost+spent <= budget]
        if not feasible:break
        def score(a):
            gain=len(a.people-covered)
            if mode=='density':return (gain/a.cost,gain,-a.cost,a.name)
            if mode=='gain':return (gain,-a.cost,a.name)
            return (-a.cost,gain,a.name)
        a=max(feasible,key=score)
        gain=len(a.people-covered)
        if gain==0:break
        chosen.append(a);remaining.remove(a);covered.update(a.people);spent+=a.cost
        trace.append({'activity':a.name,'cost':a.cost,'new_people':gain,'cumulative_covered':len(covered),'budget_used':spent})
    return _result('Greedy '+mode,chosen,trace)


def best_pair(items,budget):
    best=[]; best_val=-1;best_cost=0
    for size in (0,1,2):
        for sub in combinations(items,size):
            cost=sum(a.cost for a in sub)
            if cost>budget:continue
            cov=len(set().union(*(a.people for a in sub))) if sub else 0
            if (cov>best_val or (cov==best_val and cost<best_cost)):
                best=list(sub); best_val=cov;best_cost=cost
    return _result('Best <=2',best,[])


def paper_inspired(items,budget):
    validate(items,budget)
    a=best_pair(items,budget)
    b=greedy(items,budget,'density')
    winner=a if a.covered>b.covered else b
    return Result('Du et al. (2024) two-branch method (text-level reconstruction)', winner.chosen,winner.cost,winner.covered,winner.people,
                  [{'branch':'best_at_most_two','covered':a.covered,'chosen':a.chosen},
                   {'branch':'density_greedy','covered':b.covered,'chosen':b.chosen}]+winner.trace)


def exact(items,budget,max_n=22):
    validate(items,budget)
    if len(items)>max_n: raise ValueError(f'Exact optimizer restricted to <= {max_n} activities')
    best=[];best_people=set(); best_cost=0
    # Recursive exact search, suitable only for small n
    def dfs(i, chosen, spent, people):
        nonlocal best,best_people,best_cost
        if i==len(items):
            if len(people)>len(best_people) or (len(people)==len(best_people) and spent<best_cost):
                best=chosen[:];best_people=people.copy();best_cost=spent
            return
        dfs(i+1,chosen,spent,people)
        a=items[i]
        if spent+a.cost<=budget:dfs(i+1,chosen+[a],spent+a.cost,people|set(a.people))
    dfs(0,[],0,set())
    return _result('Exact exhaustive',best,[])
