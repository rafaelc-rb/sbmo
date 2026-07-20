# DL Query expressions for the 7 competency questions

The community "SPARQL Query" (Snap SPARQL) plugin for Protégé (v2.0.2, the
latest release) fails to start on modern Protégé Desktop versions (5.6.x) —
this is a known, unresolved upstream bug
(see [issue #22](https://github.com/protegeproject/sparql-query-plugin/issues/22)
and [#21](https://github.com/protegeproject/sparql-query-plugin/issues/21)).

The `queries/CQ1..CQ7.rq` files remain in this repo as the formal SPARQL-DL
query template for each competency question (matching the templates already
quoted in the dissertation). To actually execute them against the reasoner in
Protégé, use the built-in **DL Query** tab instead (Manchester OWL Syntax),
which is unaffected by the plugin bug and uses the same Pellet reasoner.

Open the DL Query tab, use the `sbmo:` prefix on every class/property name,
check **"Instances"** (not "Subclasses") in the "Query for" panel, and read
the number of individuals returned.

**Verified 2026-07-20 in Protégé 5.6.9 + Pellet: all seven expressions below
returned exactly the expected count.**

| CQ | DL Query expression (paste into the "Query" field, `sbmo:` prefix required) | Expected | What is counted |
|----|------------------------------------------------------|-----------------|------------------|
| CQ1 | `sbmo:SoftwareBusinessModel and (sbmo:hasRevenueSource some (sbmo:AdvertisingRevenue or sbmo:PerpetualLicenseRevenue or sbmo:SupportRevenue or sbmo:MarketplaceFeesRevenue or sbmo:OpenCoreRevenue or sbmo:DualLicensingRevenue or sbmo:SubscriptionRevenue or sbmo:TransactionRevenue or sbmo:UsageConsumptionRevenue)) and (sbmo:hasDeliveryMode some (sbmo:DesktopDelivery or sbmo:HybridDelivery or sbmo:MobileDelivery or sbmo:MultiTenantSaaS or sbmo:OnPremises or sbmo:SingleTenantSaaS))` | 26 | SBM cases |
| CQ2 | `sbmo:SoftwareBusinessModel and (sbmo:hasPricingStrategy some (sbmo:CostBasedPricing or sbmo:FreemiumPricing or sbmo:PayAsYouGoPricing or sbmo:SubscriptionBasedPricing or sbmo:ValueBasedPricing)) and (sbmo:hasRevenueSource some (sbmo:AdvertisingRevenue or sbmo:PerpetualLicenseRevenue or sbmo:SupportRevenue or sbmo:MarketplaceFeesRevenue or sbmo:OpenCoreRevenue or sbmo:DualLicensingRevenue or sbmo:SubscriptionRevenue or sbmo:TransactionRevenue or sbmo:UsageConsumptionRevenue))` | 26 | SBM cases |
| CQ3 | `sbmo:SoftwareBusinessModel and (sbmo:targetsCustomerType some (sbmo:B2B or sbmo:B2C or sbmo:Enterprise or sbmo:Government or sbmo:DeveloperTools or sbmo:SME)) and (sbmo:usesAcquisitionChannel some (sbmo:DigitalMarketing or sbmo:DirectSales or sbmo:MarketplaceChannel or sbmo:PartnerChannel or sbmo:ProductLedGrowth or sbmo:Referral))` | 27 | SBM cases |
| CQ4 | `sbmo:SoftwareBusinessModel and (sbmo:hasEcosystemRole some (sbmo:exhibitsNetworkEffect some sbmo:NetworkEffectType))` | 19 | SBM cases |
| CQ5 | `sbmo:SoftwareBusinessModel and (sbmo:hasSuccessFactor some sbmo:SuccessFactor) and (sbmo:facesChallenge some sbmo:ImplementationChallenge)` | 31 | SBM cases |
| CQ6 | `sbmo:MitigationStrategy and (sbmo:mitigates some (sbmo:SecurityConcerns or sbmo:RevenueStreamTransformation or sbmo:CustomerTrustMaintenance or sbmo:PartnerEcosystemDisruption or sbmo:OrganizationalReadiness or sbmo:QualityManagement))` | 49 | mitigation-strategy individuals |
| CQ7 | `sbmo:SoftwareBusinessModel and (sbmo:hasDeliveryMode some (sbmo:DesktopDelivery or sbmo:HybridDelivery or sbmo:MobileDelivery or sbmo:MultiTenantSaaS or sbmo:OnPremises or sbmo:SingleTenantSaaS)) and (sbmo:hasRevenueSource some (sbmo:AdvertisingRevenue or sbmo:PerpetualLicenseRevenue or sbmo:SupportRevenue or sbmo:MarketplaceFeesRevenue or sbmo:OpenCoreRevenue or sbmo:DualLicensingRevenue or sbmo:SubscriptionRevenue or sbmo:TransactionRevenue or sbmo:UsageConsumptionRevenue)) and (sbmo:hasPricingStrategy some (sbmo:CostBasedPricing or sbmo:FreemiumPricing or sbmo:PayAsYouGoPricing or sbmo:SubscriptionBasedPricing or sbmo:ValueBasedPricing)) and (sbmo:hasEcosystemRole some (sbmo:Marketplace or sbmo:OEMComponent or sbmo:PluginComplement or sbmo:StandaloneProduct or sbmo:TwoSidedPlatform))` | 26 | SBM cases |

## Why CQ1, CQ2, CQ3, and CQ7 enumerate leaf classes instead of the parent class

The first version of these queries used the abstract parent class directly,
e.g. `hasRevenueSource some RevenueSource`. Under the open-world assumption,
Pellet trivially entails this for **all 31 cases**, not just the ones with
explicit data: `SoftwareBusinessModel` carries a `hasRevenueSource min 1
RevenueSource` restriction (Section 6.5.3 of the dissertation), so for *every*
declared `SoftwareBusinessModel` individual the reasoner must posit *some*
(possibly anonymous, unnamed) filler of type `RevenueSource` to keep the
ontology satisfiable — regardless of whether the A-Box actually asserts one.
This is a case of the same phenomenon the mandatory cardinality restrictions
are meant to exploit for structural completeness (Section 6.5.3), but it
makes the *parent-class* formulation of the query useless as an empirical
(explicit-data) check: it is entailed by the schema alone.

Enumerating the concrete named leaf subclasses instead (e.g. `hasRevenueSource
some (SubscriptionRevenue or ... or DualLicensingRevenue)`) fixes this: since
the T-Box declares no covering axiom stating that `RevenueSource` is
*exactly* the union of these leaf classes, the reasoner cannot infer that an
anonymous filler belongs to any specific named leaf class. The query then only
matches individuals with a genuinely asserted edge to a named leaf-class
value, correctly reproducing the counts computed independently from the raw
survey data by `analyze_survey.py` (26, 26, 27, and 26 respectively).

CQ4 (`exhibitsNetworkEffect`), CQ5 (`hasSuccessFactor`/`facesChallenge`), and
CQ6 (`mitigates`, tested against a leaf-class union of `ImplementationChallenge`
for the same reason as a precaution) are unaffected by this issue because
neither `EcosystemRole` nor `SoftwareBusinessModel` carries a mandatory
cardinality restriction on those properties in the T-Box — only the seven
properties listed in Section 6.5.3 do.

## Why CQ6 counts individuals, not cases

Unlike the other six competency questions, `mitigates` (`MitigationStrategy ->
ImplementationChallenge`) has no counterpart property linking
`SoftwareBusinessModel` directly to `MitigationStrategy` in the T-Box. CQ6
("which mitigation practices address specific challenges?") is answered at
the level of mitigation-practice individuals, not SBM cases, so the DL Query
naturally (and more precisely) reports the number of distinct mitigation
individuals that address at least one challenge (49), rather than the number
of cases that selected both a mitigation and a challenge (30, the case-level
figure `analyze_survey.py` originally computed before this was reconciled
with the DL Query formulation).

## Why CQ4 is a nested expression

`exhibitsNetworkEffect` links `EcosystemRole -> NetworkEffectType`, not
`SoftwareBusinessModel` directly. The nested existential
(`hasEcosystemRole some (exhibitsNetworkEffect some NetworkEffectType)`)
requires a case's ecosystem-role individual to itself have an outgoing
network-effect edge, which is exactly how `build_abox.py` asserts it (only
when both dimensions were selected for that case) — so the count (19) matches
the case-level figure computed independently by `analyze_survey.py`.
