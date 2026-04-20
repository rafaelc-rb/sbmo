# SBMO MVP Scope Plan

## Objective

This document defines the implementation scope of the **SBMO MVP** for practical validation through the instantiation of **real software cases**.

The MVP is considered successful if it:

- covers the SMS-backed dimensions that are necessary to describe and compare real software business models;
- includes enough relations, typed attributes, and constraints to avoid reducing the ontology to a taxonomy;
- can be instantiated, checked, and queried in Protégé without major refactoring.

## Implementation status (current)

This document is maintained as both scope reference and progress tracker.

- **Completed in ontology (`sbmo.rdf`)**:
  - New dimensions: `ProductOrServiceType`, `IntellectualPropertyRegime`, `PricingBaseUnit`
  - Core cardinalities with `minQualifiedCardinality`
  - Data properties layer (intrinsic + documentation)
  - Coverage-gap subclasses added before field validation
  - Clean T-Box distribution (synthetic individuals removed)
- **Pending in research workflow**:
  - Real-case instantiation with companies
  - CQ execution over empirical A-Box data
  - Validation reporting and potential post-field refinements

## Scope principles

### 1. Completeness with parsimony

The MVP should include the minimum necessary coverage to avoid unjustified omissions of relevant SMS evidence. It is not intended to be exhaustive.

### 2. Practical applicability

Every element kept in the MVP should help with at least one of the following:

- describing a real software case;
- comparing cases;
- checking consistency;
- answering practical queries.

### 3. Ontological expressiveness

The MVP must not remain only a hierarchy of classes. It must combine:

- classes;
- object properties;
- data properties;
- cardinality constraints.

### 4. Evidence-driven inclusion

An element should enter the MVP when most of the following are true:

1. It is supported by the SMS or by the validation evidence used for real cases.
2. It improves the practical description of real software business models.
3. Its absence would weaken case instantiation or comparison.
4. Its exclusion would be difficult to justify during validation.

## Modeling rules

### 1. Rule for new dimensions

Any new business-model dimension added to the MVP must be modeled as:

- an OWL class representing the dimension; and
- a dedicated object property linking `SoftwareBusinessModel` to that dimension,

unless there is a clear reason to reuse an existing relation.

No new top-level dimension should enter the MVP as an isolated hierarchy without an explicit connection to `SoftwareBusinessModel`.

### 2. Rule for data properties

Data properties are part of the MVP expressive core. They are divided into:

- **intrinsic data properties**: typed attributes used to describe the instantiated software business model itself;
- **documentation data properties**: typed attributes used to identify and trace the real case used in validation.

For the MVP, unless a new application-layer class is explicitly introduced, data properties should be attached to `SoftwareBusinessModel` individuals.

No data property should be added without:

- an explicit domain;
- an explicit range;
- a practical use during instantiation or validation.

### 3. Rule for object properties

Object properties should not be added only to increase the number of relations in the model.

A new object property should enter the MVP only if it:

- improves the semantic description of real cases;
- reduces the risk of the ontology remaining overly taxonomic;
- supports comparison, querying, consistency checking, or future inference.

### 4. Rule for cardinality

Cardinality constraints should be used whenever the intention is to guarantee that each instantiated case contains the minimum required relations.

For the MVP:

- minimum cardinality is preferred when the goal is mandatory presence;
- maximum cardinality should be avoided unless there is strong empirical justification;
- existential formulations alone should not be relied upon when the intended effect is per-individual obligation.

## MVP scope

### 1. Core classes already in scope

The current SBMO core remains in scope:

- `SoftwareBusinessModel`
- `RevenueSource`
- `PricingStrategy`
- `DeliveryMode`
- `CustomerType`
- `EcosystemRole`
- `AcquisitionChannel`
- `NetworkEffectType`
- `SuccessFactor`
- `ImplementationChallenge`
- `MitigationStrategy`

### 2. Core object properties already in scope

The current object properties remain in scope:

- `hasRevenueSource`
- `hasPricingStrategy`
- `hasDeliveryMode`
- `targetsCustomerType`
- `hasEcosystemRole`
- `usesAcquisitionChannel`
- `hasSuccessFactor`
- `facesChallenge`
- `exhibitsNetworkEffect`
- `mitigates`

These relations are kept because they already represent the SBMO as a configuration, not only as a list of categories.

### 3. New dimensions that must enter the MVP

To avoid relevant gaps during validation with real software cases, the MVP should incorporate the following additional dimensions from the SMS:

- `ProductOrServiceType`
- `IntellectualPropertyRegime`
- `PricingBaseUnit`

For implementation consistency, each of these dimensions should enter the ontology as:

- a new class; and
- a new object property from `SoftwareBusinessModel`.

Recommended object properties:

- `hasProductOrServiceType`
- `hasIntellectualPropertyRegime`
- `hasPricingBaseUnit`

### 4. Cardinality policy for the MVP

The following relations should remain mandatory for each `SoftwareBusinessModel` individual:

- `hasDeliveryMode min 1 DeliveryMode`
- `hasEcosystemRole min 1 EcosystemRole`
- `hasRevenueSource min 1 RevenueSource`
- `hasPricingStrategy min 1 PricingStrategy`
- `targetsCustomerType min 1 CustomerType`
- `usesAcquisitionChannel min 1 AcquisitionChannel`

The following relation should also become mandatory in the MVP:

- `hasProductOrServiceType min 1 ProductOrServiceType`

