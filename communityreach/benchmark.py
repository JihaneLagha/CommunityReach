import csv,random,time,tracemalloc
from .core import Activity,paper_inspired,greedy,exact

def random_instance(n,seed,universe=400):
    rng=random.Random(seed)
    return [Activity(f'P{i:04d}',rng.randint(10,100),frozenset(f'B{j}' for j in rng.sample(range(universe),rng.randint(8,35)))) for i in range(n)]

def execute():
    rows=[]
    for n in (10,30,100,300,1000):
        for seed in range(3):
            items=random_instance(n,seed,universe=max(400,n*20))
            budget=round(n*12)
            for name,alg in [('paper_inspired',paper_inspired),('density',lambda x,y:greedy(x,y,'density')),('gain',lambda x,y:greedy(x,y,'gain'))]+([('exact',exact)] if n<=10 else []):
                tracemalloc.start(); t0=time.perf_counter(); out=alg(items,budget); elapsed=time.perf_counter()-t0
                _,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
                rows.append(dict(n=n,seed=seed,algorithm=name,covered=out.covered,cost=out.cost,budget=budget,elapsed_s=round(elapsed,6),peak_kib=round(peak/1024,1)))
    return rows

if __name__=='__main__':
    import os
    rows=execute();os.makedirs('results',exist_ok=True)
    with open('results/benchmark.csv','w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
    print(f'Wrote {len(rows)} benchmark rows to results/benchmark.csv')
