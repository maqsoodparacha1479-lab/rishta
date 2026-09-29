# RISHTA WEBSITE — FINAL BRAND UI & CSS QA REPORT

**Date:** 26 September 2026 · **Project:** `C:\Users\Hp\Downloads\rishta`
**Scope:** the visual refinement and CSS-quality phase, done as controlled, isolated edits to the existing stylesheet (no rewrite).

> **Status:** visual and CSS QA is complete, and every automated check passes (1,116/1,116). This is **not** declared "production ready", because owner items remain open (§22): the hero-photo licence, Terms §4, the Urdu spelling confirmation, the domain, and testing on Safari and real devices.

---

## 1. Current UI Audit

Measured on the stylesheet before any edit:

| Area | Finding |
| --- | --- |
| Fonts | 3 font-family tokens only (Fraunces, Work Sans, Noto Nastaliq Urdu). No raw font declarations. Italic is used only on Fraunces, which is loaded with italics, so there's no faux-italic. |
| Colours | Tokenised brand palette. A few WhatsApp tints were already tokenised last round. The only other literals are decorative cover-art gradients. |
| Radius | **Inconsistent:** 12px ×7, 14px ×6, 18px ×3, one-off 10/16/20/22px next to the `--radius-*` tokens. |
| Shadows | **12 hard-coded shadow values** (modal, popover, floating buttons, header, CTA hover, input rings). |
| `!important` | 9, all intentional (`[hidden]`, reduced motion, reveal fallback). |
| z-index | Tokenised scale (float 90 / header 100 / popover 120 / modal 200); the skip link sits at 1000 by design. No conflicts found. |
| Breakpoints | 900px and 640px each appeared **twice**, 1080px three times (duplicated media blocks). |
| Duplicate selectors | `.hero__badge*` (layout + animation split); `.site-header` ×3 (layout, entrance animation, view transition). |
| Animation | The header replayed an entrance animation **on every page load**. The floating buttons waited about 1.2s to appear on every page. |
| Images | Only the home hero used `<img>`, serving the 346 KB original to phones. News covers were CSS art. There were no images on About, How It Works, Registration or Success Stories. |
| Inline styles | 0 (the CSP forbids them). |

## 2. Previous CSS Problems

Carried over from earlier phases: the radius and shadow drift above, duplicated media blocks (the v4 page-component responsive rules were added as a separate block), duplicated selectors, a header animation that replayed on every navigation, and an unoptimised hero image. **No broken layout, overflow or contrast failures were found**: the baseline regression passed 1,013/1,013.

## 3. CSS Changes

Every change was made by a scripted edit that fails if its target isn't found exactly, so nothing was replaced silently.

- **Tokens added:** `--radius-xs`; `--radius-sm` changed from 10px to 12px; `--shadow-overlay`, `--shadow-modal`, `--shadow-header`, `--shadow-cta`, `--shadow-fab`, `--shadow-fab-hover`, `--ring-input`, `--ring-error`.
- **Radius and shadow literals replaced by tokens:** 0 hard-coded shadows remain. The only px radii left are intentional: the brand mark's leaf corner (14/14/14/4), 2–6px bars and the focus radius, and the arch shapes.
- **Breakpoints merged:** page-component rules moved into the single responsive section. Each of 900px and 640px now appears once. The two remaining 1080px blocks are the header's own navigation block (kept beside the header on purpose) and the global responsive block.
- **Duplicate selectors:** hero badge animations folded into the badge rules, and the header entrance-animation rule and keyframes deleted.
- **New components:** `.btn-text`, disabled states, `.illus` figures, `.cover--img`.
- **Size:** `styles.css` went from 82.1 KB to 83.9 KB. The new image and figure rules outweigh what was removed.

## 4. Brand Color System

