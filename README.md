# SBMO — Software Business Model Ontology

OWL ontology for **Software Business Models**, developed as part of a master's dissertation at PPGES/UNIPAMPA. Grounded on a Systematic Mapping Study (SMS) of 67 primary studies (2014–2024).

## Metadata

| Field | Value |
|-------|-------|
| **IRI** | `https://rafaelc-rb.github.io/sbmo` |
| **Version IRI** | `https://rafaelc-rb.github.io/sbmo/1.0` |
| **Format** | OWL 2 (RDF/XML) |
| **Tool** | Protégé Desktop 5.x |
| **Reasoner** | Pellet |
| **File** | [`sbmo.rdf`](sbmo.rdf) |

## Ontology metrics

| Metric | Count |
|--------|-------|
| Top-level classes | 14 |
| Subclasses | 75 |
| Object Properties | 13 |
| Data Properties | 8 |
| Individuals | 0 (pure T-Box distribution) |
| Axioms | Disjointness (EcosystemRole, NetworkEffectType) + `minQualifiedCardinality` restrictions |
| CQs support | **7/7 structurally supported** (T-Box); empirical execution with real cases is planned |

## Scope

| Dimension | Key concepts |
|-----------|-------------|
| Monetization & pricing | Subscription, usage, transaction, advertising, perpetual license, support, marketplace fees, open core, dual licensing; cost-based, pay-as-you-go, value-based, freemium |
| Delivery & deployment | Multi-tenant SaaS, single-tenant, on-premises, mobile, desktop, hybrid |
| Market segmentation | B2B, B2C, SME, Enterprise, Government, Developer tools |
| Ecosystem dynamics | Standalone, two-sided platform, marketplace, OEM component, plugin/complement; direct, cross-sided, data-driven network effects |
| Go-to-market | Direct sales, product-led growth, partners, digital marketing, marketplaces, referral |
| Product & intellectual property | Product/service type, IP regime, pricing base unit |
| Adoption & implementation | Success factors, challenges, mitigation strategies |

## Validation status

The current repository intentionally ships a **clean T-Box** (no synthetic A-Box individuals). Real-case instantiation is planned in the empirical validation stage with software ventures.

The empirical validation data (31 anonymized cases), questionnaire instrument, and Informed Consent are published on Zenodo: [`validation/zenodo-package/`](validation/zenodo-package/README.md), DOI [10.5281/zenodo.22001648](https://doi.org/10.5281/zenodo.22001648).

## Data gap policy

The SMS is the primary evidence source. If any element lacks SMS support, the gap must be documented in [`docs/DATA_GAPS.md`](docs/DATA_GAPS.md) before complementary research is conducted.

## Structure

```
├── sbmo.rdf                  # Ontology (Protégé)
├── docs/
│   ├── CONTEXT.md            # Project overview and scope
│   ├── COMPETENCY_QUESTIONS.md # CQ1–CQ7 and structural support status
│   ├── DATA_GAPS.md          # Evidence gaps and resolution tracking
│   ├── DESIGN_DECISIONS.md   # Non-trivial modeling decisions log
│   └── FUTURE_WORK.md        # Extensions outside current evidence scope
└── .cursor/rules/
    └── ontology-modeling.mdc # Local assistant guidance for ontology tasks
```

## Related repositories

| Repository | Content |
|------------|---------|
| `sbm-ontology-dissertation` | Dissertation (LaTeX) |
| `sbm-sms-data-repo` | SMS extraction data, coding scheme, statistics |
| `sbm-sms-journal` | SMS journal article (IEEE) |
| `ontology-papers-for-reference` | Reference papers on ontology engineering |

## Author

**Rafael C. Ribeiro** — PPGES, Federal University of Pampa (UNIPAMPA), Brazil.
