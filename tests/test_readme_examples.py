from pathlib import Path
import unittest


class ReadmeExampleTests(unittest.TestCase):
    def test_chinese_readme_does_not_expose_local_server_paths(self):
        readme = Path("README.md").read_text(encoding="utf-8")

        self.assertNotIn("/Users/", readme)
        self.assertNotIn("food_hack/test_data", readme)

    def test_chinese_readme_shows_only_one_real_run_card(self):
        readme = Path("README.md").read_text(encoding="utf-8")

        self.assertIn("core-card.png", readme)
        self.assertNotIn("detailed-report-long.png", readme)
        self.assertNotIn("front-label.png", readme)
        self.assertNotIn("side-label-origin.png", readme)
        self.assertNotIn("back-label-nutrition.png", readme)


if __name__ == "__main__":
    unittest.main()
