---
name: cbec-qualification-review
description: Use this skill when the user needs cross-border e-commerce qualification review, seller onboarding review, merchant KYB/KYC document review, product/category admission checks, brand authorization review, certificate/license/document validation, platform qualification checklists, remediation letters, or auditable approve/reject/escalate decisions for platforms such as Amazon, TikTok Shop, Shopee, Temu, Lazada, AliExpress, Walmart Marketplace, eBay, Tmall Global, JD Worldwide, or similar marketplaces.
metadata:
  short-description: Cross-border e-commerce qualification review
---

# Cross-Border E-commerce Qualification Review

Use this skill to turn messy merchant, brand, product, and certificate materials into an auditable qualification decision. The output must be operational: approve, conditionally approve, request more information, reject, or escalate to human review.

This skill is not a generic compliance Q&A skill. It reviews a concrete application package or designs the review rules for such packages.

## Core Modes

| Mode | Use when | Output |
|---|---|---|
| Case intake | User provides a seller/product/category/application scenario | Scope, missing inputs, first checklist |
| Document review | User provides licenses, certificates, reports, labels, authorization letters, screenshots, PDFs, or images | Extracted fields, inconsistencies, red flags, evidence table |
| Platform/category review | User names a marketplace, market, or product category | Current-rule verification plan and required qualification checklist |
| Decision memo | User asks whether an application can pass | Decision, reasons, evidence, source URLs, remediation |
| Remediation | User asks how to fix failed materials | Supplement request, revised document list, applicant-facing wording |
| Rulebook design | User is building an internal审核/准入 process | Rule matrix, data model, severity taxonomy, audit trail |

## Always Establish Scope

Before issuing a final decision, identify:

- Applicant type: manufacturer, brand owner, distributor, importer, marketplace seller, agent, service provider.
- Business model: export, import, cross-border bonded, direct mail, marketplace FBA/FBT/FBM, domestic-to-overseas, overseas-to-China.
- Platform and market: marketplace name, destination country/region, store site, warehouse model.
- Product scope: category, subcategory, HS/code if relevant, regulated attributes, claims, ingredients/materials.
- Brand/IP scope: brand owner, trademark region/class, authorization chain, license territory, validity period.
- Documents submitted: file name, document type, issuer, holder, number, issue date, expiry date, scope, language.
- Requested outcome: platform onboarding, category gating, product listing approval, customs/import readiness, service-provider qualification.

If any blocker is missing, ask only the minimum necessary question. Otherwise proceed with assumptions and flag them.

## Workflow

1. **Triage the case**
   - Load `references/audit-workflow.md`.
   - Classify the case as seller/KYB, brand/IP, product/category, market/import, platform listing, or service-provider review.
   - Assign initial risk: low, medium, high, critical.

2. **Build the document inventory**
   - Load `references/document-taxonomy.md` when reviewing documents or creating required-material lists.
   - Extract fields at document level, not just summary level.
   - Check consistency across applicant name, registered address, brand owner, product name, category, territory, validity dates, and issuer.

3. **Map platform, country, and category rules**
   - Load `references/platform-market-matrix.md` when a platform, marketplace site, or target country is involved.
   - Load `references/global-country-framework.md` for country/region routing, especially when no country-specific rule pack exists.
   - Check `data/rulepacks/index.json` for available rule packs and combine them per its `composition_order` (global -> platform -> region -> country -> category). If no country pack exists, use `data/rulepacks/global-baseline.json` and verify official sources in real time.
   - Do not rely on memory for current platform rules. Verify current requirements from official platform/regulator sources before definitive conclusions.

4. **Apply decision rules**
   - Load `references/decision-rules.md`.
   - Convert every issue into a finding with severity, rule basis, evidence, impact, and required action.
   - A single critical blocker can force reject or human escalation even if the score is otherwise high.

5. **Verify evidence and currency**
   - Load `references/verification-playbook.md` whenever making claims about laws, platform rules, registries, or certificate validity.
   - Cite source URL, source tier, checked date, and whether the source directly confirms the point.
   - If the source is stale, indirect, applicant-provided only, or social content, downgrade confidence.

6. **Protect sensitive data**
   - Load `references/privacy-security.md` whenever documents include personal data, license numbers, identity documents, contracts, bank info, or contact info.
   - Redact unnecessary sensitive values in user-facing output.

