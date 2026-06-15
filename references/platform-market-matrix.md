# Platform and Market Matrix

This file is a routing map, not a live rulebook. Platform and regulator requirements change. For final decisions, verify current official sources and cite checked dates.

## Platform Review Surfaces

| Platform family | Common review surfaces |
|---|---|
| Amazon | Seller identity, category gating, brand registry/IP, product compliance, safety docs, restricted products, FBA/labeling |
| TikTok Shop | Seller/KYB, local entity or cross-border seller eligibility, category qualifications, product certifications, content/claims, fulfillment model |
| Shopee/Lazada | Seller identity, regional marketplace eligibility, brand authorization, prohibited/restricted goods, category-specific docs |
| Temu | Supplier/manufacturer qualification, product compliance, test reports, labels, factory/service capability, logistics readiness |
| AliExpress | Seller identity, brand/IP authorization, category admission, prohibited/restricted products, logistics/shipping constraints |
| Walmart/eBay | Seller identity, tax/payee, product restrictions, brand/IP, safety/compliance documentation |
| Tmall Global/JD Worldwide | Overseas entity qualification, brand authorization, product import/compliance docs, customs model, Chinese label/import requirements |

## Market Review Surfaces

| Market | Common qualification focus |
|---|---|
| US | Platform restricted categories, FDA/USDA/EPA/CPSC/FCC/FTC depending on product, importer/agent, labeling, claims |
| EU/EEA | CE/market surveillance, responsible person, GPSR, food/cosmetics/chemical rules, member-state language, VAT/IOSS/EORI where relevant |
| UK | UKCA/UK responsible person where applicable, UK product safety, labeling, VAT/import requirements |
| Japan | Importer/distributor responsibility, MHLW/PMDA/consumer labeling, Japanese language, category classification |
| Korea | MFDS/KC/category-specific rules, Korean labeling, local importer or responsible entity where required |
| ASEAN | Country-specific seller/category permits, local language labels, Halal sensitivity in selected markets, customs/import licensing |
| China import | Overseas entity/brand authorization, GACC/SAMR/NMPA or other regulator depending category, Chinese label, cross-border bonded/direct mail rules |
| Middle East | Local importer/distributor, Arabic labeling, Halal where relevant, conformity certificates depending country/category |

## Category Routing

| Category | Route to |
|---|---|
| Food, beverage, snacks, supplements | Food/supplement compliance, label, facility, ingredient, additive, claims, importer |
| Cosmetics, skincare, sunscreen, personal care | Cosmetics/drug classification, notification/registration, responsible person, ingredient and claims |
| Household chemicals, cleaners, aerosols | Chemical safety, SDS, hazard labeling, transport restrictions |
| Electronics, wireless, batteries | Electrical safety, EMC/radio, battery transport, e-waste/energy labels |
| Toys, baby products | Child safety standards, age grading, warning labels, test reports |
| Medical/therapeutic products | High risk. Escalate unless current specialist rules and professional review are available |

## Qualification Checklist Axes

For each platform/market/category combination, build a checklist from these axes:

1. Seller eligibility
2. Entity/KYB verification
3. Beneficial owner/KYC when required
4. Tax/payee/importer/local representative
5. Brand/IP rights
6. Product category admission
7. Product safety/compliance documents
8. Labeling and language
9. Claims and advertising
10. Logistics/warehouse/import route
11. Renewal and expiry monitoring
12. Manual review triggers

## High-Frequency Routes

`data/rulepacks/index.json` defines priority route hints for:

- Amazon US food / grocery
- TikTok Shop Southeast Asia cosmetics
- Temu electronics and batteries
- Tmall Global China import food/cosmetics

When one of these routes matches, `scripts/qualification_audit_schema.py checklist` returns `matched_priority_combinations` with expected packs and verification tasks. Treat these as accelerated triage instructions; final decisions still require current official platform and regulator sources.

## Current-Rule Verification

Before issuing a final decision:

- Search official marketplace policy pages for the exact platform/site/category.
- Search official regulator pages for the exact market/category if the finding depends on law/regulation.
- Prefer official policy pages over seller forums, agency blogs, or screenshots.
- Record source URL and checked date.
- If official pages are gated or unavailable, mark the conclusion as `needs_external_verification`.
