#!/usr/bin/env python3
"""Dependency-free helpers for cross-border qualification review outputs.

Commands:
  sample
  validate <json-file>
  case-check <case-file> <review-json-file>
  checklist --platform PLATFORM --market MARKET --category CATEGORY
  rulepack-new --country-code CODE --country-name NAME
  rulepack-validate <json-file>
  rulepack-index-validate
  source-freshness [json-file ...]
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import sys
from pathlib import Path
from typing import Any


ALLOWED_DECISIONS = {
    "approve",
    "conditional_approve",
    "request_more_info",
    "reject",
    "escalate_human",
    "not_applicable",
}

ALLOWED_REQUIREMENT_STATUS = {
    "satisfied",
    "partial",
    "missing",
    "invalid",
    "not_applicable",
    "needs_external_verification",
}

ALLOWED_SEVERITY = {"critical", "high", "medium", "low"}
ALLOWED_TIERS = {"T1", "T2", "T3", "T4", "T5"}
ALLOWED_PACK_TYPES = {"global", "country", "region", "platform", "category"}
ALLOWED_PACK_MATURITY = {"seed", "validated", "production", "stale"}
ALLOWED_SURFACES = {
    "seller",
    "brand_ip",
    "product_category",
    "market_import",
    "certificate",
    "platform_listing",
    "service_provider",
}


ALLOWED_RISK_LEVELS = {"low", "medium", "high", "critical"}

DEFINITIVE_STATUSES = {"approve", "conditional_approve", "reject"}
MATURE_PACKS = {"validated", "production"}
AUTHORITATIVE_TIERS = {"T1", "T2"}

REQUIRED_CASE_FIELDS = (
    "applicant_name",
    "platform",
    "destination_market",
    "product_category",
    "review_purpose",
)

SKILL_ROOT = Path(__file__).resolve().parent.parent

# Process-level checklist items that are not qualification requirements.
PROCESS_CHECKLIST = [
    "Sensitive personal or business data is redacted in user-facing output.",
]

# Pack type -> which checklist input its match keywords apply to.
PACK_MATCH_INPUT = {
    "platform": "platform",
    "category": "category",
    "country": "market",
    "region": "market",
}


def today() -> str:
    return _dt.date.today().isoformat()


def parse_date(value: Any) -> _dt.date | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        return _dt.date.fromisoformat(value)
    except ValueError:
        return None


def age_days(value: Any, as_of: _dt.date | None = None) -> int | None:
    checked = parse_date(value)
    if checked is None:
        return None
    return ((as_of or _dt.date.today()) - checked).days


def load_rulepack_index() -> dict[str, Any]:
    path = SKILL_ROOT / "data" / "rulepacks" / "index.json"
    return json.loads(path.read_text(encoding="utf-8"))


def load_rulepack(rel_path: str) -> dict[str, Any]:
    return json.loads((SKILL_ROOT / rel_path).read_text(encoding="utf-8"))


def sample() -> dict[str, Any]:
    return {
        "review_type": "cross_border_ecommerce_qualification",
        "case": {
            "case_id": "case-demo-001",
            "applicant_name": "Example Trading Co., Ltd.",
            "applicant_role": "distributor",
            "platform": "Amazon",
            "marketplace_site": "US",
            "destination_market": "United States",
            "business_model": "marketplace seller",
            "product_category": "food",
            "subcategory": "sauce",
            "brand_name": "Example Brand",
            "review_purpose": "category qualification review",
            "requested_decision_deadline": "",
            "review_date": today(),
        },
        "decision": {
            "status": "request_more_info",
            "risk_level": "high",
            "risk_score": 35,
            "summary": "Cannot decide until brand authorization and current food facility/import documentation are verified.",
            "rationale": ["Required brand and food compliance evidence is incomplete."],
        },
        "documents": [],
        "requirements": [],
        "findings": [],
        "missing_materials": [],
        "evidence": [],
        "sources": [],
        "remediation": {
            "applicant_message": "",
            "internal_next_steps": [],
        },
        "privacy": {
            "redactions_applied": [],
            "sensitive_data_notes": [],
        },
        "audit_log": [
            {
                "timestamp": today(),
                "actor": "AI reviewer",
                "action": "created_sample",
                "details": "Template sample generated.",
            }
        ],
        "disclaimer": "Operational qualification review only; not legal advice.",
    }


def checklist(platform: str, market: str, category: str) -> dict[str, Any]:
    index = load_rulepack_index()
    inputs = {
        "platform": platform.strip().lower(),
        "market": market.strip().lower(),
        "category": category.strip().lower(),
    }

    base_items: list[str] = []
    pack_items: list[str] = []
    matched_packs: list[str] = []
    matched_types: set[str] = set()
    matched_combinations: list[dict[str, Any]] = []

    for entry in index.get("packs", []):
        pack = load_rulepack(entry["path"])
        pack_type = pack.get("type")
        if pack_type == "global":
            base_items = [req["requirement"] for req in pack.get("requirements", [])]
            matched_packs.append(pack["pack_id"])
            continue
        input_key = PACK_MATCH_INPUT.get(pack_type)
        if input_key is None:
            continue
        keywords = (pack.get("match") or {}).get("keywords", [])
        target = inputs[input_key]
        if target and any(keyword.lower() in target for keyword in keywords):
            matched_packs.append(pack["pack_id"])
            matched_types.add(pack_type)
            pack_items.extend(pack.get("checklist_hints", []))
            pack_items.extend(req["requirement"] for req in pack.get("requirements", []))

    for combo in index.get("priority_combinations", []):
        if not isinstance(combo, dict):
            continue
        criteria = combo.get("criteria") if isinstance(combo.get("criteria"), dict) else {}
        platform_hit = _keyword_hit(criteria.get("platform_keywords"), inputs["platform"])
        market_hit = _keyword_hit(criteria.get("market_keywords"), inputs["market"])
        category_hit = _keyword_hit(criteria.get("category_keywords"), inputs["category"])
        if platform_hit and market_hit and category_hit:
            matched_combinations.append(
                {
                    "combo_id": combo.get("combo_id"),
                    "name": combo.get("name"),
                    "maturity": combo.get("maturity", "seed"),
                    "verification_tasks": combo.get("verification_tasks", []),
                    "expected_packs": combo.get("expected_packs", []),
                }
            )

    warnings: list[str] = []
    if "platform" not in matched_types:
        warnings.append(
            f"No platform pack matched '{platform}'. Verify official platform policy manually."
        )
    if "category" not in matched_types:
        warnings.append(
            f"No category pack matched '{category}'. Verify category-specific requirements manually."
        )
    if not matched_types.intersection({"country", "region"}):
        warnings.append(
            f"No country/region pack matched '{market}'. Using global baseline; verify official sources for this market."
        )

    return {
        "platform": platform,
        "market": market,
        "category": category,
        "generated_at": today(),
        "matched_packs": matched_packs,
        "matched_priority_combinations": matched_combinations,
        "warnings": warnings,
        "note": "Routing checklist only. Verify current official platform and regulator sources before final decision.",
        "items": base_items + PROCESS_CHECKLIST + pack_items,
    }


def _keyword_hit(keywords: Any, target: str) -> bool:
    if not isinstance(keywords, list):
        return False
    return any(isinstance(keyword, str) and keyword.lower() in target for keyword in keywords)


def rulepack_template(country_code: str, country_name: str, region: str = "") -> dict[str, Any]:
    code = country_code.strip().upper()
    name = country_name.strip()
    pack_id = f"country-{code}"
    return {
        "schema_version": "1.0",
        "pack_id": pack_id,
        "type": "country",
        "name": f"{name} qualification review pack",
        "jurisdiction": {
            "country_code": code,
            "country_name": name,
            "region": region.strip(),
        },
        "maturity": "seed",
        "version": "0.1.0",
        "updated_at": today(),
        "updated_by": "",
        "change_note": "Initial scaffold. Fill with verified official sources before use for final decisions.",
        "match": {
            "keywords": [code.lower(), name.lower()],
        },
        "freshness_policy": {
            "platform_policy_days": 90,
            "regulator_source_days": 365,
            "customs_tax_days": 180,
            "high_risk_category_days": 30,
        },
        "golden_case_ids": [],
        "regulator_map": [
            {
                "category_family": "food|cosmetics|supplements|electronics|household|toys|medical|other",
                "authority": "",
                "official_url": "",
                "notes": "Add official regulator for this category family.",
            }
        ],
        "requirements": [
            {
                "requirement_id": f"{pack_id}-seller-eligibility",
                "surface": "seller",
                "category_scope": "*",
                "applicant_role_scope": "*",
                "business_model_scope": "*",
                "requirement": f"Confirm seller/entity eligibility for {name} marketplace or import route.",
                "mandatory": "conditional",
                "evidence_expected": [
                    "business registration",
                    "tax/payee evidence where required",
                    "official platform or regulator source",
                ],
                "decision_effect": "Cannot approve until the applicable official route is verified.",
                "source_ids": [],
                "freshness_days": 90,
                "notes": "Replace this scaffold with country-specific official requirements.",
            }
        ],
        "sources": [],
        "gaps": [
            "Add official company registry source if available.",
            "Add official trademark/IP registry source if available.",
            "Add official customs/import authority source.",
            "Add product regulator sources by category family.",
        ],
    }


def check_case(case: dict[str, Any], review: dict[str, Any]) -> list[str]:
    """Check a produced review JSON against a golden case expectation."""
    errors = validate_payload(review)
    expected = case.get("expected") if isinstance(case.get("expected"), dict) else {}

    status = (review.get("decision") or {}).get("status")
    allowed = expected.get("status_any_of") or []
    if allowed and status not in allowed:
        errors.append(f"decision.status is '{status}'; expected one of {allowed}")

    findings = [item for item in review.get("findings") or [] if isinstance(item, dict)]
    for need in expected.get("min_findings") or []:
        severity = need.get("severity") if isinstance(need, dict) else None
        if severity and not any(f.get("severity") == severity for f in findings):
            errors.append(f"expected at least one finding with severity '{severity}'")

    requirements = [item for item in review.get("requirements") or [] if isinstance(item, dict)]
    for required_status in expected.get("require_requirement_status") or []:
        if not any(r.get("status") == required_status for r in requirements):
            errors.append(f"expected at least one requirement with status '{required_status}'")

    return errors


def _require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def validate_payload(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    _require(data.get("review_type") == "cross_border_ecommerce_qualification", "review_type must be cross_border_ecommerce_qualification", errors)
    _require(isinstance(data.get("case"), dict), "case must be an object", errors)
    _require(isinstance(data.get("decision"), dict), "decision must be an object", errors)

    decision = data.get("decision") if isinstance(data.get("decision"), dict) else {}
    status = decision.get("status")
    _require(status in ALLOWED_DECISIONS, f"decision.status must be one of {sorted(ALLOWED_DECISIONS)}", errors)
    _require(decision.get("risk_level") in ALLOWED_RISK_LEVELS, f"decision.risk_level must be one of {sorted(ALLOWED_RISK_LEVELS)}", errors)

    case = data.get("case") if isinstance(data.get("case"), dict) else {}
    if status in DEFINITIVE_STATUSES:
        for field in REQUIRED_CASE_FIELDS:
            _require(bool(case.get(field)), f"case.{field} is required for a definitive '{status}' decision", errors)

    for key in ("documents", "requirements", "findings", "missing_materials", "evidence", "sources", "audit_log"):
        _require(isinstance(data.get(key), list), f"{key} must be a list", errors)

    evidence_ids = {
        str(item.get("evidence_id"))
        for item in data.get("evidence") or []
        if isinstance(item, dict) and item.get("evidence_id")
    }
    declared_source_ids = {
        str(item.get("source_id"))
        for item in data.get("sources") or []
        if isinstance(item, dict) and item.get("source_id")
    }

    for idx, req in enumerate(data.get("requirements") or []):
        if not isinstance(req, dict):
            errors.append(f"requirements[{idx}] must be an object")
            continue
        _require(req.get("status") in ALLOWED_REQUIREMENT_STATUS, f"requirements[{idx}].status is invalid", errors)
        _require(bool(req.get("requirement")), f"requirements[{idx}].requirement is required", errors)
        for eid in req.get("matched_evidence_ids") or []:
            _require(str(eid) in evidence_ids, f"requirements[{idx}] references missing evidence_id {eid}", errors)
        for sid in req.get("source_ids") or []:
            _require(str(sid) in declared_source_ids, f"requirements[{idx}] references missing source_id {sid}", errors)

    finding_severities: set[str] = set()
    for idx, finding in enumerate(data.get("findings") or []):
        if not isinstance(finding, dict):
            errors.append(f"findings[{idx}] must be an object")
            continue
        _require(finding.get("severity") in ALLOWED_SEVERITY, f"findings[{idx}].severity is invalid", errors)
        _require(bool(finding.get("observed_issue")), f"findings[{idx}].observed_issue is required", errors)
        _require(bool(finding.get("required_action")), f"findings[{idx}].required_action is required", errors)
        if finding.get("severity") in ALLOWED_SEVERITY:
            finding_severities.add(finding["severity"])
        for sid in finding.get("source_ids") or []:
            _require(str(sid) in declared_source_ids, f"findings[{idx}] references missing source_id {sid}", errors)

    if status == "approve":
        _require(
            not finding_severities.intersection({"critical", "high"}),
            "approve is not allowed while critical/high findings remain",
            errors,
        )
    if status == "conditional_approve":
        _require(
            "critical" not in finding_severities,
            "conditional_approve is not allowed while critical findings remain",
            errors,
        )

    for idx, evidence in enumerate(data.get("evidence") or []):
        if not isinstance(evidence, dict):
            errors.append(f"evidence[{idx}] must be an object")
            continue
        _require(evidence.get("tier") in ALLOWED_TIERS, f"evidence[{idx}].tier is invalid", errors)
        _require(bool(evidence.get("checked_at")), f"evidence[{idx}].checked_at is required", errors)

    return errors


def validate_rulepack(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    _require(data.get("schema_version") == "1.0", "schema_version must be 1.0", errors)
    _require(bool(data.get("pack_id")), "pack_id is required", errors)
    _require(data.get("type") in ALLOWED_PACK_TYPES, f"type must be one of {sorted(ALLOWED_PACK_TYPES)}", errors)
    _require(data.get("maturity") in ALLOWED_PACK_MATURITY, f"maturity must be one of {sorted(ALLOWED_PACK_MATURITY)}", errors)
    _require(isinstance(data.get("jurisdiction"), dict), "jurisdiction must be an object", errors)
    _require(isinstance(data.get("requirements"), list), "requirements must be a list", errors)
    _require(isinstance(data.get("sources"), list), "sources must be a list", errors)
    if data.get("type") != "global":
        match = data.get("match") if isinstance(data.get("match"), dict) else {}
        _require(isinstance(match.get("keywords"), list) and bool(match.get("keywords")), "non-global packs need match.keywords", errors)

    source_ids = set()
    source_by_id: dict[str, dict[str, Any]] = {}
    for idx, source in enumerate(data.get("sources") or []):
        if not isinstance(source, dict):
            errors.append(f"sources[{idx}] must be an object")
            continue
        sid = source.get("source_id")
        _require(bool(sid), f"sources[{idx}].source_id is required", errors)
        if sid:
            sid_text = str(sid)
            _require(sid_text not in source_ids, f"sources[{idx}].source_id is duplicated: {sid_text}", errors)
            source_ids.add(sid_text)
            source_by_id[sid_text] = source
        _require(bool(source.get("title")), f"sources[{idx}].title is required", errors)
        _require(source.get("tier") in ALLOWED_TIERS, f"sources[{idx}].tier is invalid", errors)
        _require(bool(source.get("checked_at")), f"sources[{idx}].checked_at is required", errors)
        _require(parse_date(source.get("checked_at")) is not None, f"sources[{idx}].checked_at must be YYYY-MM-DD", errors)
        _require(bool(source.get("url")), f"sources[{idx}].url is required", errors)
        if source.get("tier") in AUTHORITATIVE_TIERS:
            _require(bool(source.get("language")), f"sources[{idx}].language is required for T1/T2 sources", errors)
            _require(bool(source.get("confirms")), f"sources[{idx}].confirms is required for T1/T2 sources", errors)

    requirement_ids: set[str] = set()
    mandatory_count = 0
    mandatory_with_authoritative_source = 0
    for idx, req in enumerate(data.get("requirements") or []):
        if not isinstance(req, dict):
            errors.append(f"requirements[{idx}] must be an object")
            continue
        rid = req.get("requirement_id")
        _require(bool(rid), f"requirements[{idx}].requirement_id is required", errors)
        if rid:
            rid_text = str(rid)
            _require(rid_text not in requirement_ids, f"requirements[{idx}].requirement_id is duplicated: {rid_text}", errors)
            requirement_ids.add(rid_text)
        _require(req.get("surface") in ALLOWED_SURFACES, f"requirements[{idx}].surface is invalid", errors)
        _require(bool(req.get("requirement")), f"requirements[{idx}].requirement is required", errors)
        _require("mandatory" in req, f"requirements[{idx}].mandatory is required", errors)
        _require(isinstance(req.get("evidence_expected"), list), f"requirements[{idx}].evidence_expected must be a list", errors)
        _require(bool(req.get("decision_effect")), f"requirements[{idx}].decision_effect is required", errors)
        _require(isinstance(req.get("source_ids"), list), f"requirements[{idx}].source_ids must be a list", errors)
        if "freshness_days" in req:
            _require(isinstance(req.get("freshness_days"), int) and req.get("freshness_days") > 0, f"requirements[{idx}].freshness_days must be a positive integer", errors)
        has_authoritative_source = False
        for sid in req.get("source_ids") or []:
            _require(str(sid) in source_ids, f"requirements[{idx}] references missing source_id {sid}", errors)
            if (source_by_id.get(str(sid)) or {}).get("tier") in AUTHORITATIVE_TIERS:
                has_authoritative_source = True
        if req.get("mandatory") is True:
            mandatory_count += 1
            if has_authoritative_source:
                mandatory_with_authoritative_source += 1

    if data.get("maturity") in MATURE_PACKS:
        for idx, req in enumerate(data.get("requirements") or []):
            if isinstance(req, dict) and req.get("mandatory") is True:
                _require(bool(req.get("source_ids")), f"validated/production mandatory requirements[{idx}] need source_ids", errors)
        cases = data.get("golden_case_ids")
        _require(isinstance(cases, list) and len(cases) >= 3, "validated/production packs need at least 3 golden_case_ids", errors)
        for case_id in cases or []:
            case_path = SKILL_ROOT / "cases" / f"{case_id}.json"
            _require(case_path.exists(), f"golden case not found: cases/{case_id}.json", errors)

    if data.get("maturity") == "production" and mandatory_count:
        ratio = mandatory_with_authoritative_source / mandatory_count
        _require(ratio >= 0.8, "production packs need at least 80% of mandatory requirements backed by T1/T2 sources", errors)

    return errors


def validate_rulepack_index() -> list[str]:
    errors: list[str] = []
    index = load_rulepack_index()
    seen: set[str] = set()
    _require(isinstance(index.get("packs"), list), "index.packs must be a list", errors)
    for idx, entry in enumerate(index.get("packs") or []):
        if not isinstance(entry, dict):
            errors.append(f"packs[{idx}] must be an object")
            continue
        pack_id = entry.get("pack_id")
        path_text = entry.get("path")
        _require(bool(pack_id), f"packs[{idx}].pack_id is required", errors)
        if pack_id:
            _require(str(pack_id) not in seen, f"packs[{idx}].pack_id is duplicated: {pack_id}", errors)
            seen.add(str(pack_id))
        _require(bool(path_text), f"packs[{idx}].path is required", errors)
        pack_path = SKILL_ROOT / str(path_text)
        _require(pack_path.exists(), f"packs[{idx}] path not found: {path_text}", errors)
        if not pack_path.exists():
            continue
        try:
            pack = json.loads(pack_path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"packs[{idx}] failed to read {path_text}: {exc}")
            continue
        if not isinstance(pack, dict):
            errors.append(f"packs[{idx}] file must contain a JSON object: {path_text}")
            continue
        _require(pack.get("pack_id") == pack_id, f"packs[{idx}] pack_id mismatch with {path_text}", errors)
        _require(pack.get("type") == entry.get("type"), f"packs[{idx}] type mismatch with {path_text}", errors)
        _require(pack.get("maturity") == entry.get("maturity"), f"packs[{idx}] maturity mismatch with {path_text}", errors)
        errors.extend(f"{path_text}: {error}" for error in validate_rulepack(pack))
    for idx, combo in enumerate(index.get("priority_combinations") or []):
        if not isinstance(combo, dict):
            errors.append(f"priority_combinations[{idx}] must be an object")
            continue
        _require(bool(combo.get("combo_id")), f"priority_combinations[{idx}].combo_id is required", errors)
        _require(isinstance(combo.get("criteria"), dict), f"priority_combinations[{idx}].criteria must be an object", errors)
        _require(isinstance(combo.get("expected_packs"), list), f"priority_combinations[{idx}].expected_packs must be a list", errors)
        for expected_pack in combo.get("expected_packs") or []:
            _require(str(expected_pack) in seen, f"priority_combinations[{idx}] references missing pack {expected_pack}", errors)
        _require(isinstance(combo.get("verification_tasks"), list) and bool(combo.get("verification_tasks")), f"priority_combinations[{idx}].verification_tasks must be a non-empty list", errors)
    return errors


def source_freshness(paths: list[str] | None = None) -> dict[str, Any]:
    if paths:
        pack_paths = [Path(path) for path in paths]
    else:
        pack_paths = [SKILL_ROOT / entry["path"] for entry in load_rulepack_index().get("packs", [])]

    as_of = _dt.date.today()
    stale: list[dict[str, Any]] = []
    missing: list[dict[str, Any]] = []
    unverified: list[dict[str, Any]] = []
    checked_count = 0
    for pack_path in pack_paths:
        data = json.loads(pack_path.read_text(encoding="utf-8"))
        sources = {
            str(source.get("source_id")): source
            for source in data.get("sources", [])
            if isinstance(source, dict) and source.get("source_id")
        }
        for req in data.get("requirements", []):
            if not isinstance(req, dict):
                continue
            freshness_days = req.get("freshness_days") if isinstance(req.get("freshness_days"), int) else 365
            source_ids = req.get("source_ids") or []
            if not source_ids:
                unverified.append(
                    {
                        "pack": data.get("pack_id"),
                        "maturity": data.get("maturity"),
                        "requirement_id": req.get("requirement_id"),
                        "issue": "requirement has no official source_ids; verify before final decision",
                    }
                )
            if data.get("maturity") in MATURE_PACKS and req.get("mandatory") is True and not source_ids:
                missing.append(
                    {
                        "pack": data.get("pack_id"),
                        "requirement_id": req.get("requirement_id"),
                        "issue": "mandatory mature requirement has no source_ids",
                    }
                )
            for source_id in source_ids:
                source = sources.get(str(source_id))
                if source is None:
                    missing.append(
                        {
                            "pack": data.get("pack_id"),
                            "requirement_id": req.get("requirement_id"),
                            "source_id": source_id,
                            "issue": "referenced source is missing",
                        }
                    )
                    continue
                checked_count += 1
                source_age = age_days(source.get("checked_at"), as_of)
                if source_age is None or source_age > freshness_days:
                    stale.append(
                        {
                            "pack": data.get("pack_id"),
                            "requirement_id": req.get("requirement_id"),
                            "source_id": source_id,
                            "checked_at": source.get("checked_at"),
                            "age_days": source_age,
                            "freshness_days": freshness_days,
                        }
                    )
    return {
        "as_of": as_of.isoformat(),
        "checked_source_links": checked_count,
        "unverified_requirements": unverified,
        "stale": stale,
        "missing": missing,
    }


def cmd_sample(_: argparse.Namespace) -> int:
    print(json.dumps(sample(), ensure_ascii=False, indent=2))
    return 0


def cmd_checklist(args: argparse.Namespace) -> int:
    print(json.dumps(checklist(args.platform, args.market, args.category), ensure_ascii=False, indent=2))
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    path = Path(args.file)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"ERROR: failed to read JSON: {exc}", file=sys.stderr)
        return 2
    if not isinstance(data, dict):
        print("ERROR: top-level JSON must be an object", file=sys.stderr)
        return 2
    errors = validate_payload(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("OK")
    return 0


def _load_json_object(file_path: str, label: str) -> dict[str, Any] | None:
    path = Path(file_path)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"ERROR: failed to read {label} JSON: {exc}", file=sys.stderr)
        return None
    if not isinstance(data, dict):
        print(f"ERROR: top-level {label} JSON must be an object", file=sys.stderr)
        return None
    return data


def cmd_case_check(args: argparse.Namespace) -> int:
    case = _load_json_object(args.case_file, "case")
    review = _load_json_object(args.review_file, "review")
    if case is None or review is None:
        return 2
    errors = check_case(case, review)
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(f"PASS: {case.get('case_id', args.case_file)}")
    return 0


def cmd_rulepack_new(args: argparse.Namespace) -> int:
    print(json.dumps(rulepack_template(args.country_code, args.country_name, args.region or ""), ensure_ascii=False, indent=2))
    return 0


def cmd_rulepack_validate(args: argparse.Namespace) -> int:
    path = Path(args.file)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"ERROR: failed to read JSON: {exc}", file=sys.stderr)
        return 2
    if not isinstance(data, dict):
        print("ERROR: top-level JSON must be an object", file=sys.stderr)
        return 2
    errors = validate_rulepack(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("OK")
    return 0


def cmd_rulepack_index_validate(_: argparse.Namespace) -> int:
    errors = validate_rulepack_index()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("OK")
    return 0


def cmd_source_freshness(args: argparse.Namespace) -> int:
    try:
        report = source_freshness(args.files)
    except Exception as exc:
        print(f"ERROR: failed to scan sources: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if report["stale"] or report["missing"] else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Qualification audit schema helper")
    sub = parser.add_subparsers(dest="command", required=True)

    p_sample = sub.add_parser("sample", help="print sample review JSON")
    p_sample.set_defaults(func=cmd_sample)

    p_checklist = sub.add_parser("checklist", help="print routing checklist")
    p_checklist.add_argument("--platform", required=True)
    p_checklist.add_argument("--market", required=True)
    p_checklist.add_argument("--category", required=True)
    p_checklist.set_defaults(func=cmd_checklist)

    p_validate = sub.add_parser("validate", help="validate a review JSON file")
    p_validate.add_argument("file")
    p_validate.set_defaults(func=cmd_validate)

    p_case_check = sub.add_parser("case-check", help="check a review JSON against a golden case expectation")
    p_case_check.add_argument("case_file")
    p_case_check.add_argument("review_file")
    p_case_check.set_defaults(func=cmd_case_check)

    p_rulepack_new = sub.add_parser("rulepack-new", help="print a country rule pack scaffold")
    p_rulepack_new.add_argument("--country-code", required=True)
    p_rulepack_new.add_argument("--country-name", required=True)
    p_rulepack_new.add_argument("--region", default="")
    p_rulepack_new.set_defaults(func=cmd_rulepack_new)

    p_rulepack_validate = sub.add_parser("rulepack-validate", help="validate a rule pack JSON file")
    p_rulepack_validate.add_argument("file")
    p_rulepack_validate.set_defaults(func=cmd_rulepack_validate)

    p_rulepack_index_validate = sub.add_parser("rulepack-index-validate", help="validate rulepack index and all indexed packs")
    p_rulepack_index_validate.set_defaults(func=cmd_rulepack_index_validate)

    p_source_freshness = sub.add_parser("source-freshness", help="report stale or missing rule source links")
    p_source_freshness.add_argument("files", nargs="*")
    p_source_freshness.set_defaults(func=cmd_source_freshness)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
