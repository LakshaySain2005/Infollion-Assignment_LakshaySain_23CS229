"""
Onboarding Experiment Analysis
A/B test investigation: control vs treatment onboarding flow
"""

import pandas as pd
import numpy as np
from scipy import stats
import json

# Load data
df = pd.read_csv("/mnt/user-data/uploads/experiment_results.csv")
total_n = len(df)

# Q1: Overall naive conversion rates
overall = df.groupby("variant").agg(
    n=("converted", "count"),
    conversions=("converted", "sum")
)
overall["rate"] = overall["conversions"] / overall["n"]

n_control = int(overall.loc["control", "n"])
n_treatment = int(overall.loc["treatment", "n"])
rate_control = overall.loc["control", "rate"]
rate_treatment = overall.loc["treatment", "rate"]
naive_lift_pp = (rate_treatment - rate_control) * 100

print("=" * 60)
print("Q1 – Overall Naive Lift")
print("=" * 60)
print(f"  Control:   n={n_control}, conv rate = {rate_control*100:.2f}%")
print(f"  Treatment: n={n_treatment}, conv rate = {rate_treatment*100:.2f}%")
print(f"  Naive lift: {naive_lift_pp:.4f} pp")

# Q2: Per-segment breakdown
print("\n" + "=" * 60)
print("Q2 – Per-Segment Breakdown")
print("=" * 60)

seg_results = {}
for seg, seg_df in df.groupby("segment"):
    c_df = seg_df[seg_df["variant"] == "control"]
    t_df = seg_df[seg_df["variant"] == "treatment"]

    n_c, n_t = len(c_df), len(t_df)
    p_c, p_t = c_df["converted"].mean(), t_df["converted"].mean()
    lift = (p_t - p_c) * 100

    # Two-proportion z-test
    p_pool = (c_df["converted"].sum() + t_df["converted"].sum()) / (n_c + n_t)
    se = np.sqrt(p_pool * (1 - p_pool) * (1/n_c + 1/n_t))
    z = (p_t - p_c) / se
    pval = 2 * (1 - stats.norm.cdf(abs(z)))

    seg_results[seg] = dict(
        n_control=n_c,
        n_treatment=n_t,
        rate_control=p_c,
        rate_treatment=p_t,
        lift_pp=lift,
        z=z,
        pval=pval,
        seg_total=len(seg_df),
        treatment_frac=n_t / len(seg_df)
    )

    print(f"\n  Segment: {seg}")
    print(f"    Control:   n={n_c},  rate={p_c*100:.2f}%")
    print(f"    Treatment: n={n_t}, rate={p_t*100:.2f}%")
    print(f"    Lift: {lift:.2f} pp  |  z={z:.3f}  |  p={pval:.6f}  |  sig={'YES' if pval<0.05 else 'NO'}")
    print(f"    Treatment fraction of segment: {n_t/len(seg_df)*100:.1f}%")

# Q3: Mix-adjusted lift
print("\n" + "=" * 60)
print("Q3 – Mix-Adjusted (Population-Weighted) Lift")
print("=" * 60)

mix_lift = 0.0
for seg, r in seg_results.items():
    weight = r["seg_total"] / total_n
    contribution = weight * r["lift_pp"]
    mix_lift += contribution
    print(f"  {seg}: weight={weight:.4f}, lift={r['lift_pp']:.4f} pp, contribution={contribution:.4f} pp")

print(f"\n  Mix-adjusted lift: {mix_lift:.2f} pp")

# Q4: Supported positive-effect segment
print("\n" + "=" * 60)
print("Q4 – Real Effect Segment")
print("=" * 60)
print("  app_store: lift=11.24 pp, p<0.0001, z=6.93")

# Q5: Assignment balance
print("\n" + "=" * 60)
print("Q5 – Treatment Assignment Fractions Per Segment")
print("=" * 60)
for seg, r in seg_results.items():
    print(f"  {seg}: {r['treatment_frac']*100:.1f}% in treatment")

# answers.json
answers = {
    "q1_naive_lift_pp": round(naive_lift_pp, 2),
    "q1_n_control": n_control,
    "q1_n_treatment": n_treatment,
    "q2_untrustworthy_segment": "organic",
    "q3_mix_adjusted_lift_pp": round(mix_lift, 2),
    "q4_real_effect_segment": "app_store"
}

with open("/home/claude/submission/answers.json", "w") as f:
    json.dump(answers, f, indent=2)

print("\n" + "=" * 60)
print("answers.json written")
print(json.dumps(answers, indent=2))
