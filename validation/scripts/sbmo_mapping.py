"""
SBMO validation — shared mapping module.

Maps the Portuguese Google Forms option labels to SBMO ontology class local
names (as declared in sbmo/sbmo.rdf). Used by both analyze_survey.py and
build_abox.py so the analysis and the A-Box stay consistent.

The label key is the "base" of each option, i.e. the text BEFORE the first
parenthesis, stripped. See base_label().

Anonymity note: this module only deals with the controlled vocabulary. No
respondent/company/product identifiers are handled here.
"""

import re

NS = "https://rafaelc-rb.github.io/sbmo#"
ONTOLOGY_IRI = "https://rafaelc-rb.github.io/sbmo"


def base_label(option: str) -> str:
    """Return the option text before the first '(' , stripped."""
    return re.split(r"\s*\(", option, 1)[0].strip()


# Sentinels that are valid answers but do NOT map to a class:
OTHER = "Outro"                                   # escape-hatch -> free-text column
NO_NETWORK_EFFECT = "Sem efeitos de rede significativos"  # absence of assertion

# Each dimension: column index in the CSV, the object property, the range
# (parent) class, whether it is multi-select, the paired free-text "Outro"
# column, and the label->class map (Portuguese base label -> class local name).
DIMENSIONS = [
    {
        "key": "product_type", "col": 10, "prop": "hasProductOrServiceType",
        "parent": "ProductOrServiceType", "multi": True, "other_col": 11,
        "map": {
            "Aplicação": "Application",
            "Plataforma": "Platform",
            "Serviço gerenciado": "ManagedService",
            "Serviço de API": "APIService",
            "Produto de dados": "DataProduct",
            "Infraestrutura": "Infrastructure",
            "SDK / Kit de desenvolvimento": "SDK",
        },
    },
    {
        "key": "delivery", "col": 12, "prop": "hasDeliveryMode",
        "parent": "DeliveryMode", "multi": True, "other_col": 13,
        "map": {
            "SaaS multi-tenant": "MultiTenantSaaS",
            "SaaS single-tenant": "SingleTenantSaaS",
            "On-premises": "OnPremises",
            "Entrega mobile": "MobileDelivery",
            "Entrega desktop": "DesktopDelivery",
            "Entrega híbrida": "HybridDelivery",
        },
    },
    {
        "key": "revenue", "col": 14, "prop": "hasRevenueSource",
        "parent": "RevenueSource", "multi": True, "other_col": 15,
        "map": {
            "Receita por assinatura": "SubscriptionRevenue",
            "Receita por uso/consumo": "UsageConsumptionRevenue",
            "Receita por transação": "TransactionRevenue",
            "Receita por publicidade": "AdvertisingRevenue",
            "Receita por licença perpétua": "PerpetualLicenseRevenue",
            "Receita por suporte": "SupportRevenue",
            "Taxa de marketplace": "MarketplaceFeesRevenue",
            "Receita open core": "OpenCoreRevenue",
            "Receita por licenciamento dual": "DualLicensingRevenue",
        },
    },
    {
        "key": "pricing", "col": 16, "prop": "hasPricingStrategy",
        "parent": "PricingStrategy", "multi": True, "other_col": 17,
        "map": {
            "Precificação por assinatura": "SubscriptionBasedPricing",
            "Precificação pay-as-you-go": "PayAsYouGoPricing",
            "Precificação freemium": "FreemiumPricing",
            "Precificação baseada em valor": "ValueBasedPricing",
            "Precificação baseada em custo": "CostBasedPricing",
        },
    },
    {
        "key": "customer", "col": 20, "prop": "targetsCustomerType",
        "parent": "CustomerType", "multi": True, "other_col": 21,
        "map": {
            "B2B": "B2B",
            "B2C": "B2C",
            "PMEs": "SME",
            "Enterprise": "Enterprise",
            "Governo": "Government",
            "Ferramentas para desenvolvedores": "DeveloperTools",
        },
    },
    {
        "key": "ecosystem", "col": 22, "prop": "hasEcosystemRole",
        "parent": "EcosystemRole", "multi": True, "other_col": 23,
        "map": {
            "Produto standalone": "StandaloneProduct",
            "Plataforma bilateral": "TwoSidedPlatform",
            "Marketplace": "Marketplace",
            "Componente OEM": "OEMComponent",
            "Plugin / complemento": "PluginComplement",
        },
    },
    {
        "key": "channel", "col": 24, "prop": "usesAcquisitionChannel",
        "parent": "AcquisitionChannel", "multi": True, "other_col": 25,
        "map": {
            "Venda direta": "DirectSales",
            "Crescimento liderado pelo produto": "ProductLedGrowth",
            "Canal de parceiros": "PartnerChannel",
            "Marketing digital": "DigitalMarketing",
            "Canal de marketplace": "MarketplaceChannel",
            "Indicação": "Referral",
        },
    },
    {
        "key": "ip_regime", "col": 26, "prop": "hasIntellectualPropertyRegime",
        "parent": "IntellectualPropertyRegime", "multi": True, "other_col": 27,
        "map": {
            "Proprietário": "Proprietary",
            "Open source permissivo": "PermissiveOpenSource",
            "Open source": "OpenSource",
            "Licença dual": "DualLicense",
            "Open core": "OpenCore",
            "Copyleft": "Copyleft",
        },
    },
    {
        "key": "price_unit", "col": 28, "prop": "hasPricingBaseUnit",
        "parent": "PricingBaseUnit", "multi": True, "other_col": 29,
        "map": {
            "Usuário / licença": "UserSeat",
            "Baseado em transação": "TransactionBased",
            "Tempo de computação": "ComputingTime",
            "Compartilhamento de receita": "RevenueSharing",
            "Chamadas de API": "APICalls",
            "Armazenamento": "Storage",
            "Dispositivo": "Device",
        },
    },
    {
        "key": "network_effect", "col": 30, "prop": "exhibitsNetworkEffect",
        "parent": "NetworkEffectType", "multi": True, "other_col": 31,
        # exhibitsNetworkEffect links EcosystemRole -> NetworkEffectType (handled
        # specially in build_abox.py).
        "map": {
            "Efeito de rede direto": "DirectNetworkEffect",
            "Efeito de rede cruzado": "CrossSidedNetworkEffect",
            "Efeito de rede orientado a dados": "DataDrivenNetworkEffect",
        },
    },
    {
        "key": "success", "col": 32, "prop": "hasSuccessFactor",
        "parent": "SuccessFactor", "multi": True, "other_col": 33,
        "map": {
            "Gestão do ecossistema": "EcosystemManagement",
            "Expansão de mercado": "MarketExpansion",
            "Melhoria da qualidade do serviço": "ServiceQualityImprovement",
            "Preparação organizacional": "OrganizationalPreparedness",
            "Orientação baseada em valor": "ValueBasedOrientation",
        },
    },
    {
        "key": "challenge", "col": 34, "prop": "facesChallenge",
        "parent": "ImplementationChallenge", "multi": True, "other_col": 35,
        "map": {
            "Preocupações com segurança": "SecurityConcerns",
            "Transformação de fluxo de receita": "RevenueStreamTransformation",
            "Manutenção da confiança do cliente": "CustomerTrustMaintenance",
            "Disrupção do ecossistema de parceiros": "PartnerEcosystemDisruption",
            "Prontidão organizacional": "OrganizationalReadiness",
            "Gestão de qualidade": "QualityManagement",
        },
    },
    {
        "key": "mitigation", "col": 36, "prop": "mitigates",
        "parent": "MitigationStrategy", "multi": True, "other_col": 37,
        # mitigates links MitigationStrategy -> ImplementationChallenge (handled
        # specially in build_abox.py using the challenge->mitigation map col 38).
        "map": {
            "Estratégia de precificação flexível": "FlexiblePricingStrategy",
            "Adoção de modelo híbrido": "HybridModelAdoption",
            "Implementação piloto": "PilotImplementation",
            "Compensação de parceiros": "PartnerCompensation",
        },
    },
]

