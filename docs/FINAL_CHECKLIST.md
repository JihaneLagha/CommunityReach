# Code freeze checklist (CMPS641)

- [ ] Run `python run_all_checks.py` on Windows (with the virtual environment activated or with `.venv\Scripts\python.exe`).
- [ ] Launch `python -m streamlit run app.py`; upload `data/humanitarian_aid_40_activities.csv` and run budgets 3500, 6500, 10000.
- [ ] Confirm CSV export downloads and opens correctly; verify coverage and costs against `run_all_checks.py`.
- [ ] Test zero budget, budget smaller than all costs, missing CSV fields, duplicate names, and malformed entries.
- [ ] Run `python run_phase7.py` and `python run_phase9.py` if you need fresh machine-specific figures; archive console output and record Python version, OS and CPU/RAM.
- [ ] Independently walk through original paper Algorithm 1, Theorem 2.4 and proof; distinguish oracle complexity from actual set operation costs.
- [ ] Explain BAC as a candidate-selector with no new published approximation guarantee.
- [ ] Record known limitations: synthetic data; no real humanitarian outcomes; coverage only; no urgency/fairness/logistics model.
- [ ] Before GitHub push: exclude `.venv`, `__pycache__`, confidential data, backups; check git status and `git diff --cached`.
- [ ] Validate repository installation from a clean folder on a second machine if possible.
- [ ] Freeze the version with a Git tag only after all checks pass.

**Code freeze = tests and UI verified on your Windows machine, no unresolved correctness bugs, and reproducibility instructions checked.** The professor's proposal and report should follow that freeze.
