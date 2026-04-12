## Ontology design decisions log

Non-trivial modeling decisions, their rationale, and alternatives considered.

---

### DD-001: Top-level class structure

| Field | Value |
|-------|-------|
| **Date** | 2026-02-14 |
| **Decision** | 11 top-level classes under `owl:Thing`, each mapping to a SMS dimension. |
| **Classes** | SoftwareBusinessModel, RevenueSource, PricingStrategy, DeliveryMode, CustomerType, EcosystemRole, AcquisitionChannel, NetworkEffectType, SuccessFactor, ImplementationChallenge, MitigationStrategy |
| **Rationale** | Mirrors SMS coding scheme structure and directly supports CQ1–CQ7. |
| **Rejected alternatives** | (a) Fewer classes with deeper nesting — obscures dimensional structure. (b) BMC 9 building blocks — too generic, not software-specific. |
| **Evidence** | SMS dimensions (Ch. 5), CQ1–CQ7 (Ch. 6) |

### DD-002: Subclass values as classes (not individuals)

| Field | Value |
|-------|-------|
| **Date** | 2026-02-14 |
| **Decision** | Populate subclasses using specific SMS values (e.g., SubscriptionRevenue, MultiTenantSaaS, B2B) modeled as **subclasses**, not individuals. |
| **Rationale** | Empirically grounded (each value has quantified frequency across 67 studies). Subclasses allow: (a) future specialization (e.g., MonthlySubscription), (b) class-level axioms (disjointness), (c) reasoner classification. Individuals reserved for concrete SBM instances (e.g., "Spotify's model"). |
| **Rejected alternatives** | Named individuals per value — simpler but prevents taxonomic refinement and class-level axioms. |
| **Evidence** | SMS closed-ended statistics, open-ended coding scheme; Noy & McGuinness (2001) |

### DD-003: Disjointness scope

| Field | Value |
|-------|-------|
| **Date** | 2026-02-14 |
| **Decision** | Apply `owl:AllDisjointClasses` only to EcosystemRole subtypes (StandaloneProduct, TwoSidedPlatform, Marketplace) and NetworkEffectType subtypes (DirectNetworkEffect, CrossSidedNetworkEffect, DataDrivenNetworkEffect). |
| **Rationale** | These subtypes are mutually exclusive by definition (an ecosystem role cannot be both standalone and marketplace). Other dimensions (e.g., RevenueSource subtypes) can co-occur in a single SBM, so disjointness would be incorrect. |
| **Evidence** | SMS coding scheme; CQ4 ecosystem–network effect analysis |

### DD-004: Existential restrictions on SoftwareBusinessModel

| Field | Value |
|-------|-------|
| **Date** | 2026-02-14 |
| **Decision** | Add `someValuesFrom` restrictions: every SoftwareBusinessModel must have at least one RevenueSource, DeliveryMode, and EcosystemRole. |
| **Rationale** | These three dimensions are the minimum viable configuration of an SBM per the SMS evidence. Other properties (PricingStrategy, CustomerType, AcquisitionChannel) are common but not universally reported. |
| **Evidence** | CQ7; SMS dimensional coverage analysis |

### DD-005: Viability-scoped evaluation

| Field | Value |
|-------|-------|
| **Date** | 2026-02-14 |
| **Decision** | Evaluate ontology via 7 competency questions (SPARQL-DL) with 2 exemplar individuals, accepting 5/7 as sufficient for viability demonstration. |
| **Rationale** | CQ5 and CQ6 require individual-level assertions (`hasSuccessFactor`, `facesChallenge`, `mitigates`) that depend on per-paper granularity not available in SMS aggregates (see GAP-002). The class hierarchy and properties fully support these CQs structurally. |
| **Evidence** | CQ1–CQ4, CQ7 SPARQL results; GAP-002, GAP-003 |

### DD-006: Replace existential restrictions with cardinality constraints

| Field | Value |
|-------|-------|
| **Date** | 2026-04-12 |
| **Decision** | Replace `someValuesFrom` (existential) restrictions with `minQualifiedCardinality 1` on SoftwareBusinessModel. Extend cardinality constraints to all 6 core object properties. Add `minQualifiedCardinality 1` on MitigationStrategy for `mitigates`. |
| **Motivation** | Dissertation committee (banca) identified that existential restrictions (`∃R.C`) do not enforce per-individual obligation under the Open World Assumption. Cardinality restrictions (`≥1 R.C`) make the intent explicit: each SBM individual must have at least one value for each core property. |
| **Properties constrained (SoftwareBusinessModel)** | `hasDeliveryMode min 1 DeliveryMode` (EQ09, 95.5%), `hasEcosystemRole min 1 EcosystemRole` (EQ16, 100%), `hasRevenueSource min 1 RevenueSource` (EQ12, 95.5%), `hasPricingStrategy min 1 PricingStrategy` (EQ14, 88%), `targetsCustomerType min 1 CustomerType` (EQ04, 100%), `usesAcquisitionChannel min 1 AcquisitionChannel` (EQ18, 92.5%) |
| **Properties constrained (MitigationStrategy)** | `mitigates min 1 ImplementationChallenge` (CQ6, by definition) |
| **Properties left unconstrained** | `facesChallenge` (qualitative, not universal), `hasSuccessFactor` (qualitative, not universal), `exhibitsNetworkEffect` (4.5% have "None") |
| **No max cardinality** | All constrained properties allow multiple values per SMS evidence (multiple selection questions, co-occurrence patterns). |
| **Supersedes** | DD-004 (expands scope from 3 core properties to 6 + MitigationStrategy) |
| **Evidence** | SMS closed-ended statistics (EQ04, EQ09, EQ12, EQ14, EQ16, EQ18); CQ1–CQ7; banca feedback |

---

*New decisions follow the same template (DD-NNN).*
