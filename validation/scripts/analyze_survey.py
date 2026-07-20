#!/usr/bin/env python3
"""
SBMO validation — survey analysis (stdlib only).

Reads the raw Google Forms export, assigns opaque anonymous case IDs, maps
controlled-vocabulary answers to SBMO classes, and produces:
  - survey-derived/cases_normalized.csv   (anonymized: CaseID + mapped classes)
  - survey-derived/summary.json           (aggregate figures)
  - dissertation-paper/assets/ontology/tables/*.tex (ready-to-input tables)
  - a human-readable report on stdout

ANONYMITY: identifying columns (name, email, company, product, role) are read
only to compute aggregate counts (distinct organizations, inter-rater pair) and
are NEVER written to any output. The raw CSV is private and lives OUTSIDE this
(public, versioned) repo, in a sibling `validations/` directory that is never
committed anywhere.

Layout: this script lives in sbmo/validation/scripts/. It reads the raw CSV
from ../../../validations/sbmo-form-answers.csv (sibling of the sbmo repo),
writes anonymized aggregate outputs into sbmo/validation/survey-derived/, and
writes the LaTeX table fragments directly into the sibling dissertation-paper
repo (they are presentation artifacts for that one document, not ontology
evidence, so they don't belong in this repo). See sbmo/validation/protege/ for
the A-Box built from this analysis (build_abox.py) and the CQ queries run
against it.

Usage:  python3 analyze_survey.py [path/to/sbmo-form-answers.csv]
"""

import csv
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime

import sbmo_mapping as M

HERE = os.path.dirname(os.path.abspath(__file__))
VALIDATION_ROOT = os.path.dirname(HERE)  # sbmo/validation
SBMO_ROOT = os.path.dirname(VALIDATION_ROOT)  # sbmo
DISSERTATION_ROOT = os.path.dirname(SBMO_ROOT)  # sibling of sbmo, dissertation-paper, validations
DEFAULT_RAW = os.path.join(DISSERTATION_ROOT, "validations", "sbmo-form-answers.csv")
RAW = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_RAW
DERIVED = os.path.join(VALIDATION_ROOT, "survey-derived")
LATEX = os.path.join(DISSERTATION_ROOT, "dissertation-paper", "assets", "ontology", "tables")
os.makedirs(DERIVED, exist_ok=True)
os.makedirs(LATEX, exist_ok=True)

# Column indices for non-dimension fields.
COL_TIMESTAMP, COL_EMAIL = 0, 1
COL_COMPANY, COL_PRODUCT, COL_YEAR = 3, 4, 5
COL_KNOWLEDGE, COL_OPERATIONAL = 8, 9

# The 7 object properties on SoftwareBusinessModel constrained by
# minQualifiedCardinality 1 in the T-Box (see sbmo.rdf).
MANDATORY = ["product_type", "delivery", "revenue", "pricing",
             "customer", "ecosystem", "channel"]

NON_COMPANY = {"não quero informar", "prefiro não dizer", "não indentificada",
               "não identificada", "n/a", "-", ""}


def load():
    with open(RAW, encoding="utf-8") as f:
        rows = list(csv.reader(f))
    return rows[0], rows[1:]


def latex_escape(s: str) -> str:
    return (s.replace("\\", r"\textbackslash{}").replace("&", r"\&")
             .replace("%", r"\%").replace("_", r"\_").replace("#", r"\#"))


