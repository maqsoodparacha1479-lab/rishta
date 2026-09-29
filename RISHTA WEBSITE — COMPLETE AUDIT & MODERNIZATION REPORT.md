# RISHTA WEBSITE — COMPLETE AUDIT & MODERNIZATION REPORT

**Date:** 25 September 2026 · **Project:** `C:\Users\Hp\Downloads\rishta`
**Supersedes:** `RISHTA WEBSITE — PREMIUM MULTI-PAGE REDESIGN REPORT.md` (kept for history)

---

## 1. Executive Summary

A complete audit was carried out first. It covered the current site, both previous iterations, the CSS, functionality, security and the brand wording. The site was then modernised selectively, keeping the stable multi-page work.

What this round changed:
- **The owner's slogans are now the brand line.** The home headline is **"Family aur Aapki Pasand"**, and the owner's approved Urdu **"قابلِ اعتماد طریقے سے"** sits beneath it. Both also appear in the footer brand block, the home page title and the social share image. Both come from one source in `site.json`.
- **Urdu spelling:** the brief spelled the Urdu "کابلی". The project's original, approved text spells it **قابلِ**, and per the brief's own rule the project's version was preserved. See §7; please confirm.
- **Design-system cleanup and fixes:** WhatsApp tints are now tokens; the phone footer no longer breaks contact details mid-word; About and How It Works sections are renamed to the requested structure.
- **Tests:** **1,013 automated checks, all passing**, including new checks that the slogans are exact.

**Verdict:** ready for staging and client review, **not yet for production** (§31). The site has **no backend**, so there is no login, online payment, OTP or profile database. None of these were simulated.

## 2. Complete Existing-System Audit

| Area | Finding |
| --- | --- |
| Repository | Static site. No git, no `package.json` or lock files, no framework, no deployment configuration. |
| Build system | `src/build.py` (Python stdlib) generates 20 static HTML pages from `src/` (added in v4). |
| Routing | Flat `.html` files: `index`, `about`, `how-it-works`, `matches`, `registration`, `success-stories`, `news`, `news-*` (4), `faq`, `contact`, `privacy`, `terms`, `safety`, `profile-*` (3), `404`. |
| Components | Build partials (head, sprite, header, footer, widgets) plus BEM CSS components. |
| API layer / backend / database | **None.** |
| Authentication / authorization / sessions / cookies / tokens | **None.** No login, signup or logout exists. |
| Registration | 5-step browser form → WhatsApp hand-off to a consultant. Nothing is stored. |
| Payment | **None.** No gateway, keys or code. The fee is collected offline by the consultant. |
| News / blog | 4 static articles generated from `src/articles/`. No CMS. |
| Assets | `hero-bg.jpg` (licence unknown), `og-image.png`. All other artwork is CSS or SVG. |
| CSS / theme / fonts | One tokenised stylesheet. Fraunces + Work Sans + Noto Nastaliq Urdu (subset). |
| Environment configuration / secrets | None exist. Business contacts live in `src/data/site.json`. |
| SEO | Titles, descriptions, OG/Twitter, JSON-LD and `robots.txt`. Canonical and sitemap wait on `base_url`. |
| Tests | No project tests existed. A browser harness was built for this work (§28). |
| Stray file | `24 sep file.zip` is a snapshot of v3. Not used by the site; don't upload it. |

**Keep:** the multi-page architecture, builder, design tokens, WhatsApp/Help stack, registration flow, CSP and accessibility work.
**Modernise:** the brand line (slogans), About/How It Works naming, footer on phones, colour tokens.
**Remove:** nothing further. The obsolete fee cards and flip cards were already removed in v4 and remain absent (tested).

## 3. Previous Implementations Audit

No git history exists. The iterations were reconstructed from the on-disk snapshots: `rishta-backup-2026-09-24` (**v1**, the original site, labelled v2.0 in its own code), `rishta-backup-v3-2026-09-24` and `24 sep file.zip` (**v3**), and the current project (**v4 → v5**).

