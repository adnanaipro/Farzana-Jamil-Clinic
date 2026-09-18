# NexaCare Medical Demo Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and publish a visually premium, specialty-neutral Essential Plan demonstration website for NexaCare Medical that Bukhari AI Solutions can use when pitching private doctors.

**Architecture:** A dependency-free static site uses semantic HTML, one shared stylesheet, and one progressively enhanced JavaScript file. Four HTML pages share the same local visual system; Python standard-library checks enforce structure, safety, path validity, and demo disclosures, while browser and Lighthouse checks validate rendered quality.

**Tech Stack:** HTML5, CSS3, vanilla JavaScript, local SVG/WebP assets, Python 3 standard-library tests, Apache `.htaccess`, static hosting.

**Spec:** `docs/superpowers/specs/2026-09-16-nexacare-medical-demo-design.md`

## Global Constraints

- The site is an independent demonstration concept, not a real clinic.
- Use only semantic HTML5, modern CSS3, vanilla JavaScript, and local assets.
- No React, Vite, TypeScript, Tailwind build tooling, Node dependency, PHP/MySQL, database, admin panel, booking workflow, authentication, patient form, payment flow, analytics, tracking pixel, AI chatbot, or runtime API.
- All public paths are relative and work when copied directly into Hostinger `public_html`.
- Use `noindex, nofollow, noarchive, nosnippet` on every HTML page and disallow crawlers in `robots.txt`.
- Never publish fake ratings, reviews, review counts, qualifications, registrations, addresses, awards, affiliations, or clinical outcomes.
- The only real contact destination is Bukhari AI Solutions WhatsApp `03214854145`; clinic contact controls are labelled demonstration interactions.
- Use the locked palette: `#102A33`, `#0E7C78`, `#E9785D`, `#F6F8F5`, `#EAF3F0`, `#FFFFFF`, `#17313A`, `#5B6E73`, `#D8E3DF`.
- Follow the two-button rule: dark primary action on the left and light secondary action on the right.
- Target WCAG 2.2 AA and Lighthouse 95+ where the audit environment permits.
- Check 320, 390, 768, 1024, and 1440px widths plus 200% zoom.

---

### Task 1: Native Project Foundation and Structural Test Harness

**Files:**
- Create: `index.html`
- Create: `privacy-notice.html`
- Create: `cookie-policy.html`
- Create: `website-terms.html`
- Create: `favicon.svg`
- Create: `robots.txt`
- Create: `.htaccess`
- Create: `README.md`
- Create: `tests/site_checks.py`

**Interfaces:**
- Produces: Four HTML documents with shared selectors `site-header`, `site-footer`, `demo-marquee`, and page-specific `<main id="main-content">`.
- Produces: `tests/site_checks.py` as the single dependency-free regression suite used by later tasks.

- [ ] **Step 1: Write failing structural checks**

Create `tests/site_checks.py` with Python `unittest`, `html.parser`, and `pathlib`. Include exact assertions for the four required HTML files, one `<h1>` per page, `main-content`, the noindex robots meta value, shared CSS/JS relative paths, legal cross-links, and absence of prohibited build/runtime files.

```python
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = ["index.html", "privacy-notice.html", "cookie-policy.html", "website-terms.html"]
PROHIBITED = ["package.json", "vite.config.js", "vite.config.ts", "src", "dist", ".env"]

class SiteChecks(unittest.TestCase):
    def test_required_pages_exist(self):
        for name in PAGES:
            self.assertTrue((ROOT / name).is_file(), name)

    def test_one_h1_and_demo_noindex(self):
        for name in PAGES:
            text = (ROOT / name).read_text(encoding="utf-8")
            self.assertEqual(len(re.findall(r"<h1(?:\s|>)", text, re.I)), 1, name)
            self.assertIn('content="noindex, nofollow, noarchive, nosnippet"', text)
            self.assertIn('id="main-content"', text)

    def test_prohibited_project_items_are_absent(self):
        for name in PROHIBITED:
            self.assertFalse((ROOT / name).exists(), name)
```

