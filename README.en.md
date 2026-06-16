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

The expensive mistake in cross-border commerce is often not choosing the wrong product. It is **stocking the product first, then discovering that the marketplace needs more documents, the authorization does not cover the channel, the label must be reprinted, or the category cannot be sold**.

Give it a product, target market, marketplace, packaging label, certificate report, or brand document. It surfaces what can move forward, what needs remediation, and what should stop for human review.

## Core Problems It Solves

- **Pre-listing uncertainty**: can this product sell on Amazon, TikTok Shop, Shopee, Temu, Lazada, AliExpress, or Tmall Global?
- **Marketplace review blocks**: is the real gap brand authorization, a test report, a label issue, an expired certificate, or a scope mismatch?
- **Packaging and claims risk**: what needs to change in ingredients, allergens, warnings, marks, responsible party, language, or product claims?
- **Pricing and logistics without evidence**: who are the competitors, where is the price band, and will freight or warehousing destroy margin?
- **Inconsistent team review**: reviewers rely on experience, but supplement requests, evidence records, and audit trails are hard to standardize.

## What Users Get

| What you need to know | What it returns |
| --- | --- |
| Whether to keep pushing the product | go / caution / stop / unknown, plus the top risks |
| What is missing before listing | Gaps across marketplace, market, category, brand, label, certificates, and logistics |
| Why the marketplace is blocking review | Missing, expired, mismatched, or unverifiable documents |
| Whether packaging needs revision | Label, warning, ingredient, mark, localization, and claim risks |
| How to price and position | Competitor tiers, channel price bands, packaging angles, and differentiation notes |
| What to ask suppliers or clients for | Clear remediation wording with material, issuer, format, validity, and scope |
| How a team can review consistently | Status, evidence, source, finding, decision, and audit records |

## See The Outputs

### Consumer And Competitor Signals

![Consumer and competitor signals](./assets/demo-consumer-competitor-signals.png)

### Competitor Pricing And Channel Insight

![Competitor pricing and channels](./assets/demo-competitor-pricing-channels.png)

### Packaging, Formula And Pricing Suggestions

![Packaging, formula and pricing](./assets/demo-packaging-formula-pricing.png)

### Logistics Comparison And Budget

![Logistics budget comparison](./assets/demo-logistics-budget-eu.png)

### US Retail Shelf Concept

![US retail shelf concept](./assets/demo-retail-shelf-concept.png)

## Who It Is For

- **Cross-border sellers and brands**: know whether the product is worth continuing before sampling, stocking, advertising, or booking inventory.
- **Product and operations teams**: evaluate admission, packaging, logistics, and compliance cost alongside sales potential.
- **Compliance and qualification teams**: turn review judgment into fixed statuses, evidence tables, gap lists, and auditable records.
- **Agencies and service providers**: identify which client materials can be used, which must be reissued, and how to ask clearly.

## Coverage

- Marketplaces: Amazon, TikTok Shop, Shopee, Temu, Lazada, AliExpress, Tmall Global
- Markets and regions: US, EU / EEA, UK, Japan, China import, ASEAN / Southeast Asia
- Categories: food, cosmetics, supplements, electronics, household chemicals

Review routes connect to official or authoritative source entry points such as Amazon Seller Central, TikTok Shop Seller Center, FDA, CBP, European Commission, FCC, CPSC, ASEAN, Singapore HSA, Malaysia NPRA, GOV.UK, MHLW, METI, GACC, SAMR, NMPA, WIPO, EUIPO, and USPTO.

## Why It Is More Than Generic Advice

- It establishes platform, country, category, business model, applicant role, brand/IP, and material scope before judging.
- Applicant-provided files prove submission, not external truth; important facts still need registry, issuer, regulator, or platform verification.
- Every issue is tied to severity, evidence, source, impact, and required action so humans can review it.
- Missing scope, missing evidence, expired materials, out-of-scope authorization, suspected alteration, or conflicting official sources produce remediation, rejection, or human escalation instead of a forced pass.

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

## Quality Status

The project has source coverage, structured outputs, and replayable examples. Indexed requirements have source entry points, and key paths cover approval, supplement request, rejection, human escalation, expired certificates, territory mismatch, and unverified applicant evidence.

Rule-pack maturity is still `seed`. It is useful for pre-launch checkups, material pre-review, remediation drafting, and internal review support. Final marketplace submission, enforcement decisions, legal conclusions, and high-risk category decisions still require human review and current official confirmation.

## Safety And Scope

This project supports cross-border product launch review, marketplace listing preparation, qualification review, material pre-review, remediation drafting, and internal process design. It does not provide legal advice and does not replace final judgment from marketplaces, regulators, certification bodies, or professional compliance advisors.

When documents contain identity records, bank accounts, personal contact details, contracts, business registration numbers, or other sensitive data, follow [`references/privacy-security.md`](./references/privacy-security.md) for minimization, redaction, and audit records.
