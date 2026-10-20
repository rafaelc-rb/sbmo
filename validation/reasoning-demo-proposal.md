# Proposta: demonstração de raciocínio na SBMO (R30, R28, R34, R29)

- **Fase:** 1 (proposta). **Data:** 2026-10-20.
- **Aprovada em 2026-10-20 e aplicada (SBMO 1.1).** Decisões: D1 sim (sem `Marketplace ⊑ TwoSidedPlatform`, só registrada); D2 sim; D3 opção (b), aplicada às duas propriedades de ano (`hasLaunchYear` e `hasSourceYear`, ambas com range `xsd:gYear`); D4 nomes mantidos; D5 nova §7.3; D6 versão 1.1; D7 ajuste mínimo nas frases sobre SWRL. Também aprovados: recontagem dos `rdfs:comment` sobre 63 estudos e ajuste da convenção de nomes de indivíduos (§6.4.2). Os testes negativos ficaram em `protege/`, junto com um `catalog-v001.xml` versionado. O texto abaixo é o da proposta.
- **Nada foi alterado** no `sbmo.rdf`, na A-Box de validação nem na dissertação. Todas as variantes da ontologia foram montadas e raciocinadas em cópias temporárias.
- **Itens do tracker:** R30 (inferências do Pellet), R28 (disjunção), R34 (Suassu na avaliação), R29 (expressividade DL). Pareceres: Lunardi ("Formalização, raciocínio e inferências"), notas do Bernardino (bloco JP: conjuntos disjuntos, expressividade, "screenshot do Protégé"), Mossmann P5.
- **Caso de demonstração:** Case02 = Suassu (resposta "parcialmente operacional"; descreve o modelo planejado para os próximos 12 meses). Case02 é o único caso da sua organização (`ORG_02`) e não é o produto descrito duas vezes (`PROD_01` = Case01/Case03), então nomeá-lo não expõe outro caso.

---

## 0. Resumo dos resultados

| Item | Antes (sbmo.rdf atual) | Depois (proposta) |
|---|---|---|
| Classes nomeadas | 89 (14 de topo + 75 subclasses) | **93** (+ 4 classes definidas) |
| Axiomas `EquivalentClasses` | 0 | 4 |
| Axiomas `DisjointClasses` (OWLAPI) | 6 (6 pares) | 21 (77 pares), com a decisão D1; 22 (78 pares) sem ela |
| Axiomas lógicos | 131 | 150 (com D1) / 151 (sem D1) |
| Expressividade DL (Pellet 2.3.1) | ALCQ(D) | **ALCQ(D)**, sem mudança |
| Expressividade (ROBOT 1.9.6 / OWLAPI 4.5) | `RRESTRCQ(D)` | `RRESTRCUCINTEQ(D)` (mesma lógica, ver §d) |
| A-Box dos 31 casos | consistente | consistente (todas as variantes) |
| 7 CQs (`check_cq_result_sets.py`) | ALL OK | **ALL OK**, mesmos conjuntos |
| Casos por classe definida | n/a | SubscriptionSaaS 18; FreemiumSubscription 4; PlatformBusiness 15; NetworkedPlatform 10 |
| Inferências sobre o Case02 (Suassu) | só supertipos | + `SubscriptionSaaSModel`, + `FreemiumSubscriptionModel` |
| Teste negativo N1 (papel duplo) | inconsistente | inconsistente (3 axiomas na explicação) |
| Teste negativo N2 (valor usado na dimensão errada) | **consistente** (erro passa) | **inconsistente** (erro detectado) |

---

## 1. Ambiente e reprodutibilidade

- owlready2 0.51 (Pellet 2.3.1 embutido, com OWLAPI 3.4.3), rdflib 7.6.0, OpenJDK 27 (`/usr/lib/jvm/java-27-openjdk`; o Java padrão da máquina é o 21), ROBOT 1.9.6 (jar oficial do GitHub, só para métricas). Nenhum desses pacotes estava instalado; usei um venv temporário.
- **Linha de base:** `check_cq_result_sets.py` contra o `sbmo.rdf` atual: ALL OK (26, 26, 27, 19, 31, 49, 26).
- **Explicações:** o comando `pellet explain` da CLI 2.3.1 funciona para `Case02 type SubscriptionSaaSModel`, mas o renderizador Manchester dele quebra (`ClassCastException` em `DescriptionSorter`) quando há uma união dentro de uma interseção, como em `NetworkedPlatformModel`. Para não depender disso, escrevi um auxiliar Java de ~60 linhas (`Justify.java`) que chama a API de explicação do próprio Pellet (`PelletExplanation`) e imprime cada justificativa em Manchester e em DL. O raciocínio é o mesmo, só o renderizador muda. O auxiliar compila com o `javac` do JDK 27.
- Protótipos (scripts, variantes, testes e saídas) ficam no diretório temporário da sessão; os que entram no repositório estão listados no §i.

---

## a) Classes definidas (R30)

### Princípios adotados

1. **Fillers são folhas nomeadas**, nunca a classe de dimensão. Como `SoftwareBusinessModel` tem `minQualifiedCardinality 1` em sete propriedades, `hasRevenueSource some RevenueSource` vale para todo caso, só pelo esquema (o mesmo motivo documentado em `protege/dl_queries.md` para CQ1–CQ3 e CQ7). Com folhas, a classificação exige um valor declarado.
2. **Nenhuma definição depende de ausência** ("não tem efeito de rede", "só tem papel standalone"): sob mundo aberto, isso não é inferível sem axiomas de fechamento.
3. **Nada trivial:** nenhuma classe cobre a maioria absoluta dos casos (máximo: 18/31 = 58,1%). Cinco casos não caem em nenhuma.
4. **Duas condições declaradas para a classificação de um caso**, para gerar exatamente o padrão pedido pela banca: "foram declarados A e B; pelos axiomas, o Pellet inferiu C".
5. Cada classe corresponde a uma configuração recorrente no SMS e combina dimensões que já são objeto de CQs (CQ1, CQ2, CQ4), funcionando como **configurações nomeadas** no sentido da CQ7.

### As quatro classes

| # | Nome | DL | Manchester Syntax |
|---|---|---|---|
| 1 | `SubscriptionSaaSModel` | SubscriptionSaaSModel ≡ SoftwareBusinessModel ⊓ ∃hasDeliveryMode.MultiTenantSaaS ⊓ ∃hasRevenueSource.SubscriptionRevenue | `SoftwareBusinessModel and (hasDeliveryMode some MultiTenantSaaS) and (hasRevenueSource some SubscriptionRevenue)` |
| 2 | `FreemiumSubscriptionModel` | FreemiumSubscriptionModel ≡ SoftwareBusinessModel ⊓ ∃hasPricingStrategy.FreemiumPricing ⊓ ∃hasRevenueSource.SubscriptionRevenue | `SoftwareBusinessModel and (hasPricingStrategy some FreemiumPricing) and (hasRevenueSource some SubscriptionRevenue)` |
| 3 | `PlatformBusinessModel` | PlatformBusinessModel ≡ SoftwareBusinessModel ⊓ ∃hasEcosystemRole.(TwoSidedPlatform ⊔ Marketplace) | `SoftwareBusinessModel and (hasEcosystemRole some (TwoSidedPlatform or Marketplace))` |
| 4 | `NetworkedPlatformModel` | NetworkedPlatformModel ≡ SoftwareBusinessModel ⊓ ∃hasEcosystemRole.((TwoSidedPlatform ⊔ Marketplace) ⊓ ∃exhibitsNetworkEffect.NetworkEffectType) | `SoftwareBusinessModel and (hasEcosystemRole some ((TwoSidedPlatform or Marketplace) and (exhibitsNetworkEffect some NetworkEffectType)))` |