- [ ] **Step 2: Run the test and verify failure**

Run: `python3 -m unittest tests/site_checks.py -v`

Expected: FAIL because the four public pages do not exist.

- [ ] **Step 3: Implement the minimal native skeleton**

Create all public files. Each page must include:

```html
<meta name="robots" content="noindex, nofollow, noarchive, nosnippet">
<link rel="stylesheet" href="assets/css/style.css">
<script src="assets/js/main.js" defer></script>
<a class="skip-link" href="#main-content">Skip to main content</a>
```

Create `robots.txt` with:

```text
User-agent: *
Disallow: /
```

Create `.htaccess` with UTF-8, security headers suitable for a dependency-free static site, compression, asset caching, and a rule denying web access to `/tests` and `/docs`.

- [ ] **Step 4: Run the structural test**

Run: `python3 -m unittest tests/site_checks.py -v`

Expected: PASS for existence, H1, noindex, and prohibited-file checks.

- [ ] **Step 5: Commit the foundation**

```bash
git add index.html privacy-notice.html cookie-policy.html website-terms.html favicon.svg robots.txt .htaccess README.md tests/site_checks.py
git commit -m "feat: add NexaCare static site foundation"
```

### Task 2: Complete Homepage Content and Safety Disclosures

**Files:**
- Modify: `index.html`
- Modify: `tests/site_checks.py`

**Interfaces:**
- Consumes: Shared page foundation from Task 1.
- Produces: Section IDs `care`, `doctor`, `experience`, `visit`, `confidence`, `location`, `faq`, and `contact`.
- Produces: Reusable clinic-demo controls with class `js-demo-action` and `data-demo-action` labels.

- [ ] **Step 1: Add failing homepage-content checks**

Extend `tests/site_checks.py` with assertions that `index.html` contains every required section ID, the exact representative-profile label, four approved service names, no testimonial markup, no star-rating text, and the Bukhari AI number.

```python
    def test_homepage_required_sections_and_safe_content(self):
        text = (ROOT / "index.html").read_text(encoding="utf-8")
        for section_id in ["care", "doctor", "experience", "visit", "confidence", "location", "faq", "contact"]:
            self.assertIn(f'id="{section_id}"', text)
        self.assertIn("Representative practitioner profile", text)
        for service in ["New Patient Consultation", "Preventive Health Review", "Ongoing Health Support", "Follow-Up Consultation"]:
            self.assertIn(service, text)
        self.assertNotRegex(text.lower(), r"testimonial|5\.0|five-star|registered physician")
        self.assertIn("03214854145", text)
```

- [ ] **Step 2: Run the targeted check and verify failure**

Run: `python3 -m unittest tests.site_checks.SiteChecks.test_homepage_required_sections_and_safe_content -v`

Expected: FAIL because the homepage sections are not complete.

- [ ] **Step 3: Write complete patient-facing homepage copy**

Implement the full information architecture in the spec. Use one H1:

```text
Healthcare that feels clear from the first click.
```

Use this supporting line:

```text
A refined demonstration of how a modern medical website can introduce your care, build patient confidence, and make the next step easier.
```

Use a concise demo marquee, visible representative-image captions, the four approved broad service examples, a representative Dr. Ayesha Malik profile, three visit steps, four patient-confidence proof elements, a location demonstration panel without an address, administrative FAQs, and a full-width Bukhari AI conversion section.

Add one native `<dialog id="demo-dialog">` with an empty `data-dialog-message` target that Task 4 will progressively enhance.

- [ ] **Step 4: Run all content checks**

Run: `python3 -m unittest tests/site_checks.py -v`

Expected: PASS with no fabricated review or credential markers.

- [ ] **Step 5: Commit homepage content**

```bash
git add index.html tests/site_checks.py
git commit -m "feat: add safe specialty-neutral homepage content"
```

