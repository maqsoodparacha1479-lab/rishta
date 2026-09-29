# Rishta Trust — Matrimonial Consultancy Website

A static, multi-page website for a confidential, family-focused matchmaking consultancy in Faisalabad & Khanpur, Pakistan. The published site is plain HTML/CSS/JS: upload the root files to any static host.

## Editing the site
Pages are generated from `src/`. **Edit files in `src/`, then run:**

```
python src/build.py
```

Python 3.8+ with the standard library only. Don't edit the generated `.html` files in the project root; the next build overwrites them.

| Path | What it holds |
| --- | --- |
| `src/data/site.json` | Offices, WhatsApp numbers, emails, **registration fee**, main navigation, news categories, `base_url` |
| `src/data/proposals.json` | The sample proposal listings (generates Find a Match cards and `profile-*.html`) |
| `src/pages/*.html` | One file per page. A `<!--meta {...} -->` header sets title, description and the active nav item |
| `src/articles/*.html` | News articles (generates `news-<slug>.html`, the News list and related articles) |
| `src/partials/` | Shared head, icon sprite, header, footer, WhatsApp/Help widgets |
| `src/data/images.json` | Image registry used by `{{img:key}}` and article `"image"`. `status: "demo"` marks replaceable placeholders |
| `src/illustrations.py` | Regenerates the demo SVG illustrations in `assets/illustrations/` (`python src/illustrations.py`) |
| `styles.css`, `script.js` | Edited directly (not generated) |

Templates use `{{…}}` tokens, e.g. `{{fee.amount}}`, `{{wa:khanpur:Message}}`, `{{icon:shield}}`, `{{offices:cards}}`. See `render()` in `src/build.py`.

## Changing the fee, slogans or a phone number
Edit `src/data/site.json` (`fee`, `slogan`, `slogan_urdu`, `offices`) and rebuild. If you change Urdu text, add any new letters to the `text=` list of the Urdu font link in `src/partials/head.html`. Every page, the registration flow and the WhatsApp links update together.

## How registration and contact work
There is no server, database or payment gateway. The registration form (5 steps) and contact form validate in the browser, then open **WhatsApp with the details pre-filled** for the chosen consultant. Nothing is stored by the website, and **no payment is taken online**: the consultant confirms the details and collects the PKR 5,000 fee with an official receipt.

## Before going live
- Set `base_url` in `src/data/site.json` and rebuild. This adds canonical URLs, absolute social-image URLs and `sitemap.xml`.
- Configure the host to serve `404.html` for missing pages and to set security headers (HSTS, `X-Content-Type-Options`, `frame-ancestors`).
- Confirm usage rights for `assets/hero-bg.jpg` and that the sample proposals are current.
- Review the Terms & Conditions fee section (it still mentions a consultancy advance and final balance).