Em (4), `NetworkEffectType` como filler é seguro: `exhibitsNetworkEffect` não tem restrição de cardinalidade mínima, então só casam papéis com efeito de rede declarado (mesma lógica da CQ4). O efeito tem de estar **no mesmo papel de plataforma**, e não em qualquer papel do caso; isso é mais forte do que a conjunção `PlatformBusinessModel ⊓ ∃hasEcosystemRole.∃exhibitsNetworkEffect.⊤`.

### Rastreabilidade ao SMS (números atuais do Cap. 5, 63 estudos)

| Classe | Evidência no Cap. 5 |
|---|---|
| SubscriptionSaaSModel | Tabela 2 (`tab:business-models-distribution`): "SaaS (Software as a Service)", 266 menções (5,9%), 3º modelo mais citado; "Subscription-based pricing", 149 (3,3%). §5.2.2 e Figura 9 (`fig:sms_revenue_sources`): receita por assinatura em 74,6% dos estudos (fonte mais frequente) e SaaS multi-tenant em 69,8% (modo de entrega mais frequente). §5.4: "predominance of SaaS/subscription models". |
| FreemiumSubscriptionModel | Tabela 2: "Freemium model", 264 menções (5,8%), 4º mais citado; Tabela 3 (`tab:extracted-business-models`): "free basic version with paid premium features". A parte paga é capturada pela receita por assinatura (74,6%, Figura 9); no questionário, a opção freemium é "plano gratuito + upgrades pagos". |
| PlatformBusinessModel | Tabela 2: "Platform business model", 389 menções (8,6%), o modelo mais citado; Tabela 3: "Marketplace Model", 63. §5.2.4: plataformas bilaterais em 49,2% dos estudos. §5.4: "relevance of platform-based value creation". |
| NetworkedPlatformModel | Tabela 2: "Network effects", 133 menções (2,9%). §5.2.4 e Figura 12 (`fig:sms_network_effects`): efeitos diretos 34,9%, cruzados 33,3%, orientados a dados 23,8%. §6.3.2 já afirma que "two-sided platforms are predominantly associated with cross-sided network effects". §5.4: "platform-based value creation and network effects". |

### Classificação dos 31 casos (Pellet, rodado de fato)

| Classe definida | Casos | % de 31 | Casos | Igual ao conjunto derivado do CSV |
|---|---|---|---|---|
| SubscriptionSaaSModel | 18 | 58,1% | 02, 04, 05, 06, 07, 13, 15, 17, 18, 20, 21, 22, 24, 26, 28, 29, 30, 31 | sim |
| FreemiumSubscriptionModel | 4 | 12,9% | 02, 05, 22, 24 | sim |
| PlatformBusinessModel | 15 | 48,4% | 01, 03, 06, 08, 10, 12, 13, 16, 18, 20, 23, 25, 28, 30, 31 | sim |
| NetworkedPlatformModel | 10 | 32,3% | 01, 03, 08, 10, 12, 13, 16, 20, 23, 28 | sim |

- Casos em nenhuma classe definida: 5 (Case09, 11, 14, 19, 27). Casos em 1 classe: 8; em 2: 15; em 3: 3. Nenhum caso nas quatro, pois `FreemiumSubscriptionModel` e `NetworkedPlatformModel` não se cruzam nesta amostra.
- Os conjuntos foram conferidos de forma independente do raciocinador, a partir de `survey-derived/cases_normalized.csv`, como faz `check_cq_result_sets.py`.
- Resultados idênticos com e sem a decisão D1 (Marketplace ⊥ TwoSidedPlatform), e com e sem as novas disjunções.

### Inferência no nível da T-Box

O Pellet infere **NetworkedPlatformModel ⊑ PlatformBusinessModel** sem nenhum indivíduo: a justificativa são só as duas definições. Essa é a diferença visível entre a hierarquia declarada e a inferida no Protégé (captura 1).

### Candidatos considerados e descartados

| Candidato | Motivo |
|---|---|
| `FreemiumModel ≡ SBM ⊓ ∃hasPricingStrategy.FreemiumPricing` (6 casos) | Uma condição só: a "inferência" apenas repete o tipo do valor declarado. A versão com receita por assinatura gera o padrão A + B → C. |
| SaaS + `SubscriptionBasedPricing` (16 casos) | Quase igual à classe 1 (16 dos 18; a Seção 7.4 já mostra φ = 0,812 entre preço e receita por assinatura). Ficar com a receita alinha a classe à CQ1 (receita × entrega). |
| Open source BM (regime aberto; 188 menções no SMS) | Só 1 caso dos 31 (Case05), o que não ilustra classificação. |
| API-based BM (`∃hasProductOrServiceType.APIService`, 14 casos) | Uma condição só; Tabela 3 traz só 44 menções. |
| "Modelo standalone" (só papel standalone) | Exige fechamento (`hasEcosystemRole only StandaloneProduct`), ou seja, depende de ausência de informação. |

### `rdfs:comment` propostos (mesmo estilo das demais classes)

- **SubscriptionSaaSModel:** "A software business model delivered as multi-tenant SaaS and monetized through subscription revenue. Defined class: membership is inferred by the reasoner from the declared delivery mode and revenue source. SMS evidence: SaaS (266 coded mentions) and subscription-based pricing (149) are among the most frequent business models; subscription revenue is reported in 74.6% and multi-tenant SaaS in 69.8% of the 63 primary studies."
- **FreemiumSubscriptionModel:** "A software business model that combines a freemium pricing strategy with subscription revenue from the paid tiers. Defined class: membership is inferred from the declared pricing strategy and revenue source. SMS evidence: freemium model (264 coded mentions); subscription revenue in 74.6% of the 63 primary studies."
- **PlatformBusinessModel:** "A software business model in which the company plays a two-sided platform or marketplace role in its ecosystem. Defined class: membership is inferred from the declared ecosystem role. SMS evidence: platform business model (389 coded mentions, the most frequent) and marketplace model (63); two-sided platforms in 49.2% of the 63 primary studies."
- **NetworkedPlatformModel:** "A platform business model whose two-sided platform or marketplace role exhibits a declared network effect. Defined class: membership is inferred from the declared ecosystem role and its network effect; the reasoner also infers that it is a subclass of PlatformBusinessModel. SMS evidence: network effects (133 coded mentions); direct (34.9%), cross-sided (33.3%), and data-driven (23.8%) network effects across the 63 primary studies."

---

## b) Disjunção (R28)

### O ponto central

Na A-Box cada valor de cada caso é um indivíduo próprio, e **nenhum indivíduo tem mais de um tipo declarado** (conferido no `.ttl`). Os indivíduos de desafio (por exemplo `Case02_SecurityConcerns`) são reutilizados por `facesChallenge` e por `mitigates`, mas as duas propriedades têm o mesmo range. Daí:

