## Project overview

This repository contains the **Software Business Model Ontology (SBMO)** in OWL 2 (RDF/XML), modeled in Protégé Desktop.  
The ontology is part of a master's dissertation at PPGES/UNIPAMPA and is designed for practical validation with real software ventures.

### Evidence base

The ontology is grounded on a **Systematic Mapping Study (SMS)** — 67 peer-reviewed studies (2014–2024):

- **61 codes** in 9 classes and 35 subclasses
- **12 closed-ended** + **21 open-ended** extraction questions
- **4,630 classifications** total
- **10 research questions** (RQ1–RQ10)

### Ontology dimensions (from SMS)

1. Monetization & pricing
2. Delivery & deployment
3. Market segmentation
4. Ecosystem dynamics
5. Go-to-market
6. Product & intellectual property
7. Adoption & implementation

### Current ontology status

- Pure T-Box distribution (`sbmo.rdf`) with no named individuals.
- Version 1.1: 93 classes (14 top-level, 75 subclasses, 4 defined classes), 13 object properties, and 8 data properties; OWL 2 DL, expressivity ALCQ(D).
- Minimum completeness constraints modeled with `minQualifiedCardinality`; disjointness between dimensions and within dimensions where it holds by definition (DD-012).
- CQ1–CQ7 are structurally supported by the ontology schema and answered over 31 real cases (`validation/`).

### Related repositories

| Repository | Content |
|------------|---------|
| `sbm-sms-data-repo` | SMS extraction data, coding scheme, statistics |
| `sbm-sms-journal` | SMS journal article (IEEE) |
| `sbm-ontology-dissertation` | Dissertation (LaTeX) |
| `ontology-papers-for-reference` | Reference papers on ontology engineering |

### Documentation index

| File | Purpose |
|------|---------|
| [`COMPETENCY_QUESTIONS.md`](COMPETENCY_QUESTIONS.md) | CQ1–CQ7 — what the ontology must answer |
| [`DATA_GAPS.md`](DATA_GAPS.md) | Evidence gaps requiring complementary research |
| [`DESIGN_DECISIONS.md`](DESIGN_DECISIONS.md) | Modeling decisions log |
| [`FUTURE_WORK.md`](FUTURE_WORK.md) | Proposed extensions beyond current SMS scope |