| Token | Value | Use |
| --- | --- | --- |
| `--color-primary` | `#5B1A33` wine | CTAs, active nav, links, headings accent |
| `--color-primary-hover` | `#45132A` | Button hover |
| `--color-primary-deep` | `#2E0F1D` | Top strip, footer, dark sections, logo tile |
| `--color-primary-soft` | `#F3E6E9` | Icon tiles, soft fills |
| `--color-accent` / `-strong` / `-soft` | `#D4A853` / `#8A6420` / `#F6ECD6` | Gold on dark / gold text and marks on light / tints |
| `--color-secondary` | `#F4ECE3` cream | Alternate section bands |
| `--color-background` / `--color-surface` | `#FBF8F4` / `#FFFFFF` | Page / cards |
| `--color-text-primary` / `-secondary` | `#24171C` / `#5E4B53` | Text |
| `--color-border` / `-strong` | wine at 12% / 24% | Borders |
| success / warning / error | `#2F6B4F` / `#8F6212` / `#A12C2C` | States |
| WhatsApp green + ink/deep/soft | brand-mandated | WhatsApp controls only |

The logo tile (deep wine + gold heart), header CTA, active nav, links, fee panels and footer are all built from these tokens, so they read as one system.

## 5. Header Redesign

The header already matched the brand. It was kept and refined, not recoloured.

- **Surface:** cream (`--color-background`). Transparent at the top of a page, blending into the hero's cream; after 8px of scroll it becomes a 93%-opaque cream surface with backdrop blur, a hairline border and `--shadow-header`. It uses the site's standard transition timing.
- **Contents:** logo tile + "Rishta Trust / Matrimonial Consultancy" · Home, About, How It Works, Find a Match, Success Stories, News · WhatsApp icon · **Register** (primary wine pill, the same component as every other primary CTA).
- **Active state:** wine text, weight 600, and now a **stronger gold-brown underline** (`--color-accent-strong`) instead of the pale gold. The pale gold is kept for hover.
- **Replay removed:** the header no longer replays an entrance animation on every page.
- **Measured contrast** (automated, see §21): brand name 16.5:1, nav link 16.3:1, active nav 12.1:1, Register CTA 11.8:1, top-strip link 16.1:1. **Identical at the top and when scrolled.** The requirement is ≥ 4.5:1.
- **Mobile:** logo + hamburger. The drawer slides and fades (280ms) with no layout jump. It lists all 6 pages plus FAQs and Contact, "Register — PKR 5,000" and WhatsApp. Esc and outside click close it, focus returns to the toggle, and `aria-expanded`/`aria-label` update (all tested). Screenshots checked at 320, 375 and 390.
- **Login is still not shown:** the site has no authentication, and a Login link would lead nowhere. It should be added when accounts exist.
- **Dropdowns:** there are none.

## 6. Typography System

| Role | Family | Token |
| --- | --- | --- |
| Display / headings | Fraunces (variable, optical sizing, roman + italic) | `--font-display` |
| Body / UI (nav, buttons, forms, labels) | Work Sans 400–700 | `--font-body` |
| Urdu | Noto Nastaliq Urdu 500 (subset) | `--font-urdu` |

- **Scale:** fluid `clamp()` values for H1–H3, lead, body, small and label. The hero H1 runs from 2.6rem to 4.4rem.
- **Rhythm:** headings balance their lines, body line-height is 1.65, labels have 0.14em tracking, and paragraphs are capped at about 34–42rem.
- Buttons and form controls inherit the body font (`font: inherit`), so there are no system-font buttons.
- **New automated audit:** every visible text node on all 20 pages must render in one of the three families. Urdu must use Nastaliq, Latin text must not, and there must be no faux italic on the body font. **20/20 pages pass.**

## 7. Family/Urdu Font Fix

- **"Family aur Aapki Pasand":** set in Fraunces, with "Aapki Pasand" in the loaded true italic. It carries `lang="ur-Latn"` (Roman Urdu), appears in the home H1 and the footer brand, and comes from `site.json → slogan`.
- **Urdu slogan "قابلِ اعتماد طریقے سے":** set in Noto Nastaliq Urdu with `lang="ur"`, right-to-left, line-height 1.9, and no letter-spacing (tracking breaks Nastaliq joining). The spelling is the owner's approved original, preserved exactly and checked codepoint by codepoint in tests.
- **Font load verified:** a test checks that the browser has the Urdu face loaded for the slogan's glyphs (`document.fonts.check` passes), so there's no fallback font.
- **Subset:** the Urdu font file only contains the glyphs in use, via `text=`. This phase added no new Urdu text, so no glyphs were missing. The README says how to extend the subset.

