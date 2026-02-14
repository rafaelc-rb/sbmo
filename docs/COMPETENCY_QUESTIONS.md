## Competency Questions (CQ1–CQ7)

What the ontology must be able to answer. Source: Dissertation Chapter 6.

Validation: SPARQL-DL queries via Snap SPARQL plugin (Protégé) with Pellet reasoner.

---

### CQ1 — Revenue sources × Delivery mode — **Validated**

> Which revenue sources are associated with a given delivery mode?

- **Classes**: SoftwareBusinessModel, RevenueSource, DeliveryMode
- **Properties**: `hasRevenueSource`, `hasDeliveryMode`
- **Evidence**: Subscription 76.1%, Usage 41.8%, Transaction 32.8%; Multi-tenant SaaS 71.6%
- **Gap**: see GAP-003
- **SPARQL result**: 2 results (SaaS_B2B_Subscription → multiTenantSaaS/subscriptionRevenue; Freemium_B2C_Platform → multiTenantSaaS/advertisingRevenue)

### CQ2 — Pricing × Revenue source — **Validated**

> Which pricing structures are compatible with a given revenue source?

- **Classes**: PricingStrategy, RevenueSource
- **Properties**: `hasPricingStrategy`, `hasRevenueSource`
- **Evidence**: Subscription-based (153 mentions), Freemium (264), Pay-as-you-go (40), Value-based (33)
- **SPARQL result**: 2 results (subscriptionBasedPricing/subscriptionRevenue; freemiumPricing/advertisingRevenue)

### CQ3 — Customer types × Acquisition channels — **Validated**

> Which customer types are most frequently associated with specific acquisition channels?

- **Classes**: CustomerType, AcquisitionChannel
- **Properties**: `targetsCustomerType`, `usesAcquisitionChannel`
- **Evidence**: B2B → Direct sales 75%, Partners 61%; B2C → Product-led growth 68%, Digital marketing 54%
- **SPARQL result**: 2 results (b2b/directSales; b2c/productLedGrowth)

### CQ4 — Ecosystem roles × Network effects — **Validated**

> Which ecosystem roles tend to imply particular network effect types?

- **Classes**: EcosystemRole, NetworkEffectType
- **Properties**: `hasEcosystemRole`, `exhibitsNetworkEffect`
- **Evidence**: Two-sided platforms → Cross-sided 76%; Standalone → Direct 50%
- **SPARQL result**: 1 result (twoSidedPlatform → crossSidedNetworkEffect). standaloneProduct has no network effect assertion — consistent with model.

### CQ5 — Success factors & challenges × SBM class — **Validated**

> Which success factors and challenges are recurrent for a given class of SBMs?

- **Classes**: SoftwareBusinessModel, SuccessFactor, ImplementationChallenge
- **Properties**: `hasSuccessFactor`, `facesChallenge`
- **Evidence**: Ecosystem management (138), Market expansion (84); Security (41), Revenue transformation (38)
- **SPARQL result**: 8 results (SaaS_B2B → ecosystemManagement, serviceQualityImprovement × securityConcerns, revenueStreamTransformation; Freemium_B2C → marketExpansion, ecosystemManagement × customerTrustMaintenance, partnerEcosystemDisruption)

### CQ6 — Mitigation × Challenges — **Validated**

> Which mitigation practices address specific challenges?

- **Classes**: MitigationStrategy, ImplementationChallenge
- **Properties**: `mitigates`
- **Evidence**: Flexible pricing (58), Hybrid adoption (13), Pilot (8), Partner compensation (3)
- **Gap**: see GAP-002
- **SPARQL result**: 4 results (flexiblePricingStrategy→revenueStreamTransformation, hybridModelAdoption→organizationalReadiness, pilotImplementation→securityConcerns, partnerCompensation→partnerEcosystemDisruption)

### CQ7 — SBM as multi-dimensional configuration — **Validated**

> How can an SBM be described as a configuration across delivery, monetization, and ecosystem?

- **Classes**: SoftwareBusinessModel, DeliveryMode, RevenueSource, PricingStrategy, EcosystemRole
- **Properties**: `hasDeliveryMode`, `hasRevenueSource`, `hasPricingStrategy`, `hasEcosystemRole`
- **Evidence**: Three-dimensional taxonomy (Delivery × Monetization × Ecosystem)
- **Gap**: see GAP-001
- **SPARQL result**: 2 results — each SBM individual returned with all 4 dimensions populated.

---

**Summary**: 7/7 validated via SPARQL-DL (Snap SPARQL + Pellet reasoner).
