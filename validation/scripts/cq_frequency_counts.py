#!/usr/bin/env python3
"""
SBMO validation — combination counts for the frequency-type competency
questions (stdlib only).

CQ3 ("Which customer types are most frequently associated with specific
acquisition channels?") and CQ5 ("Which success factors and implementation
challenges are recurrent for a given class of SBMs?") ask for frequencies, so
their answer is the number of cases in which each pair of values co-occurs.
This script counts, for every pair (customer type x acquisition channel and
success factor x implementation challenge), the number of SBM cases that
assert both values.

Inputs (all anonymized and versioned in this repo):
  - survey-derived/cases_normalized.csv                     (primary source)
  - protege/sbmo-validation-abox.ttl                        (cross-check 1)
  - zenodo-package/data/statistical_analysis/processed_data.csv
                         (cross-check 2: the indicator matrices used by the
                          RV analysis of reproduce_sbmo_analysis_fixed.r)
The script aborts if the three sources disagree on any count, and checks the
marginal counts against the per-value frequencies in survey-derived/summary.json
(the source of the dissertation's tab:frequencies).

Outputs:
  - survey-derived/cq_frequency_counts.csv  (long format: cq, value_a, value_b, n_cases)
  - LaTeX table fragment for the dissertation (default path below, or argv[1])

Usage:  python3 cq_frequency_counts.py [path/to/cq_frequency_counts.tex]
"""

import csv
import json
import os
import re
import sys
from collections import defaultdict

import sbmo_mapping as M

HERE = os.path.dirname(os.path.abspath(__file__))
VALIDATION_ROOT = os.path.dirname(HERE)  # sbmo/validation
SBMO_ROOT = os.path.dirname(VALIDATION_ROOT)  # sbmo
DISSERTATION_ROOT = os.path.dirname(SBMO_ROOT)
CASES = os.path.join(VALIDATION_ROOT, "survey-derived", "cases_normalized.csv")
SUMMARY = os.path.join(VALIDATION_ROOT, "survey-derived", "summary.json")
ABOX = os.path.join(VALIDATION_ROOT, "protege", "sbmo-validation-abox.ttl")
PROCESSED = os.path.join(VALIDATION_ROOT, "zenodo-package", "data",
                         "statistical_analysis", "processed_data.csv")
OUT_CSV = os.path.join(VALIDATION_ROOT, "survey-derived", "cq_frequency_counts.csv")
DEFAULT_TEX = os.path.join(DISSERTATION_ROOT, "sbm-ontology-dissertation", "assets",
                           "ontology_evaluation", "tables", "cq_frequency_counts.tex")
OUT_TEX = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_TEX

# CQ -> (row dimension key, column dimension key), as tested in Section 7.4.
CQS = {"CQ3": ("customer", "channel"), "CQ5": ("success", "challenge")}

# Column headers of processed_data.csv (R analysis) for each dimension key.
R_DIMENSION = {"customer": "Customer type", "channel": "Acquisition channel",
               "success": "Success factor", "challenge": "Implementation challenge"}