## 8. Hero Improvements

- The existing photo is now **responsive**: `hero-480.jpg` (62 KB) and `hero-736.jpg` (139 KB) via `srcset`/`sizes`, instead of the 346 KB original for everyone. That's about 82% less on phones and 60% less on desktop.
- Explicit width and height, `object-fit: cover` in the arch frame, `fetchpriority="high"`, and alt text: "A bride and groom in traditional Pakistani wedding dress".
- The image is served from the registry (`src/data/images.json → hero`), so a licensed or real photo can replace it without touching markup. **Its licence is still unconfirmed** (§22).
- The load sequence is unchanged: eyebrow → slogan → Urdu line → text → CTAs, then the image scales and fades in and the badges follow.

## 9. Demo Images Added

Seven **original SVG illustrations** were generated by `src/illustrations.py` in the brand palette. They are culturally grounded (Mughal arch, jali lattice, marigold garlands, diyas, a tea table) and **contain no people**, so there is no identity, consent or licence risk. They total 32 KB.

| Illustration | Used on | Purpose |
| --- | --- | --- |
| `family-meeting.svg` | About (approach), "Registration sitting" article | Family introduction over tea |
| `journey.svg` | How It Works hero | Stepping stones to a lit doorway (the process) |
| `registration.svg` | Registration sidebar | Clipboard checklist + receipt (onboarding) |
| `rings.svg` | Success Stories hero | Marriage, without inventing a couple |
| `verification.svg` | Verification article | ID card, document, stamp, shield |
| `privacy-photo.svg` | "Why we never publish photos" article | Veiled frame + padlock |
| `support.svg` | Free-registration article | Heart, garland, diyas |

- **Registry:** every image is listed in `src/data/images.json` with `status: "demo"` or `"owner"`. Swapping in real photography means editing one entry and rebuilding.
- **Alt text:** page illustrations have descriptive alt text. News covers are **decorative** (`alt=""`), because the card title already carries the meaning.

**Deliberately not added:**
- **Demo profile photos on Find a Match:** the business never publishes candidate photos, so demo faces would contradict that promise and could be mistaken for real users.
- **Success-story photos:** there are no real stories.
- **Contact page:** it already has maps.
- **Footer:** the brief says to avoid images there.

## 10. News Visual Improvements

- **Consistent 16:9 covers** on all news cards, using illustrations instead of generic CSS art. They zoom slightly on hover (scale 1.035 over 0.9s), and the card lifts 3px. Nothing jumps.
- **News page:** the featured article is a wide row card (image ~55%, text ~45%); the rest are a 3-column grid.
- **Home:** the featured card plus two side cards with **inset square thumbnails**. A first attempt cropped the art into tall slivers; that was caught in visual QA and fixed.
- **Phones:** everything stacks to single cards with 16:9 covers.
- **Article pages:** a 2:1 hero illustration under the headline.

## 11. Registration Page

- **Fee panel:** REGISTRATION FEE / **PKR 5,000** (display size, up to 3.75rem) / One-time registration. There is no other price anywhere (tested on every page).
- **New:** a supporting illustration at the top of the sidebar.
- **Form:** the 5-step stepper (Details · Contact · Profile · Review · Send), the "What's included", "How payment works" and privacy messaging are all unchanged.
- The final screen's "Edit my details" now uses the new `.btn-text` style.
- The Register CTAs use the same `.btn-primary` / `.btn-gold` components as the header CTA.

## 12. Card Improvements

All cards now use the token system: `--radius-lg` for content cards (proposal, benefit, news, office, registration, legal), `--radius-md` for secondary panels and icon tiles, one 1px `--color-border`, and `--shadow-1`/`--shadow-2` only. Hover lifts cards by 3–4px, with a slight zoom on images. No gradients were added.

## 13. Button Improvements

| Variant | Use |
| --- | --- |
| `.btn-primary` | Wine: main CTAs (header Register, Register Now, Continue) |
| `.btn-secondary` | Outline neutral |
| `.btn-gold` | CTA on dark panels |
| `.btn-ghost-light` | Outline on dark sections |
| `.btn-whatsapp` | WhatsApp only |
| **`.btn-text` (new)** | Minimal text button with a soft hover fill |

