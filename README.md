# SBMO — Software Business Model Ontology

OWL ontology for **Software Business Models**, developed as part of a master's dissertation at PPGES/UNIPAMPA. Grounded on a Systematic Mapping Study (SMS) of 67 primary studies (2014–2024).

## Metadata

| Field | Value |
|-------|-------|
| **IRI** | `https://rafaelc-rb.github.io/sbmo` |
| **Version IRI** | `https://rafaelc-rb.github.io/sbmo/1.0` |
| **Format** | OWL 2 (RDF/XML) |
| **Tool** | Protégé Desktop 5.x |
| **File** | [`sbmo.rdf`](sbmo.rdf) |

## Scope

| Dimension | Key concepts |
|-----------|-------------|
| Monetization & pricing | Subscription, usage, transaction, advertising, perpetual license; cost-based, pay-as-you-go, value-based, freemium |
| Delivery & deployment | Multi-tenant SaaS, single-tenant, on-premises, mobile, desktop, hybrid |
| Market segmentation | B2B, B2C, SME, Enterprise |
| Ecosystem dynamics | Standalone, two-sided platform, marketplace; direct, cross-sided, data-driven network effects |
| Go-to-market | Direct sales, product-led growth, partners, digital marketing, marketplaces |
| Adoption & implementation | Success factors, challenges, mitigation strategies |

## Data gap policy

The SMS is the primary evidence source. If any element lacks SMS support, the gap must be documented in [`docs/DATA_GAPS.md`](docs/DATA_GAPS.md) before complementary research is conducted.

## Structure

```
├── sbmo.rdf                  # Ontology (Protégé)
├── docs/
│   ├── CONTEXT.md            # Project context (for AI)
│   ├── COMPETENCY_QUESTIONS.md
│   ├── DATA_GAPS.md
│   └── DESIGN_DECISIONS.md
└── .cursor/rules/
    └── ontology-modeling.mdc # AI modeling rules
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
