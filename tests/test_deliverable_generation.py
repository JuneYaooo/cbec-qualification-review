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


if __name__ == "__main__":
    unittest.main()
