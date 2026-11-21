from html.parser import HTMLParser
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.resources = []
        self.landmarks = set()
        self.buttons = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if "id" in attributes:
            self.ids.add(attributes["id"])
        if tag in {"main", "header", "nav", "footer"}:
            self.landmarks.add(tag)
        for attribute in ("src", "href"):
            value = attributes.get(attribute, "")
            if value and not value.startswith(("#", "http:", "https:", "mailto:", "tel:")):
                self.resources.append(value.split("?", 1)[0])
        if tag == "button":
            self.buttons.append(attributes)


class BakerySiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.parser = SiteParser()
        cls.parser.feed(cls.html)

    def test_primary_sections_and_landmarks_exist(self):
        self.assertTrue({"main", "header", "nav", "footer"}.issubset(self.parser.landmarks))
        self.assertTrue({"main", "top", "bakes", "our-story", "visit"}.issubset(self.parser.ids))

    def test_local_styles_scripts_and_images_exist(self):
        missing = [path for path in self.parser.resources if not (ROOT / path).is_file()]
        self.assertEqual([], missing, f"Missing local site resources: {missing}")

    def test_mobile_navigation_has_an_accessible_control(self):
        toggles = [button for button in self.parser.buttons if button.get("aria-controls") == "primary-navigation"]
        self.assertEqual(1, len(toggles))
        self.assertEqual("false", toggles[0].get("aria-expanded"))

    def test_page_has_a_skip_link_and_descriptive_title(self):
        self.assertRegex(self.html, r'<a class="skip-link" href="#main">')
        self.assertRegex(self.html, r"<title>Sunny Crumble Bakery .+?</title>")

    def test_workflows_pin_third_party_actions(self):
        workflows = list((ROOT / ".github" / "workflows").glob("*.yml"))
        self.assertEqual(1, len(workflows))
        for workflow in workflows:
            content = workflow.read_text(encoding="utf-8")
            for action_ref in re.findall(r"uses:\s*([^\s]+)", content):
                self.assertRegex(
                    action_ref,
                    r"@(?:[0-9a-f]{40})(?:\s|$)",
                    f"{workflow.name} uses an action without a full commit pin: {action_ref}",
                )
            self.assertRegex(content, r"zricethezav/gitleaks@sha256:[0-9a-f]{64}")
            self.assertIn("git --redact /repo", content)


if __name__ == "__main__":
    unittest.main()
