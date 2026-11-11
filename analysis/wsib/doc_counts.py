"""Documents per fund per quarter, lower bound, from WSIB cumulative paid-in / distributed."""
import glob, os, sys
import pandas as pd
QMAP = {"0331": 1, "0630": 2, "0930": 3, "1231": 4}
fr = []
for p in sorted(glob.glob(os.path.join(sys.argv[1], "ir*.csv"))):
    t = os.path.basename(p)[2:8]
    d = pd.read_csv(p); d["period"] = (2000 + int(t[4:6])) * 10 + QMAP[t[:4]]; fr.append(d)
pn = pd.concat(fr)
pn["key"] = pn["fund"].str.strip() + " | " + pn["init_date"]
per = sorted(pn["period"].unique()); nxt = {p: per[i + 1] for i, p in enumerate(per[:-1])}
prev = pn[["key", "period", "paid_in", "distributed", "market_value"]].copy()
prev["period"] = prev["period"].map(nxt); prev = prev.dropna(subset=["period"]); prev["period"] = prev["period"].astype(int)
m = pn.merge(prev, on=["key", "period"], suffixes=("", "_prev"))
m = m[(m["market_value_prev"] > 0) | (m["market_value"] > 0)]          # active funds
TH = 10_000                                                               # ignore rounding noise
m["call"] = (m["paid_in"] - m["paid_in_prev"]) > TH
m["dist"] = (m["distributed"] - m["distributed_prev"]) > TH
m["docs_lb"] = 2 + m["call"].astype(int) + m["dist"].astype(int)          # 분기보고서 + 계좌명세서 + 납입 + 분배
q = m.groupby("period").agg(funds=("key", "size"), call=("call", "mean"), dist=("dist", "mean"), docs=("docs_lb", "mean"))
print(q.round(3).to_string())
print("\nall quarters: funds/q median", q["funds"].median(), "| call share", round(m["call"].mean(), 3),
      "| dist share", round(m["dist"].mean(), 3), "| docs/fund/q mean", round(m["docs_lb"].mean(), 2),
      "| quarter range", round(q["docs"].min(), 2), "~", round(q["docs"].max(), 2))
print("docs distribution:", m["docs_lb"].value_counts(normalize=True).sort_index().round(3).to_dict())