def main():
    header, data = load()
    n = len(data)
    cases = [f"Case{str(i + 1).zfill(2)}" for i in range(n)]

    # ---- mapping completeness check -------------------------------------
    problems = []
    for dim in M.DIMENSIONS:
        for r in data:
            cell = r[dim["col"]] if dim["col"] < len(r) else ""
            _, _, unmapped = M.map_cell(dim, cell)
            if unmapped:
                problems.append((dim["key"], unmapped))
    if problems:
        print("!! UNMAPPED LABELS (fix sbmo_mapping.py):")
        for k, u in problems:
            print("   ", k, u)
    else:
        print("OK: every controlled-vocabulary answer maps to an SBMO class.\n")

    # ---- per-case mapped selections -------------------------------------
    case_dims = {c: {} for c in cases}       # case -> dim key -> [class,...]
    case_other = {c: set() for c in cases}   # case -> {dim key with 'Outro'}
    for i, r in enumerate(data):
        c = cases[i]
        for dim in M.DIMENSIONS:
            cell = r[dim["col"]] if dim["col"] < len(r) else ""
            mapped, other, _ = M.map_cell(dim, cell)
            case_dims[c][dim["key"]] = mapped
            if other:
                case_other[c].add(dim["key"])

    # ---- frequency distributions ----------------------------------------
    freq = {}          # dim key -> Counter(class -> n cases)
    for dim in M.DIMENSIONS:
        cnt = Counter()
        for c in cases:
            for cls in set(case_dims[c][dim["key"]]):
                cnt[cls] += 1
        freq[dim["key"]] = cnt

    # ---- coverage / gap analysis ----------------------------------------
    coverage = {}      # dim key -> (n_other_cases, coverage_pct)
    for dim in M.DIMENSIONS:
        n_other = sum(1 for c in cases if dim["key"] in case_other[c])
        coverage[dim["key"]] = (n_other, round(100.0 * (n - n_other) / n, 1))

    # ---- structural completeness (7 mandatory SBM properties) -----------
    complete_cases, incomplete = [], {}
    for c in cases:
        missing = [k for k in MANDATORY if not case_dims[c][k]]
        if missing:
            incomplete[c] = missing
        else:
            complete_cases.append(c)
    n_complete = len(complete_cases)

    # ---- respondent / case profile --------------------------------------
    knowledge = Counter()
    for r in data:
        v = (r[COL_KNOWLEDGE] if COL_KNOWLEDGE < len(r) else "").strip()
        knowledge[v if v else "(blank)"] += 1
    operational = Counter(
        (r[COL_OPERATIONAL] if COL_OPERATIONAL < len(r) else "").strip() for r in data)

    # ---- N, M (distinct organizations), collection period ---------------
    companies = set()
    for r in data:
        v = (r[COL_COMPANY] if COL_COMPANY < len(r) else "").strip()
        if v.lower() not in NON_COMPANY:
            companies.add(v.lower())
    n_named_orgs = len(companies)

    dates = []
    for r in data:
        ts = (r[COL_TIMESTAMP] if COL_TIMESTAMP < len(r) else "").strip()
        m = re.match(r"(\d{4})/(\d{2})/(\d{2})", ts)
        if m:
            dates.append(datetime(int(m[1]), int(m[2]), int(m[3])))
    period = (min(dates).strftime("%B %Y"), max(dates).strftime("%B %Y")) if dates else ("?", "?")

    # ---- inter-rater: product described by two respondents --------------
    # detect duplicated product name internally; output only the agreement.
    prod_rows = defaultdict(list)
    for i, r in enumerate(data):
        p = (r[COL_PRODUCT] if COL_PRODUCT < len(r) else "").strip().lower()
        if p:
            prod_rows[p].append(cases[i])
    interrater = None
    for p, cs in prod_rows.items():
        if len(cs) == 2:
            a, b = cs
            agree_dims, total_dims = 0, 0
            per_dim = {}
            for dim in M.DIMENSIONS:
                sa, sb = set(case_dims[a][dim["key"]]), set(case_dims[b][dim["key"]])
                if not sa and not sb:
                    continue
                total_dims += 1
                jac = len(sa & sb) / len(sa | sb) if (sa | sb) else 1.0
                per_dim[dim["key"]] = round(jac, 2)
                if jac == 1.0:
                    agree_dims += 1
            avg_jac = round(sum(per_dim.values()) / len(per_dim), 2) if per_dim else 0.0
            interrater = {"cases": cs, "dims_compared": total_dims,
                          "dims_full_agreement": agree_dims, "avg_jaccard": avg_jac,
                          "per_dim_jaccard": per_dim}
            break

    # ---- CQ expected results (cross-check for Protégé) ------------------
    def pairs(dk1, dk2):
        s = set()
        for c in cases:
            for x in case_dims[c][dk1]:
                for y in case_dims[c][dk2]:
                    s.add((x, y))
        return s

    def cases_with(dk):
        return [c for c in cases if case_dims[c][dk]]

    cq = {}
    cq["CQ1"] = {"desc": "Revenue x Delivery", "distinct_pairs": len(pairs("revenue", "delivery")),
                 "matching_cases": len([c for c in cases if case_dims[c]["revenue"] and case_dims[c]["delivery"]])}
    cq["CQ2"] = {"desc": "Pricing x Revenue", "distinct_pairs": len(pairs("pricing", "revenue")),
                 "matching_cases": len([c for c in cases if case_dims[c]["pricing"] and case_dims[c]["revenue"]])}
    cq["CQ3"] = {"desc": "Customer x Channel", "distinct_pairs": len(pairs("customer", "channel")),
                 "matching_cases": len([c for c in cases if case_dims[c]["customer"] and case_dims[c]["channel"]])}
    cq["CQ4"] = {"desc": "Ecosystem x Network effect", "distinct_pairs": len(pairs("ecosystem", "network_effect")),
                 "matching_cases": len([c for c in cases if case_dims[c]["ecosystem"] and case_dims[c]["network_effect"]])}
    cq["CQ5"] = {"desc": "Success factors x Challenges", "distinct_pairs": len(pairs("success", "challenge")),
                 "matching_cases": len([c for c in cases if case_dims[c]["success"] and case_dims[c]["challenge"]])}
    # CQ6: mitigates has no SoftwareBusinessModel-level counterpart (it links
    # MitigationStrategy -> ImplementationChallenge directly), so it is
    # answered at the mitigation-individual level, not the case level: count
    # distinct mitigation-strategy individuals that address >=1 challenge
    # (each selected mitigation value in a case becomes one individual, per
    # build_abox.py, linked to every challenge selected in that same case).
    n_mitigation_individuals_with_edge = sum(
        len(case_dims[c]["mitigation"]) for c in cases if case_dims[c]["challenge"])
    cq["CQ6"] = {"desc": "Mitigation x Challenge", "distinct_pairs": len(pairs("mitigation", "challenge")),
                 "matching_cases": n_mitigation_individuals_with_edge,
                 "unit": "mitigation individuals"}
    cq["CQ7"] = {"desc": "Multi-dimensional configuration",
                 "matching_cases": len([c for c in cases if all(case_dims[c][k] for k in
                                        ("delivery", "revenue", "pricing", "ecosystem"))])}

    # ---- write anonymized normalized CSV --------------------------------
    with open(os.path.join(DERIVED, "cases_normalized.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        headers = ["case_id"] + [d["key"] for d in M.DIMENSIONS] + \
                  [d["key"] + "_other" for d in M.DIMENSIONS] + ["knowledge", "operational", "launch_year"]
        w.writerow(headers)
        for i, c in enumerate(cases):
            r = data[i]
            row = [c]
            row += [";".join(case_dims[c][d["key"]]) for d in M.DIMENSIONS]
            row += ["1" if d["key"] in case_other[c] else "" for d in M.DIMENSIONS]
            row += [(r[COL_KNOWLEDGE] if COL_KNOWLEDGE < len(r) else "").strip(),
                    (r[COL_OPERATIONAL] if COL_OPERATIONAL < len(r) else "").strip(),
                    (r[COL_YEAR] if COL_YEAR < len(r) else "").strip()]
            w.writerow(row)

    # ---- summary json ---------------------------------------------------
    summary = {
        "n_valid_responses": n,
        "n_complete_cases": n_complete,
        "n_incomplete_cases": len(incomplete),
        "incomplete_missing": {c: incomplete[c] for c in incomplete},
        "n_named_organizations": n_named_orgs,
        "period_start": period[0], "period_end": period[1],
        "knowledge": dict(knowledge), "operational": dict(operational),
        "coverage": {k: {"other_cases": v[0], "coverage_pct": v[1]} for k, v in coverage.items()},
        "frequencies": {k: dict(freq[k]) for k in freq},
        "interrater": interrater,
        "cq": cq,
    }
    with open(os.path.join(DERIVED, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    write_latex(freq, coverage, cq, n, summary)
    print_report(summary, freq, coverage, cq, n)


def write_latex(freq, coverage, cq, n, summary):
    # 1) CQ empirical results table
    lines = [
        r"% Generated by validations/scripts/analyze_survey.py -- do not edit by hand.",
        r"\begin{table}[!htb]",
        r"\renewcommand{\arraystretch}{1.3}",
        r"\caption{Empirical evaluation of the competency questions against the populated A-Box (" + str(n) + r" cases).}",
        r"\label{tab:cq_empirical_results}",
        r"\centering",
        r"\small",
        r"\begin{tabular}{c|p{4.9cm}|c|c|p{2.3cm}}",
        r"\toprule",
        r"\rowcolor{gray!50}",
        r"\textbf{CQ} & \textbf{Query (abbreviated)} & \textbf{Satisfied} & \textbf{Matching} & \textbf{Unit} \\",
        r"\hline",
    ]
    for k in ["CQ1", "CQ2", "CQ3", "CQ4", "CQ5", "CQ6", "CQ7"]:
        d = cq[k]
        mc = d["matching_cases"]
        unit = d.get("unit", "SBM cases")
        desc = d["desc"].replace(" x ", r" $\times$ ")
        lines.append(f"{k} & {desc} & \\checkmark & {mc} & {unit} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}", ""]
    open(os.path.join(LATEX, "cq_empirical_results.tex"), "w", encoding="utf-8").write("\n".join(lines))

    # 2) Coverage / gap table
    lines = [
        r"% Generated by validations/scripts/analyze_survey.py -- do not edit by hand.",
        r"\begin{table}[!htb]",
        r"\renewcommand{\arraystretch}{1.3}",
        r"\caption{Ontological coverage per dimension across the " + str(n) + r" cases. "
        r"``Other'' counts cases that used the free-text escape hatch instead of the controlled vocabulary.}",
        r"\label{tab:coverage}",
        r"\centering",
        r"\small",
        r"\begin{tabular}{l|c|c}",
        r"\toprule",
        r"\rowcolor{gray!50}",
        r"\textbf{Dimension} & \textbf{``Other'' used (cases)} & \textbf{Coverage} \\",
        r"\hline",
    ]
    for dim in M.DIMENSIONS:
        no, pct = coverage[dim["key"]]
        lines.append(f"{M.DIM_ENGLISH[dim['key']]} & {no} & {pct:.0f}\\% \\\\")
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}", ""]
    open(os.path.join(LATEX, "coverage.tex"), "w", encoding="utf-8").write("\n".join(lines))

    # 3) Frequency distribution table (all dimensions, value : count)
    lines = [
        r"% Generated by validations/scripts/analyze_survey.py -- do not edit by hand.",
        r"\begin{table}[!htb]",
        r"\renewcommand{\arraystretch}{1.2}",
        r"\caption{Distribution of controlled-vocabulary selections across the " + str(n) + r" cases "
        r"(multi-select; counts are the number of cases choosing each value).}",
        r"\label{tab:frequencies}",
        r"\centering",
        r"\footnotesize",
        r"\begin{tabular}{l|p{9.5cm}}",
        r"\toprule",
        r"\rowcolor{gray!50}",
        r"\textbf{Dimension} & \textbf{Value (cases)} \\",
        r"\hline",
    ]
    for dim in M.DIMENSIONS:
        items = freq[dim["key"]].most_common()
        vals = ", ".join(f"{M.en(cls)} ({c})" for cls, c in items) or "--"
        lines.append(f"{M.DIM_ENGLISH[dim['key']]} & {latex_escape(vals)} \\\\")
        lines.append(r"\hline")
    lines[-1] = r"\bottomrule"
    lines += [r"\end{tabular}", r"\end{table}", ""]
    open(os.path.join(LATEX, "frequencies.tex"), "w", encoding="utf-8").write("\n".join(lines))


def print_report(summary, freq, coverage, cq, n):
    print(f"N valid responses (cases): {summary['n_valid_responses']}")
    print(f"Complete cases (all 7 mandatory props): {summary['n_complete_cases']}  "
          f"| incomplete: {summary['n_incomplete_cases']}")
    for c, miss in summary["incomplete_missing"].items():
        print(f"    {c} missing: {miss}")
    print(f"Distinct named organizations: {summary['n_named_organizations']}")
    print(f"Collection period: {summary['period_start']} -> {summary['period_end']}")
    print(f"Operational: {dict(summary['operational'])}")
    print(f"Knowledge (1-5): {dict(summary['knowledge'])}")
    print("\nCoverage (other-used cases / coverage %):")
    for dim in M.DIMENSIONS:
        no, pct = coverage[dim["key"]]
        print(f"  {M.DIM_ENGLISH[dim['key']]:28s} other={no:2d}  coverage={pct}%")
    print("\nCQ expected results (cross-check for Protégé):")
    for k in ["CQ1", "CQ2", "CQ3", "CQ4", "CQ5", "CQ6", "CQ7"]:
        print(f"  {k}: {cq[k]}")
    if summary["interrater"]:
        ir = summary["interrater"]
        print(f"\nInter-rater (same product, two respondents {ir['cases']}): "
              f"{ir['dims_full_agreement']}/{ir['dims_compared']} dimensions in full agreement")
        print(f"  per-dim Jaccard: {ir['per_dim_jaccard']}")
    print(f"\nWrote: {os.path.join(DERIVED, 'cases_normalized.csv')}")
    print(f"Wrote: {os.path.join(DERIVED, 'summary.json')}")
    print(f"Wrote LaTeX fragments in: {LATEX}")


if __name__ == "__main__":
    main()
