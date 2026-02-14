## Competency Questions (CQ1–CQ7)

What the ontology must be able to answer. Source: Dissertation Chapter 6.

---

### CQ1 — Revenue sources × Delivery mode

> Which revenue sources are associated with a given delivery mode?

- **Classes**: SoftwareBusinessModel, RevenueSource, DeliveryMode
- **Properties**: `hasRevenueSource`, `hasDeliveryMode`
- **Evidence**: Subscription 76.1%, Usage 41.8%, Transaction 32.8%; Multi-tenant SaaS 71.6%
- **Gap**: see GAP-003

### CQ2 — Pricing × Revenue source

> Which pricing structures are compatible with a given revenue source?

- **Classes**: PricingStrategy, RevenueSource
- **Properties**: `hasPricingStrategy`, `hasRevenueSource`
- **Evidence**: Subscription-based (153 mentions), Freemium (264), Pay-as-you-go (40), Value-based (33)

### CQ3 — Customer types × Acquisition channels

> Which customer types are most frequently associated with specific acquisition channels?

- **Classes**: CustomerType, AcquisitionChannel
- **Properties**: `targetsCustomerType`, `usesAcquisitionChannel`
- **Evidence**: B2B → Direct sales 75%, Partners 61%; B2C → Product-led growth 68%, Digital marketing 54%

### CQ4 — Ecosystem roles × Network effects

> Which ecosystem roles tend to imply particular network effect types?

- **Classes**: EcosystemRole, NetworkEffectType
- **Properties**: `hasEcosystemRole`, `exhibitsNetworkEffect`
- **Evidence**: Two-sided platforms → Cross-sided 76%; Standalone → Direct 50%

### CQ5 — Success factors & challenges × SBM class

> Which success factors and challenges are recurrent for a given class of SBMs?

- **Classes**: SoftwareBusinessModel, SuccessFactor, ImplementationChallenge
- **Properties**: `hasSuccessFactor`, `facesChallenge`
- **Evidence**: Ecosystem management (138), Market expansion (84); Security (41), Revenue transformation (38)

### CQ6 — Mitigation × Challenges

> Which mitigation practices address specific challenges?

- **Classes**: MitigationStrategy, ImplementationChallenge
- **Properties**: `mitigates`
- **Evidence**: Flexible pricing (58), Hybrid adoption (13), Pilot (8), Partner compensation (3)
- **Gap**: see GAP-002

### CQ7 — SBM as multi-dimensional configuration

> How can an SBM be described as a configuration across delivery, monetization, and ecosystem?

- **Classes**: SoftwareBusinessModel, DeliveryMode, RevenueSource, PricingStrategy, EcosystemRole
- **Properties**: `hasDeliveryMode`, `hasRevenueSource`, `hasPricingStrategy`, `hasEcosystemRole`
- **Evidence**: Three-dimensional taxonomy (Delivery × Monetization × Ecosystem)
- **Gap**: see GAP-001
