"""Conformal alert-tier experiment on WSIB quarterly private equity data.

Quarterly fund return:
    r_t = (MV_t - MV_{t-1} - C_q + D_q) / (MV_{t-1} + 0.5 C_q - 0.5 D_q)   (Modified Dietz)
Market factor: same-quarter median return within strategy group.
Residual e = r - median. Nonconformity score = |e|.
Tiers from nested split-conformal quantiles at 80 / 95 / 99 %.
"""
import glob
import json
import math
import os
import sys

import numpy as np
import pandas as pd

CSV_DIR, OUT_DIR = sys.argv[1], sys.argv[2]
os.makedirs(OUT_DIR, exist_ok=True)
QMAP = {"0331": 1, "0630": 2, "0930": 3, "1231": 4}
LEVELS = [0.80, 0.95, 0.99]
TIERS = ["정상", "주의", "경고", "위험"]
MIN_MV = 5_000_000  # skip tiny denominators


def group(strategy: str) -> str:
    s = (strategy or "").lower()
    if "buyout" in s:
        return "Buyout"
    if "venture" in s:
        return "Venture"
    if "growth" in s:
        return "Growth"
    return "Credit/Special/Other"


frames = []
for path in sorted(glob.glob(os.path.join(CSV_DIR, "ir*.csv"))):
    tag = os.path.basename(path)[2:8]  # MMDDYY
    year, q = 2000 + int(tag[4:6]), QMAP[tag[:4]]
    df = pd.read_csv(path)
    df["period"] = year * 10 + q
    df["label"] = f"{year}Q{q}"
    frames.append(df)
panel = pd.concat(frames, ignore_index=True)

# --- parse validation: total value should equal MV + distributions
chk = (panel["market_value"] + panel["distributed"] - panel["total_value"]).abs()
parse_ok = float((chk <= 2).mean())

panel["key"] = panel["fund"].str.strip() + " | " + panel["init_date"]
panel = panel.sort_values(["key", "period"])
periods = sorted(panel["period"].unique())
nxt = {p: periods[i + 1] for i, p in enumerate(periods[:-1])}

prev = panel[["key", "period", "market_value", "paid_in", "distributed"]].copy()
prev["period"] = prev["period"].map(nxt)
prev = prev.dropna(subset=["period"])
prev["period"] = prev["period"].astype(int)
m = panel.merge(prev, on=["key", "period"], suffixes=("", "_prev"))
m = m[(m["market_value_prev"] >= MIN_MV)]
m["contrib_q"] = m["paid_in"] - m["paid_in_prev"]
m["dist_q"] = m["distributed"] - m["distributed_prev"]
# Modified Dietz: flows assumed mid-quarter, avoids blow-ups when a large call lands on a small fund
m["ret"] = (m["market_value"] - m["market_value_prev"] - m["contrib_q"] + m["dist_q"]) / (
    m["market_value_prev"] + 0.5 * m["contrib_q"] - 0.5 * m["dist_q"])
m["grp"] = m["strategy"].map(group)
m["bench"] = m.groupby(["period", "grp"])["ret"].transform("median")
m["resid"] = m["ret"] - m["bench"]
m["score"] = m["resid"].abs()
m = m.replace([np.inf, -np.inf], np.nan).dropna(subset=["score"])
ret_periods = sorted(m["period"].unique())
label = dict(zip(m["period"], m["label"]))


def cq(scores: np.ndarray, level: float) -> float:
    """Split-conformal quantile with finite-sample correction."""
    n = len(scores)
    k = min(n, math.ceil((n + 1) * level))
    return float(np.sort(scores)[k - 1])


def tier_of(score: float, qs: list[float]) -> int:
    t = 0
    for i, qv in enumerate(qs):
        if score > qv:
            t = i + 1
    return t


def evaluate(test_p, calib_scores, test_df):
    qs = [cq(calib_scores, lv) for lv in LEVELS]
    tiers = test_df["score"].apply(lambda s: tier_of(s, qs))
    out = {"period": label[test_p], "n": int(len(test_df)), "q80": qs[0], "q95": qs[1], "q99": qs[2]}
    for lv, qv in zip(LEVELS, qs):
        out[f"cov{int(lv*100)}"] = float((test_df["score"] <= qv).mean())
    for i, t in enumerate(TIERS):
        out[f"n_{t}"] = int((tiers == i).sum())
    return out, tiers


