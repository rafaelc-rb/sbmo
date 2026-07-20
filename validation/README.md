# SBMO empirical validation

Artifacts supporting the empirical validation reported in the dissertation
(Chapter 6, "Ontology Evaluation"): a Google Forms survey of 31 real software
business models, mapped onto the SBMO vocabulary and instantiated into an
anonymized A-Box. Everything here keeps the canonical T-Box `../sbmo.rdf`
**untouched** and treats the survey data as **anonymous** and **publishable**.

## Where the raw survey data lives

The raw Google Forms export (`sbmo-form-answers.csv`) contains respondent,
company, and product identifiers under an informed-consent confidentiality
promise. It is **never committed to this (or any) repository**. It lives
locally in a sibling, non-versioned directory:

```
dissertation/
├── sbmo/               <- this repo
│   └── validation/      <- you are here (versioned, anonymized)
├── dissertation-paper/  <- the dissertation repo (LaTeX tables are written here)
└── validations/         <- LOCAL ONLY, not a git repo, not versioned anywhere
    └── sbmo-form-answers.csv
```

The scripts in `scripts/` default to reading from that sibling path; pass an
explicit path as the first argument to override it.

**`survey-derived/cases_normalized.csv` is the versioned, anonymized stand-in
for the raw CSV.** It has the same 31 rows, indexed by opaque `case_id`
(`Case01`..`Case31`), with every controlled-vocabulary answer mapped to its
SBMO class plus `knowledge`/`operational`/`launch_year` — everything the
dissertation tables and the A-Box are built from. It intentionally excludes
all free-text fields (business model description, pricing description,
"other" escape-hatch answers, challenge-mitigation mapping, comments): an
automated scan of those fields for this survey turned up not just expected
product/company name mentions but also a respondent's first name leaked in an
unrelated free-text answer, so they cannot be safely redacted and published
verbatim. No dissertation text quotes them directly (the Discussion section
paraphrases recurring themes only), so nothing is lost by keeping them
private-only.

## Contents (this directory)

- `scripts/sbmo_mapping.py` — Portuguese label -> SBMO class mapping (shared).
- `scripts/analyze_survey.py` — anonymized analysis; writes `survey-derived/`
  (aggregate data) and the dissertation's LaTeX table fragments (see below).
- `scripts/build_abox.py` — builds the anonymized A-Box from the raw CSV.
- `scripts/mapping.md` — human-readable review sheet of the mapping.
- `survey-derived/` — generated, anonymized outputs: `cases_normalized.csv`
  (CaseID + mapped categories, no identifiers) and `summary.json` (aggregate
  figures: counts, coverage, frequencies, CQ cross-check).
- `protege/sbmo-validation-abox.ttl` — the anonymized A-Box (31 cases) that
  `owl:imports` the T-Box.
- `protege/queries/CQ1..CQ7.rq` — SPARQL-DL queries, one per competency
  question.

Note: the LaTeX table fragments (`cq_empirical_results.tex`, `coverage.tex`,
`frequencies.tex`) are **not** stored in this repo. They are presentation
artifacts for one specific document, not ontology evidence, so
`analyze_survey.py` writes them directly into the sibling
`dissertation-paper/assets/ontology/tables/` (a versioned part of the
dissertation repo instead).

## Reproduce the analysis

```
cd scripts
python3 analyze_survey.py      # -> ../survey-derived/ (anonymized) and
                                #    ../../../dissertation-paper/assets/ontology/tables/*.tex
python3 build_abox.py          # -> ../protege/sbmo-validation-abox.ttl
```
Only the Python standard library is required. Both scripts assume the sibling
`dissertation/validations/sbmo-form-answers.csv` and `dissertation/dissertation-paper/`
layout described above; pass a path explicitly to `analyze_survey.py` if your
raw CSV lives elsewhere (the dissertation-paper output path is not
currently overridable via CLI).

## Run the competency questions in Protégé (manual step)

1. Open `protege/sbmo-validation-abox.ttl` in Protégé 5.x. It imports the
   T-Box, so both load together (keep `../sbmo.rdf` reachable, or import by
   IRI). Prefer the official Protégé distribution
   (https://github.com/protegeproject/protege-distribution/releases) over a
   distro package — e.g. the Arch Linux `protege` package ships without any
   reasoner or plugin preinstalled, which required extra setup.
2. Install the **Pellet** reasoner plugin if not already present (File >
   Check for plugins). Start it (Reasoner > Pellet > Start reasoner). Confirm
   the ontology is **consistent** (no warnings).
3. `queries/CQ1..CQ7.rq` are the formal SPARQL-DL query templates (used in
   the dissertation text), but the community **SPARQL Query plugin (Snap
   SPARQL) is broken on modern Protégé Desktop** — a known, unresolved
   upstream bug (see `protege/dl_queries.md`). Use the built-in **DL Query**
   tab instead: it uses the same Pellet reasoner and is unaffected by the
   bug. `protege/dl_queries.md` gives the equivalent Manchester Syntax
   expression for each CQ and the expected result count.
4. Record the number of matching individuals per CQ. The expected counts
   (computed independently by `analyze_survey.py`) are in
   `survey-derived/summary.json` under `"cq"` — they should match.

## Structural check (OOPS!)

Submit `../sbmo.rdf` at http://oops.linkeddata.es and record the reported
pitfalls (critical / important / minor). Results already folded into the
dissertation: 0 critical, 1 important (P41, no license — fixed by the
`dcterms:license` annotation on the ontology header), 3 minor (P07, P08, P13).