7. **Output the result**
   - Load `references/report-templates.md`.
   - Provide a concise executive decision first, then detailed findings, evidence table, missing materials, remediation, and audit log.

## Decision Statuses

Use exactly one final status:

- `approve`: No material blocker. Remaining issues are low-risk operational notes.
- `conditional_approve`: Can proceed only after clearly bounded low/medium fixes.
- `request_more_info`: Cannot decide because material evidence is missing.
- `reject`: Critical non-compliance, invalid authorization, prohibited product, forged/expired material, or unfixable mismatch.
- `escalate_human`: Legal ambiguity, suspected fraud, sanctions/export-control concern, high-value dispute, privacy-sensitive identity issue, or conflicting authoritative sources.
- `not_applicable`: The requested review type does not apply to the given platform/category/market.

## Evidence Rules

Field names follow the JSON contract in `references/report-templates.md`. Every important conclusion must include:

- `evidence_id`
- `kind` (submitted_document, official_source, registry, issuer_lookup, platform_policy, regulator, other)
- `reference` (document or source)
- `tier`
- `checked_at`
- `extracted_fact`
- `confidence`

Link conclusions back to rules: requirements reference evidence via `matched_evidence_ids`, and findings reference sources via `source_ids`.

Never invent license numbers, registration numbers, certificates, platform rules, official names, expiration dates, or issuer names. If no source confirms a requirement, write `not verified` and explain what to verify.

## Source Tiers

| Tier | Source |
|---|---|
| T1 | Official marketplace policy, official regulator, government registry, court/customs/regulatory database |
| T2 | Official accreditation body, certification body registry, standards body, official lab accreditation lookup |
| T3 | Major law firm, customs broker, compliance consultant, trade association |
| T4 | Applicant-provided documents, supplier statements, screenshots, emails, contracts |
| T5 | Social posts, forum comments, informal videos, unverifiable claims |

T4 evidence can prove what the applicant submitted, but not necessarily that the fact is true. Verify externally when the decision depends on it.

## Hard Rules

- Do not provide a pass decision when required documents are missing, expired, mismatched, outside scope, or only asserted by the applicant.
- Do not treat a document image as genuine just because it looks professional.
- Do not treat marketplace rules as stable; require source checking for current decisions.
- Do not expose full personal identity numbers, bank accounts, private addresses, phone numbers, or emails unless the user explicitly needs a machine-readable internal record.
- Do not call social media or seller anecdotes authoritative for qualification review.
- Do not give legal advice as final authority. Phrase legal conclusions as operational review findings requiring official/professional confirmation where appropriate.

## Script Helper

Use `scripts/qualification_audit_schema.py` to create or validate structured review JSON:

```bash
python3 scripts/qualification_audit_schema.py sample
python3 scripts/qualification_audit_schema.py checklist --platform amazon --market US --category food
python3 scripts/qualification_audit_schema.py validate path/to/review.json
python3 scripts/qualification_audit_schema.py case-check cases/golden-expired-certificate.json path/to/review.json
python3 scripts/qualification_audit_schema.py rulepack-new --country-code DE --country-name Germany
python3 scripts/qualification_audit_schema.py rulepack-validate data/rulepacks/global-baseline.json
```

The script is intentionally dependency-free so it can run in constrained environments. `checklist` builds its output from the rule packs in `data/rulepacks/` and warns when no platform/category/market pack matched. Golden cases in `cases/` define expected decisions for representative scenarios; use `case-check` to verify a produced review against them.

## Reference Map

| File | Load when |
|---|---|
| `references/audit-workflow.md` | Any real review or rulebook design |
| `references/document-taxonomy.md` | Documents, materials, certificates, labels, authorization chains |
| `references/platform-market-matrix.md` | Platform, country, category, or marketplace-specific scope |
| `references/global-country-framework.md` | Any country/region not yet covered by a mature rule pack |
| `references/rulepack-governance.md` | Adding, reviewing, versioning, and maintaining country/platform rule packs |
| `references/decision-rules.md` | Findings, severity, scoring, final decisions |
| `references/verification-playbook.md` | Source checking, freshness, certificate verification, search templates |
| `references/privacy-security.md` | PII, KYB/KYC, contracts, confidential documents |
| `references/report-templates.md` | JSON, Markdown memo, supplement request, internal audit record |
| `references/implementation-blueprint.md` | Productizing this skill in an app/backend |