DIM_BY_KEY = {d["key"]: d for d in DIMENSIONS}

# Short English display labels for the class local names (for the English
# dissertation tables). Falls back to the local name if missing.
ENGLISH_LABEL = {
    # product type
    "Application": "Application", "Platform": "Platform",
    "ManagedService": "Managed service", "APIService": "API service",
    "DataProduct": "Data product", "Infrastructure": "Infrastructure", "SDK": "SDK",
    # delivery
    "MultiTenantSaaS": "SaaS (multi-tenant)", "SingleTenantSaaS": "SaaS (single-tenant)",
    "OnPremises": "On-premises", "MobileDelivery": "Mobile", "DesktopDelivery": "Desktop",
    "HybridDelivery": "Hybrid",
    # revenue
    "SubscriptionRevenue": "Subscription", "UsageConsumptionRevenue": "Usage/consumption",
    "TransactionRevenue": "Transaction", "AdvertisingRevenue": "Advertising",
    "PerpetualLicenseRevenue": "Perpetual license", "SupportRevenue": "Support",
    "MarketplaceFeesRevenue": "Marketplace fees", "OpenCoreRevenue": "Open core",
    "DualLicensingRevenue": "Dual licensing",
    # pricing
    "SubscriptionBasedPricing": "Subscription", "PayAsYouGoPricing": "Pay-as-you-go",
    "FreemiumPricing": "Freemium", "ValueBasedPricing": "Value-based",
    "CostBasedPricing": "Cost-based",
    # customer
    "B2B": "B2B", "B2C": "B2C", "SME": "SME", "Enterprise": "Enterprise",
    "Government": "Government", "DeveloperTools": "Developer tools",
    # ecosystem
    "StandaloneProduct": "Standalone", "TwoSidedPlatform": "Two-sided platform",
    "Marketplace": "Marketplace", "OEMComponent": "OEM component",
    "PluginComplement": "Plugin/add-on",
    # channel
    "DirectSales": "Direct sales", "ProductLedGrowth": "Product-led growth",
    "PartnerChannel": "Partner channel", "DigitalMarketing": "Digital marketing",
    "MarketplaceChannel": "Marketplace channel", "Referral": "Referral",
    # ip
    "Proprietary": "Proprietary", "PermissiveOpenSource": "Permissive OSS",
    "OpenSource": "Open source", "DualLicense": "Dual license", "OpenCore": "Open core",
    "Copyleft": "Copyleft",
    # price unit
    "UserSeat": "User/seat", "TransactionBased": "Transaction", "ComputingTime": "Compute time",
    "RevenueSharing": "Revenue share", "APICalls": "API calls", "Storage": "Storage",
    "Device": "Device",
    # network effect
    "DirectNetworkEffect": "Direct", "CrossSidedNetworkEffect": "Cross-side",
    "DataDrivenNetworkEffect": "Data-driven",
    # success
    "EcosystemManagement": "Ecosystem management", "MarketExpansion": "Market expansion",
    "ServiceQualityImprovement": "Service quality", "OrganizationalPreparedness": "Org. readiness",
    "ValueBasedOrientation": "Value focus",
    # challenge
    "SecurityConcerns": "Security", "RevenueStreamTransformation": "Revenue-model transition",
    "CustomerTrustMaintenance": "Customer trust", "PartnerEcosystemDisruption": "Partner disruption",
    "OrganizationalReadiness": "Org. readiness", "QualityManagement": "Quality management",
    # mitigation
    "FlexiblePricingStrategy": "Flexible pricing", "HybridModelAdoption": "Hybrid model",
    "PilotImplementation": "Pilot implementation", "PartnerCompensation": "Partner compensation",
}

