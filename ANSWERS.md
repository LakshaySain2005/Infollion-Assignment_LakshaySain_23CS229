# Onboarding Experiment — Investigation Report

## Investigation Process

- Loaded the CSV (14,000 rows, no nulls, clean data).
- Verified variant distribution overall and per segment before computing rates.
- Computed naive conversion rates for control and treatment.
- Broke down rates and sample sizes per segment to identify heterogeneity.
- Flagged severe treatment-assignment imbalance in organic (69%) and paid_search (30%).
- Ran a two-proportion z-test for each segment.
- Computed the mix-adjusted population-weighted overall lift.
- Compared naive vs. mix-adjusted lift to identify the Simpson's Paradox mechanism.
- Confirmed app_store as the only segment with a statistically significant large positive effect.
- Checked influencer separately; its negative lift was not significant.
- Confirmed referral shows +2.81 pp but does not cross p < 0.05.

---

## Q1 — Overall Naive Lift

| Variant | n | Conversion Rate |
|---|---:|---:|
| Control | 7,136 | 19.82% |
| Treatment | 6,864 | 26.43% |

**Naive lift: +6.61 percentage points**

Computed as treatment conversion rate minus control conversion rate: 26.43% − 19.82% = 6.61 pp.

---

## Q2 — Per-Segment Breakdown

| Segment | Control n | Control Rate | Treatment n | Treatment Rate | Lift (pp) | p-value | Significant? |
|---|---:|---:|---:|---:|---:|---:|---|
| app_store | 925 | 8.76% | 960 | 20.00% | +11.24 | < 0.0001 | YES |
| influencer | 119 | 23.53% | 131 | 16.79% | −6.74 | 0.184 | NO |
| organic | 1,298 | 35.29% | 2,917 | 35.07% | −0.21 | 0.893 | NO |
| paid_search | 3,353 | 15.18% | 1,459 | 14.39% | −0.79 | 0.482 | NO |
| referral | 1,441 | 23.46% | 1,397 | 26.27% | +2.81 | 0.083 | NO |

**Untrustworthy segment: organic**

The organic segment has a severe assignment imbalance: 69.2% of organic users were assigned to treatment versus 30.8% to control. This indicates a systematic issue in variant assignment, so the organic control group is not a reliable counterfactual for the treatment group. The observed lift of −0.21 pp is near zero, but the assignment imbalance makes causal conclusions from this segment unreliable.

---

## Q3 — Mix-Adjusted Overall Lift

**Mix-adjusted lift: +1.63 percentage points**

For each segment, the treatment-vs-control lift was weighted by that segment's share of the total user population.

| Segment | Population weight | Segment lift (pp) | Weighted contribution (pp) |
|---|---:|---:|---:|
| app_store | 13.46% | +11.24 | +1.51 |
| influencer | 1.79% | −6.74 | −0.12 |
| organic | 30.11% | −0.21 | −0.06 |
| paid_search | 34.37% | −0.79 | −0.27 |
| referral | 20.27% | +2.81 | +0.57 |
| **Total** | **100%** | — | **+1.63** |

The difference from the naive +6.61 pp is driven by treatment-assignment imbalance. High-converting segments were over-represented in treatment while lower-converting segments were under-represented, inflating the naive aggregate comparison. The mix-adjusted calculation accounts for the actual population mix.

---

## Q4 — Segment With a Real, Meaningful Positive Effect

**Segment: app_store**

Evidence:
- Lift of +11.24 percentage points (8.76% → 20.00%).
- z-score = 6.93.
- p-value < 0.0001.
- Sample sizes are substantial: 925 control and 960 treatment.
- Assignment is approximately balanced at 50/50.

Referral has a +2.81 pp lift but p = 0.08. Influencer has a negative, non-significant result. Organic and paid_search show near-zero lifts.

---

## Q5 (Bonus) — Assignment Imbalance

| Segment | % in Treatment |
|---|---:|
| app_store | 50.9% |
| influencer | 52.4% |
| organic | **69.2%** |
| paid_search | **30.3%** |
| referral | 49.2% |

Organic is 69% treatment and paid_search is 30% treatment, large deviations from an approximately 50/50 split.

A plausible explanation is that randomisation was not performed within segments and variant assignment may have depended on time, batches, or a variable correlated with acquisition channel. This means the naive overall lift is affected by selection bias rather than being a clean causal estimate.
