# CommunityReach Phase 10 — Humanitarian Aid Case Study

**DATA STATUS: ENTIRELY SYNTHETIC — NOT REAL AID-RECIPIENT DATA.**

This case is an illustrative planning exercise, not an empirical evaluation of a humanitarian organization. Names, regions, budgets, activity costs, beneficiary eligibility, and IDs are invented. No actual Lebanese household, actual aid delivery outcome, vendor quote, or organizational operating cost is represented.

## Scenario

A hypothetical humanitarian coalition must choose from **40 aid activities** (eight types in each of five fictional districts) to reach as many **unique eligible households** as possible under an activity budget. Each `H####` is a *synthetic household identifier*. **Do not call them individual people in the report**, even though the current Streamlit UI uses the generic label `people`.

The columns match the existing `communityreach.io.read_activities` parser precisely:

- `name` — unique activity name
- `cost` — synthetic budget units per activity (not real USD or verified quotes)
- `beneficiaries` — semicolon-delimited synthetic household IDs

Some households are eligible for multiple services. This creates real overlap within the constructed example; the optimizer counts each household only once, even if multiple activities serve it. The model assumes fixed activity costs, indivisible activities, and known eligible household lists.

## Data characteristics

- Activities: **40**
- Unique synthetic households eligible across all activities: **516**
- Total cost of funding every activity: **20,420 budget units**
- Synthetic districts: North District, Coastal District, Central District, Hill District, Rural District
- No identifying or confidential data
- Generation seed: `6412026`

## Suggested budget tests (all in synthetic budget units)

- **3,500** — restrictive
- **6,500** — intermediate
- **10,000** — larger

Use the same uploaded CSV for each budget; click Optimize budget after changing the value. Export a separate comparison CSV after each test. Note the selected activities, coverage, spending, and timings. Run each scenario more than once before drawing conclusions about runtime; UI timing is not a controlled benchmark.

`reference_results.csv` contains results from this dataset, calculated against the local prototype's algorithms in this environment. These results are a reproducibility check, **not a real-world result**. Results may differ if your project files were modified.

## Interpretation caution

The objective is **maximum distinct eligible households covered**, not medical benefit, fairness, urgency, health outcomes, geographic equity, or delivery feasibility. Counting each household once can undervalue second services to the same household. Real humanitarian planning requires validated cost and eligibility inputs, vulnerability priorities, consent/privacy controls, and operational constraints; these are **not represented**. No claim is made that the tool should make real aid-allocation decisions without expert review.

## Evidence still required for a strong Track C proposal

1. Faithful primary paper Algorithm 1 implementation and a proof overview marking which arguments were independently checked.
2. Small exact-optimum tests, budget-feasibility and reproducibility tests, and nontrivial overlapping-beneficiary cases.
3. Benchmarks against manual/spreadsheet or simple greedy processes using the *same* instances; runtime, memory, solution quality, and failure cases.
4. Explain the app's end-user workflow and demonstrate import, optimization, exports, error handling, and scaling limits.
5. A credible data-acquisition plan for a real nonprofit or a transparent statement that real data are unavailable; **do not represent synthetic data as real**.
6. Honest originality statement: BAC is a selector of existing candidates rather than a novel approximation algorithm.
7. One-page proposal with problem, 2024 paper, Track C, risk, baseline, data source, expected user, and success metrics; course instructor must approve the paper and topic.
