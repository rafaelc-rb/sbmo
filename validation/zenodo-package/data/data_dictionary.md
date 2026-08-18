# Data dictionary

All files in `data/` are anonymized, aggregate derivatives of the raw Google
Forms export (`sbmo-form-answers.csv`), which is **not** included in this
package and is never published (see `../README.md`, "Anonymity"). No file
listed here contains a respondent name, company name, or product name.

## `cases_normalized.csv`

31 rows, one per case (`Case01`..`Case31`), matching the order of the
dissertation's `Case01`-`Case31` identifiers. Every controlled-vocabulary
answer is already mapped to its SBMO ontology class local name (see
`label_to_class_mapping.md` for the Portuguese label -> class mapping used to
build this file). Multi-select dimensions use `;` to separate multiple
selected classes within a cell.

| Column | Meaning |
|---|---|
| `case_id` | Opaque case identifier (`Case01`..`Case31`) |
| `product_type` .. `mitigation` | SBMO class(es) selected for each of the 13 dimensional questions (Sections 2–14 of the questionnaire) |
| `*_other` | 1 if the free-text "Other" escape hatch was selected for that dimension, blank otherwise (no free text itself is stored) |
| `knowledge` | Respondent's self-assessed knowledge of the business model, 1 (low) to 5 (high); blank if not answered |
| `operational` | Operational status: `Sim` (Yes/Operational), `Não` (No/Planning), `Parcialmente` (Partially) |
| `launch_year` | Reported launch year of the product/service |

## `respondent_role_categories.csv`

31 rows (`case_id`, `respondent_role_category`). The respondent role/function
was extracted from the raw "name and role" field and classified into one of
six categories (Founder, Leadership, Technical Advisory, Product & Design,
Engineering, Other / Analyst) by keyword matching on the full raw string; the
name portion of that field was never extracted or stored anywhere, including
in memory beyond the classification step. See
`sbmo/validation/scripts/extract_respondent_role.py` for the classification
logic.

## `statistical_analysis/`

Aggregate outputs of the reproducible R analysis (`../scripts/reproduce_sbmo_analysis_fixed.r`),
underlying Chapter 7 ("Ontology Evaluation"), Section "Statistical Analysis
of the Empirical Validation", of the dissertation:

| File | Contents |
|---|---|
| `operational_status.csv` | Count and percentage of cases per operational status |
| `coverage.csv` | Per-dimension controlled-vocabulary coverage (valid answers, "Other" count, coverage ratio, number of observed classes) |
| `option_frequencies.csv` | Count and percentage of each selected option, per dimension (Portuguese labels, as collected) |
| `rv_associations.csv` | RV coefficient, permutation-test $p$-value, and Benjamini-Hochberg $q$-value for each of the 6 CQ1-CQ6 dimension pairs |
| `sensitivity_analysis.csv` | Same RV coefficients recomputed on the 27-observation subsample (one response per organization) |
| `strongest_binary_pairs.csv` | Strongest binary ($\phi$-coefficient, Fisher's exact test) option pair per competency-question pair (Portuguese labels) |
| `processed_data.csv` | Full anonymized processed matrix: `CaseID`, pseudonymous `OrganizationClusterID`/`ProductClusterID` (sequential IDs, not derived from or reversible to the real names), `LaunchYear`, `KnowledgeScore`, `OperationalStatus`, and one binary (0/1) indicator column per controlled-vocabulary option (Portuguese labels, as collected) |

`OrganizationClusterID`/`ProductClusterID` let a reader reproduce the
sensitivity analysis (Section 7.4.3 of the dissertation) without any
identifying information: they only indicate which rows share the same
organization or product, not what that organization or product is.