1. A disjunção entre **folhas da mesma dimensão** restringe o *valor*, não o *caso*. `StandaloneProduct ⊥ TwoSidedPlatform` não impede um caso de ter os dois papéis (Case03, 06, 23, 28, 30 e 31 declaram ambos, cada um como indivíduo próprio, e a A-Box é consistente); impede que **o mesmo papel** seja os dois. Restringir combinações no caso exigiria outro mecanismo (fechamento ou propriedades funcionais), que não é o que a definição das categorias justifica.
2. Por isso a disjunção nunca acusa nada na A-Box de validação. Ela atua quando um dado errado dá dois tipos a um indivíduo, seja por declaração direta (teste N1), seja por **inferência via domínio/range** (teste N2).
3. O caso mais útil é a disjunção **entre as dimensões**. Um valor usado na propriedade errada (por exemplo, o valor de *pricing* freemium declarado como fonte de receita, um erro plausível, pois "freemium" é chamado de modelo de receita em parte da literatura) recebe pelo range um segundo tipo de outra dimensão. Hoje isso passa sem aviso.
4. Isso também corrige a justificativa atual (§6.4.3 e DD-003): "um SBM pode combinar várias fontes de receita" é verdade no nível do caso e não é argumento contra disjunção no nível do valor. O critério correto é: **duas categorias são disjuntas quando nenhum valor pode, por definição, pertencer a ambas.**

O critério "por definição" foi aplicado às definições do próprio instrumento (texto entre parênteses de cada opção no questionário, `zenodo-package/data/statistical_analysis/processed_data.csv`) e às descrições do SMS.

### Revisão dimensão por dimensão

| Dimensão | Declarar | Não declarar (e por quê) |
|---|---|---|
| **Entre dimensões** | `AllDisjointClasses(SoftwareBusinessModel, DeliveryMode, RevenueSource, PricingStrategy, CustomerType, EcosystemRole, NetworkEffectType, AcquisitionChannel, ProductOrServiceType, IntellectualPropertyRegime, PricingBaseUnit)` (55 pares). Cada dimensão classifica um aspecto diferente da configuração; um valor de entrega não é um valor de receita. Pares confundíveis que passam a ser separados: `TransactionRevenue`/`TransactionBased`, `Marketplace`/`MarketplaceChannel`, `Platform`/`TwoSidedPlatform`, `ManagedService`/`SingleTenantSaaS`. | `SuccessFactor`, `ImplementationChallenge`, `MitigationStrategy` ficam fora: as categorias de adoção se sobrepõem conceitualmente a escolhas de configuração (`FlexiblePricingStrategy` × `PricingStrategy`, `HybridModelAdoption`) e entre si (um mesmo aspecto organizacional aparece como fator, `OrganizationalPreparedness`, e como desafio, `OrganizationalReadiness`). |
| RevenueSource | `SubscriptionRevenue ⊥ PerpetualLicenseRevenue` ("pagamentos periódicos recorrentes" × pagamento único por direito perpétuo). É o exemplo que o §3 (linha 200) já usa para disjunção, mas que a ontologia não declarava. | Suporte pode ser cobrado por assinatura; open core e licença dual são estratégias de licenciamento vendidas por assinatura ou perpetuamente; uso × transação × taxa de marketplace se sobrepõem. |
| PricingStrategy | (nenhuma) | As categorias usam critérios diferentes (base do preço: custo/valor; esquema de cobrança: assinatura/pay-as-you-go; escalonamento: freemium) e se combinam, como no próprio Case02 (assinatura + freemium). |
| DeliveryMode | `AllDisjointClasses(MultiTenantSaaS, SingleTenantSaaS, OnPremises)`: "infraestrutura compartilhada" × "instância dedicada por cliente" × "instalado na infraestrutura do próprio cliente". | `HybridDelivery` é por definição uma combinação ("cloud e on-premises"); `MobileDelivery`/`DesktopDelivery` descrevem o cliente (critério ortogonal). |
| CustomerType | `B2C ⊥ B2B`, `B2C ⊥ SME`, `B2C ⊥ Enterprise`, `B2C ⊥ Government` (consumidores finais não são organizações); `SME ⊥ Enterprise` (faixas de porte). | `B2B` se sobrepõe a `SME`/`Enterprise` (como você apontou); `Government` pode se sobrepor a `Enterprise` ("grandes organizações") e a `B2B` (empresas públicas); `DeveloperTools` atravessa B2B e B2C. |
| EcosystemRole | Manter `StandaloneProduct ⊥ TwoSidedPlatform` e `StandaloneProduct ⊥ Marketplace`; **novos** `StandaloneProduct ⊥ OEMComponent` ("independente, autocontido" × "embutido em produtos de outras empresas") e `StandaloneProduct ⊥ PluginComplement` (× "estende a funcionalidade de outra plataforma"). | **D1:** o par existente `Marketplace ⊥ TwoSidedPlatform` não vale por definição: o marketplace "facilita transações entre vendedores e compradores", e a plataforma bilateral "conecta dois grupos distintos de usuários"; todo marketplace satisfaz a definição de plataforma bilateral. 4 casos (08, 16, 20, 31) declaram os dois papéis. Recomendo retirar esse par (ver §h). |
| NetworkEffectType | Manter os 3 pares existentes (mesmo lado × outro lado × via dados). | n/a |
| AcquisitionChannel | `DirectSales ⊥ PartnerChannel` ("equipe de vendas, outbound" × "revendedores, distribuidores, integradores"); `DirectSales ⊥ MarketplaceChannel` (× "listado em app stores ou marketplaces"). | `ProductLedGrowth` × `DirectSales`: há movimentos híbridos (vendas assistidas sobre self-service). `DigitalMarketing` e `Referral` geram demanda para qualquer canal. `PartnerChannel` × `MarketplaceChannel` pode coincidir (marketplaces de parceiros). |
| ProductOrServiceType | (nenhuma) | Categorias sobrepostas (um serviço de API é uma plataforma; um serviço gerenciado é uma aplicação). |
| IntellectualPropertyRegime | `Proprietary ⊥ OpenSource`, `Proprietary ⊥ PermissiveOpenSource`, `Proprietary ⊥ Copyleft` ("código fechado, todos os direitos reservados" × código aberto); `PermissiveOpenSource ⊥ Copyleft` (permissiva × recíproca). | `OpenCore` e `DualLicense` combinam código aberto e licença comercial por definição. |
| PricingBaseUnit | (nenhuma) | `APICalls` é um tipo de transação; `RevenueSharing` é cobrado por transação em marketplaces; métricas se compõem (por usuário por hora). Sem exclusão limpa. |
| Adoção (fatores, desafios, mitigação) | (nenhuma) | Ver primeira linha. |

Total proposto: 55 pares entre dimensões + 17 pares dentro das dimensões, em 16 axiomas novos. Com D1: 6 − 1 + 72 = **77 pares, 21 axiomas `DisjointClasses`**.

### Consistência (A-Box dos 31 casos)

Pellet `consistency` sobre T-Box + A-Box: **consistente** em todas as variantes (atual; + classes definidas; + disjunções com e sem D1). Também nenhuma classe ficou insatisfatível (`pellet unsat` sobre as T-Boxes propostas: "Found no unsatisfiable concepts").

### Testes negativos (arquivos separados, fora do `sbmo.rdf` e da A-Box)

Cada arquivo importa a A-Box de validação sem alterá-la e acrescenta **uma** afirmação errada sobre o Case02.

**N1 · `case02-negative-test-disjoint-roles.ttl`**: `ex:Case02_StandaloneProduct a sbmo:TwoSidedPlatform .`
- Atual: **inconsistente**. Proposta: **inconsistente**.
- Explicação do Pellet (1 justificativa, 3 axiomas):
  1. `Case02_StandaloneProduct Type StandaloneProduct` (A-Box)
  2. `Case02_StandaloneProduct Type TwoSidedPlatform` (afirmação do teste)
  3. `StandaloneProduct DisjointWith TwoSidedPlatform` (T-Box)

