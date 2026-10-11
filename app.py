"""CommunityReach user-facing comparison dashboard (pre-proposal prototype)."""
import io
import time

import pandas as pd
import streamlit as st

from communityreach import read_activities, greedy, paper_inspired, exact
from communityreach.paper_v2 import paper_algorithm_1
from communityreach.budget_aware import budget_aware

st.set_page_config(page_title="CommunityReach", page_icon="ðŸŒ±", layout="wide")
st.title("CommunityReach")
st.caption("Budgeted maximum coverage â€” research and application prototype")
st.write("Choose activities to maximize **unique beneficiaries** without exceeding a budget. Upload your data or use the sample dataset.")

uploaded = st.file_uploader(
    "Upload CSV (columns: name, cost, beneficiaries; beneficiary IDs separated by semicolons)",
    type=["csv"],
)
source = io.StringIO(uploaded.getvalue().decode("utf-8-sig")) if uploaded is not None else "data/sample_activities.csv"
if uploaded is None:
    st.info("Using synthetic sample data. These are not real student or organization records.")

try:
    activities = read_activities(source)
    st.write(f"Loaded **{len(activities):,} activities**.")
    budget = st.number_input("Available budget", min_value=0, value=1000, step=50)
    with st.expander("View activities", expanded=len(activities) <= 30):
        st.dataframe(
            pd.DataFrame([
                {"Activity": a.name, "Cost": a.cost, "Beneficiary count": len(a.people)}
                for a in activities
            ]),
            hide_index=True,
            width='stretch',
        )

    if len(activities) > 1000:
        st.warning("Large datasets may take significant time: the current Python algorithms repeatedly evaluate beneficiary sets. Start with 40â€“300 activities for interactive use.")
    if st.button("Optimize budget", type="primary"):
        algorithms = [
            ("Paper Algorithm 1 (V2)", paper_algorithm_1),
            ("Budget-Aware CommunityReach", budget_aware),
            ("Original prototype (V1)", paper_inspired),
            ("Greedy density", lambda data, b: greedy(data, b, "density")),
            ("Greedy gain", lambda data, b: greedy(data, b, "gain")),
        ]
        if len(activities) <= 20:
            algorithms.append(("Exact exhaustive", lambda data, b: exact(data, b, max_n=20)))

        results = []
        records = []
        for label, algorithm in algorithms:
            start = time.perf_counter()
            result = algorithm(activities, int(budget))
            elapsed_ms = (time.perf_counter() - start) * 1000
            if result.cost > budget:
                raise AssertionError(f"{label} returned an over-budget selection")
            results.append((label, result))
            records.append({
                "Algorithm": label,
                "Covered people": result.covered,
                "Spent": result.cost,
                "Remaining": int(budget) - result.cost,
                "Activities selected": len(result.chosen),
                "Runtime (ms)": round(elapsed_ms, 3),
                "Selected projects": "; ".join(result.chosen),
            })

        df = pd.DataFrame(records)
        st.caption("Runtime timings are single-run measurements. BAC runs all four candidate methods; its timing includes that additional work.")
        st.subheader("Comparison")
        st.dataframe(df, hide_index=True, width='stretch')
        metric1, metric2, metric3 = st.columns(3)
        v2 = results[0][1]
        metric1.metric("V2 coverage", f"{v2.covered:,}")
        metric2.metric("V2 budget spent", f"{v2.cost:,} / {int(budget):,}")
        metric3.metric("V2 remaining budget", f"{int(budget) - v2.cost:,}")
        st.bar_chart(df.set_index("Algorithm")["Covered people"])
        bac = results[1][1]
        st.subheader("Budget-aware result")
        st.write(f"**{bac.covered} beneficiaries**, **{bac.cost} spent**; "
                 f"savings vs V2: **{v2.cost - bac.cost}** when coverage is at least V2.")
        st.write("Chosen activities:", ", ".join(bac.chosen) or "None")
        with st.expander("Budget-aware candidate comparison"):
            st.json(bac.trace)
        st.subheader("Research algorithm decision")
        st.write("Selected activities:", ", ".join(v2.chosen) if v2.chosen else "None")
        st.caption("V2 follows the selection and rejection order of Algorithm 1 in Du, Li & Wang (2024). Ties depend on input order.")
        with st.expander("Decision trace"):
            st.json(v2.trace)
        st.download_button(
            "Export comparison CSV",
            data=df.to_csv(index=False).encode("utf-8-sig"),
            file_name="communityreach_v2_comparison.csv",
            mime="text/csv",
        )
        st.warning("Research prototype only. Budget-aware selection compares existing candidates; it is not a new approximation algorithm. Timings are single-run measurements.")
except Exception as exc:
    st.error(f"Input or processing error: {exc}")

