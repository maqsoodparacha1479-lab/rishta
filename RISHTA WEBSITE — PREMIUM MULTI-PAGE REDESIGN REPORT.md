# RISHTA WEBSITE — PREMIUM MULTI-PAGE REDESIGN REPORT

**Date:** 25 September 2026
**Project:** `C:\Users\Hp\Downloads\rishta`
**Backups:** `rishta-backup-2026-09-24` (original site), `rishta-backup-v3-2026-09-24` (previous redesign, before this work)

**Verdict in one line:** the site is ready for staging and client review. It is not ready for production launch until the items in §25 are resolved. Online payment, OTP verification, login and a profile database do not exist and were not faked.

---

## 1. Existing System Audit

| Area | Finding |
| --- | --- |
| Framework | Static HTML + one CSS file + one vanilla JS file. No framework, package manager, git, tests or build. |
| Routes / pages | `index.html`, `news.html`, 4 `news-*.html`, `privacy.html`, `terms.html` (the v3 redesign). |
| Backend / API / database | **None.** |
| Authentication / login / signup / logout | **None.** No accounts exist. |
| Registration flow | None. Only a callback form and a quick-inquiry form, both handing off to WhatsApp. |
| Payment integration | **None.** No Stripe, JazzCash, Easypaisa or other gateway, keys or code. |
| Admin | None. |
| News / blog | 4 static article pages (no CMS). |
| Assets | `assets/hero-bg.jpg` (usage rights unknown), `assets/og-image.png`. |
| Security controls | CSP `<meta>` on every page, `rel=noopener`, DOM-built WhatsApp links (no `innerHTML` of user input), referrer policy. |
| Responsive | Previously tested at 320–1920px with no overflow. |
| Extra file | `24 sep file.zip` in the project root is a snapshot of the v3 build. It was left untouched and **should not be uploaded** to the host. |

Because there is no backend, the brief's server-side items (payment verification, OTP, authorization, IDOR, rate limiting, duplicate-account detection) have **nothing to verify or connect to**. §20 covers this in detail.

## 2. Previous UI/CSS Problems Found

- **Multiple fee cards** (Basic Rs 2,000–3,000 / Premium 5,000–10,000 / Executive 15,000–30,000+), plus a "Registration category" dropdown and package references in the FAQ and one article. All of these conflict with the single PKR 5,000 fee.
- **Three 3D flip cards.** No longer required, and their JS/CSS were the most complex part of the page.
- **Single long page.** Every topic sat on `index.html`, with anchors instead of real pages.
- **Duplicated chrome.** Header, footer and widgets were copied by hand into every HTML file, so they drift as soon as pages multiply.
- The WhatsApp button had a pulse animation (finite, but not wanted).
- No damaged CSS found. The v3 stylesheet passed all layout tests, so it was **kept and extended**, not rewritten. Only the flip-card, package, quick-inquiry and pulse rules were removed (~9 KB).

## 3. Fee Card Removal

Removed from the public UI:
- Package cards and the "deserving" banner from the homepage.
- The package "Select" buttons and their preselect JS.
- The "Registration category" dropdown and its options.
- Package mentions in the FAQ and the verification article.
- Their CSS: `.package*`, `.deserving*`.

There was no backend or payment logic tied to the packages, so nothing server-side needed preserving.

**Automated check (every page):** no `.package` / `.flip-card` elements, and no text matching Basic/Premium/Executive/Gold/Silver + package/plan/tier, "Rs. <number>", "monthly" or "per month". Passes on all 20 pages.

**Not changed (legal text):** `terms.html` §4 "Fees & Payment" still lists a "Consultancy Advance… Final balance due at Nikah or Rukhsati". This contradicts a single one-time fee. It's the client's legal text, so it was **flagged, not rewritten** (see §25).

## 4. Registration Page

`registration.html`:
- **Hero:** "Start your matrimonial journey" and "Create your profile and take the first step towards finding a meaningful match."
- **Fee panel:** REGISTRATION FEE · **PKR 5,000** · One-time registration · "Paid to your consultant after they confirm your details. Never taken on this website." One amount only. No discounts, badges or comparisons.
- **What's included:** only services the site already describes. Registration sitting, profile screening, private-database matching, consent-based sharing, family introductions and follow-up, and an official receipt. Verification is described as "available with your authorization", because whether it's included in the fee is unconfirmed.
- **How payment works:** the site takes no payments. The consultant explains the options and issues a receipt. "We will never ask for card details, OTP codes or passwords."
- **Form:** 5 steps (see §5), with consent in step 4.