**N2 · `case02-negative-test-misused-value.ttl`** (recomendado como segundo teste): `ex:Case02 sbmo:hasRevenueSource ex:Case02_FreemiumPricing .`
- Atual: **consistente**, ou seja, o erro passa despercebido. Proposta: **inconsistente**.
- Explicação do Pellet (2 justificativas):
  - J1: `Case02 hasRevenueSource Case02_FreemiumPricing` (teste) + `hasRevenueSource Range RevenueSource` + `Case02 hasPricingStrategy Case02_FreemiumPricing` (A-Box) + `hasPricingStrategy Range PricingStrategy` + `DisjointClasses(SoftwareBusinessModel, DeliveryMode, RevenueSource, PricingStrategy, …)`.
  - J2: `Case02 hasRevenueSource Case02_FreemiumPricing` + `hasRevenueSource Range RevenueSource` + `Case02_FreemiumPricing Type FreemiumPricing` + `FreemiumPricing SubClassOf PricingStrategy` + o mesmo `DisjointClasses`.
- É uma cadeia de raciocínio de verdade: o tipo `RevenueSource` não está declarado em lugar nenhum; ele é **inferido** pelo range, e só então colide com o tipo declarado.

---

## c) Inferências do Suassu (Case02): declarado × inferido

Gerado por script (Pellet via owlready2 para a realização; justificativas via `Justify.java`), sobre a ontologia proposta. As classes definidas não alteram as linhas dos valores.

### Versão compacta (proposta para o Cap. 7)

| Indivíduo | Declarado na A-Box | Inferido pelo Pellet | Axiomas que justificam (justificativa J1) |
|---|---|---|---|
| Case02 | tipo `SoftwareBusinessModel`; `hasDeliveryMode Case02_MultiTenantSaaS` (tipo `MultiTenantSaaS`); `hasRevenueSource Case02_SubscriptionRevenue` (tipo `SubscriptionRevenue`) | **`SubscriptionSaaSModel`** | definição de `SubscriptionSaaSModel` (≡) + as 5 asserções ao lado |
| Case02 | tipo `SoftwareBusinessModel`; `hasPricingStrategy Case02_FreemiumPricing` (tipo `FreemiumPricing`); `hasRevenueSource Case02_SubscriptionRevenue` | **`FreemiumSubscriptionModel`** | definição de `FreemiumSubscriptionModel` (≡) + as 5 asserções ao lado |
| Case02 | `hasEcosystemRole Case02_StandaloneProduct` | nem `PlatformBusinessModel` nem `not PlatformBusinessModel` | mundo aberto: o caso poderia ter outro papel não declarado |
| Case02_StandaloneProduct | tipo `StandaloneProduct` | `EcosystemRole`; **`not TwoSidedPlatform`** (e `not Marketplace`, `not OEMComponent`, `not PluginComplement`) | `StandaloneProduct ⊑ EcosystemRole` ou range de `hasEcosystemRole`; axiomas de disjunção |
| 22 indivíduos de valor do Case02 | a folha (por exemplo `MultiTenantSaaS`, `UserSeat`, `SecurityConcerns`) | a classe de dimensão (`DeliveryMode`, `PricingBaseUnit`, `ImplementationChallenge`, …) | 2 justificativas cada: `SubClassOf` e o range da propriedade (4 para desafios: também o range de `mitigates`) |
| Case02_FlexiblePricingStrategy, Case02_PilotImplementation | `FlexiblePricingStrategy`, `PilotImplementation` | `MitigationStrategy` | `SubClassOf` ou domínio de `mitigates` |

Observações para o texto:
- Para cada classe definida, o Pellet encontrou pelo menos 5 justificativas (limite que usei). As alternativas trocam `Case02 Type SoftwareBusinessModel` pelo domínio de qualquer propriedade usada pelo caso (por exemplo `∃targetsCustomerType.⊤ ⊑ SoftwareBusinessModel`), ou seja, o tipo do caso seria inferido mesmo se não estivesse declarado.
- Essas são as inferências **sobre o Suassu que não estão na A-Box**: duas classificações em configurações nomeadas, tipos de dimensão para todos os valores e conhecimento negativo sobre o papel no ecossistema.
- **Propriedades inferidas** (pedido de Lunardi): a SBMO não tem propriedades inversas nem cadeias, então o Pellet não infere asserções de propriedade novas. O texto deve dizer isso; propriedades inversas são o pitfall P13 do OOPS! e se ligam ao R26.

### Versão completa (saída do script)

