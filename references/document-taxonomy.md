# Document Taxonomy

Use this file to classify submitted materials, extract fields, and detect mismatches.

## Universal Document Fields

Extract when visible:

- document type
- holder/entity/person
- issuer
- document number
- issue date
- expiry date
- jurisdiction
- product/category/brand scope
- address
- authorized representative
- signature/seal/notarization
- language
- source file/page
- extraction confidence

If OCR is uncertain, mark `extraction_confidence: low` and require manual confirmation.

## Seller and Entity Documents

| Document | Key fields | Checks |
|---|---|---|
| Business license / registration certificate | Legal name, registration number, address, business scope, status, legal representative | Applicant name match, active status, business scope relevant |
| Tax registration / VAT / EIN / EORI | Tax ID, holder, jurisdiction | Holder match, marketplace/site requirement |
| Bank/payee document | Account holder, bank, country, currency | Holder match, sensitive data redaction |
| Beneficial owner / director ID | Name, ID type, nationality, expiry | PII handling, sanctions/manual review trigger |
| Importer of record / local representative | Entity, jurisdiction, authority, responsibility | Required for market/category, address and contact present |

## Brand and IP Documents

| Document | Key fields | Checks |
|---|---|---|
| Trademark certificate | Mark, class, owner, territory, registration number, status, expiry | Category/class fit, territory fit, owner match |
| Brand authorization letter | Grantor, grantee, brand, territory, platform/channel, product scope, dates, signature | Chain completeness, platform/channel allowed, still valid |
| Distribution agreement | Parties, territory, exclusivity, product scope, term | Applicant right to sell, conflict with brand owner |
| Invoice/proof of supply | Seller, buyer, product, date | Supports supply chain but rarely proves IP rights alone |

Red flags:

- authorization grants "global" rights but signer is only a local distributor
- territory excludes the target marketplace country
- platform/channel is not mentioned when platform requires it
- trademark class does not cover the product category
- product uses a brand variant not shown in the authorization

## Product and Compliance Documents

| Document | Key fields | Checks |
|---|---|---|
| Product specification | Product name, model/SKU, ingredients/materials, intended use | Match category and listing |
| Label/artwork | Required language, net content, warnings, importer/manufacturer, claims | Market/platform label requirements |
| Test report | Lab, accreditation, standard, sample ID, product/model, result, date | Lab scope, standard relevance, sample match, recency |
| Certificate of analysis | Batch, analytes, limits, result, method, lab | Batch/category fit, not a substitute for all regulatory approvals |
| SDS/MSDS | Hazard classification, product name, issuer, date | Required for chemicals, batteries, aerosols, cosmetics logistics |
| GMP/HACCP/ISO | Holder, site, standard, scope, certification body, validity | Manufacturing site match, scope fit, cert body credibility |
| Halal/Organic/Kosher | Certifier, product/site, territory, validity | Claim support and marketplace acceptance |

## Category-Specific Materials

### Food and beverage

- facility registration
- food safety plan/HACCP/GMP
- ingredient list with percentages when needed
- allergen statement
- nutrition facts
- additive and contaminant test reports
- health/sanitary certificate
- certificate of origin
- importer/local representative where required

### Cosmetics and personal care

- responsible person/local agent
- product notification/registration where required
- INCI ingredient list
- safety assessment/CPSR/PIF where required
- GMP certificate
- claim substantiation
- preservative/microbiology/heavy metal test reports
- sunscreen/OTC/drug classification evidence when claims trigger it

### Dietary supplements and health products

- product classification basis
- manufacturing GMP
- ingredient legality/novel ingredient status
- structure/function claim review
- label disclaimer and warnings
- COA and contaminant testing
- importer/local registration where required

### Electronics, batteries, toys, and household goods

- CE/FCC/UKCA/RCM or market-specific conformity evidence
- safety test reports
- battery transport docs
- RoHS/REACH/Prop 65/chemical declarations where relevant
- child safety/toy standards where relevant

## Consistency Checks

Run these across all documents:

- Applicant legal name equals seller/store applicant or valid authorization exists.
- Brand owner equals trademark owner or authorization chain is complete.
- Product name/SKU/model on test report matches listing.
- Certificate scope covers product category and manufacturing site.
- Issuer is competent for the claimed certificate.
- Issue/expiry dates are valid at review time.
- Territory and marketplace/channel cover intended sale.
- Language/translation is adequate for the platform or local market.
- Document holder is not a trading company when platform requires manufacturer evidence, unless accepted by rule/source.