### Task 3: Visual System, Responsive Layout, and Local SVG Artwork

**Files:**
- Create: `assets/css/style.css`
- Create: `assets/icons/icon-sprite.svg`
- Create: `assets/images/map-artwork.svg`
- Create: `assets/images/pattern-care.svg`
- Modify: `index.html`
- Modify: `privacy-notice.html`
- Modify: `cookie-policy.html`
- Modify: `website-terms.html`
- Modify: `tests/site_checks.py`

**Interfaces:**
- Consumes: All HTML structure and class hooks from Tasks 1–2.
- Produces: CSS custom properties `--ink`, `--teal`, `--coral`, `--canvas`, `--mist`, `--surface`, `--text`, `--muted`, and `--border`.
- Produces: Responsive component classes for buttons, cards, hero, service grid, bento gallery, dialog, privacy bar, and mobile quick actions.

- [ ] **Step 1: Add failing design-system checks**

Extend `tests/site_checks.py` to verify the stylesheet exists, contains every locked color token, includes `:focus-visible`, `@media (prefers-reduced-motion: reduce)`, breakpoints for mobile and desktop, `clamp(`, and `overflow-wrap`.

```python
    def test_css_contains_locked_tokens_and_accessibility_rules(self):
        css = (ROOT / "assets/css/style.css").read_text(encoding="utf-8")
        for value in ["#102A33", "#0E7C78", "#E9785D", "#F6F8F5", "#EAF3F0", "#FFFFFF", "#17313A", "#5B6E73", "#D8E3DF"]:
            self.assertIn(value.lower(), css.lower())
        for marker in [":focus-visible", "prefers-reduced-motion", "clamp(", "overflow-wrap"]:
            self.assertIn(marker, css)
```

- [ ] **Step 2: Run the CSS check and verify failure**

Run: `python3 -m unittest tests.site_checks.SiteChecks.test_css_contains_locked_tokens_and_accessibility_rules -v`

Expected: FAIL because the complete visual system does not exist.

- [ ] **Step 3: Implement the visual system**

Build the locked theme with local system fonts, fluid type, generous spacing, fine borders, soft shadows, and restrained coral accents. Implement the asymmetrical hero, image-led service grid, editorial profile, bento gallery, three-step journey, confidence dashboard, map panel, CTA, four-column footer, fixed privacy bar, and mobile quick actions.

Use `.button--primary` for the left dark action and `.button--secondary` for the right light action. Keep primary button text contrast at or above AA and reserve coral for accents.

- [ ] **Step 4: Run the test suite and render a local first viewport**

Run:

```bash
python3 -m unittest tests/site_checks.py -v
python3 -m http.server 4173
```

Expected: Tests PASS; the homepage opens with the intended desktop and mobile structure and no missing local SVG assets.

- [ ] **Step 5: Commit the visual foundation**

```bash
git add assets index.html privacy-notice.html cookie-policy.html website-terms.html tests/site_checks.py
git commit -m "feat: implement NexaCare responsive visual system"
```

### Task 4: Accessible Interactions and Progressive Enhancement

**Files:**
- Create: `assets/js/main.js`
- Modify: `index.html`
- Modify: `cookie-policy.html`
- Modify: `tests/site_checks.py`

**Interfaces:**
- Consumes: `.js-menu-toggle`, `.js-demo-action`, `.js-accordion-trigger`, `#demo-dialog`, `#privacy-bar`, and `#reset-privacy` hooks.
- Produces: `openDemoDialog(actionLabel)`, `closeMenu({restoreFocus})`, and safe local preference helpers `readPreference`, `writePreference`, `removePreference`.

- [ ] **Step 1: Add failing interaction-source checks**

Extend `tests/site_checks.py` to confirm `assets/js/main.js` contains the site-specific storage key `nexacare_demo_privacy_v1`, Escape handling, `showModal`, focus restoration, accordion `aria-expanded` updates, and safe storage exception handling.