| Indivíduo | Declarado | Inferido | Justificativa J1 | Nº de justificativas |
|---|---|---|---|---|
| Case02 | SoftwareBusinessModel | FreemiumSubscriptionModel | SoftwareBusinessModel(Case02); SubscriptionRevenue(Case02_SubscriptionRevenue); FreemiumPricing(Case02_FreemiumPricing); FreemiumSubscriptionModel ≡ SoftwareBusinessModel ⊓ (∃ hasPricingStrategy.FreemiumPricing) ⊓ (∃ hasRevenueSource.SubscriptionRevenue); hasRevenueSource(Case02, Case02_SubscriptionRevenue); hasPricingStrategy(Case02, Case02_FreemiumPricing) | ≥ 5 |
|  |  | SubscriptionSaaSModel | SoftwareBusinessModel(Case02); SubscriptionRevenue(Case02_SubscriptionRevenue); MultiTenantSaaS(Case02_MultiTenantSaaS); SubscriptionSaaSModel ≡ SoftwareBusinessModel ⊓ (∃ hasDeliveryMode.MultiTenantSaaS) ⊓ (∃ hasRevenueSource.SubscriptionRevenue); hasRevenueSource(Case02, Case02_SubscriptionRevenue); hasDeliveryMode(Case02, Case02_MultiTenantSaaS) | ≥ 5 |
| Case02_APIService | APIService | ProductOrServiceType | hasProductOrServiceType(Case02, Case02_APIService); ⊤ ⊑ ∀ hasProductOrServiceType.ProductOrServiceType | 2 |
| Case02_Application | Application | ProductOrServiceType | hasProductOrServiceType(Case02, Case02_Application); ⊤ ⊑ ∀ hasProductOrServiceType.ProductOrServiceType | 2 |
| Case02_B2B | B2B | CustomerType | targetsCustomerType(Case02, Case02_B2B); ⊤ ⊑ ∀ targetsCustomerType.CustomerType | 2 |
| Case02_DigitalMarketing | DigitalMarketing | AcquisitionChannel | usesAcquisitionChannel(Case02, Case02_DigitalMarketing); ⊤ ⊑ ∀ usesAcquisitionChannel.AcquisitionChannel | 2 |
| Case02_DirectSales | DirectSales | AcquisitionChannel | usesAcquisitionChannel(Case02, Case02_DirectSales); ⊤ ⊑ ∀ usesAcquisitionChannel.AcquisitionChannel | 2 |
| Case02_Enterprise | Enterprise | CustomerType | targetsCustomerType(Case02, Case02_Enterprise); ⊤ ⊑ ∀ targetsCustomerType.CustomerType | 2 |
| Case02_FreemiumPricing | FreemiumPricing | PricingStrategy | hasPricingStrategy(Case02, Case02_FreemiumPricing); ⊤ ⊑ ∀ hasPricingStrategy.PricingStrategy | 2 |
| Case02_MultiTenantSaaS | MultiTenantSaaS | DeliveryMode | hasDeliveryMode(Case02, Case02_MultiTenantSaaS); ⊤ ⊑ ∀ hasDeliveryMode.DeliveryMode | 2 |
| Case02_OrganizationalPreparedness | OrganizationalPreparedness | SuccessFactor | hasSuccessFactor(Case02, Case02_OrganizationalPreparedness); ⊤ ⊑ ∀ hasSuccessFactor.SuccessFactor | 2 |
| Case02_OrganizationalReadiness | OrganizationalReadiness | ImplementationChallenge | facesChallenge(Case02, Case02_OrganizationalReadiness); ⊤ ⊑ ∀ facesChallenge.ImplementationChallenge | 4 |
| Case02_Proprietary | Proprietary | IntellectualPropertyRegime | hasIntellectualPropertyRegime(Case02, Case02_Proprietary); ⊤ ⊑ ∀ hasIntellectualPropertyRegime.IntellectualPropertyRegime | 2 |
| Case02_Referral | Referral | AcquisitionChannel | usesAcquisitionChannel(Case02, Case02_Referral); ⊤ ⊑ ∀ usesAcquisitionChannel.AcquisitionChannel | 2 |
| Case02_RevenueStreamTransformation | RevenueStreamTransformation | ImplementationChallenge | facesChallenge(Case02, Case02_RevenueStreamTransformation); ⊤ ⊑ ∀ facesChallenge.ImplementationChallenge | 4 |
| Case02_SME | SME | CustomerType | targetsCustomerType(Case02, Case02_SME); ⊤ ⊑ ∀ targetsCustomerType.CustomerType | 2 |
| Case02_SecurityConcerns | SecurityConcerns | ImplementationChallenge | facesChallenge(Case02, Case02_SecurityConcerns); ⊤ ⊑ ∀ facesChallenge.ImplementationChallenge | 4 |
| Case02_ServiceQualityImprovement | ServiceQualityImprovement | SuccessFactor | hasSuccessFactor(Case02, Case02_ServiceQualityImprovement); ⊤ ⊑ ∀ hasSuccessFactor.SuccessFactor | 2 |
| Case02_StandaloneProduct | StandaloneProduct | EcosystemRole | hasEcosystemRole(Case02, Case02_StandaloneProduct); ⊤ ⊑ ∀ hasEcosystemRole.EcosystemRole | 2 |
| Case02_SubscriptionBasedPricing | SubscriptionBasedPricing | PricingStrategy | hasPricingStrategy(Case02, Case02_SubscriptionBasedPricing); ⊤ ⊑ ∀ hasPricingStrategy.PricingStrategy | 2 |
| Case02_SubscriptionRevenue | SubscriptionRevenue | RevenueSource | hasRevenueSource(Case02, Case02_SubscriptionRevenue); ⊤ ⊑ ∀ hasRevenueSource.RevenueSource | 2 |
| Case02_SupportRevenue | SupportRevenue | RevenueSource | hasRevenueSource(Case02, Case02_SupportRevenue); ⊤ ⊑ ∀ hasRevenueSource.RevenueSource | 2 |
| Case02_UserSeat | UserSeat | PricingBaseUnit | hasPricingBaseUnit(Case02, Case02_UserSeat); ⊤ ⊑ ∀ hasPricingBaseUnit.PricingBaseUnit | 2 |
| Case02_ValueBasedOrientation | ValueBasedOrientation | SuccessFactor | hasSuccessFactor(Case02, Case02_ValueBasedOrientation); ⊤ ⊑ ∀ hasSuccessFactor.SuccessFactor | 2 |
| Case02_FlexiblePricingStrategy | FlexiblePricingStrategy | MitigationStrategy | mitigates(Case02_FlexiblePricingStrategy, Case02_SecurityConcerns); ∃ mitigates.⊤ ⊑ MitigationStrategy | 4 |
| Case02_PilotImplementation | PilotImplementation | MitigationStrategy | mitigates(Case02_PilotImplementation, Case02_SecurityConcerns); ∃ mitigates.⊤ ⊑ MitigationStrategy | 4 |

Sondagens de mundo aberto (classes de teste temporárias, só no script): Case02 ∈ PlatformBusinessModel: não; Case02 ∈ ¬PlatformBusinessModel: não; Case02_StandaloneProduct ∈ ¬TwoSidedPlatform: sim.

---

## d) Expressividade (R29)

| Ferramenta | Antes | Depois |
|---|---|---|
| Pellet 2.3.1 `info` (OWLAPI 3.4.3) | **ALCQ(D)** | **ALCQ(D)** |
| ROBOT 1.9.6 `measure` (OWLAPI 4.5) | `RRESTRCQ(D)` | `RRESTRCUCINTEQ(D)` |

- A expressividade não muda: interseção, união e restrição existencial já estão em ALC. As cadeias do ROBOT são a lista de construtos sem normalização que o verificador do OWLAPI 4.5 produz (U, CINT e E aparecem separados, embora sejam cobertos por C). A notação usual é a do Pellet: ALCQ(D) (ALC com restrições qualificadas de cardinalidade e tipos de dados).
- O Protégé 5.6 usa o OWLAPI 4.5.x (o `sbmo.rdf` foi gerado pelo OWLAPI 4.5.29), então ele **pode** mostrar a mesma cadeia do ROBOT. Por isso o guia (§f, passo 6) inclui a leitura no Protégé. Sugestão para a §7.1: reportar ALCQ(D) e, se o Protégé mostrar outra cadeia, dizer em uma frase que ela lista os mesmos construtos.
- **Achado paralelo (D3):** o ROBOT diz `owl2_dl = false` para o `sbmo.rdf` atual. Há duas violações de perfil: `dcterms:license` não está declarada como `owl:AnnotationProperty`, e `xsd:gYear` (range de `hasLaunchYear` e `hasSourceYear`) não pertence ao *datatype map* do OWL 2. O Pellet raciocina normalmente. O texto afirma "OWL 2 DL" em vários lugares. Ver §h.

---

## e) Impacto no texto

### Números e lugares que mudam

