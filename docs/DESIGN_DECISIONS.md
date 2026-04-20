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

### DD-007: Add three new MVP dimensions (ProductOrServiceType, IntellectualPropertyRegime, PricingBaseUnit)

| Field | Value |
|-------|-------|
| **Date** | 2026-04-20 |
| **Decision** | Add three new top-level classes (`ProductOrServiceType`, `IntellectualPropertyRegime`, `PricingBaseUnit`) with dedicated object properties linking them to `SoftwareBusinessModel`, and populate subclasses from SMS closed-ended extraction categories. |
| **New classes** | ProductOrServiceType (7 subclasses: Application, Platform, ManagedService, APIService, DataProduct, Infrastructure, SDK), IntellectualPropertyRegime (6 subclasses: Proprietary, PermissiveOpenSource, OpenSource, DualLicense, OpenCore, Copyleft), PricingBaseUnit (7 subclasses: UserSeat, TransactionBased, ComputingTime, RevenueSharing, APICalls, Storage, Device) |
| **New object properties** | `hasProductOrServiceType` (SBM → ProductOrServiceType), `hasIntellectualPropertyRegime` (SBM → IntellectualPropertyRegime), `hasPricingBaseUnit` (SBM → PricingBaseUnit) |
| **Cardinality** | `hasProductOrServiceType min 1 ProductOrServiceType` on SoftwareBusinessModel (mandatory). `hasIntellectualPropertyRegime` and `hasPricingBaseUnit` left unconstrained (optional) per MVP_SCOPE_PLAN.md §4. |
| **Disjointness** | Not applied. ProductOrServiceType values can co-occur (e.g., Application + Platform). IntellectualPropertyRegime includes hybrid forms (DualLicense, OpenCore). PricingBaseUnit values can co-occur (e.g., UserSeat + Storage). |
| **Excluded values** | "Others" (catch-all, not a valid ontological category) from all three dimensions. "MAU" from PricingBaseUnit (0 occurrences in SMS). |
| **Rationale** | These three dimensions were identified in MVP_SCOPE_PLAN.md as necessary to avoid relevant gaps during validation with real software cases. Each is directly grounded in SMS extraction questions (EQ08, EQ10, EQ13) and their closed-ended category distributions. |
| **Evidence** | EQ08 distribution (q_08, 7 categories with evidence), EQ10 distribution (q_10, 6 categories), EQ13 distribution (q_13, 7 categories with evidence > 0); MVP_SCOPE_PLAN.md §3 and §4 |

### DD-008: Data properties — intrinsic and documentation subsets

| Field | Value |
|-------|-------|
| **Date** | 2026-04-20 |
| **Decision** | Add 8 `owl:DatatypeProperty` attributes to `SoftwareBusinessModel`: 3 intrinsic (`hasBillingPeriodicity`, `hasLaunchYear`, `hasPricingDescription`) and 5 documentation (`hasCompanyName`, `hasProductName`, `hasEvidenceSource`, `hasSourceYear`, `hasCaseDescription`). |
| **Rationale** | The ontology was 100% relational (only object properties). Data properties are required by MVP_SCOPE_PLAN.md to avoid reducing the ontology to a taxonomy and to support traceable real-case validation. |
| **Intrinsic subset criteria** | Each candidate was evaluated by: (1) SMS evidence support, (2) usefulness for distinguishing real cases, (3) contribution beyond existing classes/object properties. |
| **Included intrinsic** | `hasBillingPeriodicity` (EQ15, 26/67 articles; complements PricingStrategy), `hasLaunchYear` (EQ29; temporal analysis), `hasPricingDescription` (EQ14/EQ15; captures free-text nuances) |
| **Excluded intrinsic** | `hasBasePriceAmount` (volatile, currency-dependent), `hasTrialPeriodDays` (too granular, not universal), `hasRevenueSharePercentage` (only applies to marketplace/platform subset) |
| **Documentation properties** | All 5 candidates from MVP_SCOPE_PLAN.md §6 included. Minimum traceability layer for real-case validation. |
| **Domain/Range** | All properties: domain `SoftwareBusinessModel`. Ranges: `xsd:string` for textual attributes, `xsd:gYear` for year attributes. |
| **Evidence** | EQ14, EQ15, EQ29 (SMS extraction); MVP_SCOPE_PLAN.md §5 and §6 |

### DD-009: Remove exemplar individuals and clean TBox for real-case validation

| Field | Value |
|-------|-------|
| **Date** | 2026-04-20 |
| **Decision** | Remove all 26 exemplar individuals (2 SBM instances + 24 value individuals) from `sbmo.rdf`. The ontology now contains only the TBox (classes, properties, restrictions). |
| **Motivation** | (1) The existing exemplar individuals (`SaaS_B2B_Subscription`, `Freemium_B2C_Platform`) violate the new `hasProductOrServiceType min 1` cardinality constraint (DD-007), causing reasoner inconsistency. (2) The validation plan involves real companies at UNIPAMPA's technology campus; synthetic individuals would pollute the Protégé workspace and interfere with the research. |
| **Audit result** | Relational audit confirmed all 14 top-level classes are connected via object properties (domain, range, or both). All 66 subclasses are correctly placed. No orphan classes or isolated branches. MitigationStrategy connects indirectly to SBM through ImplementationChallenge (by design, supports CQ6). |
| **Supersedes** | DD-005 (viability-scoped evaluation with 2 exemplars is no longer the active validation approach; replaced by real-case research with companies). |
| **Evidence** | MVP_SCOPE_PLAN.md §7 (real-case validation); DD-007 cardinality conflict; research design (company interviews at technology campus) |

---

*New decisions follow the same template (DD-NNN).*
