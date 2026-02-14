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

---

*New decisions follow the same template (DD-NNN).*