def from_cases_csv():
    """case -> dim key -> set(class), from the anonymized normalized CSV."""
    with open(CASES, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    keys = {k for pair in CQS.values() for k in pair}
    return {r["case_id"]: {k: {v for v in r[k].split(";") if v} for k in keys} for r in rows}


def from_abox():
    """Same structure, rebuilt from the A-Box assertions and rdf:type triples."""
    text = open(ABOX, encoding="utf-8").read()
    types = dict(re.findall(r"^ex:(\S+) a sbmo:(\w+) \.", text, re.M))
    prop_to_key = {M.DIM_BY_KEY[k]["prop"]: k for pair in CQS.values() for k in pair}
    out = defaultdict(lambda: defaultdict(set))
    current = None
    for line in text.splitlines():
        m = re.match(r"^ex:(Case\d+) a sbmo:SoftwareBusinessModel", line)
        if m:
            current = m.group(1)
            continue
        if not line.startswith("    "):
            current = None
            continue
        m = re.match(r"^\s+sbmo:(\w+) ex:(\w+)", line)
        if current and m and m.group(1) in prop_to_key:
            out[current][prop_to_key[m.group(1)]].add(types[m.group(2)])
    return out


def from_processed():
    """Same structure, rebuilt from the R analysis indicator matrices."""
    with open(PROCESSED, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    out = defaultdict(lambda: defaultdict(set))
    for r in rows:
        for key, rdim in R_DIMENSION.items():
            for col, val in r.items():
                if not col.startswith(rdim + "__") or val != "1":
                    continue
                label = M.base_label(col.split("__", 1)[1])
                if label == M.OTHER:
                    continue
                out[r["CaseID"]][key].add(M.DIM_BY_KEY[key]["map"][label])
    return out


def crosstab(data, a, b):
    counts = defaultdict(int)
    for dims in data.values():
        for x in dims.get(a, ()):
            for y in dims.get(b, ()):
                counts[(x, y)] += 1
    return counts


def marginals(data, key):
    n = defaultdict(int)
    for dims in data.values():
        for x in dims.get(key, ()):
            n[x] += 1
    return n


def main():
    primary, abox, processed = from_cases_csv(), from_abox(), from_processed()
    assert len(primary) == 31, len(primary)
    freq = json.load(open(SUMMARY, encoding="utf-8"))["frequencies"]

    tables = {}
    for cq, (a, b) in CQS.items():
        ct = crosstab(primary, a, b)
        for name, other in (("A-Box", abox), ("processed_data.csv", processed)):
            if crosstab(other, a, b) != ct:
                sys.exit(f"!! {cq}: counts from {name} differ from cases_normalized.csv")
        ma, mb = marginals(primary, a), marginals(primary, b)
        for key, m in ((a, ma), (b, mb)):
            if dict(m) != freq[key]:
                sys.exit(f"!! {cq}: marginals of {key} differ from summary.json frequencies")
        rows = sorted(ma, key=lambda x: (-ma[x], M.en(x)))
        cols = sorted(mb, key=lambda y: (-mb[y], M.en(y)))
        n_both = sum(1 for d in primary.values() if d[a] and d[b])
        tables[cq] = (a, b, rows, cols, ct, ma, mb, n_both)
        print(f"{cq}: OK, three sources agree; {n_both} cases assert both dimensions")

    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["cq", "value_a", "value_b", "n_cases"])
        for cq, (a, b, rows, cols, ct, *_rest) in tables.items():
            for x in rows:
                for y in cols:
                    w.writerow([cq, x, y, ct[(x, y)]])
    print(f"Wrote: {OUT_CSV}")

    write_latex(tables)
    print(f"Wrote: {OUT_TEX}")


TITLES = {"CQ3": ("Customer type", "Acquisition channel"),
          "CQ5": ("Success factor", "Implementation challenge")}


def write_latex(tables):
    ncols = max(len(t[3]) for t in tables.values())
    lines = [
        "% Generated by sbmo/validation/scripts/cq_frequency_counts.py -- do not edit by hand.",
        r"\begin{table}[!htb]",
        r"\renewcommand{\arraystretch}{1.2}",
        r"\caption[Value combinations answering CQ3 and CQ5]{Value combinations answering CQ3 and CQ5: "
        r"number of cases (of 31) asserting both values. Selections are multi-valued, so a case can "
        r"contribute to several cells; $n$ is the number of cases selecting each value "
        r"(Table~\ref{tab:frequencies}).}",
        r"\label{tab:cq_frequency_counts}",
        r"\centering",
        r"\footnotesize",
        r"\setlength{\tabcolsep}{3.5pt}",
        r"\begin{tabular}{l|*{" + str(ncols) + r"}{>{\centering\arraybackslash}p{1.64cm}}|c}",
        r"\bottomrule",
    ]
    for i, (cq, (a, b, rows, cols, ct, ma, mb, n_both)) in enumerate(tables.items()):
        ta, tb = TITLES[cq]
        if i:
            lines.append(r"\hline")
        lines.append(r"\rowcolor{gray!50}")
        lines.append(rf"\multicolumn{{{ncols + 2}}}{{l}}{{\textbf{{{cq}: {ta} $\times$ {tb}}} "
                     rf"({n_both} cases assert both dimensions)}} \\")
        head = [""] + [M.en(y) for y in cols] + [""] * (ncols - len(cols)) + ["$n$"]
        lines.append(" & ".join(rf"\textbf{{{h}}}" if h else "" for h in head) + r" \\")
        lines.append(r"\hline")
        for x in rows:
            cells = [str(ct[(x, y)]) for y in cols] + [""] * (ncols - len(cols))
            lines.append(" & ".join([M.en(x)] + cells + [str(ma[x])]) + r" \\")
        lines.append(r"\hline")
        cells = [str(mb[y]) for y in cols] + [""] * (ncols - len(cols))
        lines.append(" & ".join(["$n$"] + cells + [""]) + r" \\")
    lines += [r"\toprule", r"\end{tabular}", r"\fonte{the author.}", r"\end{table}", ""]
    os.makedirs(os.path.dirname(OUT_TEX), exist_ok=True)
    with open(OUT_TEX, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    main()
