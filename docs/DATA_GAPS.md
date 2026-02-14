## Data gaps tracker

Evidence gaps identified during ontology modeling where SMS data is insufficient and complementary research is needed.

### Policy

1. Record the gap **before** adding any element without SMS evidence.
2. Specify what is needed and suggest a research approach.
3. Update status when resolved, citing the new source.

**Status**: `open` | `in-progress` | `resolved` | `deferred`

---

### GAP-001: Dalepiane's SBM taxonomy

| Field | Value |
|-------|-------|
| **Element** | CQ7 — Multi-dimensional SBM classification |
| **Gap** | Taxonomy by Igor Dalepiane (unpublished) for classifying SBMs across delivery, monetization, and ecosystem dimensions. Content not available in any repository. |
| **Impact** | CQ7 cannot be fully answered. |
| **Suggested approach** | Obtain from co-author (Dalepiane) or advisor (Prof. Bernardino). |
| **Status** | `open` |

### GAP-002: Challenge–mitigation specific mappings

| Field | Value |
|-------|-------|
| **Element** | CQ6 — `mitigates` relationship |
| **Gap** | SMS reports aggregate counts for challenges and mitigations separately, but not which strategy mitigates which challenge. |
| **Impact** | `mitigates` property can exist but specific pairings lack direct evidence. |
| **Suggested approach** | Analyze open-ended extraction data (per-paper JSONs) for co-occurrences. If insufficient, targeted grey literature review. |
| **Status** | `open` |

### GAP-003: Revenue source × Delivery mode cross-tabulation

| Field | Value |
|-------|-------|
| **Element** | CQ1 — `RevenueSource` × `DeliveryMode` association |
| **Gap** | SMS reports individual distributions but no explicit cross-tabulation between revenue sources and delivery modes. |
| **Impact** | Axioms constraining revenue–delivery compatibility lack quantitative support. |
| **Suggested approach** | Build co-occurrence matrix from per-paper extraction data. If insufficient, targeted literature review on SaaS monetization. |
| **Status** | `open` |

---

*New gaps follow the same template (GAP-NNN).*
