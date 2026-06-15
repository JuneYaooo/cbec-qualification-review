# Verification Playbook

Use this reference when verifying rules, registries, certificates, and evidence freshness.

## Verification Principles

- Current official source beats memory.
- Applicant-provided documents are evidence of submission, not proof of external truth.
- Screenshots need URL, date, and context; otherwise treat as weak evidence.
- If a source is paywalled, gated, or unavailable, mark the requirement `needs_external_verification`.
- Record checked date for every source used in a decision.

## Source Priority

1. Official platform policy page for the exact marketplace/site/category.
2. Official regulator or government registry.
3. Official certification/accreditation body registry.
4. Official standards body or recognized accreditation database.
5. Reputable compliance firm/trade association for interpretation only.
6. Applicant documents.
7. Social/forum content for context only.

## Search Templates

Use these patterns, replacing brackets:

- `[platform] seller requirements [market] [category] official`
- `[platform] restricted products [category] official policy`
- `[platform] category approval requirements [category] [market]`
- `[market regulator] [product category] import registration requirements`
- `[certificate type] verify certificate [issuer]`
- `[lab name] accreditation scope [standard]`
- `[trademark registry] [brand] [class] [country]`
- `[company registry] [legal name] [registration number]`

For Chinese sources:

- `[平台] [类目] 资质 要求 官方`
- `[国家/地区] [品类] 进口 注册 标签 要求 官方`
- `[证书类型] [签发机构] 证书 查询`
- `[品牌] 商标 注册 类别 查询`

## Certificate Verification Checklist

| Certificate/report | Verify |
|---|---|
| Business license | Registry status, legal name, registration number, business scope |
| Trademark | Owner, class, territory, status, expiry |
| Brand authorization | Grantor authority, grantee, territory, platform/channel, product scope, date, signature/seal |
| Test report | Lab identity, accreditation, standard, sample/product match, report date, result |
| ISO/HACCP/GMP | Certification body, accreditation, site/scope, expiry |
| Halal/Organic/Kosher | Certifier recognition, product/site scope, validity |
| FDA/regulatory registration | Official lookup when available, facility/product/category match, renewal period |
| CE/FCC/KC/UKCA style conformity | Responsible party, standard, test lab, DoC, technical file route where relevant |

## Freshness Guidance

Rule-source freshness windows are defined per rulepack `freshness_policy`; canonical defaults live in `references/rulepack-governance.md`. The table below covers evidence staleness:

| Evidence type | Treat as stale when |
|---|---|
| Platform policy | Older than 90 days without recheck |
| Regulatory requirement | Older than 365 days without recheck, or sooner if known transition period or high-risk category |
| Test report | Product/category dependent; commonly stale after 12-36 months unless platform states otherwise |
| Certificate | Expired or status cannot be confirmed |
| Authorization letter | Expired, unsigned, territory/platform mismatch, or grantor authority unclear |
| Screenshot | Missing capture date/source URL or older than platform's relevant review window |

## Verification Output

For each checked source:

- `source_id`
- `title`
- `url`
- `tier`
- `checked_at`
- `confirms`
- `does_not_confirm`
- `notes`

When you cannot verify, say what exact registry, issuer, platform help center, or professional channel should be checked next.