The following relations should enter the MVP as modeled but initially optional:

- `hasIntellectualPropertyRegime`
- `hasPricingBaseUnit`
- `hasSuccessFactor`
- `facesChallenge`
- `exhibitsNetworkEffect`

The following constraint remains mandatory:

- `mitigates min 1 ImplementationChallenge` for `MitigationStrategy`

This policy keeps the core case description complete while avoiding over-constraining dimensions that are not universally available in the evidence base.

### 5. Intrinsic data properties that should be evaluated for inclusion

The MVP should include a small subset of intrinsic typed attributes. Candidate properties are:

- `hasBillingPeriodicity`
- `hasLaunchYear`
- `hasBasePriceAmount`
- `hasTrialPeriodDays`
- `hasRevenueSharePercentage`
- `hasPricingDescription`

These should not all be added automatically. Each one must be evaluated according to:

1. evidence support;
2. usefulness for distinguishing real cases;
3. contribution beyond what is already captured by classes and object properties.

Recommended initial datatypes:

- `hasBillingPeriodicity` -> `xsd:string`
- `hasLaunchYear` -> `xsd:gYear` or `xsd:integer`
- `hasBasePriceAmount` -> `xsd:decimal`
- `hasTrialPeriodDays` -> `xsd:integer`
- `hasRevenueSharePercentage` -> `xsd:decimal`
- `hasPricingDescription` -> `xsd:string`

### 6. Documentation data properties that should enter the MVP

The following documentation properties should enter the MVP to support traceable real-case validation:

- `hasCompanyName`
- `hasProductName`
- `hasEvidenceSource`
- `hasSourceYear`
- `hasCaseDescription`

Recommended datatypes:

- `hasCompanyName` -> `xsd:string`
- `hasProductName` -> `xsd:string`
- `hasEvidenceSource` -> `xsd:string`
- `hasSourceYear` -> `xsd:gYear` or `xsd:integer`
- `hasCaseDescription` -> `xsd:string`

### 7. What stays outside the MVP

The following elements may remain outside the MVP, provided that the exclusion is explicit and deliberate:

- `GeographicScope`
- `IndustryFocus`
- `CompanyCharacteristics`
- `ModelMaturity`
- `FutureTrends`
- fine-grained technical architecture such as multi-instance, single-version, remote hosting, or connectivity requirements
- full Business Model Canvas coverage
- temporal evolution or pivot history
- mass population of instances
- legal and regulatory dimension
- alignment with external ontologies

These items are not rejected permanently. They are postponed because they are not essential to the first practical validation cycle.

## Practical implementation order

### Phase 1. Stabilize the current core

- preserve the current central classes;
- preserve the current core object properties;
- preserve the current mandatory cardinalities already present in the ontology.

### Phase 2. Add the missing MVP dimensions

- create `ProductOrServiceType`;
- create `IntellectualPropertyRegime`;
- create `PricingBaseUnit`;
- create the object properties linking them to `SoftwareBusinessModel`;
- define their subclasses from the SMS extraction categories.

### Phase 3. Define the cardinality profile

- keep the current mandatory cardinalities already implemented;
- add `hasProductOrServiceType min 1 ProductOrServiceType`;
- keep `hasIntellectualPropertyRegime` and `hasPricingBaseUnit` optional in the first MVP cycle unless stronger validation evidence requires otherwise.

### Phase 4. Add intrinsic data properties

- choose a small defensible subset of intrinsic typed attributes;
- assign explicit domains and ranges;
- keep only the attributes that materially improve case description.

### Phase 5. Add documentation data properties

- add the minimum traceability attributes for real-case validation;
- keep this layer small and operational.

### Phase 6. Audit the relational layer

- review whether the existing and newly added object properties are enough to compare cases meaningfully;
- identify isolated branches that do not contribute to practical use;
- add extra relations only if they clearly improve semantic expressiveness.

### Phase 7. Instantiate real software cases

The MVP should be tested with a small but representative case set.

Recommended size:

- 4 to 8 real software cases

Recommended diversity:

- B2B SaaS subscription case
- B2C freemium case
- platform or marketplace case
- on-premises or hybrid case
- case with strong ecosystem participation
- case with clear network effects

For each case, populate at least:

- company and product identification;
- product or service type;
- delivery mode;
- revenue source;
- pricing strategy;
- customer type;
- ecosystem role;
- acquisition channel.

Populate when evidence is available:

- intellectual property regime;
- pricing base unit;
- intrinsic data properties;
- success factors;
- implementation challenges;
- mitigation strategies;
- network effects.

### Phase 8. Evaluate inference readiness

- verify whether the ontology already supports useful reasoning through classification or consistency checking;
- identify SWRL candidates only if they add practical value to the MVP;
- postpone broader rule sets if they increase complexity without improving the first validation cycle.

### Phase 9. Validate in practice

The MVP validation should demonstrate that the ontology can:

- represent real software business models consistently;
- compare different cases through shared dimensions;
- answer practical competency-style queries;
- represent relevant intrinsic attributes through typed properties, not only through inter-concept relations;
- enforce minimum completeness through cardinality constraints;
- avoid collapsing into a purely taxonomic model;
- support consistency checking and, if implemented, inference.

## Expected outcome

At the end of this phase, the SBMO should have a version that is sufficiently complete, coherent, clear, and practical to be instantiated in real software companies without obvious conceptual gaps relative to the intended MVP scope.
