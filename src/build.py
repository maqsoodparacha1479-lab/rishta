#!/usr/bin/env python3
"""Rishta Trust static site builder.

Usage:  python src/build.py          (Python 3.8+, standard library only)

Reads src/ (data, partials, pages, articles) and writes finished static HTML
to the project root. The output needs no server-side code; edit files in src/
and re-run this script instead of editing the generated .html files.
"""
import datetime
import html
import json
import pathlib
import re
import urllib.parse

SRC = pathlib.Path(__file__).resolve().parent
ROOT = SRC.parent
SITE = json.loads((SRC / "data" / "site.json").read_text("utf-8"))
PROPOSALS = json.loads((SRC / "data" / "proposals.json").read_text("utf-8"))
IMAGES = {k: v for k, v in json.loads((SRC / "data" / "images.json").read_text("utf-8")).items() if not k.startswith("_")}
OFFICES = {o["id"]: o for o in SITE["offices"]}
# Branches with published contact details; "pending" branches are listed by city only
CONTACT_OFFICES = [o for o in SITE["offices"] if not o.get("pending")]
BASE = SITE.get("base_url", "").rstrip("/")
YEAR = str(datetime.date.today().year)

esc = html.escape
TOKEN = re.compile(r"\{\{\s*(.+?)\s*\}\}", re.S)
META = re.compile(r"\A\s*<!--meta\s*(\{.*?\})\s*-->", re.S)


# --------------------------------------------------------------------------- helpers
def ic(name, cls="icon"):
    return f'<svg class="{cls}"><use href="#i-{name}"/></svg>'


def wa_url(office_id, message=None):
    office = OFFICES[office_id]
    text = message if message is not None else office["wa_greeting"]
    return f"https://wa.me/{office['wa']}?text={urllib.parse.quote(text)}"