| Feature | History | Current behaviour | Status | Decision / reason |
| --- | --- | --- | --- | --- |
| File names | v1: `index.html.html` etc. The site loaded **unstyled, without JS**, and the legal links returned 404s | Correct names | Fixed in v3 | Keep |
| Header | v1 anchor nav → v3 sticky header → v4 multi-page nav + Register | Sticky, scroll state, mobile drawer, Esc | Working (tested) | Keep |
| Hero | v1 Urdu line + callback form → v3/v4 "Find a meaningful match" | **v5: owner slogans** | Working (tested) | Modified to the owner's brand line |
| Pricing | v1/v3: 3 package cards (Rs 2k–30k+) | Single PKR 5,000 fee | Removed in v4 (tested absent) | Keep removed |
| Flip cards | v3: 3 × 3D flip cards | 3 static benefit cards | Replaced in v4 | Keep |
| Registration | v1: callback form → WhatsApp | 5-step form → WhatsApp hand-off | Working (tested) | Keep. No backend steps exist to add |
| Match search | v1: 3 static sample listings | Filterable page + 3 profile pages | Working (tested) | Keep |
| News | v3: 4 static articles | Editorial list, filters, articles | Working (tested) | Keep |
| WhatsApp | v1: single floating link; v3: pulse | Floating button, "Chat with us", no pulse | Working (tested) | Keep |
| Help widget | v3 new | Popover with 4 real channels | Working (tested) | Keep |
| Footer | v1: 4 columns; v4: CTA + 5 columns | + slogans; phone layout fixed | Working (tested) | Modified |
| Animations | v1 fade-up hid content without JS; v3 reveal-ready fix | Hero sequence, reveal, timeline, view transitions | Working | Keep |
| Maps | v1: invalid-looking embed IDs | Address-query embeds | Working (loads, no errors) | Keep |
| Authentication | Never existed | — | Not implemented | Needs a backend |
| Payment | Never existed | — | Not implemented | Needs a backend |
| Responsive CSS | v1: 3 breakpoints; v3/v4: tokenised | 1080 / 900 / 640 / 360 | Working (tested) | Keep |

## 4. Previous Problems Found

**In earlier iterations:**
- Double file extensions (v1).
- A false "request recorded" message (v1).
- Broken package preselect (v1).
- `innerHTML` with user input (v1).
- Multiple fee cards (v1/v3).
- No brand slogan: the owner's Urdu line had been dropped from the hero in v4.

**Found in the v4 audit (this round):**
- **Brand slogan missing.** "Family aur Aapki Pasand" appeared nowhere; the Urdu line survived only in the top strip and footer.
- **Footer on phones:** at 390px the Connect column broke emails and phone numbers mid-word (e.g. `0323-` / `0785312`).
- **Hard-coded colours:** WhatsApp tint colours were literals instead of tokens (`#E3F8EA`, `#128C4A`, `#0B2E1A`).
- **Repeated selectors:** `.site-header` ×3 and `.hero__badge*` ×2. Each covers a separate concern (layout, animation, view transition), so they were documented and kept.
- **No visual defects** at any of the 9 widths: 540/540 layout checks passed in the baseline.

**Visual audit method:** automated overflow, overlap and text-size checks on all 20 pages at 320/375/390/414/768/1024/1280/1440/1920, plus screenshot review of the home, registration, news, matches, profile, how-it-works, stories and footer at desktop and phone widths.

## 5. Recovery Work

Nothing needed reverting. The v4 build was stable (baseline **949/949 passing** before any change). Earlier good work was kept as-is:
- the v1 business content and legal text
- the v1 **Urdu wording**, now restored to the hero
- the v3 accessibility, CSP and floating stack
- the v4 pages and builder

## 6. Business Requirements

| Requirement | Status |
| --- | --- |
| One public fee: PKR 5,000 one-time | ✅ Shown in the header menu, hero facts, home CTA, registration hero and review step, footer, FAQ. Tested on every page |
| No Basic/Premium/Gold/Silver/monthly/subscription pricing | ✅ Tested absent on all 20 pages |
| No invented discounts or offers | ✅ None |
| Backend fee logic preserved | N/A: no backend exists |

**Open business items** (unchanged since the last report):
- **Terms §4** still mentions a "consultancy advance / final balance".
- **Free registration for deserving families** is still mentioned in the FAQ and one article. It's an existing policy; confirm whether to keep it.
- **Confirm what the fee includes.**