## 5. PKR 5,000 Registration Flow

Progress indicator: **01 Details · 02 Contact · 03 Profile · 04 Review · 05 Send**

| Step | Fields / behaviour |
| --- | --- |
| 1 Details | Candidate's name, registering for, gender, age (18–70), marital status, city/country |
| 2 Contact | WhatsApp/mobile (validated), email (optional, validated if given), preferred consultant |
| 3 Profile | Education, profession, about (optional, max 400 characters, warns against including CNIC) |
| 4 Review | Summary of every answer, fee line (PKR 5,000 one-time), required consent checkbox linking Terms and Privacy |
| 5 Send | "Your registration is **not complete yet**." Opens WhatsApp to the chosen consultant with everything pre-filled, then lists what happens next |

- **Can't skip steps:** each step validates before advancing. Enter key advances instead of submitting early.
- **Other states:** Back keeps entered values, and "Edit my details" returns to step 1. Errors appear inline with `aria-invalid`, and focus moves to the first invalid field.
- **Data minimisation:** age instead of date of birth. No CNIC, address, photo or password fields.

**What this flow is honestly not:**
- There is **no OTP / contact verification**. The number is confirmed when the consultant contacts the family.
- There is **no online payment and no payment success state**.
- There is **no duplicate-account state** (no accounts exist).
- There are **no server error or retry states** (no server exists).

All of these need a backend (see §25).

## 6. Pages Created

20 generated pages, each with a unique title and meta description, Open Graph/Twitter tags, the shared header, footer, WhatsApp and Help widgets, page transitions and responsive layout:

| Page | File | Status |
| --- | --- | --- |
| Home | `index.html` | Rebuilt |
| About Us | `about.html` | New |
| How It Works | `how-it-works.html` | New |
| Find a Match | `matches.html` | New |
| Profile detail ×3 | `profile-rt-23840.html`, `-17146`, `-23693` | New |
| Registration | `registration.html` | New |
| Success Stories | `success-stories.html` | New (empty state) |
| News | `news.html` | Rebuilt |
| News articles ×4 | `news-*.html` | Migrated and corrected |
| FAQ | `faq.html` | New (was a homepage section) |
| Contact | `contact.html` | New |
| Privacy Policy | `privacy.html` | Legal text unchanged |
| Terms & Conditions | `terms.html` | Legal text unchanged |
| Safety / Security | `safety.html` | New |
| Error | `404.html` | New |

**Architecture change:** pages are generated by `src/build.py` (Python standard library only) from `src/data`, `src/pages`, `src/articles` and `src/partials`. The header, footer, widgets, fee and phone numbers now have one source each. Output is plain static HTML, so hosting doesn't change. URLs are flat `.html` files; most static hosts also serve them without the extension (`/registration`).

**Loading and error states:** pages are static, so there's no loading state to show. Dynamic parts have empty states (match filters, news filters, success stories) and validation/error states (forms). `404.html` is the site-level error page.

## 7. Header

- **Desktop:** logo + brand · Home, About, How It Works, Find a Match, Success Stories, News · WhatsApp icon + a prominent **Register** button.
- **Mobile:** logo + hamburger. An animated drawer lists all 6 pages plus FAQs and Contact, then "Register — PKR 5,000" and "Chat on WhatsApp".
- **Behaviour:** sticky; transparent at the top, then a solid blurred surface with a shadow after 8px of scroll (280ms). Height never changes, so there's no layout shift.
- **Accessibility:** Esc, outside click and link click close the drawer, and focus returns to the toggle. `aria-expanded` and `aria-current="page"` are set.
- **Login is not shown**, because there is no authentication to log in to.

## 8. Homepage

Order, as specified: Hero → Trust band (4 commitments) → How It Works (4 steps) → **three benefit cards** (Verified Profiles, Privacy & Security, Serious Matchmaking; static cards with a subtle hover, no 3D) → Match preview (3 sample listings) → Success Stories band (no testimonials, see §12) → News (featured + 2) → Registration CTA with the PKR 5,000 fee panel → footer.

The hero reads "Find a meaningful match. *Begin a meaningful journey.*" with **Register Now** and **How It Works** buttons, a "One-time fee: PKR 5,000" fact, and the existing hero photo.

## 9. Matches

