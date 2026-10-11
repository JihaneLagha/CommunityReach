# CommunityReach — Preliminary feasibility assessment

**Date:** 11 October 2026  
**Course:** CMPS641 — Design & Analysis of Algorithms  
**Candidate track:** C — Applied Development  
**Decision:** PROMISING, but NOT YET READY to reserve the paper.

## What exists now

- Standalone Python optimization engine, CLI demonstration and a Streamlit UI source file.
- Data loader for CSV activities with costs and anonymized beneficiary IDs.
- Paper-inspired two-branch selection method, two greedy baselines, and an exact solver for small cases.
- Five automated test methods, including 150 reproducible random small-instance comparisons against exact solutions; all passed in this runtime.
- A reproducible benchmark script with 48 rows, covering 10–1,000 activities and three random seeds per size; all synthetic.
- A small synthetic university-services example and a synthetic example where selecting the best pair is beneficial.

## Observed demonstration (synthetic dataset)

With budget **1,000 units**, the tested sample data produced:

| Method | Unique people reached | Amount spent |
|---|---:|---:|
| Research-inspired two-branch method | 20 | 725 |
| Greedy marginal-gain/cost | 20 | 725 |
| Greedy highest marginal gain | 20 | 900 |
| Exact exhaustive optimum | 23 | 975 |

The main research-inspired implementation obtained 20/23 = **86.96% of the exact optimum** on this particular synthetic case. This is an *empirical observed ratio for one case*, not a verified approximation guarantee.

## Benchmark results

Each number below is the **mean of three deterministic-seed test instances**, recorded on the provided runner; durations vary by machine. Budgets scale with the activity count; the distinct beneficiary universe also scales to avoid saturating every beneficiary.

| Activities | Two-branch mean coverage | Density greedy mean coverage | Gain greedy mean coverage | Two-branch mean runtime |
|---:|---:|---:|---:|---:|
| 10 | 85.3 | 85.3 | 60.0 | 0.4 ms |
| 30 | 236.7 | 236.7 | 209.7 | 3.1 ms |
| 100 | 771.3 | 771.3 | 623.7 | 32.3 ms |
| 300 | 2347.3 | 2347.3 | 1893.0 | 301.6 ms |
| 1000 | 7895.7 | 7895.7 | 6344.0 | 3594.9 ms |

**Interpretation:** These random cases do not yet show an advantage over density greedy, although the two-branch method is guaranteed by construction in this implementation to do **at least as well as density greedy** because it explicitly takes the better branch. The extra best-pair search has runtime overhead. We need deliberately constructed challenging instances, better real datasets, and additional statistical seeds before making claims of meaningful practical improvement.

## Main risks BEFORE proposing to the professor

1. **Exact paper fidelity:** The source's descriptive text and theorem were checked, but the image containing Algorithm 1 has not been independently examined line by line. This implementation is *paper-inspired*, not yet verified as a faithful implementation of the figure.
2. **Approximation mathematics:** The published theorem claims `1 - exp(-2/3)` in `O(n^2)` value-oracle time. The published proof and possible assumptions must be checked carefully before claiming the bound for code.
3. **Real-world validation:** The current datasets are deliberately synthetic. Track C requires realistic data and comparison to manual/spreadsheet or existing practice. At minimum, obtain a real or publicly sourced activity/coverage dataset and a clear user story.
4. **Novelty:** Budgeted maximum coverage is a known problem. Novelty should be claimed in a specific user workflow/experimental evaluation, not as invention of the optimization algorithm.
5. **System test:** Streamlit is included as source but was **not launched in this execution environment** because Streamlit is not installed here. The pure-Python CLI, tests, and benchmarks ran.
6. **Complexity:** The paper's `O(n^2)` counts abstract value-oracle operations; real Python set operations also depend on beneficiary counts.

## Recommended next step

Open the original paper's Algorithm 1 diagram and verify the code line by line; analyze the proof, then trial the web UI locally with real-style inputs, expand test scenarios, and only then draft the one-page course proposal. No grade or publication outcome can be guaranteed.

**Original paper:** Du, H. W., Li, X., and Wang, G. (2024), *New approximations for monotone submodular maximization with knapsack constraint*, Journal of Combinatorial Optimization 48:28. https://doi.org/10.1007/s10878-024-01214-x
