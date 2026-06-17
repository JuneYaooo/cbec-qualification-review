# LaunchFit Skill Complete Lite Design

## Goal

Turn LaunchFit AI into a complete, lightweight Codex Skill package centered on target-market benchmarking: easy for an agent to trigger, deterministic where possible, runnable from CLI, verified by golden cases, and honest about offline versus externally verified facts.

This is not a web app and not a SaaS backend. The project should remain a Skill: `SKILL.md` plus references, rule packs, examples, and scripts that an agent can call reliably.

The core value is not merely "compliance checking." The Skill should first help the user understand how comparable products win in the destination market, then use qualification, packaging, logistics, and source verification to judge whether the user's product can credibly follow, avoid, or improve on those patterns.

## Product Boundary

The complete-lite version includes:

- Skill instructions that tell agents when to use the workflow and which command to run.
- A maintainable CLI execution layer for deterministic work.
- A formal offline case-bundle schema and validator.
- A benchmark-first workflow that turns competitor screenshots, links, tables, or manually collected rows into market signals.
- Report generation for JSON and Markdown.
- Batch execution for multiple case bundles.
- Golden cases that prove common seller and reviewer workflows.
- Rule-pack coverage and maturity reporting.
- Lightweight adapter contracts for OCR, live web/source checks, registry checks, and logistics quotes as enhancement inputs.

The complete-lite version does not include:

- Browser UI or dashboard.
- Database persistence.
- User account, auth, billing, or hosted API service.
- Mandatory OCR, scraping, registry, or freight integrations.
- Claims that user-provided screenshots, documents, or quotes are externally verified.

OCR, scraping, registry checks, and freight quote APIs are important enhancement layers. They should be easy to plug in, but the Skill must remain useful when the user only provides screenshots, product links, tables, copied label text, or manually extracted certificate fields.

## Benchmark-First Workflow

Target-market benchmarking is the main workflow, not a side table.

The Skill should support these benchmark source types:

- Direct competitors: same product and same buyer intent.
- Substitute products: different form or formula solving the same need.
- Adjacent reference products: products that teach price, packaging, channel, or claims expectations.
- Category leaders: high-share or high-review-count products.
- Local niche brands: smaller local products that reveal localization patterns.
- Platform best sellers: marketplace products that show search and listing conventions.
- Offline retail shelf products: mass retail, club store, specialty, pharmacy, or grocery examples.
- DTC and social commerce products: brands that show storytelling, bundling, and creator-driven positioning.

Each benchmark row should capture:

- product name, brand, channel, channel role, market, source basis, and checked date
- pack size, price, unit price, bundle/variant strategy, and positioning
- product type, formula/material/flavor, origin story, and core buyer promise
- packaging structure, visual hierarchy, language, warnings, responsible party, and local label cues
- visible claims, proof points, certification signals, badges, and platform trust markers
- review rating/count when available, repeated praise, repeated objections, and purchase triggers
- logistics or fulfillment signals such as FBA, local warehouse, cold chain, fragile/glass, battery, liquid, or oversize
- copy/avoid/improve takeaway for the user's product

Benchmark output should summarize:

- reference price band and unit economics
- channel map and which channel sets buyer expectations
- packaging conventions and local visual language
- claims/proof map and which claims require substantiation
- trust-signal map
- review signal map
- launch positioning recommendation
- copy / avoid / improve actions
- verification checklist before ordering, printing, listing, or shipping

Do not invent benchmark products, prices, reviews, or source details. If no external source was checked, mark rows as `user_provided`, `assumption`, or `not_checked`. If external search or user-provided URLs were checked, mark rows as `current_checked` with source IDs.

## Architecture

Keep the Skill small, but stop growing one giant script.

Create a small Python package under `launchfit/`:

- `launchfit/cli.py`: argument parsing and command dispatch.
- `launchfit/schema.py`: review JSON, case bundle, rule pack, and golden case validation.
- `launchfit/rulepacks.py`: rulepack loading, matching, index validation, source freshness.
- `launchfit/reporting.py`: launch report generation and Markdown rendering.
- `launchfit/benchmarking.py`: benchmark row validation, normalization, scoring, summaries, and benchmark-first report sections.
- `launchfit/checks.py`: deterministic document, packaging, benchmark, logistics, and decision checks.
- `launchfit/golden.py`: golden replay and case-check logic.
- `launchfit/adapters.py`: offline/noop adapter protocol for future OCR, web, registry, and logistics connectors.

Keep `scripts/qualification_audit_schema.py` as a compatibility wrapper that imports `launchfit.cli.main`. This preserves all current commands.