## 7. Brand/Slogan Implementation

| Slogan | Where it appears | Source |
| --- | --- | --- |
| **Family aur Aapki Pasand** | Home H1 (`lang="ur-Latn"`, "Aapki Pasand" in italic wine), footer brand block on every page, home `<title>` and meta description, social share image | `site.json → slogan` |
| **قابلِ اعتماد طریقے سے** | Directly under the home H1 in Nastaliq with a gold rule, footer brand block, social share image | `site.json → slogan_urdu` |

**Spelling decision.** The brief wrote "کابلی اعتماد طریقے سے" and also said: *"If the exact Urdu spelling currently exists in the project, inspect and preserve that exact approved version."* The owner's original site (v1, `index.html.html` line 105) contains "فیملی کی مرضی، **قابلِ** اعتماد طریقے سے".
- Codepoints were verified: `0642 0627 0628 0644 0650 …`, i.e. **ق ا ب ل ِ**.
- "کابلی" (ک…ی) appears in no version of the project. It reads as *kābulī* ("from Kabul"), so it's almost certainly a typing slip for **قابلِ** (*qābil-e*, as in *qābil-e-iʿtimād*, "trustworthy").
- The project's approved spelling was therefore used. Automated tests check that it is codepoint-identical to the original and that "کابلی" appears nowhere.
- **If the owner really wants a different spelling, change `slogan_urdu` in `site.json`, add any new letters to the font `text=` list in `src/partials/head.html`, and rebuild.**

**Placement:** the slogans appear in the hero and the footer only. They aren't repeated in every section; the tests cap it at 2 occurrences per page. The existing Urdu top-strip line ("قابلِ اعتماد رشتہ سروس — فیصل آباد", from v1) is kept unchanged. No Urdu-script version of "Family aur Aapki Pasand" was invented.

## 8. Design System

Tokens in `styles.css :root`:
- **Colour:** primary wine `#5B1A33` (+ hover and deep), champagne gold (accent / strong / soft), cream secondary, background, surface, text primary/secondary, borders, success/warning/error, **WhatsApp green + ink/deep/soft (new tokens)**.
- **Type:** Fraunces display, Work Sans body, Noto Nastaliq Urdu, fluid clamp scale.
- **Space:** section, gutter.
- **Radius:** 10/16/24/pill.
- **Shadow:** 2 levels plus a focus ring.
- **Motion:** 160/280/640ms, one easing curve.
- **Z-index scale:** float 90, header 100, popover 120, modal 200.

Components: buttons (primary/secondary/gold/ghost/WhatsApp), cards (proposal, benefit, news, office, aside), inputs with error/valid states, tags/badges, modal, popover, stepper, fee panel.

**CSS audit:**
- **9 `!important`:** all intentional (`[hidden]`, reduced-motion, reveal fallback).
- **Hard-coded hex values:** the only remaining ones are decorative cover-art gradients.
- **No inline styles:** 0 inline `style=` attributes, which the CSP enforces.
- **One breakpoint scale:** 1080/900/640/360.
- **Unused CSS:** the dead flip-card and package CSS was removed in v4.

## 9. Header

- **Desktop:** logo + "Rishta Trust / Matrimonial Consultancy" · Home, About, How It Works, Find a Match, Success Stories, News · WhatsApp icon + **Register** (primary).
- **Behaviour:** sticky; transparent at the top, then a blurred solid surface with a shadow after scrolling. No height change.
- **Mobile:** hamburger opens an animated drawer with all pages plus FAQs and Contact, "Register — PKR 5,000" and WhatsApp. Esc and outside click close it, and focus returns to the toggle (tested).
- **Login is not shown:** there is no authentication (§2), and a dead login link would be a fake feature.

## 10. Homepage

Hero (slogans) → Trust band → How It Works (4 steps: Register, Build your profile, Discover matches, Connect) → 3 benefit cards (Verified Profiles, Privacy & Security, Serious Matchmaking) → Match preview → Success Stories band → News & Insights → Registration CTA (PKR 5,000) → Footer.

