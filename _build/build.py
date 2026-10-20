"""Generates the static site for santiwari07.github.io from projects.json.

Usage (from the repo root):  python _build/build.py
Edit projects.json to add or change projects, then run this again and commit.
"""
import html
import json
import shutil
from datetime import date
from pathlib import Path

BUILD = Path(__file__).resolve().parent
ROOT = BUILD.parent
SITE = "https://santiwari07.github.io"

# Paste the content="..." value of Google Search Console's HTML-tag verification here.
GOOGLE_VERIFICATION = "Kd4qy_v7eZxDXbZWmEYi1RAqnSe9DXiDpP45ADvpNmk"

PERSON = {
    "name": "Sanskar Tiwari",
    "handle": "santiwari07",
    "role": "ENTC student at PICT Pune building AI, computer vision and embedded systems",
    "links": [
        ("GitHub", "https://github.com/SanTiwari07"),
        ("LinkedIn", "https://www.linkedin.com/in/santiwari07"),
        ("Kaggle", "https://www.kaggle.com/santiwari07"),
        ("Research paper", "https://zenodo.org/records/20760578"),
        ("YouTube", "https://www.youtube.com/channel/UCFehdcKwzbkUomeo2yOG1Mw"),
        ("Instagram", "https://www.instagram.com/sanskarmakesstuff/"),
        ("LeetCode", "https://leetcode.com/u/santiwari07/"),
        ("Portfolio", "https://santiwari07.qzz.io/"),
    ],
}

ACHIEVEMENTS = [
    ("1st place", "TechFiesta '26 · KrishiSahAI",
     "International hackathon · Agriculture domain · Top of 700+ teams · ₹50,000 grand prize", None),
    ("1st place", "HackVenture 2026 · GramDrishti",
     "National hackathon by Sponfest · Agritech domain", "/projects/gramdrishti/"),
    ("Runner-up", "Pune Agri International Hackathon · Krishi Prabandh",
     "National runner-up · ₹15 lakh government grant for development · Presented to the Maharashtra CM", None),
    ("Top 3", "VOIS Innovation Marathon 2.0 · KrishiSaarthi",
     "Vodafone Idea Foundation · Top 3 of 630+ teams · ₹2,00,000 cash prize", None),
    ("Paper", "Real-Time Pothole Detection Based on Vision-Dominant Sensor Fusion and Dual ESP32 Architecture",
     "Preprint on Zenodo · DOI 10.5281/zenodo.20760578", "/projects/pothole-detection/"),
]

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&'
         'family=Inter+Tight:wght@500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">')

e = html.escape


def clip(text, n=155):
    return text if len(text) <= n else text[: n - 1].rsplit(" ", 1)[0] + "…"


def local(url):
    """Serve images hosted on this site from a root-relative path."""
    return url[len(SITE):] if url.startswith(SITE) else url


def person_ld():
    return {
        "@type": "Person",
        "@id": f"{SITE}/#person",
        "name": PERSON["name"],
        "alternateName": ["santiwari07", "SanTiwari07", "sanskarmakesstuff"],
        "url": f"{SITE}/",
        "image": f"{SITE}/assets/og.png",
        "jobTitle": "Software Engineer Intern",
        "description": "Electronics and Telecommunication Engineering student at PICT, Pune, building AI, "
                       "computer vision and embedded systems.",
        "worksFor": {"@type": "Organization", "name": "MindstriX Technologies LLP"},
        "affiliation": {"@type": "CollegeOrUniversity", "name": "Pune Institute of Computer Technology (PICT)"},
        "address": {"@type": "PostalAddress", "addressLocality": "Pune", "addressRegion": "Maharashtra",
                    "addressCountry": "IN"},
        "knowsAbout": ["Computer Vision", "Embedded Systems", "Machine Learning", "LLM integration",
                       "Android security", "ESP32", "YOLOv8"],
        "sameAs": [url for _, url in PERSON["links"]],
    }