- **States:** hover (colour + 1px lift + CTA shadow token), active (scale 0.98), focus-visible (token ring), and **disabled (new**: 50% opacity, not-allowed cursor, no lift or shadow; covers `:disabled` and `aria-disabled`).
- **Size:** at least 40px tall (48px default) for touch.

## 14. Form Improvements

Forms were reviewed: registration, contact, match filters and search. **Login does not exist.**

- **Every input:** a visible `<label>` (tested; placeholders are never the only label), a consistent 52px height, a 1px strong border, hover border, a wine focus border with `--ring-input`, and an `aria-invalid` error state with `--ring-error`, a pale error fill and a linked message.
- **Valid and disabled states:** a green valid border, and **a new disabled state** (cream fill, muted text, not-allowed cursor).
- **Other:** a custom select arrow and a native checkbox in the brand colour.

## 15. Animation Review

| Animation | Decision |
| --- | --- |
| Header entrance (replayed on every page) | **Removed** |
| Floating-button entrance delay 1.05–1.2s | **Shortened** to 0.25–0.35s |
| WhatsApp pulse | Already removed (v4) |
| Hero fade-up sequence + image scale, badges | Kept (home only) |
| Scroll reveal (once), How It Works line draw | Kept |
| Card hover lift, image zoom, icon nudge, button press | Kept (transform only) |
| Mobile drawer slide/fade, FAQ open, registration step slide | Kept |
| Page transitions (180 / 320ms View Transitions) | Kept; never delays navigation |

- **No infinite or spinning animations.** Everything uses transform/opacity except colour transitions.
- **Reduced motion:** everything is disabled under `prefers-reduced-motion`, and content stays visible if the script fails.

## 16. Responsive QA

**Automated:** 20 pages × 9 widths (320, 375, 390, 414, 768, 1024, 1280, 1440, 1920), checking for no horizontal overflow, no element escaping the viewport, no floating-button overlap or off-screen buttons, and no text under 12px. **540/540 pass.**

**Screenshots reviewed:**
- **Desktop:** home news, news page, article, How It Works, registration, About.
- **Phone (390px):** news, success stories.
- **Earlier this phase:** the hero at 1440/390/320 and the footer at 390.

**Found and fixed:** the cropped home news thumbnails (§10).

## 17. Accessibility QA

**Tested:**
- One `h1` per page; every control labelled; accessible names on all buttons and links; ARIA references resolve; no duplicate IDs.
- **Images:** all have an `alt` attribute (decorative covers have `alt=""`), explicit dimensions, and no distortion.
- Header contrast of at least 4.5:1 (actual 11.8–16.5).
- Modal focus trap and restore; Esc closes the nav, Help and modals; keyboard access through the registration stepper.
- Reduced motion; `lang` attributes on the Urdu and Roman-Urdu slogans.

**Not tested:** a full-page contrast audit beyond the header (body pairs were chosen for at least 4.5:1), and real screen-reader sessions.

## 18. Security QA

The visual changes added no scripts, no third-party hosts and no inline code.

- **CSP:** unchanged. `img-src 'self' data:` covers the new local JPEG and SVG files. There are **0 CSP violations** on all 20 pages.
- **SVG safety:** the illustrations are static SVG with no scripts or external references, loaded via `<img>`, where browsers never run SVG scripts.
- **Image URLs:** all come from the checked-in registry and the build escapes them. Nothing comes from user input.
- **Secrets / data exposure:** no API keys, environment variables, auth, payment data or private profile data exist or are exposed. The demo images represent no real person.
- **Registration data:** handled the same way as before (WhatsApp hand-off, nothing stored, no `localStorage`).

## 19. Performance QA

| Asset | Before | After |
| --- | --- | --- |
| Hero image on phones | 346 KB | **62 KB** (`hero-480.jpg`) |
| Hero image on desktop | 346 KB | **139 KB** (`hero-736.jpg`) |
| Social share image | 626 KB PNG | **96 KB** JPEG |
| New illustrations | — | 32 KB total (SVG), lazy-loaded |
| `styles.css` / `script.js` | 82.1 / 22.9 KB | 83.9 / 22.9 KB |

