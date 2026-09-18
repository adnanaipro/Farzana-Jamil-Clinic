# NexaCare Medical Demo Website Design

**Date:** 2026-09-16  
**Mode:** Independent demonstration concept  
**Provider:** Bukhari AI Solutions  
**Commercial scope:** Essential Plan

## 1. Purpose and success criteria

NexaCare Medical will be a premium, specialty-neutral demonstration website that Bukhari AI Solutions can show to private doctors across multiple specialties. It must look credible as a modern medical-practice website while never presenting fictional details as a real clinic.

The demo succeeds when it:

- creates a strong first impression on desktop and mobile;
- demonstrates the complete patient-facing value of an Essential Plan website;
- can be adapted to a real doctor without redesigning the whole site;
- remains static, fast, accessible, privacy-conscious, and Hostinger-compatible;
- clearly identifies representative content and prevents search indexing;
- gives prospective clients a clear path to contact Bukhari AI Solutions.

## 2. Chosen direction

Use a realistic fictional medical brand rather than an agency landing page or a specialty-switching interface. The experience should feel like a finished private-practice website first. A restrained demo notice and final Bukhari AI sales call-to-action will explain its purpose without weakening the medical presentation.

The design personality is calm, modern, refined, reassuring, and clinically credible. Avoid generic blue-and-white hospital styling, heavy gradients, excessive glass effects, crowded icon grids, exaggerated claims, and futuristic AI imagery.

## 3. Locked brand specification

| Element | Specification |
| --- | --- |
| Brand name | NexaCare Medical |
| Positioning | Modern private medical care with clear information and easy contact |
| Primary | Deep Ink Navy `#102A33` |
| Secondary | Clinical Teal `#0E7C78` |
| Accent | Warm Coral `#E9785D` |
| Page background | Soft Porcelain `#F6F8F5` |
| Alternate background | Pale Mineral `#EAF3F0` |
| Surface | White `#FFFFFF` |
| Main text | `#17313A` |
| Muted text | `#5B6E73` |
| Border | `#D8E3DF` |
| Heading type | Local system serif stack led by Georgia; bold, editorial, restrained |
| Body type | Local system sans stack led by Segoe UI; clear and compact |
| Primary button | Deep navy fill, white text, coral micro-accent |
| Secondary button | White/transparent fill, navy border and text |
| Card style | White surfaces, fine borders, 18–28px radii, soft low-opacity shadows |
| Icon style | Consistent local SVG line icons with rounded geometry |
| Image direction | Warm natural light, South Asian context, credible modern clinic, no procedures |
| Motion | Subtle reveal, marquee, and carousel motion with full reduced-motion fallbacks |
| Logo | Custom local SVG combining an abstract `N`, medical cross, and care pathway |

Normal text and controls must meet WCAG 2.2 AA contrast targets. Coral is decorative or used for sufficiently large text, not low-contrast body copy.

## 4. Content model and truth safeguards

NexaCare Medical, its practitioner, services, contact details, and imagery are fictional demonstration content. The site must state this clearly and must not imply that the practice exists.

Use a representative profile named **Dr. Ayesha Malik, Consultant Physician** only inside a section visibly labelled `Representative practitioner profile`. The biography may describe the type of information a real doctor would provide, but it must not claim real qualifications, registrations, awards, years of experience, outcomes, or affiliations.

Use broad, non-diagnostic service examples:

- New Patient Consultation
- Preventive Health Review
- Ongoing Health Support
- Follow-Up Consultation

Every service description must remain general and administrative. Do not give diagnosis, treatment selection, prognosis, emergency instructions, or outcome promises.

Do not publish fake ratings, review counts, patient names, or testimonial quotations. Instead, include a premium `Patient confidence` section that explains how verified reviews, location, timings, and doctor information would appear on a real client website.

Clinic contact controls are demonstration interactions. Clicking them opens an accessible explanation panel saying that the live version would connect to the clinic's verified phone, WhatsApp, email, directions, or external booking system. The separate Bukhari AI call-to-action may use the verified business WhatsApp number `03214854145`.