def head(title, desc, path, image=None, ld=None, kind="website"):
    url = SITE + path
    image = image or f"{SITE}/assets/og.png"
    verify = f'<meta name="google-site-verification" content="{e(GOOGLE_VERIFICATION)}">' if GOOGLE_VERIFICATION else ""
    ld_tag = ""
    if ld:
        ld_tag = '<script type="application/ld+json">' + json.dumps(
            {"@context": "https://schema.org", "@graph": ld}, ensure_ascii=False) + "</script>"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="author" content="Sanskar Tiwari">
<link rel="canonical" href="{url}">
{verify}
<meta property="og:type" content="{kind}">
<meta property="og:site_name" content="Sanskar Tiwari · santiwari07">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{e(image)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#030303">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
{FONTS}
<link rel="stylesheet" href="/assets/style.css">
{ld_tag}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="topbar">
  <div class="wrap topbar-in">
    <a class="logo" href="/">Sanskar Tiwari</a>
    <nav aria-label="Main">
      <a href="/#about">About</a>
      <a href="/#projects">Projects</a>
      <a href="/#achievements">Awards</a>
      <a href="https://santiwari07.qzz.io/#contact" rel="noopener">Contact</a>
    </nav>
  </div>
</header>
"""


def foot():
    links = " ".join(f'<a href="{e(u)}" rel="me noopener">{e(n)}</a>' for n, u in PERSON["links"])
    return f"""<footer class="foot">
  <div class="wrap">
    <p class="foot-name">Sanskar Tiwari <span class="mono">· santiwari07</span></p>
    <p class="foot-links">{links}</p>
    <p class="muted small">© {date.today().year} Sanskar Tiwari. Projects by santiwari07, ENTC at PICT Pune.</p>
  </div>
</footer>
</body>
</html>
"""


def link_buttons(links):
    labels = [("demo", "Live demo"), ("website", "Project site"), ("video", "Watch video"),
              ("paper", "Read the paper"), ("github", "Source on GitHub")]
    out = []
    for key, label in labels:
        if key in links:
            cls = "btn primary" if key in ("demo", "website") or (key == "github" and len(links) == 1) else "btn"
            out.append(f'<a class="{cls}" href="{e(links[key])}" rel="noopener">{label} <span aria-hidden="true">↗</span></a>')
    return "\n".join(out)


def chips(items):
    return "".join(f"<li>{e(s)}</li>" for s in items)


def card(p, cats, n):
    img = (f'<div class="card-img"><img src="{e(local(p["image"]))}" alt="{e(p.get("image_alt", p["name"]))}" '
           f'loading="lazy" decoding="async"></div>') if p.get("image") else ""
    return f"""<article class="card">
  <a class="card-link" href="/projects/{p['slug']}/">
    {img}
    <div class="card-body">
      <p class="eyebrow mono">{n:02d} · {e(cats[p['category']])}</p>
      <h3>{e(p.get('short', p['name']))}</h3>
      <p>{e(p['tagline'])}</p>
      <ul class="chips">{chips(p['stack'][:4])}</ul>
    </div>
  </a>
</article>"""


def row(p):
    ev = f" · {e(p['event'])}" if p.get("event") else ""
    return f"""<li class="row">
  <a href="/projects/{p['slug']}/">
    <span class="row-name">{e(p.get('short', p['name']))}</span>
    <span class="row-tag">{e(p['tagline'])}</span>
    <span class="row-meta mono">{p['year']}{ev}</span>
  </a>
</li>"""


def build_index(data):
    cats, projects = data["categories"], data["projects"]
    featured = [p for p in projects if p.get("featured")]
    cards = "\n".join(card(p, cats, i + 1) for i, p in enumerate(featured))
    groups = []
    for key, label in cats.items():
        items = [p for p in projects if p["category"] == key]
        if items:
            groups.append(f'<section class="group" aria-labelledby="g-{key}"><h3 id="g-{key}" class="group-h mono">'
                          f'{e(label)} <span class="count">{len(items)}</span></h3><ul class="rows">'
                          + "".join(row(p) for p in items) + "</ul></section>")
    ach = "".join(f'<li><span class="badge mono" data-kind="{e(k.split()[0].lower())}">{e(k)}</span>'
                  f'<div><strong>{f"<a href={chr(34)}{u}{chr(34)}>{e(t)}</a>" if u else e(t)}</strong>'
                  f'<span class="muted">{e(s)}</span></div></li>'
                  for k, t, s, u in ACHIEVEMENTS)
    more = "".join(f'<li><a href="{e(m["url"])}" rel="noopener"><strong>{e(m["name"])}</strong>'
                   f'<span class="muted">{e(m["desc"])}</span></a></li>' for m in data["more"])
    elsewhere = "".join(f'<li><a href="{e(u)}" rel="me noopener">{e(n)} <span aria-hidden="true">↗</span></a></li>'
                        for n, u in PERSON["links"])

    item_list = {"@type": "ItemList", "name": "Projects by Sanskar Tiwari (santiwari07)",
                 "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"{SITE}/projects/{p['slug']}/",
                                      "name": p["name"]} for i, p in enumerate(projects)]}
    site_ld = {"@type": "WebSite", "@id": f"{SITE}/#website", "url": f"{SITE}/",
               "name": "Sanskar Tiwari · santiwari07", "author": {"@id": f"{SITE}/#person"}}
    page_ld = {"@type": "ProfilePage", "@id": f"{SITE}/", "url": f"{SITE}/", "mainEntity": {"@id": f"{SITE}/#person"},
               "name": "Sanskar Tiwari (santiwari07)"}

    title = "Sanskar Tiwari (santiwari07) · AI, Computer Vision & Embedded Systems Projects"
    desc = ("Sanskar Tiwari (santiwari07) is an ENTC student at PICT Pune and LLM intern at MindstriX. "
            f"{len(projects)} projects: Sudarshan malware sandbox, NarraReel, YOLOv8 pothole detection and more.")
    body = f"""<main id="main">
<section class="hero">
  <div class="hero-ghost" aria-hidden="true">SANSKAR TIWARI</div>
  <div class="hero-streaks" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
  <div class="wrap">
    <p class="eyebrow mono">Software Engineer Intern · AI, computer vision &amp; embedded systems</p>
    <h1><span>Sanskar</span> <span>Tiwari</span></h1>
    <p class="aka mono">aka <strong>santiwari07</strong> · sanskarmakesstuff</p>
    <p class="lede">I build systems that combine software, hardware and machine learning: a YOLOv8 and dual-ESP32 pothole rig,
    a sandbox that takes apart fake banking apps, satellite tools that tell field officers which farms to visit first.
    Most of what I know I learned by building, breaking and debugging real systems.</p>
    <div class="cta">
      <a class="btn primary" href="#projects">View Work</a>
      <a class="btn" href="https://github.com/SanTiwari07" rel="me noopener">GitHub ↗</a>
      <a class="text-link" href="https://www.linkedin.com/in/santiwari07" rel="me noopener">LinkedIn</a>
    </div>
    <dl class="stats">
      <div><dt class="mono">TechFiesta '26</dt><dd>International gold</dd></div>
      <div><dt class="mono">4×</dt><dd>Hackathon podiums</dd></div>
      <div><dt class="mono">{len(projects)}</dt><dd>Projects documented</dd></div>
      <div><dt class="mono">1</dt><dd>Research preprint</dd></div>
    </dl>
  </div>
</section>

<section id="projects" class="section">
  <div class="wrap">
    <div class="section-h"><p class="label mono"><span>01</span> / Selected work</p><h2>Things I built that work outside the lab.</h2></div>
    <div class="cards">
{cards}
    </div>
  </div>
</section>

<section class="section alt" aria-labelledby="all-h">
  <div class="wrap">
    <div class="section-h"><p class="label mono"><span>02</span> / Index</p><h2 id="all-h">Every project, by area.</h2></div>
    <div class="groups">
{''.join(groups)}
    </div>
    <h3 class="group-h mono more-h">Early builds &amp; experiments</h3>
    <ul class="more">{more}</ul>
  </div>
</section>

<section id="achievements" class="section">
  <div class="wrap">
    <div class="section-h"><p class="label mono"><span>03</span> / Recognition</p><h2>Four podiums, two first places.</h2></div>
    <ul class="awards">{ach}</ul>
  </div>
</section>

<section id="about" class="section alt">
  <div class="wrap about">
    <div>
      <div class="section-h"><p class="label mono"><span>04</span> / About</p><h2>Hi, I'm Sanskar</h2></div>
      <p>I'm a third-year Electronics and Telecommunication Engineering student at PICT (Pune Institute of Computer
      Technology) and a Software Engineer Intern at MindstriX Technologies LLP, where I work on LLM integration,
      API development and AI R&amp;D.</p>
      <p>I like projects where code meets the physical world: computer vision on embedded hardware, sensor fusion,
      and AI that stays inside deterministic rules so it can be trusted with money, crops or security decisions.</p>
      <p>Right now I'm building AI-native Android apps that combine the Gemini API with real-world sensor data.
      I'm open to internships and collaborations, and the fastest way to reach me is
      <a href="https://www.linkedin.com/in/santiwari07" rel="me noopener">LinkedIn</a>.</p>
    </div>
    <div>
      <h3 class="group-h mono">Find me elsewhere</h3>
      <ul class="elsewhere">{elsewhere}</ul>
    </div>
  </div>