# Human-friendly English name for each dimension (for table captions/rows).
DIM_ENGLISH = {
    "product_type": "Product/service type", "delivery": "Delivery mode",
    "revenue": "Revenue source", "pricing": "Pricing strategy",
    "customer": "Customer type", "ecosystem": "Ecosystem role",
    "channel": "Acquisition channel", "ip_regime": "IP regime",
    "price_unit": "Pricing base unit", "network_effect": "Network effect",
    "success": "Success factor", "challenge": "Implementation challenge",
    "mitigation": "Mitigation strategy",
}


def en(class_name: str) -> str:
    return ENGLISH_LABEL.get(class_name, class_name)


def map_cell(dim: dict, cell: str):
    """Split a CSV cell into (mapped_classes, other_flag, unmapped_labels).

    mapped_classes: list of class local names.
    other_flag: True if the 'Outro' escape-hatch was selected.
    unmapped_labels: any base label that is neither in the map, 'Outro', nor the
    no-network-effect sentinel (should be empty if the mapping is complete).
    """
    mapped, other, unmapped = [], False, []
    for part in cell.split(";"):
        b = base_label(part)
        if not b:
            continue
        if b == OTHER:
            other = True
        elif b == NO_NETWORK_EFFECT:
            continue  # valid answer, no assertion
        elif b in dim["map"]:
            mapped.append(dim["map"][b])
        else:
            unmapped.append(b)
    return mapped, other, unmapped
