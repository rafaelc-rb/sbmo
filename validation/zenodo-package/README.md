# SBMO empirical validation (Zenodo deposit package)

Supporting materials for the empirical validation reported in the
dissertation *Software Business Model Ontology (SBMO)* (PPGES/UNIPAMPA),
Chapter 7, "Ontology Evaluation": a questionnaire-based survey of 31 real
software business models, used to instantiate and evaluate the SBMO ontology
(`https://github.com/rafaelc-rb/sbmo`).

This directory is meant to be uploaded as-is (zipped) to Zenodo as a single
dataset deposit, referenced from the dissertation by its DOI.

## Contents

```
zenodo-package/
├── README.md                          <- this file
├── informed_consent/
│   └── informed_consent.md            <- Termo de Consentimento (verbatim, Portuguese)
├── instrument/
│   └── questionnaire.md               <- questionnaire structure (verbatim, Portuguese), no answers
├── data/
│   ├── cases_normalized.csv           <- 31 cases, SBMO classes, anonymized
│   ├── respondent_role_categories.csv <- 31 cases, respondent role category, anonymized
│   ├── label_to_class_mapping.md      <- Portuguese form label -> SBMO class mapping
│   ├── data_dictionary.md             <- column-by-column description of every CSV here
│   └── statistical_analysis/          <- aggregate outputs behind Chapter 7's statistical analysis
└── scripts/
    ├── reproduce_sbmo_analysis_fixed.r  <- R script that produced data/statistical_analysis/
    └── extract_respondent_role.py       <- Python script that produced respondent_role_categories.csv
```

## Anonymity

The raw Google Forms export (respondent name, company name, product name,
free-text answers) is **not included** in this package and is never
published, per the confidentiality promise of the Informed Consent
(`informed_consent/`). Every file under `data/` is either:

- an anonymized, aggregate derivative (`cases_normalized.csv`,
  `respondent_role_categories.csv`, everything in `statistical_analysis/`),
  indexed by opaque `Case01`-`Case31` identifiers and, where organizations or
  products repeat, by pseudonymous sequential cluster IDs that carry no
  information about the underlying name; or
- documentation with no case-level data at all (`data_dictionary.md`,
  `label_to_class_mapping.md`).

See `data/data_dictionary.md` for exactly what each column contains, and
`sbmo/validation/README.md` (in the ontology repository) for the full
anonymization rationale, including why free-text fields (business model
description, "Other" specify fields, additional comments) are never
published: an automated scan of those fields on this survey found a
respondent's real first name leaked in an unrelated free-text answer, so
they cannot be safely redacted.

## Provenance of `instrument/` and `informed_consent/`: fully verified (2026-08-18)

`instrument/` and `informed_consent/` were first drafted from the
form-generator script (`sbmo/scripts/sbmo_create_individual_form.gs`), not
from the live Google Form, and an initial spot check (fetching the public
form URL) found the Informed Consent draft to be incomplete relative to the
real form. On 2026-08-18, Rafael provided a full 13-page PDF export of the
live Google Form ("SBMO - Validação de Modelo de Negócio de Software -
Google Formulários.pdf"), which was compared line by line against both
`instrument/` and `informed_consent/`. Both were rewritten as verbatim
transcriptions of that PDF and are now confirmed accurate:

- **Informed Consent**: the PDF confirmed the earlier finding that the
  script draft was incomplete: it omits the CNS Resolution 466/2012
  reference, the right-to-a-copy and right-to-revoke clauses in the consent
  checkbox text, and uses a personal Gmail address instead of the
  institutional UNIPAMPA e-mails actually shown on the form.
  `informed_consent.md` is now the full, verbatim Portuguese text from
  the PDF.
- **Questionnaire instrument**: all 15 sections, 40 questions, help texts,
  and option lists in the PDF match the script exactly, with no
  discrepancy (this also independently confirms the earlier cross-check
  against the 31 real responses in `sbmo-form-answers.csv`, since every
  option value actually selected by a respondent already matched the
  script verbatim). `instrument/questionnaire.md` is now the full,
  verbatim transcription.

No English translation is included: no evidence was found that the
English-language variant of the form (which the script can also generate)
was ever actually deployed, and all 31 raw responses use Portuguese field
values, so only the Portuguese form is a confirmed data-collection
instrument.

## Reproducing the statistical analysis

`scripts/reproduce_sbmo_analysis_fixed.r` requires the raw CSV (not included
here, for the anonymity reasons above) with the same column layout described
by `instrument/questionnaire.md`. Running it against that raw file
reproduces every CSV under `data/statistical_analysis/`. Requires base R
only (fixed seed `20260815`, 9,999 permutations per hypothesis test); no
additional R packages are needed.

`scripts/extract_respondent_role.py` requires the same raw CSV and reproduces
`data/respondent_role_categories.csv`; standard-library Python 3 only.

## Citation

Cite this dataset as: Ribeiro, R. C. *SBMO Empirical Validation Dataset*
(2026), Zenodo. DOI: [10.5281/zenodo.22001648](https://doi.org/10.5281/zenodo.22001648).

Related to the dissertation: Ribeiro, R. C. *Software Business Model
Ontology (SBMO)*, master's dissertation, PPGES/UNIPAMPA, 2026, and to the
ontology repository: `https://github.com/rafaelc-rb/sbmo`.

## License

Recommended: **CC BY 4.0** for the data and documentation in this package
(consistent with the MIT-licensed `sbmo.rdf` ontology and code in the
sibling repository). Confirm the final choice on Zenodo when creating the
deposit; Zenodo lets you pick the license at upload time.