```python
    def test_interaction_contracts_exist(self):
        js = (ROOT / "assets/js/main.js").read_text(encoding="utf-8")
        for marker in ["nexacare_demo_privacy_v1", "showModal", "Escape", "aria-expanded", "try", "catch"]:
            self.assertIn(marker, js)
```

- [ ] **Step 2: Run the interaction check and verify failure**

Run: `python3 -m unittest tests.site_checks.SiteChecks.test_interaction_contracts_exist -v`

Expected: FAIL because the JavaScript interaction layer is incomplete.

- [ ] **Step 3: Implement progressive enhancement**

Implement:

```javascript
const STORAGE_KEY = "nexacare_demo_privacy_v1";

function readPreference() {
  try { return localStorage.getItem(STORAGE_KEY); }
  catch { return null; }
}

function writePreference(value) {
  try { localStorage.setItem(STORAGE_KEY, value); }
  catch { /* Keep the site usable when storage is blocked. */ }
}
```

Add accessible mobile-menu open/close behavior, Escape close, focus return, dialog messaging from `data-demo-action`, FAQ accordion state, privacy-bar acknowledgement, cookie-page preference reset, current-year output, and reduced-motion-safe reveal enhancement. Do not trap focus incorrectly or hide focusable content inside `aria-hidden="true"`.

- [ ] **Step 4: Validate syntax and contracts**

Run:

```bash
node --check assets/js/main.js
python3 -m unittest tests/site_checks.py -v
```

Expected: Both commands PASS.

- [ ] **Step 5: Commit interactions**

```bash
git add assets/js/main.js index.html cookie-policy.html tests/site_checks.py
git commit -m "feat: add accessible NexaCare interactions"
```

### Task 5: Generate and Integrate Representative Healthcare Imagery

**Files:**
- Create: `assets/images/nexacare-hero.webp`
- Create: `assets/images/nexacare-doctor.webp`
- Create: `assets/images/nexacare-clinic.webp`
- Create: `assets/images/nexacare-consultation.webp`
- Modify: `index.html`
- Modify: `tests/site_checks.py`

**Interfaces:**
- Consumes: Hero, service, doctor, and gallery media slots from Tasks 2–3.
- Produces: Local optimized WebP images with explicit width/height attributes and visible representative-image disclosures.

- [ ] **Step 1: Add failing image checks**

Extend `tests/site_checks.py` to assert all four image paths exist, each referenced `<img>` has `width`, `height`, and `alt`, the hero is not lazy-loaded, below-fold images use `loading="lazy"`, and the page contains the exact disclosure `AI-generated representative image`.

- [ ] **Step 2: Run image checks and verify failure**

Run: `python3 -m unittest tests/site_checks.py -v`

Expected: FAIL because representative image files are not present.

- [ ] **Step 3: Generate the approved image set**

Generate a coherent set showing a modern South Asian private-practice context: a confident female consultant in a bright refined clinic, an editorial doctor portrait, a calm reception/interior view, and a respectful consultation scene without procedures. Use warm natural light, the navy/teal/coral palette, realistic proportions, no visible logos, no readable medical records, no text, and no identifiable real people.

Crop and optimize to practical WebP dimensions: hero 1600×1200, portrait 1200×1500, clinic 1600×1067, consultation 1600×1067.

- [ ] **Step 4: Integrate and verify imagery**

Add responsive `<picture>` or `<img>` elements with explicit dimensions, useful alt text, and visible nearby disclosure captions. Set `fetchpriority="high"` on the hero and lazy-load below-fold images.

Run: `python3 -m unittest tests/site_checks.py -v`

Expected: PASS with no missing images or disclosure failures.

- [ ] **Step 5: Commit local imagery**

```bash
git add assets/images index.html tests/site_checks.py
git commit -m "feat: integrate representative NexaCare imagery"
```

