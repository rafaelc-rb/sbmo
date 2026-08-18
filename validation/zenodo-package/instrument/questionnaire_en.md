# SBMO Validation Questionnaire (instrument, English translation)

*This is a translation of the verified Portuguese original
(`questionnaire_pt.md`), confirmed against a PDF export of the real form
that collected the 31 responses. No evidence was found that an
English-language variant of the form was ever actually deployed; all 31 raw
responses use Portuguese field values, so only the Portuguese form is a
confirmed data-collection instrument. Structure only, no responses. The
form begins with the E-mail field (required) and the Informed Consent (see
`../informed_consent/informed_consent_en.md`), followed by these 15
sections. Estimated completion time: 15-20 minutes. Sections 9, 10, and 11
are optional; all others are required. Multi-select questions marked
"Select all that apply" (Section 2 requires at least one).*

**Initial field:** E-mail (required).

## 1. Company and product identification

Basic information to identify the company and its main software product or service.

- **Company name** (required): Official name of the company. *(used for research administration only, not published)*
- **Product or service name** (required): Name of the main software product or service you offer. *(not published)*
- **Launch year** (optional): Year the product/service was first launched or made available (e.g. 2018).
- **Brief description of the business model** (required): In 2-4 sentences, describe how this product/service creates value and revenue. Example: "We offer a B2B SaaS for project management, sold via monthly subscription with a free tier for small teams."
- **Respondent's name and role** (required): Your name and role in the company (e.g. "Alex Smith, CTO"). *(not published; only the role portion is used, in aggregated categories, for the socio-demographic analysis)*
- **What is your knowledge of the business model of this product/service?** (required): scale 1 (No) to 5 (I know it very well).
- **Is the business model of this product/service already operational?** (required): Yes / No / Partially. If "No" or "Partially", answer the remaining questions based on the planned scenario for the next 12 months.

## 2. Type of product or service *(required; select all that apply, at least one)*
Application; Platform; Managed service; API service; Data product; Infrastructure; SDK / developer kit; Other (specify).

## 3. Delivery mode *(required; select all that apply)*
SaaS multi-tenant; SaaS single-tenant; On-premises; Mobile delivery; Desktop delivery; Hybrid delivery; Other (specify).

## 4. Revenue sources *(required; select all that apply)*
Subscription revenue; Usage/consumption revenue; Transaction revenue; Advertising revenue; Perpetual license; Support revenue; Marketplace take rate; Open core; Dual licensing; Other (specify).

## 5. Pricing strategy *(required; select all that apply)*
Subscription pricing; Pay-as-you-go pricing; Freemium; Value-based pricing; Cost-based pricing; Other (specify).
Also collects: **Billing cadence** (free text, optional; e.g. monthly, annual, per transaction) and **Pricing description** (free text, optional; e.g. "We have 3 plans: Free, Pro (R$99/month), Enterprise (custom quote).").

## 6. Customer type *(required; select all that apply)*
B2B; B2C; SMEs; Enterprise; Government; Developer tools; Other (specify).

## 7. Ecosystem role *(required; select all that apply)*
Standalone product; Two-sided platform; Marketplace; OEM component; Plugin / add-on; Other (specify).

## 8. Acquisition channel *(required; select all that apply)*
Direct sales; Product-led growth; Partner channel; Digital marketing; Marketplace channel; Referral; Other (specify).

## 9. Intellectual property *(optional; select all that apply)*
Proprietary; Permissive open source (MIT, Apache, BSD); Open source (broad, community-driven); Dual license; Open core; Copyleft (GPL, AGPL); Other (specify).

## 10. Base pricing unit *(optional; select all that apply)*
User / license; Transaction-based; Compute time; Revenue share; API calls; Storage; Device; Other (specify).

## 11. Network effects *(optional; select all that apply)*
Direct network effect; Cross-side network effect; Data-driven effect; No significant network effects; Other (specify).

## 12. Success factors *(required; select all that apply)*
Ecosystem management; Market expansion; Service quality; Organizational readiness; Value focus; Other (specify).

## 13. Implementation challenges *(required; select all that apply)*
Security concerns; Revenue stream transformation; Customer trust; Partner ecosystem disruption; Organizational readiness; Quality management; Other (specify).

## 14. Mitigation strategies *(required; select all that apply)*
Flexible pricing; Hybrid model; Pilot implementation; Partner compensation; Other (specify).
Also collects: **Which challenge does each mitigation address?** (free text, optional). Example given on the form: "Flexible pricing -> revenue stream transition; Pilot -> security".

## 15. Additional comments
- **Comments or additional notes** (free text, optional): Is there any aspect of your software business model that was not covered by the questions above? Any important dimension you consider missing?
- **Would you be available for a short follow-up call (15-20 min) to clarify answers?** (optional): Yes / No / Maybe.

---

Each of the 13 controlled-vocabulary questions (Sections 2-14, excluding the two free-text fields in Sections 5 and 14) maps directly onto one SBMO ontology dimension; see `../data/data_dictionary.md` for the full label-to-class mapping used to build `../data/cases_normalized.csv`.
