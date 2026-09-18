# Onboarding Experiment Investigation

A/B test analysis of a new onboarding flow rolled out to a random subset of new users.

## Files

- `ANSWERS.md` — Full written investigation
- `answers.json` — Machine-readable answers
- `analysis.py` — Python analysis script

## Key Findings

- Naive overall lift: +6.61 pp
- Mix-adjusted lift: +1.63 pp
- Segment with a statistically significant positive effect: `app_store` (+11.24 pp, p < 0.0001)
- Assignment imbalance: `organic` was 69% treatment and `paid_search` was 30%

## How to Run

```bash
pip install pandas scipy
python3 analysis.py
```