`matches.html` shows the **3 existing sample listings** (there is no profile database). Filters cover only real fields: profile gender, age from/to, and a text search over city, education and profession. A live "Showing X of 3" count is announced to screen readers. An empty state offers "Clear filters" and "Register". Listings never show a name, photo, phone or email (tested). A banner states that registered families receive proposals directly from their consultant.

## 10. Profiles

Each `profile-*.html` page has:
- a header with a photo placeholder (photos are never published)
- Basic information
- Education & profession
- an "About, preferences & photo" block explaining that these are shared privately with both families' consent
- a Verification note: screening applies to every profile, and document checks are consent-based ("ask your consultant"). **No "Verified" badge.**
- **Ask about this profile** (WhatsApp with the ID)
- **Report this profile** (email to the head office with the ID in the subject)

The URL contains only the public listing ID.

**Not possible without a backend:** authorization rules, private fields per viewer, and IDOR protection. All published data is already public-safe by design.

## 11. News

- **`news.html`:** an editorial header (NEWS & INSIGHTS / "Thoughtful guidance for *meaningful relationships.*" / "Guidance, relationship insights and updates from our team.") with CSS-drawn arch artwork. No stock photos, so there are no image-rights questions.
- **List:** category chips, a featured article and a card grid. Each card has category, date, read time, title, excerpt and cover art.
- **Articles:** title, category, date, cover, body, a "Ready to begin?" registration card, share controls (WhatsApp, copy link, native share) and 3 related articles.
- **Content:** the 4 articles were written earlier from facts on the site. This round removed their package references and added the PKR 5,000 fee. They are dated 24 Sep 2026 and have no author byline, because no real author was given. **The client should review them before launch.**

## 12. Success Stories

There are no real testimonials, so **none are published**. The page shows "No stories published yet … this page stays empty rather than showing invented ones", followed by cards for sharing a story (via a consultant), privacy, and registering. The homepage band says the same. Tested: no `<blockquote>` testimonials anywhere.

## 13. FAQ

`faq.html` groups 14 questions under Registration & fee, Privacy & safety, Matching and Support, with a topic menu and accordions. Every answer restates what the site and Terms already say, including:
- the PKR 5,000 one-time fee
- "Can I pay online? No."
- that the form stores nothing
- how to report a profile

The existing free-registration policy for deserving families is mentioned once, as a question (see §25).

## 14. Contact

`contact.html` has:
- **A form:** name, phone/WhatsApp, optional email, office, message. It validates with inline errors, then opens a confirmation dialog offering **WhatsApp** or **email** to the chosen office.
- **A sidebar:** WhatsApp chooser, both real office emails, and a "report a concern" link.
- **Office cards:** both offices, with consultant, address, phones, email, directions and a map.

**Spam protection:** none is needed, because nothing is submitted to a server. A server-side form would need rate limiting or a CAPTCHA.

## 15. Footer

- **CTA band:** "One registration. One fee. A consultant who knows your family." with Register — PKR 5,000 and Contact us. It's hidden on Home and Registration, which have their own CTA.
- **Columns:**
  - Brand
  - **Company:** About, How It Works, Find a Match, Success Stories, News
  - **Support:** Registration, FAQ, Contact, Help (opens the Help widget)
  - **Legal:** Privacy Policy, Terms & Conditions, Safety
  - **Connect:** both offices' WhatsApp and email
- **Social links:** none, because none are configured.
- **Bottom line:** "© 2026 Rishta Trust" (the year is set at build time) and the fee.

## 16. WhatsApp

A floating button, bottom-right, on every page. It uses the **existing configured head-office number** (923230785312) from `site.json` (tested). The tooltip reads "Chat with us", the entrance is subtle and hover lifts it slightly. **The pulse animation was removed.** All WhatsApp links across the site come from `site.json`.

## 17. Help Widget

The Help button opens a popover with:
- **FAQs** → `faq.html`
- **Contact support** → `contact.html`
- **WhatsApp** → consultant chooser
- **Report a problem** → email the head office

Every option leads to a real channel. The popover moves focus inside and closes on Esc (focus returns), outside click or focus leaving. The footer "Help" link opens it too. It sits in the same fixed stack as WhatsApp and back-to-top, so the buttons can't overlap, and it respects the safe area. Tested at 375px.

## 18. Animations