- No new dependencies, and fonts are unchanged (Urdu subset).
- All non-hero images are `loading="lazy"` with explicit dimensions (tested), so there's no layout shift.
- WebP/AVIF wasn't used, because no encoder is available on this machine without installing software. Optimised JPEG plus SVG was used instead.
- `assets/hero-bg.jpg` is kept only as the master file; the site no longer references it.

## 20. Tests Executed

The project has no lint, typecheck, unit-test or E2E suite, so none could be run. These were run instead:
1. `python src/illustrations.py` (renders 7 SVGs) and `python src/build.py` (20 pages; an unknown token or image key fails the build).
2. The headless Chrome 153 browser harness (static, functional and layout suites) against a local server. **Extended this phase with:**
   - the typography audit
   - header contrast at top and scrolled
   - brand-token header check
   - image loading, dimensions, distortion, lazy-loading, decorative alt text, and no identity or verification claims in alt text
3. Chrome console / CSP / network-error capture on all 20 pages.
4. Screenshot review.

## 21. Exact Results

```
Baseline (before this phase):          FAILS=0 TOTAL=1013

python src/illustrations.py
  family-meeting.svg 7.0 KB · verification.svg 3.5 KB · privacy-photo.svg 2.5 KB · support.svg 6.2 KB
  rings.svg 2.8 KB · registration.svg 4.0 KB · journey.svg 5.6 KB
python src/build.py → Built 20 pages (base_url not set: no canonical URLs or sitemap)
  28 <img> tags · 0 references to the old og-image.png or hero-bg.jpg

Harness, final run:                    FAILS=0 TOTAL=1116
  static      521   (previous checks + per page: brand-font-only typography, image dimensions/distortion,
                     lazy loading, decorative alt, no identity claims in alt, images load)
  functional   55   (previous + header contrast at top: brand name 16.5, nav 16.3, active 12.1,
                     Register CTA 11.8, top strip 16.1; identical when scrolled; header uses brand tokens:
                     bg rgba(251,248,244,.93), CTA rgb(91,26,51))
  layout      540   (20 pages × 9 widths)

Console / CSP / network (20 pages): 0 errors, 0 CSP violations, 0 failed loads
  (only Google Maps' own log inside its embed on about.html and contact.html)
```

**Issues found and fixed this phase:**
- radius and shadow drift
- duplicated breakpoints and selectors
- the header replaying on every page load
- slow floating buttons
- a heavy hero image on phones
- a heavy share image
- the home news thumbnail crop
- two test-code bugs (in the harness, not the site): a lazy-image assertion and a swallowed newline

**Not verified:**
- **Browsers and devices:** Safari, Firefox and real phones.
- **Accessibility tools:** screen readers, and a full-page contrast audit.
- **Features that don't exist:** Login, Signup and payment.

## 22. Remaining Issues

1. **Hero photo licence and consent** for `hero-736.jpg` / `hero-480.jpg` (from the owner's original `hero-bg.jpg`) are unconfirmed. Confirm them, or replace the `hero` entry in `images.json`.
2. **Urdu slogan spelling:** the brief wrote "کابلی"; the project's approved original is **قابلِ**, which is what's used. The owner should confirm.
3. **Login/Register:** Register is live. Login needs a real account system (a backend project).
4. **Terms & Conditions §4** conflicts with the single PKR 5,000 fee. The free-registration policy and the contents of the fee also need the owner's decision.
5. **Review content:** the sample listings and the 4 articles.
6. **Deployment:** set `base_url` (canonical and sitemap), configure the host's 404 page and security headers, and don't upload `src/`, the reports, `README.md`, `assets/hero-bg.jpg` or `24 sep file.zip`.
7. **Not tested:** Safari, Firefox, real Android/iOS devices and screen readers.
8. **Image formats:** WebP/AVIF versions of the hero would save a little more once an encoder is available.

Visual and CSS QA is complete for Chromium at all nine widths. **Not declared production-ready** until items 1, 2, 4, 6 and 7 are resolved.
