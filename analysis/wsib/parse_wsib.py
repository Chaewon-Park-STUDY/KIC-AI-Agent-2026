"""Parse a WSIB quarterly private equity report (pdftotext -layout output) into fund rows."""
import re, sys, csv

NUM = r"(-|\(?[\d,]+\)?)"
row_re = re.compile(
    r"^(?P<name>\S.*?)\s{2,}(?P<date>\d{1,2}/\d{1,2}/\d{4})\s+"
    + r"\s+".join([f"(?P<c{i}>{NUM})" for i in range(6)])
    + r"\s+(?P<tvpi>-?[\d.]+x|-|NM|N/A)\s+(?P<gain>\(?[\d,\-]+\)?|-)\s+(?P<irr>\(?-?[\d.]+%\)?|NM|N/A|-)\s*$"
)

SKIP = {"PRIVATE EQUITY PORTFOLIO", "OVERVIEW BY STRATEGY", "Washington State Investment Board",
        "Performance Summary By Strategy (Base)"}


def num(s):
    s = s.strip()
    if s in ("-", ""):
        return 0.0
    neg = s.startswith("(")
    v = float(s.strip("()").replace(",", ""))
    return -v if neg else v

def parse(path):
    rows, strategy = [], None
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        m = row_re.match(line.strip())
        if m:
            d = m.groupdict()
            rows.append({
                "strategy": strategy, "fund": d["name"].strip(), "init_date": d["date"],
                "committed": num(d["c0"]), "paid_in": num(d["c1"]), "unfunded": num(d["c2"]),
                "market_value": num(d["c3"]), "distributed": num(d["c4"]), "total_value": num(d["c5"]),
                "tvpi": d["tvpi"], "irr": d["irr"],
            })
            continue
        s = line.strip()
        # strategy header lines: text only, no digits, followed by column labels on same line
        hm = re.match(r"^([A-Za-z/&\- ,]+?)\s{3,}Contributions", s)
        if hm:
            strategy = hm.group(1).strip()
        elif s and not re.search(r"\d", s) and len(s) < 60 and "  " not in s and s not in SKIP:
            strategy = s
    return rows

if __name__ == "__main__":
    rows = parse(sys.argv[1])
    w = csv.DictWriter(sys.stdout, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