# --- A. Leave-one-quarter-out (assumes quarters exchangeable)
loqo = []
for p in ret_periods:
    calib = m.loc[m["period"] != p, "score"].to_numpy()
    res, _ = evaluate(p, calib, m[m["period"] == p])
    loqo.append(res)
loqo = pd.DataFrame(loqo)

# --- B. Expanding window, forward in time (realistic deployment)
fwd, tier_rows = [], []
for i, p in enumerate(ret_periods):
    if i < 3:  # need >= 3 quarters of calibration
        continue
    calib = m.loc[m["period"].isin(ret_periods[:i]), "score"].to_numpy()
    test = m[m["period"] == p]
    res, tiers = evaluate(p, calib, test)
    fwd.append(res)
    tier_rows.append(pd.DataFrame({"key": test["key"].values, "period": p, "tier": tiers.values}))
fwd = pd.DataFrame(fwd)

# --- C. Adaptive conformal (per-level alpha update on quarterly miscoverage), forward
gamma = 0.05
aci = []
alpha = {lv: 1 - lv for lv in LEVELS}
for i, p in enumerate(ret_periods):
    if i < 3:
        continue
    calib = m.loc[m["period"].isin(ret_periods[:i]), "score"].to_numpy()
    test = m[m["period"] == p]
    row = {"period": label[p]}
    for lv in LEVELS:
        a = min(max(alpha[lv], 0.001), 0.999)
        qv = cq(calib, 1 - a)
        cov = float((test["score"] <= qv).mean())
        row[f"cov{int(lv*100)}"] = cov
        alpha[lv] = alpha[lv] + gamma * ((1 - lv) - (1 - cov))
    aci.append(row)
aci = pd.DataFrame(aci)

# --- Escalation rule: 주의 two quarters in a row -> 경고
tr = pd.concat(tier_rows).sort_values(["key", "period"])
tr["prev_tier"] = tr.groupby("key")["tier"].shift(1)
escalated = tr[(tr["tier"] == 1) & (tr["prev_tier"] == 1)].groupby("period").size()

# --- Alert counts (주의 이상) and supervisor sizing
fwd["alerts"] = fwd["n_주의"] + fwd["n_경고"] + fwd["n_위험"]
fwd["alerts_per137"] = fwd["alerts"] / fwd["n"] * 137
p95_alerts = float(np.percentile(fwd["alerts_per137"], 95))
summary = {
    "quarters_in_data": [label.get(p, str(p)) for p in periods] if False else None,
    "n_report_quarters": len(periods),
    "n_return_quarters": len(ret_periods),
    "fund_quarter_obs": int(len(m)),
    "funds_per_quarter_median": float(m.groupby("period").size().median()),
    "parse_total_value_check": parse_ok,
    "resid_quantiles": {k: float(v) for k, v in m["resid"].quantile([0.01, 0.1, 0.5, 0.9, 0.99]).items()},
    "loqo_mean_cov": {k: float(loqo[k].mean()) for k in ["cov80", "cov95", "cov99"]},
    "fwd_mean_cov": {k: float(fwd[k].mean()) for k in ["cov80", "cov95", "cov99"]},
    "aci_mean_cov": {k: float(aci[k].mean()) for k in ["cov80", "cov95", "cov99"]},
    "fwd_tier_share": {t: float(fwd[f"n_{t}"].sum() / fwd["n"].sum()) for t in TIERS},
    "alerts_per137_by_quarter": dict(zip(fwd["period"], fwd["alerts_per137"].round(1))),
    "alerts_per137_p95": p95_alerts,
    "escalations_by_quarter": {label[int(k)]: int(v) for k, v in escalated.items()},
}
m.to_csv(os.path.join(OUT_DIR, "fund_quarter_returns.csv"), index=False)
loqo.to_csv(os.path.join(OUT_DIR, "loqo.csv"), index=False)
fwd.to_csv(os.path.join(OUT_DIR, "forward.csv"), index=False)
aci.to_csv(os.path.join(OUT_DIR, "aci.csv"), index=False)
json.dump(summary, open(os.path.join(OUT_DIR, "summary.json"), "w"), ensure_ascii=False, indent=2)
print(json.dumps(summary, ensure_ascii=False, indent=2))
print("\nLOQO\n", loqo.round(3).to_string(index=False))
print("\nFORWARD\n", fwd.round(3).to_string(index=False))
print("\nACI\n", aci.round(3).to_string(index=False))
