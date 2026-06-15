# Decision Rules

Use these rules to convert evidence into findings and final decisions.

## Finding Severity

| Severity | Meaning | Default effect |
|---|---|---|
| critical | Prohibited product, forged/invalid core document, no legal right, sanctions/fraud signal, category cannot be sold | Reject or escalate |
| high | Required qualification missing/expired/out of scope, major entity mismatch, unverified core certificate | Request more info, reject if unfixable |
| medium | Fixable missing field, translation gap, incomplete authorization details, stale but replaceable report | Conditional approve or request more info |
| low | Formatting issue, non-blocking operational note, low-risk missing optional material | Approve with note or conditional approve |

## Final Status Logic

- `reject`: any confirmed critical unfixable issue.
- `escalate_human`: suspected fraud, sanctions/export-control issue, legal ambiguity, conflicting official sources, identity document concern, or high-value dispute.
- `request_more_info`: required evidence is missing or cannot be verified.
- `conditional_approve`: only low/medium fixable issues remain and the platform/business process allows conditional progression.
- `approve`: all mandatory requirements are satisfied or not applicable; no high/critical unresolved findings.
- `not_applicable`: request scope is outside the relevant platform/category/market.

## Finding Object

Field names follow the JSON contract in `references/report-templates.md` (the single source of truth). Each finding should include:

- `finding_id`
- `severity`
- `surface`
- `requirement`
- `submitted_evidence`
- `observed_issue`
- `business_impact`
- `decision_effect`
- `required_action`
- `acceptable_evidence`
- `source_ids` (referencing entries in the top-level `sources` list, which carry URL and tier)
- `confidence`

## Blocker Patterns

| Pattern | Severity |
|---|---|
| Document expired before review date | high; critical if no replacement path |
| Applicant name differs from license holder with no authorization | high |
| Brand authorization does not include target territory/platform/category | high |
| Trademark class clearly excludes product category | high |
| Product category is prohibited by platform or market | critical |
| Test report product/model/SKU does not match listing | high |
| Certificate issuer cannot be verified and decision depends on it | high or escalate |
| Applicant submitted altered-looking document | escalate_human |
| Product makes medical/therapeutic claims without proper route | critical or escalate |
| Official sources conflict | escalate_human |

## Score Is Secondary

You may compute a risk score, but the score cannot override a blocker.

Suggested score:

- critical: +50
- high: +25
- medium: +10
- low: +3

Suggested bands:

- 0-9: low risk
- 10-29: medium risk
- 30-49: high risk
- 50+: critical risk

Decision still follows blocker logic.

## Applicant-Facing Tone

Use plain, specific language:

- Say exactly which document failed.
- Say exactly what replacement is acceptable.
- Avoid legal blame language unless necessary.
- Do not expose internal fraud suspicion wording to the applicant; use `requires manual verification` and keep fraud signals in internal notes.