- **Hero:** staggered entrance (eyebrow → heading → text → CTAs), and the image scales in.
- **Scroll reveal:** runs once, with IntersectionObserver.
- **Timelines:** How It Works steps and the timeline line draw once.
- **Registration:** steps slide in (≈640ms, transform/opacity only).
- **Hovers:** subtle lift on cards, benefit icons and news covers.
- **Page transitions:** cross-document View Transitions (fade-out 180ms, fade-up 320ms). They never delay navigation, and unsupported browsers navigate normally.
- **Accessibility and robustness:** everything is disabled under `prefers-reduced-motion`. Content can't stay hidden if the script fails, because the script adds the `reveal-ready` class that hides it.

## 19. Responsive QA

- **Automated:** 20 pages × 9 widths (**320, 375, 390, 414, 768, 1024, 1280, 1440, 1920**) = 180 page loads. Each checks for horizontal overflow, elements escaping the viewport, floating-button overlap, floating buttons staying in view, and text under 12px. **540/540 pass.**
- **Visual review by screenshot:** Home (1440, 390), Registration (hero, review step, mobile send step), News, Matches, Profile, How It Works, Success Stories, Footer.

## 20. Security Review

| Item | Status |
| --- | --- |
| XSS | User input goes into the review summary and WhatsApp/email links via `textContent`/`encodeURIComponent` only. Tested with `<img src=x onerror=…>` as a name: rendered as text. The build HTML-escapes all data from JSON, and the embedded config JSON escapes `</`. |
| CSP | `script-src 'self'`, no inline scripts or styles, `object-src 'none'`, `base-uri 'self'`. **0 violations on all 20 pages** (Chrome console log). |
| Secrets / API keys | None exist. Only the business's published numbers and emails. |
| Fee tampering | **Not possible:** there is no payment endpoint. PKR 5,000 is display text; the consultant quotes and collects the fee offline. If online payment is added, the server must set the amount itself and ignore any client value. |
| Client-side roles / payment status / auth | None exist, so nothing is trusted from the browser. |
| Private profile exposure / IDOR | Only 3 public sample listings. No names, photos or contacts anywhere (tested). |
| Sensitive data in URLs | Registration details travel inside the `wa.me` / `mailto:` link to WhatsApp or the mail app. **This is the same mechanism the original site used.** The data stays on the user's device until they press send, but it can end up in browser history. Minimised: no CNIC, DOB, address or photo. |
| localStorage | Not used. No drafts of personal data are stored. |
| Logging | The site has no logging. |
| CSRF / rate limiting / OTP abuse / file upload | Not applicable: no server and no uploads. **Required** once a backend exists. |
| Unsafe redirects | None. All external links are fixed `wa.me`, `mailto:`, `tel:` or Google Maps URLs, with `rel=noopener`. |
| Headers | HSTS, `X-Content-Type-Options` and `frame-ancestors` must be set by the host. |

## 21. SEO

- **Every page:** a unique title, a meta description over 40 characters, and Open Graph plus Twitter card tags (tested). Exactly one `h1` per page (tested). Semantic sections, breadcrumbs and `robots.txt`.
- **Articles:** `og:type=article`, `article:published_time`, and `Article` JSON-LD with no author.
- **Home:** `Organization` plus 2 office `ProfessionalService` entries. No reviews, ratings or FAQ schema.
- **Share image:** the 1200×630 image was re-rendered with the new messaging.
- **Not done yet:** canonical URLs, absolute OG URLs and `sitemap.xml` need the live domain. **Set `base_url` in `src/data/site.json` and rebuild**; the builder then emits all three.

## 22. Performance

- **No libraries or dependencies.** `script.js` is 22.9 KB and `styles.css` 81.3 KB, both unminified.
- The Urdu font is subset to its 26 used glyphs. Only one photo is used (explicit dimensions, `fetchpriority=high`). All other artwork is CSS, and maps load lazily.
- Only transform and opacity are animated. Scroll handling is passive and batched with requestAnimationFrame.
- **Remaining:** `hero-bg.jpg` (346 KB) and `og-image.png` (≈640 KB) should be compressed to WebP/JPEG. CSS/JS minification is optional.

## 23. Tests

The project has **no** lint, typecheck, unit tests, E2E suite or build of its own, so none could be run. What was run:
1. `python src/build.py`: the build succeeds and every template token resolves (unknown tokens fail the build).
2. A same-origin browser harness (headless Chrome 153 against a local Python server) covering static, functional and layout checks.
3. A Chrome console/CSP log capture on every page.
4. Screenshot review (see §19).

## 24. Exact Test Results