</section>
</main>
"""
    out = head(title, desc, "/", ld=[person_ld(), site_ld, page_ld, item_list], kind="profile") + body + foot()
    (ROOT / "index.html").write_text(out, encoding="utf8")


def build_project(p, data, prev, nxt):
    cats = data["categories"]
    path = f"/projects/{p['slug']}/"
    name = p["name"]
    title = f"{name}: {p['tagline']} | Sanskar Tiwari (santiwari07)"
    desc = clip(p["summary"])
    ev = f" · {e(p['event'])}" if p.get("event") else ""
    img = (f'<figure class="shot"><img src="{e(local(p["image"]))}" alt="{e(p.get("image_alt", name))}" '
           f'decoding="async"></figure>') if p.get("image") else ""
    paras = "".join(f"<p>{e(t)}</p>" for t in p.get("body", []))
    hl = "".join(f"<li>{e(t)}</li>" for t in p.get("highlights", []))
    related = [q for q in data["projects"] if q["category"] == p["category"] and q is not p][:3]
    if len(related) < 3:
        related += [q for q in data["projects"] if q.get("featured") and q is not p and q not in related][: 3 - len(related)]
    rel = "".join(row(q) for q in related)
    team = p.get("team", [])
    team_links = [(f'<a href="{e(m["url"])}" rel="noopener">{e(m["name"])}</a>' if m.get("url") else e(m["name"]))
                  + (f' <span class="mono">(<a href="{e(m["github"])}" rel="noopener">GitHub</a>)</span>' if m.get("github") else "")
                  for m in team]
    team_line = ""
    if team_links:
        joined = team_links[0] if len(team_links) == 1 else ", ".join(team_links[:-1]) + " and " + team_links[-1]
        team_line = f" with {joined}"

    code_ld = {"@type": "SoftwareSourceCode", "@id": SITE + path + "#project", "name": name,
               "description": p["summary"], "url": SITE + path, "codeRepository": p["links"].get("github"),
               "keywords": ", ".join(p["stack"]), "dateCreated": str(p["year"]),
               "author": {"@id": f"{SITE}/#person"}, "creator": {"@id": f"{SITE}/#person"}}
    if team:
        code_ld["contributor"] = [{"@type": "Person", "name": m["name"], "sameAs": [u for u in (m.get("url"), m.get("github")) if u]}
                                  for m in team]
    if p.get("image"):
        code_ld["image"] = p["image"]
    crumbs = {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Sanskar Tiwari", "item": f"{SITE}/"},
        {"@type": "ListItem", "position": 2, "name": "Projects", "item": f"{SITE}/#projects"},
        {"@type": "ListItem", "position": 3, "name": name, "item": SITE + path}]}
    person = {"@type": "Person", "@id": f"{SITE}/#person", "name": "Sanskar Tiwari",
              "alternateName": "santiwari07", "url": f"{SITE}/"}

    body = f"""<main id="main" class="project">