## 5. Information architecture

### Homepage

1. Skip link
2. Single-line right-to-left demo marquee with hover/focus pause and static reduced-motion state
3. Sticky header with NexaCare logo, concise navigation, `Preview Contact` button, and accessible mobile menu
4. Hero with one H1, representative clinician image, two contrasting actions, three trust cues, and a small image-disclosure caption
5. Specialty-neutral trust strip
6. `Care, clearly explained` service presentation
7. Editorial doctor-profile section
8. `A calmer clinic experience` visual gallery
9. `Your visit` three-step journey
10. Patient-confidence section without fabricated reviews
11. Opening-hours and location demonstration panel without fake address data
12. Administrative FAQ accordion
13. Full-width Bukhari AI conversion call-to-action
14. Four-column footer with legal links, demo status, and Bukhari AI attribution
15. Mobile quick-action bar using demo-safe controls
16. Compact privacy/third-party-service bar

### Supporting pages

- `privacy-notice.html`
- `cookie-policy.html`
- `website-terms.html`

The legal pages describe the actual demo behavior: no patient form, no analytics, no advertising pixels, no medical service, local preference storage only, and no initial third-party map load.

## 6. Key interface components

### Header and navigation

The header remains compact and readable. Desktop navigation uses section anchors. Mobile navigation opens as a controlled panel, traps no focus, closes with Escape, returns focus to the trigger, and prevents background scrolling only while open.

### Hero

The hero uses an asymmetrical two-column layout with editorial typography, one local generated image, soft layered shapes, and a small floating availability-style card labelled as a demonstration. Primary and secondary buttons follow the global two-button rule: dark action on the left, light action on the right.

### Services

Use four image-led cards, not generic icon tiles. Cards have consistent aspect ratios, meaningful headings, concise copy, and a `What this section demonstrates` micro-label. Images must be local and visibly marked as AI-generated or representative.

### Doctor profile

Use a strong portrait-and-copy composition with a visible representative-profile label. Qualification and registration chips are intentionally omitted because no verified real practitioner data exists.

### Clinic experience gallery

Use a bento-style gallery with local representative images and concise captions. Avoid medical procedures, identifiable patients, before/after comparisons, or implied real facilities.

### Patient confidence

Replace fake review cards with a premium explanation of four proof elements a live site can connect: verified Google feedback, practitioner details, clinic timings, and directions. The visual may resemble a connected trust dashboard but must not show invented ratings or reviews.

### Location and privacy

Show a designed map placeholder and opening-hours layout. Because no verified address exists, do not create or load a map iframe. Explain that the live client version adds a click-to-load Google Map after the address is verified. Keep a non-functional demo directions control that opens the demo explanation panel.

### Demo explanation panel

Use one reusable accessible dialog for clinic actions. It includes a short explanation, a close button, and a Bukhari AI WhatsApp action. It never collects data.

## 7. Architecture and file structure

Use a direct-deployment static project with no build step:

```text
nexacare-medical-demo/
  index.html
  privacy-notice.html
  cookie-policy.html
  website-terms.html
  .htaccess
  robots.txt
  favicon.svg
  assets/
    css/style.css
    js/main.js
    icons/
    images/
  docs/superpowers/specs/
  README.md
```

Use semantic HTML5, modern CSS, and vanilla JavaScript only. Do not add React, Vite, TypeScript, Tailwind build tooling, Node dependencies, PHP/MySQL, a database, an admin panel, a booking workflow, authentication, patient forms, payments, analytics, tracking pixels, an AI chatbot, or external runtime APIs.

All production paths are relative and use lowercase hyphenated filenames. The project must run through a basic static server and by direct placement in Hostinger `public_html`.

## 8. Data flow and state

The site has no server-side data flow.

- Navigation and accordions are controlled in local JavaScript.
- Demo-action controls pass a short action label into one reusable dialog.
- The privacy bar stores only a site-specific acknowledgement/preference in `localStorage`.
- No personal or patient information is requested, submitted, persisted, or transmitted.
- The map remains local artwork because there is no verified address or embed URL.
- The Bukhari AI WhatsApp link sends only a prefilled sales-intent message initiated by the visitor.

