# SBMO — Software Business Model Ontology

OWL ontology for **Software Business Models**, developed as part of a master's dissertation at PPGES/UNIPAMPA. Grounded on a Systematic Mapping Study (SMS) of 63 primary studies (2014–2024).

## Metadata

| Field | Value |
|-------|-------|
| **IRI** | `https://rafaelc-rb.github.io/sbmo` |
| **Version IRI** | `https://rafaelc-rb.github.io/sbmo/1.1` |
| **Format** | OWL 2 DL (RDF/XML); DL expressivity ALCQ(D) |
| **Tool** | Protégé Desktop 5.x |
| **Reasoner** | Pellet |
| **File** | [`sbmo.rdf`](sbmo.rdf) |

## Ontology metrics

| Metric | Count |
|--------|-------|
| Classes (total) | 93 |
| Top-level classes | 14 |
| Subclasses | 75 |
| Defined classes | 4 (`owl:equivalentClass`; inferred subclasses of `SoftwareBusinessModel`) |
| Object Properties | 13 |
| Data Properties | 8 |
| Individuals | 0 (pure T-Box distribution) |
| Logical axioms | 150: subclass, domain/range, 8 `minQualifiedCardinality` restrictions, 4 class definitions, 21 disjointness axioms (77 disjoint pairs) |
| CQs support | **7/7 structurally supported** (T-Box) and answered over 31 real cases (A-Box, [`validation/`](validation/README.md)) |

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

The current repository intentionally ships a **clean T-Box** (no synthetic A-Box individuals). The 31 real cases of the empirical validation live in a separate A-Box that imports the T-Box ([`validation/protege/sbmo-validation-abox.ttl`](validation/protege/sbmo-validation-abox.ttl)), together with the competency-question checks, the reasoning demonstration over the defined classes, and two negative tests ([`validation/README.md`](validation/README.md)).

The empirical validation data (31 anonymized cases), questionnaire instrument, and Informed Consent are published on Zenodo: [`validation/zenodo-package/`](validation/zenodo-package/README.md), DOI [10.5281/zenodo.22001648](https://doi.org/10.5281/zenodo.22001648).

## Changes

### 1.1 (2026-10-20)

Revisions requested by the defense committee (R28, R29, R30 of the dissertation revision tracker).

- **Defined classes** (`owl:equivalentClass`): `SubscriptionSaaSModel`, `FreemiumSubscriptionModel`, `PlatformBusinessModel`, `NetworkedPlatformModel`. Pellet classifies the cases into them and infers `NetworkedPlatformModel` ⊑ `PlatformBusinessModel` (DD-011).
- **Disjointness revised** (DD-012): `SoftwareBusinessModel` and the ten configuration dimensions are pairwise disjoint; new pairs within revenue sources, delivery modes, customer types, ecosystem roles, acquisition channels, and IP regimes; `Marketplace` is no longer disjoint with `TwoSidedPlatform`.
- **OWL 2 DL profile**: `dcterms:license` declared as an annotation property; `hasLaunchYear` and `hasSourceYear` ranges changed from `xsd:gYear` (not in the OWL 2 datatype map) to `xsd:integer`, with the A-Box literals converted accordingly. ROBOT reports no profile violation for the T-Box or for T-Box + A-Box.
- **SMS evidence in `rdfs:comment`** recounted over the 63 primary studies of the corrected corpus (previously 67).
- Version IRI `…/sbmo/1.1`, `owl:versionInfo "1.1"`.

### 1.0

Version evaluated in the dissertation defense (14 top-level classes, 75 subclasses, 13 object properties, 8 data properties).

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