### Task 6: Legal Pages, Security Headers, and Cross-Page Consistency

**Files:**
- Modify: `privacy-notice.html`
- Modify: `cookie-policy.html`
- Modify: `website-terms.html`
- Modify: `.htaccess`
- Modify: `README.md`
- Modify: `tests/site_checks.py`

**Interfaces:**
- Consumes: Shared header, footer, styles, and privacy preference controls.
- Produces: Complete demo-specific legal/supporting pages and deployment guidance.

- [ ] **Step 1: Add failing legal-content checks**

Extend `tests/site_checks.py` to assert that the privacy notice says no patient information is collected, the cookie page names `nexacare_demo_privacy_v1`, the terms page includes no-medical-advice and no-emergency-reliance language, and each page links back to `index.html`.

- [ ] **Step 2: Run legal checks and verify failure**

Run: `python3 -m unittest tests/site_checks.py -v`

Expected: FAIL until the complete demo-specific legal copy is present.

- [ ] **Step 3: Complete legal pages and README**

Write concise, accurate copy reflecting actual behavior: no patient form, no analytics, no ad pixels, no real medical practice, only local preference storage, no initial map load, a visitor-initiated WhatsApp link, representative imagery, and demo-only status. Explain in `README.md` how a real client conversion replaces demo content with approved business facts and how to deploy by copying the static files to Hostinger `public_html`.

- [ ] **Step 4: Run full automated checks**

Run:

```bash
python3 -m unittest tests/site_checks.py -v
node --check assets/js/main.js
```

Expected: PASS.

- [ ] **Step 5: Commit legal and deployment documentation**

```bash
git add privacy-notice.html cookie-policy.html website-terms.html .htaccess README.md tests/site_checks.py
git commit -m "docs: complete NexaCare legal and deployment content"
```

### Task 7: Rendered Audit, Performance Refinement, and Publishing

**Files:**
- Modify: Any public file with a verified defect
- Create: `.openai/hosting.json` only for the Sites preview deployment
- Modify: `tests/site_checks.py` if a discovered regression needs permanent coverage

**Interfaces:**
- Consumes: Complete static site from Tasks 1–6.
- Produces: Verified Git commit, packaged static archive, and private published demo URL.

- [ ] **Step 1: Run the complete pre-audit suite**

Run:

```bash
python3 -m unittest tests/site_checks.py -v
node --check assets/js/main.js
git status --short
```

Expected: All tests PASS and only intentional audit changes remain.

- [ ] **Step 2: Perform rendered responsive checks**

Serve the root with `python3 -m http.server 4173`. Inspect 320, 390, 768, 1024, and 1440px viewports plus 200% zoom. Verify menu, dialog, accordions, privacy acknowledgement/reset, skip link, focus order, fixed bars, internal links, image loading, reduced motion, and no clipping or horizontal overflow.

- [ ] **Step 3: Run accessibility and Lighthouse audits**

Audit the homepage and each legal page. Correct genuine contrast, label, semantic, tap-target, performance, and best-practice defects. Do not hide elements or manipulate the page merely to raise a score.

Expected: Target 95+ in all Lighthouse categories where the environment permits; document environmental exceptions.

- [ ] **Step 4: Commit audit fixes and create the exact publish state**

```bash
git add -A
git commit -m "fix: complete NexaCare cross-device audit"
git rev-parse --verify HEAD
```

Expected: A clean working tree and an exact full commit SHA.

- [ ] **Step 5: Save and publish the static site**

Create a Sites project once, preserve private access, save a version from the exact committed static output, deploy that saved version, and verify terminal deployment status. Keep `.openai/hosting.json` aligned with the returned project ID and static directory.

- [ ] **Step 6: Final live verification**

Open the deployed HTTPS URL and repeat the homepage smoke checks: hero asset, navigation, dialog, legal links, WhatsApp CTA, privacy bar, mobile layout, and noindex metadata. Report the live URL, verification result, and any environmental limitation.

