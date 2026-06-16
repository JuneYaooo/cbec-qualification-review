<div align="center">

# cbec-qualification-review

**An AI pre-launch checkup for cross-border products: decide whether a product can sell, is worth launching, and what must be fixed before listing.**

[中文](./README.md)

[![Skill](https://img.shields.io/badge/Agent-Skill-orange.svg)](./SKILL.md)
[![Hackathon](https://img.shields.io/badge/International%20Food%20Expo%20Hackathon-2nd%20Place-gold.svg)](#)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![No dependencies](https://img.shields.io/badge/dependencies-none-green.svg)](./scripts/qualification_audit_schema.py)

2nd place project at an International Food Expo hackathon, now open sourced.

</div>

---

Use it with a product idea, target market, marketplace, packaging label, certificate report, or brand document. It surfaces the issues sellers repeatedly miss: platform admission, competitor pricing, packaging and label readiness, logistics budget, qualification gaps, and remediation tasks.

## The Three Things Sellers Get Stuck On

- **Marketplace review blocks**: what does Amazon / TikTok Shop / Shopee / Temu need, and which authorization, label, or certificate is insufficient?
- **Pre-listing uncertainty**: is the product restricted, certification-heavy, label-sensitive, hard to ship, or dependent on a local responsible party?
- **Pricing without evidence**: who are the competitors, where is the price band, and how should packaging and positioning differentiate?

## What You Can Ask Directly

```text
Is this olive oil suitable for Amazon US? Review competitors, pricing, packaging, logistics, and listing risks.
```

```text
This skincare product is going to TikTok Shop Malaysia. What documents are needed and what label risks exist?
```

```text
For this electronics product entering the EU, should we use air freight, sea freight, or overseas warehouse?
```

```text
The marketplace asked for brand authorization and lab reports. Tell me what is actually missing and draft a supplement request.
```

```text
Based on these competitor screenshots and product details, suggest price band, channels, packaging angles, and launch preparation tasks.
```

## What It Gives You

| Output | Problem Solved |
| --- | --- |
| Launch feasibility | Can this product sell, and where might it get blocked? |
| Competitor and price band | How to price and differentiate |
| Packaging and label suggestions | How to adjust front/back label, claims, marks, warnings, and localization |
| Marketplace admission checklist | What Amazon / TikTok Shop / Shopee / Temu and similar platforms require |
| Logistics budget comparison | How to choose air, sea, rail, overseas warehouse, or local delivery |
| Qualification and certificate review | Whether business registration, brand authorization, trademark, COA, SDS, and lab reports match |
| Remediation wording | Clear requests for suppliers, sellers, or service providers |

## Frequent Use Cases

| Scenario | Why It Is Frequent | Typical Output |
| --- | --- | --- |
| New product launch review | Every new listing needs market, platform, and compliance risk checks | Launch feasibility, risks, materials, next actions |
| Marketplace/category review block | Sellers often get stuck on qualification, authorization, or label requests | Gap explanation, supplement list, applicant-facing wording |
| Competitor and pricing refresh | Pricing and positioning change repeatedly | Competitor table, channel price bands, differentiation advice |
| Packaging and label localization | Food, cosmetics, electronics, and household goods often need local packaging changes | Label suggestions, warning/claim/certification checks |
| Logistics route selection | Cost, time, restrictions, and cash tied up directly affect margin | Air/sea/rail/warehouse comparison |
| Internal review SOP | Teams need reusable operating rules and audit trails | Rule matrix, JSON output, audit log, review records |

## How It Decides

![CBEC Product Launch Review project logic diagram](./assets/project-logic-diagram-en.png)

<details>
<summary>Structured Decision Statuses</summary>

| Status | Meaning |
| --- | --- |
| `approve` | Current evidence and verification support moving forward. |
| `conditional_approve` | Can proceed after bounded low/medium fixes are completed. |
| `request_more_info` | Material evidence is missing, unverifiable, or out of scope. |
| `reject` | Confirmed serious non-compliance, prohibited product, unauthorized sale, or unfixable invalid material. |
| `escalate_human` | Suspected fraud, sanctions/export-control concern, sensitive identity issue, legal ambiguity, or conflicting authoritative sources. |
| `not_applicable` | The requested review does not apply to the given platform, market, category, or purpose. |

</details>

## Who It Helps Most

| User | Real pain | Value |
| --- | --- | --- |
| Cross-border sellers and brands | Inventory is ready, then the marketplace asks for documents, rejects the label, or flags the authorization | See whether the product can move forward before sampling, stocking, ads, or warehouse booking |
| Product and operations teams | Selection decisions focus on sales and price while ignoring admission, label, logistics, and after-sales risk | Turn "worth selling" into a view of opportunity, blockers, cost pressure, and next actions |
| Compliance and qualification teams | Review standards vary by person, supplement requests are unclear, and decisions are hard to audit | Convert review work into fixed statuses, evidence tables, gap lists, and auditable records |
| Agencies and service providers | Client materials are messy, and every clarification round costs time | Identify which materials are usable, which must be reissued, and how to ask for them clearly |

## The Risks It Helps You Avoid

- **Inventory stuck before launch**: catch prohibited categories, gated categories, certification gaps, label blockers, local responsible-party needs, dangerous goods, and cold-chain constraints before the product reaches the warehouse.
- **Endless document loops**: compare business registration, brand authorization, trademark, test report, COA, SDS, and label evidence in one place so entity, product, model, territory, platform, and validity line up.
- **Pricing by guesswork**: connect competitors, channels, packaging claims, price bands, and logistics cost instead of pricing only from factory cost.
- **Packaging reprints**: review front/back label, nutrition or ingredient panels, allergens, warnings, certification marks, responsible party, language, and high-risk claims before printing.
- **Vague marketplace rejections**: translate requests such as "submit brand authorization" or "provide test reports" into the exact missing document, acceptable format, issuer, scope, and validity period.

## Coverage

The rule packs cover:

- Marketplaces: Amazon, TikTok Shop, Shopee, Temu, Lazada, AliExpress, Tmall Global
- Markets and regions: US, EU / EEA, UK, Japan, China import, ASEAN / Southeast Asia
- Categories: food, cosmetics, supplements, electronics, household chemicals

The review routes connect to official or authoritative source entry points such as Amazon Seller Central, TikTok Shop Seller Center, FDA, CBP, European Commission, FCC, CPSC, ASEAN, Singapore HSA, Malaysia NPRA, GOV.UK, MHLW, METI, GACC, SAMR, NMPA, WIPO, EUIPO, and USPTO.

Those sources do not mean a product is automatically approved. They make the review traceable: every important conclusion can point back to submitted evidence, applicable rules, source tier, and checked date.

## What Users Actually Get

| Capability | User-facing result | Why it matters |
| --- | --- | --- |
| Pre-launch checkup | go / caution / stop / unknown, plus the top 3-5 risks | Decide whether to continue, change market, change platform, or pause before stocking |
| Qualification gap review | Which material is missing, expired, mismatched, or unverifiable | Stop guessing what the marketplace actually wants |
| Brand authorization review | Whether authorization covers the owner, territory, category, marketplace channel, and validity period | Avoid hidden IP risk from "authorized, but not for this country or channel" |
| Label and claim review | Which words, marks, warnings, language, ingredients, or claims need revision | Fix packaging before printing or overseas inventory movement |
| Competitor and price-band view | Competitor tiers, channel prices, package differentiation, and price suggestions | Build pricing and positioning from evidence rather than instinct |
| Logistics comparison | Air, sea, rail, overseas warehouse, and local delivery tradeoffs | Consider margin, cash tied up, delivery time, and platform constraints together |
| Supplement request wording | Clear messages for suppliers, sellers, or service providers | Reduce back-and-forth and make document requirements concrete |
| Audit trail | Status, evidence, sources, gaps, decision, and reviewer notes | Support handoff, appeal, review, and internal process control |

## Why It Is Trustworthy

- **It establishes scope first**: platform, country, category, business model, applicant role, brand/IP, and submitted materials all affect the decision.
- **It does not trust documents just because they look official**: applicant-provided files prove submission, not external truth; important facts still need registry, issuer, regulator, or platform verification.
- **It does not rely on memory for current rules**: platform rules, regulatory requirements, and logistics constraints change, so outputs separate verified facts from assumptions.
- **It is not a black-box score**: every issue is expressed as severity, evidence, source, impact, and required action.
- **It will not force a pass**: missing scope, missing evidence, expired materials, out-of-scope authorization, suspected alteration, or conflicting official sources produce supplement, rejection, or human escalation.

## Quality Status

The project has three quality layers:

- All indexed rule requirements have source entry points, currently covering 116 source links.
- Seven replayable review examples cover approval, supplement request, rejection, human escalation, expired certificate, territory mismatch, and unverified applicant evidence.
- Review output follows a fixed JSON contract, making it usable for internal systems, SOPs, reviewer handoff, and audit records.

Rule-pack maturity is still `seed`. That means the project is useful for pre-launch checkups, material pre-review, supplement generation, and internal review support. Final platform submission, enforcement decisions, legal conclusions, and high-risk category decisions still require human review and current official confirmation.

## Safety And Scope

This project supports cross-border product launch review, marketplace listing preparation, qualification review, material pre-review, remediation drafting, and internal process design. It does not provide legal advice and does not replace final judgment from marketplaces, regulators, certification bodies, or professional compliance advisors.

When documents contain identity records, bank accounts, personal contact details, contracts, business registration numbers, or other sensitive data, follow [`references/privacy-security.md`](./references/privacy-security.md) for minimization, redaction, and audit records.
