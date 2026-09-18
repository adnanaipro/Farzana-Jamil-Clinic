"""Regression checks for the NexaCare static demonstration site."""

from html.parser import HTMLParser
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
PAGES = (
    "index.html",
    "privacy-notice.html",
    "cookie-policy.html",
    "website-terms.html",
)
NOINDEX = "noindex, nofollow, noarchive, nosnippet"
PROHIBITED_HOMEPAGE_CLAIMS = re.compile(
    r"testimonial"
    r"|(?:[0-5]\.\d)(?:\s*(?:out of|/)\s*5)?"
    r"|\b\d[\d,]*\s+reviews?\b"
    r"|five-star|registered physician|mbbs|fcps|board-certified"
    r"|years? of experience|award|affiliation|clinical outcome"
)


class PageInspector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1_count = 0
        self.main_ids = []
        self.robots_values = []
        self.stylesheets = []
        self.scripts = []
        self.links = []
        self.classes = []
        self.images = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "h1":
            self.h1_count += 1
        if tag == "main":
            self.main_ids.append(attributes.get("id"))
        if tag == "meta" and attributes.get("name") == "robots":
            self.robots_values.append(attributes.get("content"))
        if tag == "link" and attributes.get("rel") == "stylesheet":
            self.stylesheets.append(attributes.get("href"))
        if tag == "script":
            self.scripts.append(attributes.get("src"))
        if tag == "a":
            self.links.append(attributes.get("href"))
        if tag == "img":
            self.images.append(attributes)
        class_names = attributes.get("class", "").split()
        self.classes.extend(class_names)


def inspect_page(filename):
    parser = PageInspector()
    parser.feed((ROOT / filename).read_text(encoding="utf-8"))
    return parser