| Lugar | Hoje | Proposta |
|---|---|---|
| `front_matter/abstract_en.tex:9` | "14 top-level classes, 75 subclasses … 13 object properties, and 8 data properties" | "14 top-level classes, 75 subclasses …, 4 defined classes, 13 object properties, and 8 data properties", e uma oração no fim de Results sobre a classificação inferida (ver esboço) |
| `abstract_pt.tex` | sem contagens | sem mudança (conferido) |
| `06_ontology.tex:116` (§6.3.1) | "defines 14 top-level classes" | mantém 14; acrescentar que, além delas, há 4 classes definidas (§6.4.3) e 93 classes nomeadas no total |
| `06_ontology.tex:122` | "75 subclasses in total, distributed across the 13 non-central top-level classes" | mantém (continua exato); acrescentar "In addition, four defined classes are subsumed by SoftwareBusinessModel (Section 6.4.3)" |
| Tabela 5 `top_level_classes.tex` | 14 linhas | sem mudança (classes definidas não são de topo) |
| Tabela 6 `subclasses.tex` | 13 linhas | acrescentar a linha "SoftwareBusinessModel (defined classes) · SubscriptionSaaSModel, FreemiumSubscriptionModel, PlatformBusinessModel, NetworkedPlatformModel" **ou** deixar a tabela como está e criar a tabela nova `defined-classes.tex`. Recomendo a tabela nova (com DL e evidência) e uma nota no rodapé da Tabela 6. |
| Figura 14 `class_hierarchy.tex` (nó `SoftwareBusinessModel`, linha 25; legenda, linha 185) | SBM sem filhos; "(14 top-level) and subclasses (75)" | 4 filhos de SBM com estilo próprio (borda dupla, rótulo ≡), `NetworkedPlatformModel` sob `PlatformBusinessModel` com aresta tracejada "inferred"; legenda nova com "defined class"; caption: "OWL classes (14 top-level), subclasses (75), and defined classes (4; dotted edge: subsumption inferred by Pellet)" |
| Figura 21 (Apêndice B) `class_model_cardinalities_tikz.tex` + texto do `appendix_sbmo_class_model.tex` | sem classes definidas | uma caixa UML «defined» com as 4 classes e generalização para SBM, mais uma nota UML com as 4 definições em Manchester; uma frase no texto do apêndice |
| `06_ontology.tex:214` (§6.4.1) | version IRI `…/sbmo/1.0` | `…/sbmo/1.1` |
| `06_ontology.tex:228` (§6.4.3) | "Two types of axioms" | "Three types": disjunção, cardinalidade mínima, **classes definidas** (equivalência) |
| `06_ontology.tex:230` (§6.4.3, disjunção) | 2 grupos, justificativa "a single SBM may combine…" | parágrafo novo: critério no nível do valor, disjunção entre dimensões, lista dentro das dimensões, retirada de Marketplace ⊥ TwoSidedPlatform (se D1), axiomas em DL |
| `06_ontology.tex:250` (§6.4.5) e `07:43` (§7.1) | consistência sem detalhes | acrescentar: a T-Box com as classes definidas e as disjunções é consistente e não tem classes insatisfatíveis; remissão aos testes negativos (§7.3) |
| §7.1 (`07_ontology_evaluation.tex`, após linha 43) | sem expressividade | parágrafo com ALCQ(D), 93 classes, 150 axiomas lógicos (com D1), ferramenta e versão |
| `07_ontology_evaluation.tex:55` (§7.2) | "no company, product, or respondent identifier is reported" | "…with one exception: Case02 describes Suassu, the product that motivated this research (Section 1.1), and is identified by product name with the respondent's authorization; no respondent is identified" |
| `07_ontology_evaluation.tex:10` (introdução do Cap. 7) | "in two complementary stages" | mencionar a nova seção de raciocínio |
| `08_conclusion.tex:15` | "14 top-level classes, 75 subclasses …" | incluir as 4 classes definidas e uma frase sobre a classificação inferida |
| §8.3 (`08_conclusion.tex:45`) | resumo da validação | uma frase: os 31 casos foram classificados pelo Pellet em configurações nomeadas; o Suassu (Case02), motivação da Introdução, foi classificado como SubscriptionSaaSModel e FreemiumSubscriptionModel |
| `01_introduction.tex:17` (§1.1) | Suassu sem retorno | ao fim do parágrafo: "The Suassu business model is instantiated as one of the validation cases and revisited in Section 7.3." |
| `03_theoretical_background.tex:200` | exemplo Subscription/PerpetualLicense | sem mudança; agora o exemplo coincide com um axioma real (opcional: remissão a §6.4.3) |
| `sbmo/README.md`, `sbmo/docs/CONTEXT.md:28` | métricas 14/75, sem classes definidas | 93 classes (14 + 75 + 4), axiomas, versão 1.1, registro de mudanças |
| `docs/defense/revision-tracker.md:364` (R36) | "com 89 classes" | "com 93 classes" (só o número; o R36 não é deste bloco) |
| Slides da defesa e da qualificação (`docs/*/presentation`) | 14/75, 89 classes | **não mexer**: registro histórico do que foi apresentado |

### Onde entram as classes definidas (Cap. 6)

Na §6.4.3 (*Axioms and Constraints*), como terceiro tipo de axioma, com as quatro definições em DL num ambiente `align*` e a tabela nova `assets/ontology/tables/defined-classes.tex` (classe, definição informal, evidência do SMS). Texto: as classes definidas dão condições necessárias **e suficientes**; elas não são povoadas à mão; o raciocinador as usa para classificar os casos e, na T-Box, infere `NetworkedPlatformModel ⊑ PlatformBusinessModel`. Isso também responde em parte à NOTA 15 (DL), sem fazer a tabela completa do R27.

### Esboço da nova seção do Cap. 7

Proposta: nova **§7.3 "Reasoning over the Instantiated Cases"**, logo após a §7.2, porque usa a A-Box povoada. As atuais §7.3 e §7.4 viram §7.4 e §7.5 (as referências são por `\ref`, então nada quebra). Esboço em inglês, a refinar na Fase 2:

> **7.3 Reasoning over the Instantiated Cases.** The competency-question queries of Section 7.2 retrieve what the A-Box asserts. This section reports what the Pellet reasoner derives from it, using the defined classes and disjointness axioms of Section 6.4.3, and closes the loop with the motivating product of Section 1.1.
>
> **Classification of the 31 cases.** Each case was asserted only as a SoftwareBusinessModel linked to its dimensional values; no case was asserted as a member of any defined class. After realization, Pellet classified 18 cases (58.1%) as SubscriptionSaaSModel, 15 (48.4%) as PlatformBusinessModel, 10 (32.3%) as NetworkedPlatformModel, and 4 (12.9%) as FreemiumSubscriptionModel; 5 cases fell into none of the four configurations. For every class, the inferred members coincide with the set computed independently from the questionnaire data. In addition, without any individual, the reasoner infers that NetworkedPlatformModel is subsumed by PlatformBusinessModel (Figure X, inferred hierarchy).
>
> **The Suassu case (Case02).** Case02 describes Suassu, the product whose business-model definition motivated this research (Section 1.1). Its respondent reported the product as partially operational and, as instructed by the questionnaire, described the business model planned for the following twelve months. Table Y contrasts what was declared with what Pellet inferred. Two facts were declared, that Case02 is delivered as multi-tenant SaaS and earns subscription revenue; from the definition of SubscriptionSaaSModel, Pellet inferred that Case02 is a SubscriptionSaaSModel (Figure Z shows the justification). Likewise, freemium pricing combined with subscription revenue yields FreemiumSubscriptionModel. The reasoner neither classifies Case02 as a PlatformBusinessModel nor as its complement: the A-Box asserts a standalone role but does not state that it is the only one, so under the open-world assumption the question remains open. It does, however, infer that the declared role is not a two-sided platform, from the disjointness of the two role types.
>
> **Negative tests.** Two test files import the validated A-Box unchanged and add a single erroneous assertion about Case02. Typing the standalone role also as a two-sided platform makes the knowledge base inconsistent, and Pellet's explanation consists of the two type assertions and the disjointness axiom. Using the freemium pricing value as a revenue source is also detected, although no conflicting type is asserted: the range of hasRevenueSource makes the value a RevenueSource, its asserted type makes it a PricingStrategy, and the two dimensions are disjoint. Without the dimension-level disjointness introduced in this version, the same error goes unnoticed.

Elementos: tabela "declarado × inferido" (versão compacta do §c, gerada por script); tabela ou frase com as contagens por classe; capturas 1 a 5 do §f; uma frase sobre propriedades inferidas (nenhuma, sem inversas).

### Onde fechar o ciclo Suassu (Mossmann P5)

1. §1.1 (`01_introduction.tex:17`): uma frase de remissão para a §7.3.
2. §7.2 (`07_ontology_evaluation.tex:55`): a exceção de anonimato para o Case02.
3. §7.3 (nova): o parágrafo do Suassu acima, com a tabela e as capturas.
4. §8.3: uma frase de síntese.

