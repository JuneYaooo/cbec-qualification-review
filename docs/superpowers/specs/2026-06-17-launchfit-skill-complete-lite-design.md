# LaunchFit Skill Complete Lite Design

## Goal

Turn LaunchFit AI into a complete, lightweight Codex Skill package: easy for an agent to trigger, deterministic where possible, runnable from CLI, verified by golden cases, and honest about offline versus externally verified facts.

This is not a web app and not a SaaS backend. The project should remain a Skill: `SKILL.md` plus references, rule packs, examples, and scripts that an agent can call reliably.

## Product Boundary

The complete-lite version includes:

- Skill instructions that tell agents when to use the workflow and which command to run.
- A maintainable CLI execution layer for deterministic work.
- A formal offline case-bundle schema and validator.
- Report generation for JSON and Markdown.
- Batch execution for multiple case bundles.
- Golden cases that prove common seller and reviewer workflows.
- Rule-pack coverage and maturity reporting.
- Lightweight adapter contracts for OCR, live web/source checks, registry checks, and logistics quotes.

The complete-lite version does not include:

- Browser UI or dashboard.
- Database persistence.
- User account, auth, billing, or hosted API service.
- Mandatory OCR, scraping, registry, or freight integrations.
- Claims that user-provided screenshots, documents, or quotes are externally verified.

## Architecture

Keep the Skill small, but stop growing one giant script.

Create a small Python package under `launchfit/`:

- `launchfit/cli.py`: argument parsing and command dispatch.
- `launchfit/schema.py`: review JSON, case bundle, rule pack, and golden case validation.
- `launchfit/rulepacks.py`: rulepack loading, matching, index validation, source freshness.
- `launchfit/reporting.py`: launch report generation and Markdown rendering.
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
- `batch-launch-report`: generate reports for every case bundle in a directory.
- `coverage-report`: summarize rulepack maturity, source coverage, golden case coverage, and high-frequency route readiness.

## Adapter Boundary

Adapters are protocols and offline records, not integrations in this iteration.

The package should define adapter result shapes for:

- OCR extraction result.
- Source/web check result.
- Registry/certificate check result.
- Logistics quote result.

Default behavior is `offline`: return no external confirmation and mark findings as `needs_external_verification`. This keeps the Skill honest while making future MCP/API integrations straightforward.

## Case Bundle Schema

Formalize the offline bundle introduced in the MVP:

- `bundle_type`
- `case`
- `documents`
- `packaging`
- `competitors`
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
- Batch directory with mixed pass/fail cases.

Golden replay must stay dependency-free and fast.

## Documentation

Update:

- `README.md` and `README.en.md`: position this as a complete lightweight Skill, not a full automation product.
- `SKILL.md`: include a command routing table for agents.
- `examples/README.md`: add bundle-template, bundle-validate, batch, and coverage-report examples.
- `references/implementation-blueprint.md`: clarify that UI/database/live APIs are optional productization layers.

## Testing And Quality Gate

`quality-gate` must include:

- rulepack index validation
- source freshness
- golden replay
- example report fixture validation
- bundle fixture validation
- coverage report generation

All checks must run with Python standard library only.

## Success Criteria

The project is complete-lite when a user or agent can:

1. Generate a case bundle template.
2. Validate the bundle.
3. Generate JSON and Markdown reports.
4. Run one bundle or a directory of bundles.
5. See clear warnings for offline/unverified facts.
6. Run `quality-gate` and see all Skill, rulepack, source, and golden checks pass.
7. Understand from README/SKILL.md exactly what is included and what requires future external integration.

## Self-Review

- Scope stays Skill-first and CLI-lightweight.
- No UI, database, auth, or hosted service is included.
- External integrations are adapter boundaries only.
- Existing CLI commands remain backward compatible.
- The giant script is split for maintainability before adding more behavior.
