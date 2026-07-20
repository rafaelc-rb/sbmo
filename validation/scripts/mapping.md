# SBMO validation — label→class mapping (review sheet)

Auto-derived from `sbmo_mapping.py`. Portuguese form label → SBMO class (property).


## Product/service type — `hasProductOrServiceType` (range `ProductOrServiceType`)
- Aplicação  →  `Application`
- Plataforma  →  `Platform`
- Serviço gerenciado  →  `ManagedService`
- Serviço de API  →  `APIService`
- Produto de dados  →  `DataProduct`
- Infraestrutura  →  `Infrastructure`
- SDK / Kit de desenvolvimento  →  `SDK`

## Delivery mode — `hasDeliveryMode` (range `DeliveryMode`)
- SaaS multi-tenant  →  `MultiTenantSaaS`
- SaaS single-tenant  →  `SingleTenantSaaS`
- On-premises  →  `OnPremises`
- Entrega mobile  →  `MobileDelivery`
- Entrega desktop  →  `DesktopDelivery`
- Entrega híbrida  →  `HybridDelivery`

## Revenue source — `hasRevenueSource` (range `RevenueSource`)
- Receita por assinatura  →  `SubscriptionRevenue`
- Receita por uso/consumo  →  `UsageConsumptionRevenue`
- Receita por transação  →  `TransactionRevenue`
- Receita por publicidade  →  `AdvertisingRevenue`
- Receita por licença perpétua  →  `PerpetualLicenseRevenue`
- Receita por suporte  →  `SupportRevenue`
- Taxa de marketplace  →  `MarketplaceFeesRevenue`
- Receita open core  →  `OpenCoreRevenue`
- Receita por licenciamento dual  →  `DualLicensingRevenue`

## Pricing strategy — `hasPricingStrategy` (range `PricingStrategy`)
- Precificação por assinatura  →  `SubscriptionBasedPricing`
- Precificação pay-as-you-go  →  `PayAsYouGoPricing`
- Precificação freemium  →  `FreemiumPricing`
- Precificação baseada em valor  →  `ValueBasedPricing`
- Precificação baseada em custo  →  `CostBasedPricing`

## Customer type — `targetsCustomerType` (range `CustomerType`)
- B2B  →  `B2B`
- B2C  →  `B2C`
- PMEs  →  `SME`
- Enterprise  →  `Enterprise`
- Governo  →  `Government`
- Ferramentas para desenvolvedores  →  `DeveloperTools`

## Ecosystem role — `hasEcosystemRole` (range `EcosystemRole`)
- Produto standalone  →  `StandaloneProduct`
- Plataforma bilateral  →  `TwoSidedPlatform`
- Marketplace  →  `Marketplace`
- Componente OEM  →  `OEMComponent`
- Plugin / complemento  →  `PluginComplement`

## Acquisition channel — `usesAcquisitionChannel` (range `AcquisitionChannel`)
- Venda direta  →  `DirectSales`
- Crescimento liderado pelo produto  →  `ProductLedGrowth`
- Canal de parceiros  →  `PartnerChannel`
- Marketing digital  →  `DigitalMarketing`
- Canal de marketplace  →  `MarketplaceChannel`
- Indicação  →  `Referral`

## IP regime — `hasIntellectualPropertyRegime` (range `IntellectualPropertyRegime`)
- Proprietário  →  `Proprietary`
- Open source permissivo  →  `PermissiveOpenSource`
- Open source  →  `OpenSource`
- Licença dual  →  `DualLicense`
- Open core  →  `OpenCore`
- Copyleft  →  `Copyleft`

## Pricing base unit — `hasPricingBaseUnit` (range `PricingBaseUnit`)
- Usuário / licença  →  `UserSeat`
- Baseado em transação  →  `TransactionBased`
- Tempo de computação  →  `ComputingTime`
- Compartilhamento de receita  →  `RevenueSharing`
- Chamadas de API  →  `APICalls`
- Armazenamento  →  `Storage`
- Dispositivo  →  `Device`

## Network effect — `exhibitsNetworkEffect` (range `NetworkEffectType`)
- Efeito de rede direto  →  `DirectNetworkEffect`
- Efeito de rede cruzado  →  `CrossSidedNetworkEffect`
- Efeito de rede orientado a dados  →  `DataDrivenNetworkEffect`

## Success factor — `hasSuccessFactor` (range `SuccessFactor`)
- Gestão do ecossistema  →  `EcosystemManagement`
- Expansão de mercado  →  `MarketExpansion`
- Melhoria da qualidade do serviço  →  `ServiceQualityImprovement`
- Preparação organizacional  →  `OrganizationalPreparedness`
- Orientação baseada em valor  →  `ValueBasedOrientation`

## Implementation challenge — `facesChallenge` (range `ImplementationChallenge`)
- Preocupações com segurança  →  `SecurityConcerns`
- Transformação de fluxo de receita  →  `RevenueStreamTransformation`
- Manutenção da confiança do cliente  →  `CustomerTrustMaintenance`
- Disrupção do ecossistema de parceiros  →  `PartnerEcosystemDisruption`
- Prontidão organizacional  →  `OrganizationalReadiness`
- Gestão de qualidade  →  `QualityManagement`

## Mitigation strategy — `mitigates` (range `MitigationStrategy`)
- Estratégia de precificação flexível  →  `FlexiblePricingStrategy`
- Adoção de modelo híbrido  →  `HybridModelAdoption`
- Implementação piloto  →  `PilotImplementation`
- Compensação de parceiros  →  `PartnerCompensation`

## Non-mapping answers
- `Outro (...)`  → free-text escape hatch (coverage gap signal), not asserted
- `Sem efeitos de rede significativos`  → absence of network effect, not asserted