<div class="wrap narrow">
  <nav class="crumbs mono" aria-label="Breadcrumb"><a href="/">santiwari07</a> / <a href="/#projects">projects</a> / <span>{e(p['slug'])}</span></nav>
  <p class="eyebrow mono">{e(cats[p['category']])} · {p['year']}{ev}</p>
  <h1>{e(name)}</h1>
  <p class="tagline">{e(p['tagline'])}</p>
  <p class="byline">Built by <a href="/" rel="author">Sanskar Tiwari</a> <span class="mono">(santiwari07)</span>{team_line}</p>
  <div class="cta">{link_buttons(p['links'])}</div>
</div>
<div class="wrap narrow">
  {img}
  <p class="lead">{e(p['summary'])}</p>
  {paras}
  {f'<h2>What it does</h2><ul class="ticks">{hl}</ul>' if hl else ''}
  <h2>Built with</h2>
  <ul class="chips big">{chips(p['stack'])}</ul>

  <aside class="author">
    <span class="logo-mark" aria-hidden="true">ST</span>
    <div>
      <p><strong>Sanskar Tiwari</strong> <span class="mono muted">santiwari07</span></p>
      <p class="muted">ENTC student at PICT Pune and Software Engineer Intern at MindstriX. I build AI, computer vision and embedded systems.</p>
      <p class="small"><a href="/">All projects</a> · <a href="https://github.com/SanTiwari07" rel="me noopener">GitHub</a> · <a href="https://www.linkedin.com/in/santiwari07" rel="me noopener">LinkedIn</a></p>
    </div>
  </aside>

  <h2 class="mono small-h">More projects</h2>
  <ul class="rows">{rel}</ul>

  <nav class="pager" aria-label="Project navigation">
    <a href="/projects/{prev['slug']}/"><span class="mono muted">← Previous</span>{e(prev.get('short', prev['name']))}</a>
    <a href="/projects/{nxt['slug']}/" class="next"><span class="mono muted">Next →</span>{e(nxt.get('short', nxt['name']))}</a>
  </nav>