If JavaScript fails, core content, legal links, section navigation, and the Bukhari AI contact link remain usable. Interactive controls are progressively enhanced.

## 9. Responsive behavior

- Mobile-first support from 320px.
- Fluid spacing and type using `clamp()` with conservative maximums.
- No horizontal scrolling at 320px or 200% zoom.
- Hero, profile, gallery, and location layouts collapse to one column on small screens.
- Mobile quick actions remain above the privacy bar and safe-area inset.
- Touch targets are approximately 44×44 CSS pixels.
- Images declare dimensions and use responsive sizing to limit layout shift.
- The hero image loads eagerly; below-fold images lazy-load.

## 10. Accessibility

- WCAG 2.2 AA-minded color, focus, semantics, and interaction.
- Exactly one descriptive H1 on each page.
- Logical heading order and landmark structure.
- Visible keyboard focus for all interactive elements.
- Accessible names for icon-only controls.
- Menu, dialog, accordion, marquee, and any carousel behavior work by keyboard.
- Motion stops or becomes static under `prefers-reduced-motion`.
- Decorative SVGs are hidden from assistive technology; informative images have concise alt text.
- No autoplay audio or video.

## 11. SEO, privacy, and safety

- Use `noindex, nofollow, noarchive, nosnippet` on every page.
- `robots.txt` disallows crawling.
- Do not create a production sitemap or publish real medical-business schema.
- Metadata must say that NexaCare is a demonstration concept.
- The marquee uses a concise adaptation of the approved demo disclaimer and links to the full terms.
- All representative images receive visible disclosure.
- No external fonts, trackers, review widgets, map iframe, or third-party scripts load automatically.
- Emergency copy states only that a real clinic's approved urgent-care guidance would appear here and that this demo must not be used for medical advice or urgent care.

## 12. Performance and visual-quality targets

- Lighthouse target: 95+ for Performance, Accessibility, Best Practices, and SEO where the audit environment permits.
- No render-blocking external font or script dependencies.
- Local images are compressed and sized for their rendered use.
- CSS and JavaScript remain small, structured, and dependency-free.
- No console errors, broken links, missing assets, clipping, overlaps, or cumulative layout shift from unsized media.
- Visual polish is checked at 320, 390, 768, 1024, and 1440px.

## 13. Error handling and fallbacks

- Missing optional imagery uses designed color fields, never broken image icons.
- The mobile menu and dialog restore safe page state when closed.
- Invalid localStorage access is caught so the page remains functional in restricted browsing modes.
- If the WhatsApp deep link is unavailable, the visible phone number remains readable and selectable.
- Unsupported CSS effects degrade to solid surfaces and borders.

## 14. Verification and acceptance

Before completion:

1. Validate every HTML page and check internal links.
2. Run JavaScript syntax and console checks.
3. Verify keyboard navigation, Escape behavior, focus return, and accordion states.
4. Inspect the site at all target viewport widths and 200% zoom.
5. Confirm no horizontal overflow or hidden content.
6. Confirm no external requests occur before the visitor activates the Bukhari AI WhatsApp link.
7. Confirm all representative imagery is visibly labelled.
8. Confirm no fake reviews, ratings, qualifications, address, or clinical claims appear.
9. Confirm direct static-server and Hostinger-style relative-path compatibility.
10. Run Lighthouse and correct material failures before handoff.

## 15. Out of scope

- Appointment database or custom booking system
- Admin or content-management panel
- Login, patient portal, or authentication
- Medical-history or symptom forms
- Online payments
- Live Google review synchronization
- Real Google Maps embed without a verified clinic address
- Analytics, advertising pixels, and marketing cookies
- AI receptionist, chatbot, diagnosis, or clinical automation
- Production indexing or real-clinic schema

These are Business or AI Plan capabilities, or require verified production information.