### Sobreposições com outros itens (só registrar no tracker)

- **R27 (DL completo):** as 4 definições e as novas disjunções em DL na §6.4.3 são parte da tabela que o R27 pede; o R27 continua pendente para o restante (subclasses, domínios e ranges, cardinalidades).
- **R26 (SWRL / propriedades entre dimensões):** `06_ontology.tex:261` diz que o SWRL é planejado "so that the artefact can also derive implicit commitments"; depois deste bloco a ontologia já deriva algumas. Ver D7. "Propriedades inferidas" (Lunardi) dependem de inversas/cadeias, ou seja, do R26 e do P13. A NOTA 21 (topo do Cap. 7) fica parcialmente atendida.
- **R25 (reuso BMO/e3value):** sem sobreposição.

---

## f) Guia de capturas do Protégé (rascunho; vai para `docs/defense/protege-screenshot-guide.md` na Fase 2)

**Só depois da Fase 2**, porque as capturas precisam do `sbmo.rdf` 1.1 e dos arquivos de teste.

### Preparação (uma vez)

1. Protégé 5.6.x com o plugin Pellet (*File > Check for plugins… > Pellet Reasoner Plug-in*; reiniciar). A distribuição oficial é preferível ao pacote do Arch (ver `validation/README.md`).
2. Nomes curtos: *File > Preferences > Renderer*, marcar a renderização pelo nome curto do IRI, para que apareça `SubscriptionSaaSModel` e não o IRI.
3. Fonte: se a sua versão permitir ajuste em *File > Preferences* (aba *Renderer* ou *Appearance*), use 14 a 16 pt; se não, aumente a escala do sistema antes de abrir o Protégé.
4. Janela maximizada em 1920×1080 ou mais. Salvar em PNG, sem reduzir a imagem; recortar com uma margem de ~10 px em volta do painel. Largura final entre 1200 e 1800 px para figura de largura total (meia largura: 800 a 1000 px).
5. Abrir `sbmo/validation/protege/sbmo-validation-abox.ttl` (*File > Open…*). O `catalog-v001.xml` que entra na Fase 2 resolve o import do `sbmo.rdf`. Se o Protégé avisar que não encontrou o import, aponte para `sbmo/sbmo.rdf`.
6. *Reasoner > Pellet*; depois *Reasoner > Start reasoner*. Não deve aparecer aviso de inconsistência.
7. *Reasoner > Configure…*: em *Displayed inferences*, deixe marcados os tipos de indivíduos (*Types*) e as superclasses de classes.

Pasta de destino: `sbm-ontology-dissertation/assets/ontology_evaluation/figures/` (criada na Fase 2).

### Captura 1 · hierarquia declarada × inferida

- Arquivos: `protege-class-hierarchy-asserted.png` e `protege-class-hierarchy-inferred.png` (entram como subfiguras a e b).
- Passos: aba *Entities > Classes*. No topo da vista *Class hierarchy*, há um seletor *Asserted / Inferred*. Recolha todas as classes de topo e expanda só `owl:Thing > SoftwareBusinessModel`; em *Inferred*, expanda também `PlatformBusinessModel`.
- O que deve aparecer: as 4 classes definidas (ícone com ≡). Em *Asserted*, as quatro como irmãs; em *Inferred*, `NetworkedPlatformModel` aninhada em `PlatformBusinessModel`. Se, na sua versão, o modo *Asserted* mostrar as classes definidas direto sob `owl:Thing`, anote isso no guia: a legenda descreve a captura.
- Recorte: só a vista *Class hierarchy*, do `owl:Thing` até a última classe visível. As duas capturas com o mesmo tamanho.

### Captura 2 · Case02: tipos declarados e inferidos

- Arquivo: `protege-case02-declared-inferred-types.png`.
- Passos: aba *Entities > Individuals* (ou *Individuals by class*); selecione `Case02`.
- O que deve aparecer: na vista *Description*, em *Types*, `SoftwareBusinessModel` (declarado, fundo normal) e `FreemiumSubscriptionModel` e `SubscriptionSaaSModel` (inferidos, fundo amarelo claro). Na vista *Property assertions*, as asserções declaradas de `Case02` (`hasDeliveryMode Case02_MultiTenantSaaS`, `hasRevenueSource Case02_SubscriptionRevenue`, `hasPricingStrategy Case02_FreemiumPricing`, …).
- Recorte: as vistas *Description* e *Property assertions* lado a lado, com o nome `Case02` visível no topo.

### Captura 3 · explicação "A e B, logo C"

- Arquivo: `protege-case02-explanation-subscription-saas.png`.
- Passos: na captura 2, clique no botão **?** à direita de `SubscriptionSaaSModel` (inferido). Abre a janela *Explanation for Case02 Type SubscriptionSaaSModel*.
- O que deve aparecer: a primeira justificativa com 6 axiomas: a definição de `SubscriptionSaaSModel`, `Case02 Type SoftwareBusinessModel`, `Case02 hasDeliveryMode Case02_MultiTenantSaaS`, `Case02_MultiTenantSaaS Type MultiTenantSaaS`, `Case02 hasRevenueSource Case02_SubscriptionRevenue`, `Case02_SubscriptionRevenue Type SubscriptionRevenue`. O Protégé pode listar mais justificativas (o script encontrou pelo menos 5); recorte só a primeira.
- Recorte: o conteúdo da janela de explicação, sem a barra de título do sistema.

### Captura 4 · DL Query sobre uma classe definida

- Arquivo: `protege-dl-query-freemium-subscription.png`.
- Passos: *Window > Tabs > DL Query*. No campo de consulta: `sbmo:FreemiumSubscriptionModel` (com prefixo, como em `dl_queries.md`). Marque *Instances* (e *Direct instances*, se quiser só os casos). *Execute*.
- O que deve aparecer: `Case02`, `Case05`, `Case22`, `Case24`. Opcional, para o texto: rodar também a expressão anônima `sbmo:SoftwareBusinessModel and (sbmo:hasPricingStrategy some sbmo:FreemiumPricing) and (sbmo:hasRevenueSource some sbmo:SubscriptionRevenue)` e conferir o mesmo resultado (não precisa capturar).
- Recorte: o campo da consulta e a lista de resultados.

### Captura 5 · teste negativo e explicação da inconsistência

- Arquivo: `protege-negative-test-explanation.png` (N1). Opcional: `protege-negative-test-misused-value-explanation.png` (N2).
- Passos: *File > Open…* `sbmo/validation/protege/case02-negative-test-disjoint-roles.ttl` (pode abrir em janela nova). *Reasoner > Start reasoner*. O Protégé avisa que a ontologia é inconsistente; clique em **Explain**.
- O que deve aparecer (N1): 3 axiomas: `Case02_StandaloneProduct Type StandaloneProduct`, `Case02_StandaloneProduct Type TwoSidedPlatform`, `StandaloneProduct DisjointWith TwoSidedPlatform`. (N2: duas justificativas, com os ranges de `hasRevenueSource` e `hasPricingStrategy` e o `DisjointClasses` das dimensões.)
- Recorte: a janela de explicação. Depois feche essa ontologia sem salvar.

### Passo 6 (sem figura) · expressividade