</div>
</main>
"""
    out = head(title, desc, path, image=p.get("image"), ld=[code_ld, crumbs, person], kind="article") + body + foot()
    d = ROOT / "projects" / p["slug"]
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(out, encoding="utf8")


def build_404():
    body = """<main id="main" class="project"><div class="wrap narrow">
<p class="eyebrow mono">404</p><h1>Page not found</h1>
<p class="tagline">That page doesn't exist. Try the <a href="/">project index</a>.</p>
</div></main>
"""
    out = head("Page not found | Sanskar Tiwari (santiwari07)", "Page not found.", "/404.html") + body + foot()
    out = out.replace('<link rel="canonical"', '<meta name="robots" content="noindex">\n<link rel="canonical"', 1)
    (ROOT / "404.html").write_text(out, encoding="utf8")


def build_sitemap(data):
    meta = data.get("meta", {})

    def pushed(p):
        return meta.get(p["links"].get("github", "").lower(), {}).get("pushed", "")

    entries = [(f"{SITE}/projects/{p['slug']}/", pushed(p)) for p in data["projects"]]
    entries.insert(0, (f"{SITE}/", max((d for _, d in entries if d), default="")))
    items = "".join(f"<url><loc>{u}</loc>" + (f"<lastmod>{d}</lastmod>" if d else "") + "</url>" for u, d in entries)
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f"{items}</urlset>\n", encoding="utf8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf8")


def main():
    data = json.loads((BUILD / "projects.json").read_text(encoding="utf8"))
    auto_file = BUILD / "auto.json"
    auto = json.loads(auto_file.read_text(encoding="utf8")) if auto_file.exists() else {"projects": [], "meta": {}}
    data["projects"] += auto["projects"]
    data["meta"] = auto["meta"]
    projects = data["projects"]
    if (ROOT / "projects").exists():
        shutil.rmtree(ROOT / "projects")
    build_index(data)
    for i, p in enumerate(projects):
        build_project(p, data, projects[i - 1], projects[(i + 1) % len(projects)])
    build_404()
    build_sitemap(data)
    print(f"Built index + {len(projects)} project pages")


if __name__ == "__main__":
    main()
