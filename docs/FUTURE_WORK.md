## Future work

Extensions and research directions identified during ontology development that fall outside the current SMS evidence base.

---

### FW-001: Legal & compliance dimension

| Field | Value |
|-------|-------|
| **Proposed dimension** | Compliance & Legal Framework |
| **Motivation** | Different SBM configurations imply distinct legal documents for end-user relationships (e.g., SaaS B2B → SLA + DPA; on-premises → EULA; marketplace → multi-party platform terms). This mapping is deterministic in practice but absent from the current ontology. |
| **Connections to existing dimensions** | `DeliveryMode` (SaaS → SLA; on-premises → EULA), `CustomerType` (B2B → enterprise contracts; B2C → consumer protection compliance), `PricingStrategy` (freemium → tier-specific terms; pay-as-you-go → variable billing clauses), `RevenueSource` (advertising → stricter privacy policies), `EcosystemRole` (marketplace → seller/buyer/platform terms) |
| **Possible elements** | New class `LegalDocument` with subclasses: `ServiceLevelAgreement`, `DataProcessingAgreement`, `EndUserLicenseAgreement`, `TermsOfService`, `PrivacyPolicy`, `PlatformTerms`, `MaintenanceAgreement`. New property `requiresLegalDocument` (domain: `SoftwareBusinessModel`, range: `LegalDocument`). |
| **Candidate competency questions** | CQ8: "Which legal documents are required for a given SBM type?" · CQ9: "How do regulatory requirements vary by customer type and delivery mode?" |
| **Evidence gap** | SMS (67 studies, 2014–2024) does not cover legal/regulatory aspects. A dedicated evidence source is needed. |
| **Suggested research approach** | (a) Targeted literature review on legal aspects of software business models; (b) documentary analysis of real contracts from major SaaS/platform companies; (c) potential reuse of existing legal ontologies (e.g., LKIF — Legal Knowledge Interchange Format). |

---

*New future work items follow the same template (FW-NNN).*