class SiteChecks(unittest.TestCase):
    def test_representative_raster_images_are_local_sized_disclosed_and_loaded_safely(self):
        """A missing, undisclosed, or incorrectly loaded raster image must block release."""
        expected_images = {
            "assets/images/nexacare-hero.webp": {"loading": None, "fetchpriority": "high"},
            "assets/images/nexacare-doctor.webp": {"loading": "lazy"},
            "assets/images/nexacare-clinic.webp": {"loading": "lazy"},
            "assets/images/nexacare-consultation.webp": {"loading": "lazy"},
        }
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        inspector = inspect_page("index.html")
        image_by_source = {image.get("src"): image for image in inspector.images}

        for source, expected in expected_images.items():
            with self.subTest(source=source):
                self.assertTrue((ROOT / source).is_file(), f"Missing representative image: {source}")
                image = image_by_source.get(source)
                self.assertIsNotNone(image, f"Homepage must reference {source}")
                self.assertTrue(image.get("alt"), f"{source} needs useful alternative text")
                self.assertTrue(image.get("width"), f"{source} needs an explicit width")
                self.assertTrue(image.get("height"), f"{source} needs an explicit height")
                self.assertEqual(image.get("loading"), expected["loading"])
                self.assertEqual(image.get("decoding"), "async")
                if "fetchpriority" in expected:
                    self.assertEqual(image.get("fetchpriority"), expected["fetchpriority"])

        self.assertIn("AI-generated representative image", homepage)

    def test_interaction_contracts_exist(self):
        """Removing progressive enhancement safeguards would break demo controls."""
        js = (ROOT / "assets/js/main.js").read_text(encoding="utf-8")
        for marker in [
            "nexacare_demo_privacy_v1", "showModal", "Escape", "aria-expanded",
            "try", "catch", "openDemoDialog", "closeMenu", "readPreference",
            "writePreference", "removePreference", "prefers-reduced-motion",
        ]:
            with self.subTest(marker=marker):
                self.assertIn(marker, js)

    def test_interaction_markup_supports_safe_progressive_enhancement(self):
        """Removing interaction hooks would leave mobile and privacy controls unusable."""
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        cookie_policy = (ROOT / "cookie-policy.html").read_text(encoding="utf-8")
        for marker in [
            'class="menu-toggle js-menu-toggle"', 'aria-controls="primary-navigation"',
            'id="primary-navigation"', 'class="js-accordion-trigger"',
            'id="privacy-bar"', 'class="mobile-quick-actions"', 'id="current-year"',
        ]:
            with self.subTest(marker=marker):
                self.assertIn(marker, homepage)
        self.assertIn('id="reset-privacy"', cookie_policy)

    def test_dialog_fallback_can_close_when_only_the_open_attribute_exists(self):
        """A non-native dialog must not depend on the unavailable .open property."""
        js = (ROOT / "assets/js/main.js").read_text(encoding="utf-8")
        self.assertIn("function dialogIsOpen()", js)
        self.assertIn('dialog.hasAttribute("open")', js)
        self.assertIn("if (!dialogIsOpen()) return;", js)
        self.assertIn('event.key === "Escape" && dialogIsOpen()', js)

    def test_menu_link_close_restores_focus_before_hiding_the_link(self):
        """Closing the menu from a focused link must not leave focus in hidden content."""
        js = (ROOT / "assets/js/main.js").read_text(encoding="utf-8")
        self.assertIn('if (event.target.closest("a")) closeMenu({ restoreFocus: true });', js)

    def test_closed_dialog_fallback_is_not_rendered_or_focusable(self):
        """An unsupported dialog element must start closed rather than expose its controls."""
        css = (ROOT / "assets/css/style.css").read_text(encoding="utf-8")
        self.assertRegex(css, r"dialog:not\(\[open\]\)\s*\{\s*display:\s*none")


    def test_small_text_on_mineral_surfaces_meets_aa_contrast(self):
        """Teal small text on mist is 4.45:1; affected text must use an AA pair."""
        css = (ROOT / "assets/css/style.css").read_text(encoding="utf-8")
        tokens = dict(re.findall(r"--([a-z-]+):\s*(#[A-Fa-f0-9]{6})", css))

        def color_for(selectors, property_name):
            value = None
            for selector_text, declarations in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
                if any(selector in [s.strip() for s in selector_text.split(",")] for selector in selectors):
                    match = re.search(rf"(?:^|;)\s*{property_name}:\s*var\(--([a-z-]+)\)", declarations)
                    if match:
                        value = tokens[match.group(1)]
            self.assertIsNotNone(value, f"No declared {property_name} for {selectors}")
            return value

        def luminance(color):
            channels = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
            linear = [c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4 for c in channels]
            return sum(c * weight for c, weight in zip(linear, (.2126, .7152, .0722)))

        for text_selectors, surface in [
            ([".eyebrow", "#confidence .eyebrow"], "#confidence"),
            ([".site-footer nav a", ".site-footer nav a:hover"], ".site-footer"),
        ]:
            with self.subTest(surface=surface):
                foreground = color_for(text_selectors, "color")
                background = color_for([surface], "background")
                low, high = sorted([luminance(foreground), luminance(background)])
                self.assertGreaterEqual((high + .05) / (low + .05), 4.5)

    def test_css_contains_locked_tokens_and_accessibility_rules(self):
        """Missing brand/accessibility declarations break the approved CSS contract."""
        stylesheet = ROOT / "assets/css/style.css"
        self.assertTrue(stylesheet.is_file())
        css = stylesheet.read_text(encoding="utf-8")
        for name, value in {
            "ink": "#102A33", "teal": "#0E7C78", "coral": "#E9785D",
            "canvas": "#F6F8F5", "mist": "#EAF3F0", "surface": "#FFFFFF",
            "text": "#17313A", "muted": "#5B6E73", "border": "#D8E3DF",
        }.items():
            with self.subTest(token=name):
                self.assertRegex(css.lower(), rf"--{name}\s*:\s*{value.lower()}")
        for marker in [":focus-visible", "@media (prefers-reduced-motion: reduce)",
                       "@media (min-width: 48rem)", "@media (min-width: 75rem)",
                       "clamp(", "overflow-wrap", "aspect-ratio", "min-height: 44px",
                       "env(safe-area-inset-bottom", "scroll-padding", "--z-privacy",
                       ".button--primary", ".button--secondary", ".privacy-bar",
                       ".mobile-quick-actions"]:
            with self.subTest(rule=marker):
                self.assertIn(marker, css)
        self.assertNotIn("@import", css)
        self.assertNotIn("backdrop-filter", css)

    def test_demo_marquee_terms_link_has_a_44px_touch_target(self):
        """Removing the terms link's 44px target would make the demo disclosure hard to tap."""
        css = (ROOT / "assets/css/style.css").read_text(encoding="utf-8")
        match = re.search(r"\.demo-marquee a\s*\{([^{}]*)\}", css)
        self.assertIsNotNone(match, "The demo marquee terms link must have its own rule")
        self.assertRegex(match.group(1), r"min-height\s*:\s*44px")

    def test_local_svg_artwork_is_valid_and_all_used_symbols_resolve(self):
        """Missing local artwork or misspelled sprite IDs must fail before shipping."""
        svg_paths = ["assets/icons/icon-sprite.svg", "assets/images/map-artwork.svg",
                     "assets/images/pattern-care.svg"]
        for name in svg_paths:
            with self.subTest(asset=name):
                self.assertTrue((ROOT / name).is_file(), f"Missing SVG: {name}")
                root = ET.parse(ROOT / name).getroot()
                self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")
                self.assertNotIn("{http://www.w3.org/2000/svg}script", [el.tag for el in root.iter()])
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        used_symbols = re.findall(r'<use href="assets/icons/icon-sprite.svg#([^"]+)"', homepage)
        self.assertTrue(used_symbols, "Homepage must consume the local icon sprite")
        symbols = {el.get("id") for el in ET.parse(ROOT / svg_paths[0]).iter()}
        self.assertTrue(set(used_symbols).issubset(symbols))
        self.assertIn('src="assets/images/map-artwork.svg"', homepage)

    def test_required_public_pages_exist(self):
        """Removing a public page must fail the static-site contract."""
        self.assertEqual([name for name in PAGES if not (ROOT / name).is_file()], [])

    def test_each_page_has_an_accessible_shell_and_resolving_assets(self):
        """A missing main landmark or shared asset reference must be detected."""
        for page in PAGES:
            with self.subTest(page=page):
                self.assertTrue((ROOT / page).is_file(), f"Missing required page: {page}")
                inspector = inspect_page(page)
                self.assertEqual(inspector.h1_count, 1)
                self.assertIn("main-content", inspector.main_ids)
                self.assertIn("site-header", inspector.classes)
                self.assertIn("site-footer", inspector.classes)
                self.assertIn("demo-marquee", inspector.classes)
                self.assertEqual(inspector.robots_values, [NOINDEX])
                self.assertIn("assets/css/style.css", inspector.stylesheets)
                self.assertIn("assets/js/main.js", inspector.scripts)
                self.assertTrue((ROOT / "assets/css/style.css").is_file())
                self.assertTrue((ROOT / "assets/js/main.js").is_file())

    def test_legal_pages_cross_link_and_return_home(self):
        """A broken legal-policy route must fail navigation checks."""
        legal_pages = PAGES[1:]
        for page in legal_pages:
            with self.subTest(page=page):
                self.assertTrue((ROOT / page).is_file(), f"Missing required page: {page}")
                links = inspect_page(page).links
                self.assertIn("index.html", links)
                for target in legal_pages:
                    self.assertIn(target, links)

    def test_legal_pages_describe_the_actual_demo_data_and_safety_boundaries(self):
        """Legal pages must not overstate a static, non-clinical demonstration."""
        privacy = (ROOT / "privacy-notice.html").read_text(encoding="utf-8").lower()
        cookies = (ROOT / "cookie-policy.html").read_text(encoding="utf-8").lower()
        terms = (ROOT / "website-terms.html").read_text(encoding="utf-8").lower()

        for marker in [
            "no patient information", "no forms", "no analytics", "no advertising pixels",
            "no initial map", "visitor-initiated", "whatsapp", "bukhari ai solutions",
            "representative", "ai-generated",
        ]:
            with self.subTest(privacy_marker=marker):
                self.assertIn(marker, privacy)
        self.assertIn("nexacare_demo_privacy_v1", cookies)
        self.assertIn("only local", cookies)
        self.assertIn("reset", cookies)
        for marker in [
            "not a real clinic", "no medical advice", "not for emergencies",
            "no booking", "care relationship", "no clinician credentials", "verified professional facts",
        ]:
            with self.subTest(terms_marker=marker):
                self.assertIn(marker, terms)
        for marker in [
            "intellectual property", "does not claim ownership", "external whatsapp",
            "responsible for their use", "provided as-is", "availability", "no governing jurisdiction is designated",
            "jurisdiction-appropriate terms", "not responsible for loss",
        ]:
            with self.subTest(terms_safeguard=marker):
                self.assertIn(marker, terms)

    def test_embedded_and_local_svg_favicons_are_present(self):
        """Every public page needs its embedded favicon while favicon.svg remains a valid asset."""
        for page in PAGES:
            with self.subTest(page=page):
                source = (ROOT / page).read_text(encoding="utf-8")
                self.assertRegex(source, r'<link\s+rel="icon"\s+href="data:image/svg\+xml,')
        favicon = ROOT / "favicon.svg"
        self.assertTrue(favicon.is_file(), "Missing local favicon.svg")
        root = ET.parse(favicon).getroot()
        self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")

    def test_static_hosting_configuration_and_deployment_guidance_are_complete(self):
        """Hostinger deployment needs safeguards without rewriting local or WhatsApp paths."""
        htaccess = (ROOT / ".htaccess").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8").lower()
        for marker in [
            "AddDefaultCharset UTF-8", "Options -Indexes", "X-Content-Type-Options",
            "Referrer-Policy", "Content-Security-Policy", "mod_deflate", "mod_expires",
            "(?:tests|docs)",
        ]:
            with self.subTest(htaccess_marker=marker):
                self.assertIn(marker, htaccess)
        self.assertIn(
            'Header always set X-Robots-Tag "noindex, nofollow, noarchive, nosnippet"',
            htaccess,
        )
        self.assertNotIn("immutable", htaccess.lower())
        cache_control = re.search(r'Cache-Control "([^"]+)"', htaccess)
        self.assertIsNotNone(cache_control, "Static assets need an explicit cache policy")
        self.assertIn("must-revalidate", cache_control.group(1))
        max_age = re.search(r"max-age=(\d+)", cache_control.group(1))
        self.assertIsNotNone(max_age, "Static asset cache policy needs max-age")
        self.assertLessEqual(int(max_age.group(1)), 86400)
        for marker in [
            "hostinger", "public_html", "approved", "facts", "images", "contacts",
            "legal review", "whatsapp", "noindex",
        ]:
            with self.subTest(readme_marker=marker):
                self.assertIn(marker, readme)

    def test_homepage_required_sections_and_safe_content(self):
        """Missing demo disclosures or fabricated credibility claims must fail."""
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")

        for section_id in ["care", "doctor", "experience", "visit", "confidence", "location", "faq", "contact"]:
            with self.subTest(section_id=section_id):
                self.assertIn(f'id="{section_id}"', homepage)

        self.assertIn("Representative practitioner profile", homepage)
        for service in [
            "New Patient Consultation",
            "Preventive Health Review",
            "Ongoing Health Support",
            "Follow-Up Consultation",
        ]:
            with self.subTest(service=service):
                self.assertIn(service, homepage)

        self.assertNotRegex(homepage.lower(), PROHIBITED_HOMEPAGE_CLAIMS)
        self.assertIn("03214854145", homepage)

    def test_rating_and_review_claim_pattern_detects_common_fabricated_markers(self):
        """An escaped rating marker must not allow fabricated ratings or review counts."""
        for marker in ("5.0", "4.8/5", "4.8 out of 5", "128 reviews"):
            with self.subTest(marker=marker):
                self.assertRegex(marker, PROHIBITED_HOMEPAGE_CLAIMS)

    def test_prohibited_build_and_runtime_files_are_absent(self):
        """Adding a prohibited framework or server runtime entry point must fail."""
        prohibited = (
            "package.json",
            "vite.config.js",
            "vite.config.ts",
            "tsconfig.json",
            "tailwind.config.js",
            "tailwind.config.ts",
            "server.js",
            "app.js",
            "index.php",
        )
        self.assertEqual([name for name in prohibited if (ROOT / name).exists()], [])


if __name__ == "__main__":
    unittest.main()
