#!/usr/bin/env python3
"""
SBMO validation: respondent role/function extraction (stdlib only).

Reads the raw Google Forms export and classifies the free-text "Nome e
cargo do respondente" (name + role) field into a small set of role
categories, for the socio-demographic profile of participants
(dissertation Chapter 7, per the 2026-08-15 advisor feedback, see
dissertation-paper/docs/CORRECTION_PLAN_2026-08-15.md, task 2).

ANONYMITY: the raw cell always contains a real name mixed with the role
(e.g. "Jane Doe, Co-founder"). This script classifies the
FULL raw string (name included) against role keywords; the name text does
not collide with any keyword, so there is no need to parse out and handle
the name substring separately, which would itself risk leaking it into a
variable, log line, or output file. Only the resulting category label is
ever written to survey-derived/. The raw string is never printed, logged,
or persisted anywhere by this script.

Category priority (a cell is assigned the first matching category; several
respondents hold compound titles, e.g. "Desenvolvedor e posteriormente
PO/Coordenador", and the priority order resolves those to the more senior /
current role):
  1. Founder            : "fundador" (incl. "co-fundador")
  2. Leadership          : CEO/CTO/diretor/head of/coordenador/líder/PO
  3. Technical Advisory  : advisor / responsável técnico
  4. Product & Design    : design/UX/UI
  5. Engineering         : desenvolvedor/developer/fullstack/analista de sistema
  6. Other/Analyst       : fallback (generic "analista", or anything else)

Usage:  python3 extract_respondent_role.py [path/to/sbmo-form-answers.csv]
"""

import csv
import os
import re
import sys
import unicodedata
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
VALIDATION_ROOT = os.path.dirname(HERE)  # sbmo/validation
SBMO_ROOT = os.path.dirname(VALIDATION_ROOT)  # sbmo
DISSERTATION_ROOT = os.path.dirname(SBMO_ROOT)  # sibling of sbmo, dissertation-paper, validations
DEFAULT_RAW = os.path.join(DISSERTATION_ROOT, "validations", "sbmo-form-answers.csv")
RAW = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_RAW
DERIVED = os.path.join(VALIDATION_ROOT, "survey-derived")
os.makedirs(DERIVED, exist_ok=True)

COL_ROLE = 7  # "Nome e cargo do respondente"

RULES = [
    ("Founder", [r"fundador"]),
    ("Leadership", [r"\bceo\b", r"\bcto\b", r"diretor", r"head of",
                     r"coordenador", r"l[ií]der", r"\bpo\b"]),
    ("Technical Advisory", [r"advisor", r"respons[aá]vel t[eé]cnico"]),
    ("Product & Design", [r"design", r"\bux\b", r"\bui\b"]),
    ("Engineering", [r"desenvolvedor", r"developer", r"full ?stack",
                      r"analista de sistema", r"engenh"]),
]
FALLBACK = "Other / Analyst"


def strip_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s)
                    if unicodedata.category(c) != "Mn")


def classify(raw_cell: str) -> str:
    norm = strip_accents(raw_cell).lower()
    for category, patterns in RULES:
        if any(re.search(p, norm) for p in patterns):
            return category
    return FALLBACK


def load():
    with open(RAW, encoding="utf-8") as f:
        rows = list(csv.reader(f))
    return rows[0], rows[1:]


def main():
    _, data = load()
    n = len(data)
    cases = [f"Case{str(i + 1).zfill(2)}" for i in range(n)]

    categories = []
    for row in data:
        cell = row[COL_ROLE] if COL_ROLE < len(row) else ""
        categories.append(classify(cell))

    out_path = os.path.join(DERIVED, "respondent_role_categories.csv")
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["case_id", "respondent_role_category"])
        for case_id, cat in zip(cases, categories):
            w.writerow([case_id, cat])

    counts = Counter(categories)
    order = [c for c, _ in RULES] + [FALLBACK]
    print(f"Respondent role categories ({n} cases) -> {out_path}\n")
    for cat in order:
        c = counts.get(cat, 0)
        print(f"  {cat:<20s} {c:2d}  ({100 * c / n:5.1f}%)")
    assert sum(counts.values()) == n


if __name__ == "__main__":
    main()
