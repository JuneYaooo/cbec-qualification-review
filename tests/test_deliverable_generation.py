import json
import tempfile
import unittest
from pathlib import Path

from scripts.qualification_audit_schema import (
    launch_report_from_bundle,
    render_detailed_pdf_html,
    render_overview_card_html,
)


FIXTURE = Path("examples/offline-launch-case.json")
REAL_RUN_FIXTURE = Path("examples/real-runs/mantova-olive-oil-china-import/input-bundle.json")


class DeliverableGenerationTests(unittest.TestCase):
    def report(self):
        return launch_report_from_bundle(json.loads(FIXTURE.read_text(encoding="utf-8")))

    def test_overview_card_html_contains_core_decision_sections(self):
        html = render_overview_card_html(self.report())

        self.assertIn("Core Overview Card", html)
        self.assertIn("Origin", html)
        self.assertIn("Destinations", html)
        self.assertIn("Top blockers", html)
        self.assertIn("Must-check channels", html)
        self.assertIn("Next actions", html)

    def test_detailed_pdf_html_contains_auditable_sections(self):
        html = render_detailed_pdf_html(self.report())

        self.assertIn("Detailed LaunchFit Review", html)
        self.assertIn("Per-destination market reviews", html)
        self.assertIn("Source candidates", html)
        self.assertIn("Research tasks", html)
        self.assertIn("Evidence and source status", html)
        self.assertIn("Audit log", html)

    def test_cli_writes_overview_and_detailed_html(self):
        with tempfile.TemporaryDirectory() as tmp:
            review_path = Path(tmp) / "report.json"
            card_path = Path(tmp) / "card.html"
            detail_path = Path(tmp) / "detail.html"
            review_path.write_text(json.dumps(self.report()), encoding="utf-8")

            from scripts.qualification_audit_schema import main

            self.assertEqual(0, main(["launch-report-card", str(review_path), str(card_path)]))
            self.assertEqual(0, main(["launch-report-detail", str(review_path), str(detail_path)]))

            self.assertIn("Core Overview Card", card_path.read_text(encoding="utf-8"))
            self.assertIn("Detailed LaunchFit Review", detail_path.read_text(encoding="utf-8"))

    def test_overview_card_uses_compact_chinese_sections(self):
        html = render_overview_card_html(self.report())

        self.assertIn("出海体检核心卡", html)
        self.assertIn("关键阻断", html)
        self.assertIn("必须核验", html)
        self.assertIn("下一步", html)
        self.assertIn("证据状态", html)
        self.assertIn("section blocker", html)
        self.assertIn("section verify", html)
        self.assertIn("section action", html)

    def test_detailed_pdf_html_is_structured_brief_not_long_letter(self):
        html = render_detailed_pdf_html(self.report())

        self.assertIn("LaunchFit 结构化审核简报", html)
        self.assertIn("一页摘要", html)
        self.assertIn("关键阻断", html)
        self.assertIn("补件清单", html)
        self.assertIn("证据等级", html)
        self.assertNotIn("<h2>Remediation wording</h2>", html)

    def test_real_run_card_is_compact_for_readme_preview(self):
        report = launch_report_from_bundle(json.loads(REAL_RUN_FIXTURE.read_text(encoding="utf-8")))
        html = render_overview_card_html(report)

        self.assertNotIn("min-height: 1600px", html)
        self.assertNotIn("min-height: 1496px", html)
        self.assertNotIn("Chinese label artwork", html)
        self.assertNotIn("Unsupported claims", html)
        self.assertIn("width: 1200px", html)

    def test_real_run_detailed_report_hides_raw_machine_fallbacks(self):
        report = launch_report_from_bundle(json.loads(REAL_RUN_FIXTURE.read_text(encoding="utf-8")))
        html = render_detailed_pdf_html(report)

        self.assertNotIn("Requirement is not yet matched to submitted applicant/product evidence.", html)
        self.assertNotIn("Holder &#x27;", html)
        self.assertNotIn("Confirm the document covers", html)
        self.assertNotIn("Competitor rows are offline", html)
        self.assertNotIn("Marketplace restricted product policy", html)
        self.assertIn("文件持有人与待确认进口商/经销商不一致", html)


if __name__ == "__main__":
    unittest.main()