- Abrir só o `sbmo.rdf` (sem a A-Box) e ir à aba *Active ontology*, vista *Ontology metrics*. Anotar *DL expressivity*, *Class count* e *Logical axiom count*.
- "Antes": abrir a versão anterior, extraída com `git -C sbmo show c191f25:sbmo.rdf > /tmp/sbmo-1.0.rdf`. "Depois": o `sbmo.rdf` da Fase 2.
- Valores esperados pelo script: antes 89 classes e 131 axiomas lógicos; depois 93 e 150 (com D1). Registrar no tracker (R29) a cadeia exibida pelo Protégé.

### Inclusão no LaTeX (Fase 2)

Cada figura usa `\IfFileExists{assets/ontology_evaluation/figures/<arquivo>.png}{\includegraphics[...]{...}}{<caixa "figura pendente" com o nome do arquivo>}`, então o documento compila antes de as imagens existirem.

---

## g) As 7 CQs com a ontologia proposta

`check_cq_result_sets.py` (cópia temporária apontada para a T-Box proposta; o script do repositório não foi alterado), com e sem D1:

```
CQ1: returned=26 expected=26 documented=26 sets_equal=True
CQ2: returned=26 expected=26 documented=26 sets_equal=True
CQ3: returned=27 expected=27 documented=27 sets_equal=True
CQ4: returned=19 expected=19 documented=19 sets_equal=True
CQ5: returned=31 expected=31 documented=31 sets_equal=True
CQ6: returned=49 expected=49 documented=49 sets_equal=True
CQ7: returned=26 expected=26 documented=26 sets_equal=True
ALL OK
```

---

## h) Decisões para você e pontos de dúvida

- **D1 · Retirar `Marketplace ⊥ TwoSidedPlatform`?** *Recomendo sim.* Pelas definições do próprio questionário, todo marketplace é uma plataforma bilateral; o par contradiz o critério "por definição" que o texto declara, e um avaliador pode objetar. Nenhum resultado muda (CQs, classes definidas, testes). Alternativa mais forte, fora deste bloco: `Marketplace ⊑ TwoSidedPlatform`.
- **D2 · Incluir o segundo teste negativo (N2)?** *Recomendo sim.* É ele que mostra uma inconsistência obtida por inferência e o ganho das novas disjunções (antes passava, agora é detectado).
- **D3 · Perfil OWL 2 DL (achado novo, fora dos quatro itens).** Opções:
  - (a) Só registrar no tracker e qualificar a frase da §7.1 ("the T-Box uses xsd:gYear, outside the OWL 2 datatype map").
  - (b) Na Fase 2, declarar `dcterms:license` como `owl:AnnotationProperty` e trocar o range dos anos para `xsd:integer`. Isso exige mudar os literais `"2023"^^xsd:gYear` da A-Box. O CSV bruto não está nesta máquina, então seria uma edição mecânica do `.ttl` mais a mudança correspondente em `build_abox.py`, conferida por diff.
  - Testei que declarar `xsd:gYear` como `rdfs:Datatype` faz o ROBOT aceitar a T-Box, mas é um contorno: IRIs `xsd:` fora do *datatype map* não podem ser usados como tipos em OWL 2 DL, e a A-Box continua fora do perfil. Não recomendo.
  - *Minha recomendação:* (b) se você quiser afirmar OWL 2 DL sem ressalva ao lado da expressividade; senão, (a).
- **D4 · Nomes das classes.** `SubscriptionSaaSModel`, `FreemiumSubscriptionModel`, `PlatformBusinessModel`, `NetworkedPlatformModel`. Alternativas: `SaaSSubscriptionModel`; `NetworkEffectPlatformModel`.
- **D5 · Posição da seção de raciocínio.** Nova §7.3 (recomendado) ou subseção dentro da §7.2.
- **D6 · Versão.** `owl:versionIRI` 1.0 → 1.1, mais `owl:versionInfo "1.1"` e uma nota curta de mudanças no README. O A-Box importa o IRI da ontologia (sem versão), então não é afetado.
- **D7 · Frases sobre SWRL** (`06_ontology.tex:261`, `08_conclusion.tex:83`) passam a ficar imprecisas, pois a ontologia já deriva conhecimento. Proponho só um ajuste mínimo de redação ("additional implicit commitments beyond those derived from the defined classes") e registrar no R26; ou deixar intocado e só registrar.
- **Dúvidas e observações:**
  - O `README.md` do `sbmo` diz "SMS of 67 primary studies", e vários `rdfs:comment` do `sbmo.rdf` usam "67 articles" e percentuais sobre 67 (resquício de antes do R08). Os comentários novos usam 63. Corrijo os antigos junto, ou registro como pendência do R08?
  - §6.4.2 diz que indivíduos seguem lowerCamelCase, mas a A-Box usa `Case02`, `Case02_MultiTenantSaaS`. Como a nova seção vai exibir esses nomes, a frase fica visivelmente contraditória. Ajusto a convenção descrita (só redação) ou registro?
  - Captura 1, modo *Asserted*: não tenho como confirmar aqui se o Protégé 5.6 posiciona as classes definidas sob `SoftwareBusinessModel` (pelo conjunto nomeado) ou sob `owl:Thing`. O guia pede para conferir.
  - O consentimento prometia confidencialidade; a identificação do Case02 depende da autorização (vai para "Pendências finais"). O depósito Zenodo continua anônimo, mas, com o nome no texto, a linha Case02 do CSV publicado fica atribuível ao Suassu. Convém que a autorização cubra isso explicitamente.

---

## i) Plano da Fase 2 (após aprovação)

**sbmo:**
- `sbmo.rdf`: 4 classes definidas (RDF/XML no estilo do arquivo, com `rdfs:comment`); disjunções aprovadas (`owl:AllDisjointClasses` para grupos de 3 ou mais, `owl:disjointWith` para pares); retirada de Marketplace ⊥ TwoSidedPlatform (se D1); `owl:versionIRI` 1.1 e `owl:versionInfo`; itens de D3, se aprovados.
- `validation/protege/case02-negative-test-disjoint-roles.ttl` e `case02-negative-test-misused-value.ttl`; `validation/protege/catalog-v001.xml` (resolve os imports no Protégé).
- `validation/scripts/reasoning-demo.py`: classificação dos 31 casos (com conferência contra o CSV), tabela declarado × inferido do Case02, sondagens de mundo aberto, testes negativos com verificação do resultado esperado (código de saída ≠ 0 se algo divergir), métricas. Gera `validation/survey-derived/defined-class-counts.csv` e `case02-declared-inferred.csv` e as tabelas LaTeX na dissertação (como `analyze_survey.py`).
- `validation/scripts/Justify.java`: auxiliar de justificativas, compilado na hora com `javac` num diretório temporário.
- `README.md` (métricas e registro de mudanças), `validation/README.md` (como rodar), `docs/DESIGN_DECISIONS.md` (DD-011 classes definidas; DD-012 revisão da disjunção, substituindo a justificativa do DD-003), `docs/CONTEXT.md:28`.
- Rodar de novo `check_cq_result_sets.py` e `reasoning-demo.py`. Commits `feat(ontology): …`, `test(validation): …`, `docs: …`.

**dissertação:** todos os pontos do §e; tabelas novas `assets/ontology/tables/defined-classes.tex`, `assets/ontology_evaluation/tables/defined-class-counts.tex` e `case02-declared-inferred.tex`; figuras com `\IfFileExists`; `docs/defense/protege-screenshot-guide.md`; tracker (R30 pendente das capturas, R28, R34, R29; Pendências finais (a) e (b); sobreposições com R26/R27; R36 89 → 93). `make`, conferindo que não há referências indefinidas. Commits no padrão Conventional Commits, sem push.