def human_date(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{d.day} {d.strftime('%b %Y')}"


def current(key, active):
    return ' aria-current="page"' if key == active else ""


def parse(path):
    text = path.read_text("utf-8")
    m = META.match(text)
    if not m:
        raise SystemExit(f"{path}: missing <!--meta {{...}} --> header")
    return json.loads(m.group(1)), text[m.end():].strip("\n")


def load_articles():
    items = []
    for p in sorted((SRC / "articles").glob("*.html")):
        meta, body = parse(p)
        meta["slug"] = p.stem
        meta["file"] = f"news-{p.stem}.html"
        meta["body"] = body
        items.append(meta)
    # newest first, then the featured article pinned to the front (sorts are stable)
    items.sort(key=lambda a: a["date"], reverse=True)
    items.sort(key=lambda a: not a.get("featured", False))
    return items


ARTICLES = load_articles()


def image(key, cls="", decorative=False):
    """<img> from src/data/images.json. Decorative images get alt="" so screen readers skip them."""
    if key not in IMAGES:
        raise SystemExit(f"unknown image key '{key}'")
    im = IMAGES[key]
    attrs = [f'src="{im["src"]}"']
    if im.get("srcset"):
        attrs += [f'srcset="{im["srcset"]}"', f'sizes="{im["sizes"]}"']
    attrs += [f'width="{im["width"]}"', f'height="{im["height"]}"', f'alt="{"" if decorative else esc(im["alt"])}"']
    attrs += ['fetchpriority="high"'] if im.get("eager") else ['loading="lazy"']
    attrs += ['decoding="async"']
    if cls:
        attrs.insert(0, f'class="{cls}"')
    return "<img " + " ".join(attrs) + ">"


def cover(a, extra=""):
    if a.get("image"):
        return f'<div class="cover cover--img{extra}">{image(a["image"], decorative=True)}</div>'
    return f'<div class="cover cover--{a.get("art", "a")}{extra}" aria-hidden="true"><span></span></div>'


# --------------------------------------------------------------------------- components
def news_card(a, featured=False, heading="h3"):
    cat = SITE["news_categories"][a["category"]]
    cls = "news-card news-card--featured" if featured else "news-card"
    return f'''<article class="{cls} reveal" data-category="{a["category"]}">
  {cover(a)}
  <div class="news-card__body">
    <div class="news-card__meta"><span class="tag">{esc(cat)}</span><time datetime="{a["date"]}">{human_date(a["date"])}</time><span>{a["minutes"]} min read</span></div>
    <{heading} class="news-card__title"><a href="{a["file"]}">{esc(a["title"])}</a></{heading}>
    <p class="news-card__excerpt">{esc(a["excerpt"])}</p>
    <span class="link-arrow" aria-hidden="true">Read article {ic("arrow")}</span>
  </div>
</article>'''


def proposal_card(p, heading="h3"):
    return f'''<article class="proposal reveal" data-gender="{esc(p["gender"])}" data-age="{p["age"]}" data-search="{esc((p["location"] + " " + p["family_origin"] + " " + p["education"] + " " + p["profession"]).lower())}">
  <div class="proposal__media">{ic("eye-off")}<span>Photo shared privately on request</span></div>
  <div class="proposal__body">
    <div class="proposal__top"><{heading} class="proposal__id">ID: {esc(p["id"])}</{heading}><span class="tag">{esc(p["tag"])}</span></div>
    <dl class="proposal__facts">
      <dt>Gender</dt><dd>{esc(p["gender"])} ({"Groom" if p["gender"] == "Male" else "Bride"})</dd>
      <dt>Age · Height</dt><dd>{p["age"]} years · {esc(p["height"])}</dd>
      <dt>Education</dt><dd>{esc(p["education"])}</dd>
      <dt>Profession</dt><dd>{esc(p["profession"])}</dd>
      <dt>Family</dt><dd>{esc(p["family_origin"])}</dd>
    </dl>
    <a href="profile-{p["id"].lower()}.html" class="btn btn-secondary btn-block">View profile {ic("arrow", "icon icon--arrow")}</a>
  </div>
</article>'''


def office_card(o):
    phones = " / ".join(f'<a href="tel:{ph["tel"]}">{ph["display"]}</a>' for ph in o["phones"])
    maps_link = "https://www.google.com/maps/search/?api=1&amp;query=" + urllib.parse.quote(o["map_query"])
    embed = "https://www.google.com/maps?q=" + urllib.parse.quote_plus(o["map_query"]) + "&amp;output=embed"
    return f'''<article class="office reveal">
  <div class="office__body">
    <div class="office__top"><h3>{esc(o["city"])}</h3><span class="tag">{esc(o["badge"])}</span></div>
    <div class="office__person"><span class="office__avatar" aria-hidden="true">{o["initials"]}</span><span><small>Consultant</small><strong>{esc(o["consultant"])}</strong></span></div>
    <ul class="office__info">
      <li>{ic("pin")}<span>{esc(o["address"])}</span></li>
      <li>{ic("phone")}<span>{phones}</span></li>
      <li>{ic("mail")}<a href="mailto:{o["email"]}">{o["email"]}</a></li>
    </ul>
    <div class="office__actions">
      <a href="{esc(wa_url(o["id"]))}" target="_blank" rel="noopener" class="btn btn-whatsapp btn-sm">{ic("whatsapp")} WhatsApp</a>
      <a href="{maps_link}" target="_blank" rel="noopener" class="btn btn-secondary btn-sm">{ic("pin")} Directions</a>
    </div>
  </div>
  <div class="office__map"><iframe src="{embed}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Map: {esc(o["city"])} office"></iframe></div>
</article>'''


def pending_card(o):
    head = OFFICES[SITE["default_office"]]
    ask = wa_url(head["id"], f'Assalam-o-Alaikum, I would like to contact your {o["city"]} branch.')
    return f'''<article class="office office--pending reveal">
  <div class="office__body">
    <div class="office__top"><h3>{esc(o["city"])}</h3><span class="tag">{esc(o["badge"])}</span></div>
    <p class="office__pending-note">{ic("clock")}<span>Address and phone details for this branch will be published soon. Our head office can help you in the meantime.</span></p>
    <div class="office__actions"><a href="{esc(ask)}" target="_blank" rel="noopener" class="btn btn-secondary btn-sm">{ic("whatsapp")} Ask the head office</a></div>
  </div>
</article>'''


def branch_list():
    items = "".join(
        f'<li class="branch-list__item{" is-pending" if o.get("pending") else ""}">{ic("pin")}<span>{esc(o["city"])}</span>'
        + ('<small>Details soon</small>' if o.get("pending") else f'<small>{esc(o["badge"].split(" · ")[0])}</small>') + "</li>"
        for o in SITE["offices"])
    return f'<ul class="branch-list" role="list">{items}</ul>'


def nav_desktop(active):
    return "\n".join(
        f'<li><a href="{n["href"]}" class="nav__link"{current(n["key"], active)}>{esc(n["label"])}</a></li>'
        for n in SITE["nav"])


def nav_mobile(active):
    extra = [{"key": "faq", "label": "FAQs", "href": "faq.html"}, {"key": "contact", "label": "Contact", "href": "contact.html"}]
    return "\n".join(
        f'<li><a href="{n["href"]}"{current(n["key"], active)}>{esc(n["label"])} {ic("arrow")}</a></li>'
        for n in SITE["nav"] + extra)


def client_config():
    cfg = {"offices": {o["id"]: {"name": f'{o["consultant"]} ({o["city"]})', "wa": o["wa"], "email": o["email"]} for o in CONTACT_OFFICES},
           "defaultOffice": SITE["default_office"], "fee": SITE["fee"]["amount"]}
    # </ is escaped so the JSON can never close the <script> element early
    return '<script type="application/json" id="site-config">' + json.dumps(cfg).replace("</", "<\\/") + "</script>"


# --------------------------------------------------------------------------- templating
def render(text, ctx, depth=0):
    if depth > 6:
        raise SystemExit("partials nested too deeply")

    def sub(m):
        key = m.group(1)
        kind, _, arg = key.partition(":")
        if kind == "partial":
            return render((SRC / "partials" / arg).read_text("utf-8"), ctx, depth + 1)
        if kind == "wa":
            office, _, message = arg.partition(":")
            return esc(wa_url(office, message or None))
        if kind == "img":
            key, _, cls = arg.partition(":")
            return image(key, cls)
        if kind == "icon":
            return ic(arg)
        if kind == "nav":
            return nav_desktop(ctx.get("nav")) if arg == "desktop" else nav_mobile(ctx.get("nav"))
        if kind == "news":
            if arg == "home":
                return news_card(ARTICLES[0], featured=True) + '\n<div class="news-side" data-reveal-stagger>' + \
                    "\n".join(news_card(a) for a in ARTICLES[1:3]) + "</div>"
            if arg == "all":
                return news_card(ARTICLES[0], featured=True, heading="h2") + "\n" + "\n".join(news_card(a, heading="h2") for a in ARTICLES[1:])
            if arg == "chips":
                chips = ['<button type="button" class="filter-chip" data-filter="all" aria-pressed="true">All</button>']
                chips += [f'<button type="button" class="filter-chip" data-filter="{k}" aria-pressed="false">{esc(v)}</button>'
                          for k, v in SITE["news_categories"].items()]
                return "".join(chips)
        if kind == "proposals":
            items = PROPOSALS if arg == "all" else PROPOSALS[:3]
            return "\n".join(proposal_card(p) for p in items)
        if kind == "offices":
            if arg == "cards":
                return "\n".join(office_card(o) for o in CONTACT_OFFICES)
            if arg == "pending":
                return "\n".join(pending_card(o) for o in SITE["offices"] if o.get("pending"))
            if arg == "list":
                return branch_list()
            if arg == "options":
                return "\n".join(f'<option value="{o["id"]}">{esc(o["city"])} — {esc(o["consultant"])}</option>' for o in CONTACT_OFFICES)
            if arg == "strip":
                return "\n".join(
                    f'<a href="{esc(wa_url(o["id"]))}" target="_blank" rel="noopener" aria-label="WhatsApp the {esc(o["city"])} office, {o["phones"][0]["display"]} (opens WhatsApp)">{ic("whatsapp")} {esc(o.get("strip_label", o["city"]))} {o["phones"][0]["display"]}</a>'
                    for o in CONTACT_OFFICES)
            if arg == "footer":
                out = []
                for o in CONTACT_OFFICES:
                    out.append(f'<p><strong>{esc(o["city"])}</strong><br><a href="{esc(wa_url(o["id"]))}" target="_blank" rel="noopener">WhatsApp {o["phones"][0]["display"]}</a><br><a href="mailto:{o["email"]}">{o["email"]}</a></p>')
                return "\n".join(out)
        if kind == "config":
            return client_config()
        if kind == "year":
            return YEAR
        # dotted lookup into site.json, e.g. {{fee.amount}}
        value = SITE
        for part in key.split("."):
            if not isinstance(value, dict) or part not in value:
                raise SystemExit(f"unknown token {{{{{key}}}}} in {ctx.get('file')}")
            value = value[part]
        return esc(str(value))

    return TOKEN.sub(sub, text)


def page(*, file, title, description, body, nav=None, og_type="website", extra_head="", body_class=""):
    ctx = {"nav": nav, "file": file}
    canonical = f'\n  <link rel="canonical" href="{BASE}/{"" if file == "index.html" else file}">' if BASE else ""
    img = f"{BASE}/assets/og-image.jpg" if BASE else "assets/og-image.jpg"
    og_url = f'\n  <meta property="og:url" content="{BASE}/{"" if file == "index.html" else file}">' if BASE else ""
    head = (SRC / "partials" / "head.html").read_text("utf-8")
    doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
{head}
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">{canonical}
  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="{esc(SITE["name"])}">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">{og_url}
  <meta property="og:image" content="{img}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(title)}">
  <meta name="twitter:description" content="{esc(description)}">
  <meta name="twitter:image" content="{img}">
{extra_head}</head>
<body{f' class="{body_class}"' if body_class else ""}>
  <a class="skip-link" href="#main">Skip to content</a>
{{{{partial:sprite.svg}}}}
{{{{partial:header.html}}}}
  <main id="main">
{body}
  </main>
{{{{partial:footer.html}}}}
{{{{partial:widgets.html}}}}
  {{{{config}}}}
  <script src="script.js" defer></script>
</body>
</html>
'''
    out = render(doc, ctx)
    (ROOT / file).write_text(out, "utf-8", newline="\n")
    return file


def jsonld(obj):
    return '  <script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False).replace("</", "<\\/") + "</script>\n"


# --------------------------------------------------------------------------- build
def build():
    written = []

    # Static pages
    for p in sorted((SRC / "pages").glob("*.html")):
        meta, body = parse(p)
        file = meta.get("file", f"{p.stem}.html")
        extra = jsonld(meta["jsonld"]) if "jsonld" in meta else ""
        if p.stem == "index":
            extra += jsonld({"@context": "https://schema.org", "@graph": [
                {"@type": "Organization", "@id": "#organization", "name": SITE["name"],
                 "description": f'Matrimonial and family matchmaking consultancy in Pakistan with branches in {SITE["branch_cities"]}.',
                 "email": OFFICES[SITE["default_office"]]["email"],
                 "telephone": OFFICES[SITE["default_office"]]["phones"][0]["tel"]}] + [
                {"@type": "ProfessionalService", "name": f'{SITE["name"]} — {o["city"]}',
                 "parentOrganization": {"@id": "#organization"}, "telephone": o["phones"][0]["tel"], "email": o["email"],
                 "address": {"@type": "PostalAddress", "streetAddress": o["address"].split(",")[0], "addressLocality": o.get("locality", o["city"]), "addressCountry": "PK"}}
                for o in CONTACT_OFFICES]})
        written.append(page(file=file, title=meta["title"], description=meta["description"], body=body,
                            nav=meta.get("nav"), extra_head=extra, body_class=meta.get("body_class", "")))

    # Articles
    for a in ARTICLES:
        related = [r for r in ARTICLES if r is not a][:3]
        cat = SITE["news_categories"][a["category"]]
        body = f'''    <article class="article">
      <header class="article-hero">
        <div class="container">
          <ol class="breadcrumb" aria-label="Breadcrumb"><li><a href="index.html">Home</a></li><li><a href="news.html">News</a></li><li aria-current="page">{esc(a["title"])}</li></ol>
          <span class="tag">{esc(cat)}</span>
          <h1>{esc(a["title"])}</h1>
          <p class="article-hero__lead">{esc(a["excerpt"])}</p>
          <p class="article-hero__meta"><time datetime="{a["date"]}">{human_date(a["date"])}</time> · {a["minutes"]} min read</p>
        </div>
        <div class="container">{cover(a, " cover--hero")}</div>
      </header>
      <div class="section section--tight">
        <div class="container article-layout">
          <div class="prose">
{a["body"]}
          </div>
          <aside class="article-aside" aria-label="Article actions">
            <div class="aside-card">
              <h2>Ready to begin?</h2>
              <p>Registration is a one-time fee of {{{{fee.amount}}}}. A consultant confirms every application personally.</p>
              <a href="registration.html" class="btn btn-primary btn-block">Register now</a>
            </div>
            <div class="aside-card">
              <h2>Share this article</h2>
              <div class="share-row">
                <a href="https://wa.me/" data-share-whatsapp target="_blank" rel="noopener">{ic("whatsapp")} WhatsApp</a>
                <button type="button" data-share-copy>{ic("link")} Copy link</button>
                <button type="button" data-share-native hidden>Share…</button>
              </div>
              <p class="share-status" id="shareStatus" aria-live="polite"></p>
            </div>
          </aside>
        </div>
      </div>
    </article>
    <section class="section section--cream" aria-labelledby="related-title">
      <div class="container">
        <div class="news-head">
          <div class="section-head"><p class="eyebrow">Keep reading</p><h2 id="related-title">Related articles</h2></div>
          <a href="news.html" class="link-arrow">All articles {ic("arrow")}</a>
        </div>
        <div class="news-grid" data-reveal-stagger>
{chr(10).join(news_card(r) for r in related)}
        </div>
      </div>
    </section>'''
        ld = {"@context": "https://schema.org", "@type": "Article", "headline": a["title"], "description": a["excerpt"],
              "datePublished": a["date"], "dateModified": a.get("updated", a["date"]),
              "publisher": {"@type": "Organization", "name": SITE["name"]}}
        extra = f'  <meta property="article:published_time" content="{a["date"]}">\n' + jsonld(ld)
        written.append(page(file=a["file"], title=f'{a["title"]} | {SITE["name"]}', description=a["excerpt"],
                            body=body, nav="news", og_type="article", extra_head=extra))

    # Profile detail pages
    for p in PROPOSALS:
        file = f'profile-{p["id"].lower()}.html'
        ask = wa_url(SITE["default_office"], f'Assalam-o-Alaikum, I am interested in Proposal ID: {p["id"]}.')
        report = "mailto:" + OFFICES[SITE["default_office"]]["email"] + "?subject=" + urllib.parse.quote(f'Report profile {p["id"]}')
        others = [o for o in PROPOSALS if o is not p]
        body = f'''    <section class="page-hero page-hero--profile">
      <div class="container">
        <ol class="breadcrumb" aria-label="Breadcrumb"><li><a href="index.html">Home</a></li><li><a href="matches.html">Find a Match</a></li><li aria-current="page">{esc(p["id"])}</li></ol>
        <div class="profile-head">
          <div class="profile-head__photo" aria-hidden="true">{ic("eye-off")}</div>
          <div>
            <span class="tag">{esc(p["tag"])}</span>
            <h1>Proposal {esc(p["id"])}</h1>
            <p>{esc(p["gender"])} · {p["age"]} years · {esc(p["profession"])}</p>
          </div>
        </div>
      </div>
    </section>
    <section class="section section--tight">
      <div class="container profile-layout">
        <div class="profile-main">
          <section class="profile-block reveal" aria-labelledby="pb-basic">
            <h2 id="pb-basic">{ic("user")} Basic information</h2>
            <dl class="facts">
              <div><dt>Gender</dt><dd>{esc(p["gender"])}</dd></div>
              <div><dt>Age</dt><dd>{p["age"]} years</dd></div>
              <div><dt>Height</dt><dd>{esc(p["height"])}</dd></div>
              <div><dt>Marital status</dt><dd>{esc(p["marital_status"])}</dd></div>
              <div><dt>Lives in</dt><dd>{esc(p["location"])}</dd></div>
              <div><dt>Family origin</dt><dd>{esc(p["family_origin"])}</dd></div>
            </dl>
          </section>
          <section class="profile-block reveal" aria-labelledby="pb-edu">
            <h2 id="pb-edu">{ic("grad")} Education &amp; profession</h2>
            <dl class="facts">
              <div><dt>Education</dt><dd>{esc(p["education"])}</dd></div>
              <div><dt>Profession</dt><dd>{esc(p["profession"])}</dd></div>
            </dl>
          </section>
          <section class="profile-block profile-block--private reveal" aria-labelledby="pb-private">
            <h2 id="pb-private">{ic("lock")} About, preferences &amp; photo</h2>
            <p>The candidate’s name, photograph, family details, preferences and contact information are never published. Your consultant shares them privately, and only after both families agree.</p>
          </section>
          <section class="profile-block reveal" aria-labelledby="pb-verify">
            <h2 id="pb-verify">{ic("shield")} Verification</h2>
            <p>Every profile is screened before it is shared with another family. Identity and document verification happen privately, with the candidate’s consent. Ask your consultant what has been verified for this profile.</p>
          </section>
        </div>
        <aside class="profile-aside">
          <div class="aside-card">
            <h2>Interested in this profile?</h2>
            <p>Your consultant will speak to both families before any details are shared.</p>
            <a href="{esc(ask)}" target="_blank" rel="noopener" class="btn btn-whatsapp btn-block">{ic("whatsapp")} Ask about {esc(p["id"])}</a>
            <a href="registration.html" class="btn btn-secondary btn-block">Register first</a>
          </div>
          <div class="aside-card aside-card--quiet">
            <h2>Something wrong?</h2>
            <p>If this listing looks inaccurate or inappropriate, tell us and we will look into it.</p>
            <a href="{esc(report)}" class="link-arrow">{ic("flag")} Report this profile</a>
          </div>
        </aside>
      </div>
    </section>
    <section class="section section--cream" aria-labelledby="more-title">
      <div class="container">
        <div class="news-head">
          <div class="section-head"><p class="eyebrow">More listings</p><h2 id="more-title">Other sample proposals</h2></div>
          <a href="matches.html" class="link-arrow">All listings {ic("arrow")}</a>
        </div>
        <div class="proposal-grid proposal-grid--two" data-reveal-stagger>
{chr(10).join(proposal_card(o) for o in others)}
        </div>
      </div>
    </section>'''
        written.append(page(file=file, title=f'Proposal {p["id"]} | {SITE["name"]}',
                            description=f'Sample matrimonial listing {p["id"]}: {p["gender"]}, {p["age"]}, {p["profession"]}. Private details shared only with both families’ consent.',
                            body=body, nav="matches"))

    # robots.txt + sitemap.xml
    public = [f for f in written if f != "404.html"]
    robots = "User-agent: *\nAllow: /\n"
    if BASE:
        urls = "\n".join(f"  <url><loc>{BASE}/{'' if f == 'index.html' else f}</loc></url>" for f in public)
        (ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n', "utf-8")
        robots += f"\nSitemap: {BASE}/sitemap.xml\n"
    else:
        robots += "\n# Set base_url in src/data/site.json and rebuild to add canonical URLs and sitemap.xml.\n"
    (ROOT / "robots.txt").write_text(robots, "utf-8", newline="\n")

    print(f"Built {len(written)} pages" + ("" if BASE else " (base_url not set: no canonical URLs or sitemap)"))
    for f in written:
        print("  " + f)


if __name__ == "__main__":
    build()