```
python src/build.py
→ Built 20 pages (base_url not set: no canonical URLs or sitemap)

harness.html (headless Chrome 153.0.8010.53), final run:
→ FAILS=0 TOTAL=949
     static      361  (h1, meta/OG, images+alt, icon references, CSP-safe markup, labels,
                       accessible names, noopener, duplicate ids, ARIA refs, no multi-plan pricing,
                       no fee/flip cards, PKR 5,000 present, nav order, Register CTA, widgets,
                       internal links + anchors on all 20 pages)
     functional   48  (mobile nav, help widget, footer Help, WhatsApp modal + focus/inert,
                       3 benefit cards, WhatsApp number + tooltip, registration: one fee,
                       stepper, no skipping, age < 18, Enter key, bad phone/email, optional
                       email, Back keeps values, summary, XSS, consent required, routing to the
                       chosen office, message content, no fake success, edit; contact form;
                       match filters + empty state + no contact data; profile report link,
                       no "verified" badge; stories empty state; news filter; reveal; header)
     layout      540  (20 pages × 9 widths × {overflow, FAB overlap/in-view, text ≥ 12px})

Console/CSP capture (all 20 pages): 0 errors, 0 CSP violations. The only output is
Google Maps' own log inside its embed on about.html and contact.html.
```

Issues found and fixed during QA:
- The fee amount rendered at body size on the Registration hero (a specificity clash with `.page-hero p`).
- The quote icon was missing from the sprite (the icon-reference check was added to the suite).
- Two unverifiable promises ("we review every report", "we will review it") were softened.
- The share image text was updated to the new messaging.
- The footer had an orphaned column at tablet width.

**Not tested:** real Android or iOS devices, Safari, Firefox; login/signup/logout (they don't exist); payment (it doesn't exist); how the WhatsApp app itself receives the message.

## 25. Remaining Issues

**Business decisions needed:**
1. **Terms & Conditions §4** conflicts with the single fee (consultancy advance and final balance). The client or their lawyer needs to update it.
2. **Free registration for deserving families** is an existing policy in the Terms, the FAQ and one article. Keep it or remove it?
3. **Confirm what the PKR 5,000 includes**, especially whether verification is included.
4. **Hero photo rights:** `assets/hero-bg.jpg` looks like a stock or social-media image. Confirm the licence or replace it.
5. **Proposal listings** RT-23840, RT-17146, RT-23693: confirm they're real and current.
6. **Articles:** review the 4 articles before publishing.
7. **Privacy policy:** it mentions cookies and analytics the site doesn't use, and doesn't mention Google Fonts or Maps.

**Deployment:**
8. Set `base_url` and rebuild (canonical, sitemap, absolute OG).
9. Configure the host's 404 page and security headers. `404.html` uses relative asset paths, so it renders correctly only for top-level URLs.
10. Don't upload `src/`, `README.md`, this report or `24 sep file.zip`.
11. Compress the two large images.

**Needs a backend (out of scope; nothing faked):**
12. Online payment, OTP contact verification, accounts (login/signup/logout), a real profile database with authorization, and server-side storage of registrations. Each needs its own security design:
    - the server sets the fee
    - webhook-verified payment status
    - rate limiting
    - CSRF protection
    - authorization on every profile request

## 26. Production Readiness

| Area | Status |
| --- | --- |
| Single PKR 5,000 fee, old fee cards removed | ✅ Tested |
| Multi-page structure, header, footer, navigation, links | ✅ Tested |
| Registration flow (details → WhatsApp hand-off) | ✅ Tested. No payment or OTP (don't exist) |
| Contact, matches, profiles, news, FAQ, safety, stories | ✅ Tested |
| Responsive 320–1920px (Chromium) | ✅ Tested |
| Accessibility basics (keyboard, focus, labels, ARIA, reduced motion) | ✅ Tested (no automated contrast audit) |
| Client-side security (XSS, CSP, no secrets, no private data) | ✅ Tested |
| Safari / Firefox / real phones | ❌ Not tested |
| Online payment, OTP, login | ❌ Not implemented (no backend); not faked |
| Canonical / sitemap | ⚠️ Needs domain |
| Legal and content sign-off (§25 items 1–7) | ⚠️ Needs client |

**Ready for staging and client review.** Ready for production once the §25 business items (1–7) and deployment items (8–11) are done and the site has been checked on a real phone and in Safari. Online payment and accounts are a separate backend project.