The hero has CTAs **Register Now** and **How It Works**, facts (fee, offices, overseas) and the existing photo. It animates in with a fade-up sequence and a gentle image scale.

## 11. Registration

`registration.html`: **Start your matrimonial journey** · fee panel **REGISTRATION FEE / PKR 5,000 / One-time registration** · 5-step onboarding:

**01 Details · 02 Contact · 03 Profile · 04 Review · 05 Send**

Only steps the real system supports are included. Contact verification, payment and account confirmation happen with the consultant, and the page says so. Step 5 states "Your registration is **not complete yet**" and opens WhatsApp with the application. No verification, payment or activation success is ever shown (tested).

## 12. PKR 5,000 Fee

- **One amount, one source:** `site.json → fee.amount`. No competing prices.
- **Payment:** "Paid to your consultant after they confirm your details. Never taken on this website."
- **Tampering:** there is no payment request to tamper with. When online payment is added, the **server must set the amount** and confirm payment status through a verified gateway webhook. Never accept `amount=5000` from the browser.

## 13. Match Discovery

`matches.html` shows the 3 real sample listings from v1. Filters are profile gender, age range and a text search over city, education and profession, with a live result count and an empty state. Marital status isn't a filter because every listing is "Single". No names, photos, phones or emails are shown (tested).

**Not possible without a backend:** a real profile database, authorised visibility, photos.

## 14. Profile Pages

`profile-rt-*.html` (3 pages): header with a photo placeholder, basic information, education and profession, and a "private details shared only with both families' consent" block. The verification note makes no "Verified" badge claim (tested). Actions: **Ask about this profile** (WhatsApp) and **Report this profile** (email with the ID, tested). Only the public listing ID appears in the URL.

## 15. News

- **`news.html`:** an editorial header ("News & Insights" / "Thoughtful guidance for *meaningful relationships.*" / "Guidance, relationship insights and updates from our team."), CSS arch artwork and a subtle entrance.
- **List:** category chips, a large featured card and article cards, each with cover art, category, date, read time, title, excerpt and "Read article".
- **Articles** (`news-*.html`): title, category, date, cover, content, registration CTA, share controls and 3 related articles, with `Article` metadata.
- **Content:** the 4 articles are based only on facts from the site. They have **no author** (none was given) and **need client review before launch**. No CMS exists.

## 16. Success Stories

There are no real, approved testimonials, so the page shows an honest "No stories published yet" empty state with ways to share a story, and the homepage band explains the consent policy. No fake couples or statistics (tested).

## 17. FAQ

`faq.html`: 14 questions in 4 accessible accordion groups. They cover the fee, how registration works, online payment (not available), profile protection, photos, verification, overseas families, guarantees, how to report a profile and how to contact support. Every answer is based on existing site or Terms content.

## 18. Contact

- **`contact.html`:** real contacts only (2 offices, WhatsApp, 2 emails, addresses, maps).
- **Form:** name, phone, optional email, office, message.
- **States:** validation → confirmation dialog offering WhatsApp or email (tested). There's no "loading" or server "error" state, because nothing is sent to a server.
- **Abuse protection:** not applicable without a server. A server version must add rate limiting or a CAPTCHA.

## 19. WhatsApp

A floating button, bottom-right on every page. It uses the configured head-office number from `site.json` (tested). Tooltip "Chat with us", subtle entrance and hover, no pulse. It shares one fixed stack with Help and back-to-top, so the buttons can't overlap (tested at all widths). The site has no cookie banner or other widgets.

## 20. Help Widget

Popover "How can we help?" with FAQs, Contact support, WhatsApp and Report a problem. Every option leads to a real destination. It is keyboard accessible, moves focus inside, closes with Esc (focus returns), and can also be opened from the footer "Help" link. Tested at 375px.

## 21. Footer