## CLI Scope

Required commands:

- `sample`
- `checklist`
- `review-skeleton`
- `benchmark-template`
- `launch-report`
- `launch-report-markdown`
- `validate`
- `case-check`
- `golden-replay`
- `quality-gate`
- `rulepack-new`
- `rulepack-validate`
- `rulepack-index-validate`
- `source-freshness`

New lightweight commands:

- `bundle-template`: create a blank or prefilled case bundle.
- `bundle-validate`: validate case bundle shape before report generation.
- `benchmark-template`: keep existing worksheet generation and expand it to support benchmark source type and review signal fields.
- `benchmark-validate`: validate benchmark rows independently before adding them to a launch bundle.
- `benchmark-summarize`: summarize a benchmark worksheet into price band, channel map, packaging conventions, claims/proof, review themes, and copy/avoid/improve.
- `batch-launch-report`: generate reports for every case bundle in a directory.
- `coverage-report`: summarize rulepack maturity, source coverage, golden case coverage, and high-frequency route readiness.

## Adapter Boundary

Adapters are protocols and offline records in this iteration. They are enhancement inputs, not hard dependencies.

The package should define adapter result shapes for:

- OCR extraction result.
- Source/web check result.
- Registry/certificate check result.
- Logistics quote result.

Default behavior is `offline`: return no external confirmation and mark findings as `needs_external_verification`. This keeps the Skill honest while making future MCP/API integrations straightforward. When adapters are present, their outputs should feed the same benchmark, evidence, source, and logistics structures instead of creating a separate product path.

## Case Bundle Schema

Formalize the offline bundle introduced in the MVP:

- `bundle_type`
- `case`
- `documents`
- `packaging`
- `benchmarks`
- `competitors` as a backward-compatible alias for `benchmarks`
- `logistics`
- `sources`
- `external_checks`

Validation must catch:

- Missing platform, market, category, product, or review purpose.
- Invalid benchmark basis, channel role, positioning, source tier, confidence, or risk level.
- Expiry dates that are not ISO dates.
- Documents without type or file reference.
- Competitor rows without product and channel.
- Logistics rows without route and basis.

Validation should warn, not fail, when optional sections are empty.

## Golden Cases

Expand coverage without becoming heavy. Add focused fixtures for:

- Complete low-risk offline launch bundle.
- Missing core scope fields.
- Expired certificate plus brand authorization territory mismatch.
- Suspected forged document.
- Packaging claim risk.
- Logistics risk for battery/electronics.
- No competitor benchmark rows.
- Broad benchmark worksheet with direct competitors, substitute products, adjacent references, local niche brands, offline retail examples, and DTC/social products.
- Benchmark worksheet with user-provided prices only, requiring current verification.
- Batch directory with mixed pass/fail cases.

Golden replay must stay dependency-free and fast.

## Documentation

Update:

- `README.md` and `README.en.md`: position this as a benchmark-first complete lightweight Skill, not a full automation product.
- `SKILL.md`: include a command routing table for agents and require benchmark-first handling for seller-facing launch questions.
- `examples/README.md`: add bundle-template, bundle-validate, batch, and coverage-report examples.
- `references/launch-readiness-playbook.md`: strengthen benchmark coverage and the copy/avoid/improve workflow.
- `references/implementation-blueprint.md`: clarify that UI/database/live APIs are optional productization layers, while OCR/search/registry/logistics APIs are enhancement inputs.

## Testing And Quality Gate

`quality-gate` must include:

- rulepack index validation
- source freshness
- golden replay
- example report fixture validation
- benchmark worksheet validation
- bundle fixture validation
- coverage report generation

All checks must run with Python standard library only.

## Success Criteria

The project is complete-lite when a user or agent can:

1. Generate a case bundle template.
2. Validate the bundle.
3. Generate, validate, and summarize a benchmark worksheet.
4. Generate JSON and Markdown reports with benchmark-first sections.
5. Run one bundle or a directory of bundles.
6. See clear warnings for offline/unverified facts.
7. Run `quality-gate` and see all Skill, benchmark, rulepack, source, and golden checks pass.
8. Understand from README/SKILL.md exactly what is included and what improves when external OCR/search/registry/logistics adapters are available.

## Self-Review

- Scope stays Skill-first and CLI-lightweight.
- Benchmarking is the core workflow, not an optional appendix.
- No UI, database, auth, or hosted service is included.
- External integrations are enhancement inputs with adapter boundaries, not required services.
- Existing CLI commands remain backward compatible.
- The giant script is split for maintainability before adding more behavior.
