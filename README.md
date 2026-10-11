# CommunityReach — CMPS641 Track C prototype

A reproducible Python/Streamlit decision-support prototype for **budgeted maximum coverage**: select aid/community activities to maximize the number of **unique eligible beneficiaries/households** within a budget.

## Getting started (Windows PowerShell)

```powershell
cd "$env:USERPROFILE\Desktop\CommunityReach_Project"
py -3.10 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe run_all_checks.py
.\.venv\Scripts\python.exe -m streamlit run app.py
```

If `py -3.10` is unavailable, use `python -m venv .venv` instead. Open http://localhost:8501 .

Upload `data/humanitarian_aid_40_activities.csv` and test budgets 3500, 6500, and 10000. CSV columns are `name,cost,beneficiaries`; quote beneficiary fields when needed, with IDs separated by semicolons. The dataset is **synthetic** and counts **households**, not verified aid recipients.

## Code layout

- `communityreach/core.py`: baseline greedy variants, exhaustive solver (small inputs), shared structures
- `communityreach/paper_v2.py`: literal coverage specialization of Algorithm 1 of Du, Li & Wang (2024)
- `communityreach/budget_aware.py`: BAC, a cost-based **selector among four existing candidates**, not a new approximation theorem
- `communityreach/io.py`: strict CSV parser
- `app.py`: Streamlit UI and comparison CSV export
- `tests/`: unit and input tests
- `run_all_checks.py`: complete test suite + reproducible case study reference check
- `run_phase7.py`, `run_phase9.py`: historical experiments; results retained under `results/`
- `data/`: example and synthetic case-study data

## Research and caveats

Paper: Du, H. W., Li, X., & Wang, G. (2024), *New approximations for monotone submodular maximization with knapsack constraint*, Journal of Combinatorial Optimization 48, article 28. DOI: https://doi.org/10.1007/s10878-024-01214-x .

Algorithm 1 gives a claimed approximation of `1 - exp(-2/3)` in its **monotone submodular value-oracle model**. Actual Python wall time includes cost of beneficiary-set operations. The proof and code still require independent oral defense; algorithm tests and reference results are not proof of the approximation bound. Tie-breaking here uses stable input order. `BAC` is a deterministic multi-candidate selector and may be slower than greedy because it runs several algorithms.

**Not for operational humanitarian allocation without validation.** This model counts coverage of eligible households only, not urgency, fairness, aid effectiveness, logistics, or beneficiary consent. Never upload identifiable beneficiary data to a public repository. The included CSVs and results are synthetic.

## Reproducing benchmarks

```powershell
.\.venv\Scripts\python.exe run_phase7.py
.\.venv\Scripts\python.exe run_phase9.py
```

See `docs/FINAL_CHECKLIST.md` for publication and pre-proposal checks. Benchmark runtime depends on hardware and installed Python version; store hardware/versions when reporting your own results.

## Citation and AI disclosure

Cite the primary paper and any reused code/datasets. The project was developed with AI assistance for brainstorming, scaffolding, debugging, and documentation; disclose that use in the CMPS641 appendix, verify every result, and be prepared to explain all algorithm code and proofs personally.