- **Top band:** a CTA ("One registration. One fee.") on inner pages.
- **Brand block:** logo, **Family aur Aapki Pasand**, **قابلِ اعتماد طریقے سے** and a short description.
- **Columns:** Company (About, How It Works, Find a Match, Success Stories, News) · Support (Registration, FAQ, Contact, Help) · Legal (Privacy, Terms, Safety) · Connect (both offices' WhatsApp and email). No social links, because none are configured.
- **Bottom line:** © year + fee.
- **Phones (fixed):** Connect spans the full width and contact details no longer break mid-word.

## 22. Animations

- **Hero:** fade/fade-up sequence and a gentle image scale.
- **Sections:** scroll reveal (runs once).
- **Timelines:** How It Works drawing once.
- **Hovers:** card lift, button micro-interactions.
- **Registration:** step slide.
- **Page transitions:** fade + translateY via View Transitions, 180/320ms, never blocking navigation.
- **Accessibility and robustness:** everything is disabled under `prefers-reduced-motion`. Content stays visible if the script fails.

## 23. Responsive QA

All 20 pages × 9 widths (320–1920) were checked for overflow, floating-button overlap and in-view position, and text of at least 12px: **540/540 pass**.

Screenshots were reviewed at 1440, 1280, 390 and 320. Two notes:
- The new hero was checked at 1440, 390 and 320.
- Direct headless captures narrower than about 500px are cropped by Chrome's minimum window size, so phone screenshots were taken through a true-width iframe instead.

## 24. Accessibility

**Tested:** one `h1` per page; every control has a label or accessible name; ARIA references resolve; no duplicate IDs; modals keep focus inside (trap and restore, background `inert`); Esc closes the nav, Help and modals; keyboard access in the stepper; `aria-invalid` and linked error messages; `aria-current` on the nav and stepper; skip link; visible focus rings; language attributes (`lang="ur"`, `lang="ur-Latn"`); reduced motion.

**Not tested:** an automated contrast audit (colour pairs were chosen for 4.5:1 body text), and real screen-reader sessions.

## 25. Security Audit

| Check | Result |
| --- | --- |
| Authentication / authorization / sessions / cookies / tokens | Not present. Nothing to review, and nothing trusted from the browser. |
| Input validation / output encoding / XSS | Validated in the browser. User input is written with `textContent` / `encodeURIComponent` only. XSS payload test passes. The build escapes all JSON data. |
| CSP | `script-src 'self'`, no inline script or style. **0 violations on 20 pages.** |
| IDOR / private profiles | No private data exists. Listings expose no contact data (tested). |
| Payment manipulation | No payment endpoint. Server-side amount rules are documented for the future (§12). |
| Registration / OTP abuse, rate limiting, CSRF | Not applicable (no server, no OTP). **Required** when a backend is added. |
| File uploads | None. |
| Secrets / environment variables / logs | None exist; no logging. |
| Error messages | User-friendly inline messages only. There are no backend errors to leak. |
| Unsafe redirects | None. All external links are fixed and use `rel=noopener`. |
| Sensitive data in URLs | Registration details travel inside the `wa.me` link to WhatsApp. This is the mechanism the original site used; the data is minimised (no CNIC, DOB, address or photo). Documented risk: browser history. |
| Hosting headers | HSTS, `X-Content-Type-Options` and `frame-ancestors` must be set on the host. |

No obvious issue was found, but **security is not "complete"**. It must be re-audited once any backend, login or payment exists.

## 26. SEO

- **Every page:** unique title and description, OG + Twitter tags, one semantic `h1` (all tested).
- **Home:** the title now carries the slogan, plus `Organization`/office JSON-LD.
- **Articles:** `Article` JSON-LD and `article:published_time`.
- **Also:** `robots.txt`; the share image was re-rendered with both slogans.
- **Canonical URLs and sitemap:** generated automatically once `base_url` is set in `site.json`. **Not yet set** (domain unknown).
- **No fake reviews, ratings or FAQ schema.**

## 27. Performance

- No dependencies. `script.js` 22.9 KB, `styles.css` 82.1 KB (unminified).
- The Urdu font is subset to the glyphs in use; the new slogan needed no new glyphs.
- One raster photo with fixed dimensions and high priority. Maps load lazily. Only transform and opacity are animated.
- **Remaining:** compress `hero-bg.jpg` (346 KB) and `og-image.png` (626 KB).

## 28. Tests

The project has no lint, typecheck, unit tests or E2E suite, and the only build step is `python src/build.py`, so those tools couldn't be run. What was run:
1. `python src/build.py`, where any unknown template token fails the build.
2. A headless Chrome 153 browser harness against a local server: static, functional and layout suites.
3. Chrome console/CSP log capture on all pages.
4. A codepoint comparison of the Urdu slogan against the v1 original.
5. Screenshot review.

## 29. Exact Test Results

```
Baseline (v4, before changes):  FAILS=0 TOTAL=949

python src/build.py
→ Built 20 pages (base_url not set: no canonical URLs or sitemap)

Urdu slogan codepoints vs v1 original:
  0642 0627 0628 0644 0650 0020 0627 0639 062A 0645 0627 062F 0020 0637 0631 06CC 0642 06D2 0020 0633 06D2
  → built hero matches original: True

Harness, final run (after all changes):  FAILS=0 TOTAL=1013
  static      421  (all v4 checks on 20 pages, plus per page: "کابلی" absent, footer shows both
                    slogans, slogan not repeated more than twice)
  functional   52  (all v4 flows, plus: home H1 = "Family aur Aapki Pasand" with lang=ur-Latn,
                    Urdu slogan codepoint-identical to the approved text, rendered in Nastaliq,
                    slogan in the home <title>)
  layout      540  (20 pages × 9 widths)

Console/CSP (20 pages): 0 errors, 0 CSP violations
  (only Google Maps' own log inside its embed on about.html and contact.html)
```

Found and fixed during this round: the footer Connect column breaking contact details on phones, and a harness declaration bug (in the test code, not the site).

**Not tested:** Login, Signup, Logout, profile creation and payment (none exist), real devices, Safari, Firefox, screen readers.

| Function | Result |
| --- | --- |
| Home, navigation, mobile menu | PASS (automated) |
| Registration flow (browser part) | PASS (automated) |
| Match search, filters, profile details | PASS (automated) |
| Contact, News, article, FAQ, WhatsApp, Help | PASS (automated) |
| Login / Signup / Logout / authenticated areas | NOT IMPLEMENTED |
| Profile creation (account-based) | NOT IMPLEMENTED (done offline by a consultant) |
| Payment | NOT IMPLEMENTED |

## 30. Remaining Issues

1. **Confirm the Urdu slogan spelling** (قابلِ, used here, vs "کابلی" in the brief).
2. **Terms §4** conflicts with the single fee.
3. **Free registration for deserving families:** keep or remove?
4. **Confirm what the PKR 5,000 includes**, including verification.
5. **Hero photo licence.** The brief forbids unlicensed photos, and the rights to `hero-bg.jpg` are unknown. Confirm them, or replace it before launch.
6. **Confirm the sample listings are current.**
7. **Review the 4 articles.**
8. **Privacy policy** mentions cookies/analytics the site doesn't use and omits Google Fonts/Maps.
9. **Deployment:** set `base_url`; configure the 404 page and security headers on the host; don't upload `src/`, the reports, `README.md` or `24 sep file.zip`.
10. **Compress** the two large images.
11. **Backend project (not faked):** accounts (login/signup/logout), online payment with a server-set amount, OTP, a profile database with server-side authorization, rate limiting and CSRF protection.

## 31. Production Readiness

| Area | Status |
| --- | --- |
| Owner slogans (exact approved Urdu) | ✅ Tested. Spelling to be confirmed by the owner |
| PKR 5,000 single fee; old fee cards gone | ✅ Tested |
| Multi-page structure, header, footer, links | ✅ Tested |
| Registration (browser → WhatsApp hand-off) | ✅ Tested. No payment or OTP (don't exist) |
| Matches, profiles, news, stories, FAQ, contact, safety | ✅ Tested |
| Responsive 320–1920 (Chromium) | ✅ Tested |
| Accessibility basics | ✅ Tested (no contrast tool or screen-reader session) |
| Client-side security | ✅ Tested. Server security needs a future audit |
| Safari / Firefox / real phones | ❌ Not tested |
| Login, payment, OTP, profile DB | ❌ Not implemented; not simulated |
| Canonical / sitemap | ⚠️ Needs domain |
| Content and legal sign-off (§30 items 1–8) | ⚠️ Needs owner |

**Ready for staging and client review.** Production launch depends on the owner items above, the deployment settings, and a check on a real phone and in Safari.
