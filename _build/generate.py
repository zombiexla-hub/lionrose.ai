#!/usr/bin/env python3
# LionRose "What We're Building" generator.
# Single source of truth: products.json (in this folder).
# Regenerates the building section in ../index.html and all p-<slug>.html detail pages.
# Usage: python3 generate.py   (run from website/_build/)
import json, os, re, io

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.dirname(HERE)  # website/
DATA = json.load(io.open(os.path.join(HERE, "products.json"), encoding="utf-8"))
BASE = DATA["base_url"].rstrip("/")

def rd(p): return io.open(p, encoding="utf-8").read()
def wr(p, s): io.open(p, "w", encoding="utf-8").write(s)

def seo_head(name, meta_desc, url, og_image):
    return f'''<meta name="description" content="{meta_desc}" />
<link rel="canonical" href="{url}" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="LionRose" />
<meta property="og:title" content="{name} | LionRose" />
<meta property="og:description" content="{meta_desc}" />
<meta property="og:url" content="{url}" />
<meta property="og:image" content="{BASE}/{og_image}" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{name} | LionRose" />
<meta name="twitter:description" content="{meta_desc}" />
<meta name="twitter:image" content="{BASE}/{og_image}" />'''

DETAIL = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{name} | LionRose</title>
{seo}
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;900&family=JetBrains+Mono:wght@400;500;700&family=Lato:wght@300;400;700&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="lionrose-green.css" />
</head>
<body>

<div class="rail" aria-hidden="true">
  <span class="cap top">LIONROSE // STUDIO</span>
  <div class="track"></div><div class="node"></div>
  <span class="cap">34.05N // 118.24W // LA</span>
</div>

<nav>
  <a class="logo" href="index.html">Lion<b>Rose</b></a>
  <ul class="navlinks">
    <li><a href="web.html">Web Dev</a></li>
    <li><a href="hr.html">HR</a></li>
    <li><a href="media.html">Media</a></li>
    <li><a href="production.html">Production</a></li>
    <li class="keep"><a class="navcta" href="index.html#contact">Get in touch</a></li>
  </ul>
</nav>

<section class="hero med" id="hero">
  <canvas data-words="{words}"></canvas>
  <div class="hero-vig"></div>
  <div class="hero-copy">
    <a class="back" href="index.html#building">&#8592; LionRose</a>
    <span class="eyebrow" style="margin-top:1.2rem;"><i></i>LionRose Studio</span>
    <h1>{tagline}</h1>
    <p class="sub">{sub}</p>
    <div class="hero-btns">
      <a class="btn btn-p" href="{cta_href}">{cta_label}</a>
      <a class="btn btn-g" href="index.html#building">All Products</a>
    </div>
  </div>
</section>

<div class="divider"><span class="ln"></span><span class="tag">// Overview</span><span class="ln r"></span></div>
<section id="overview">
  <div class="wrap reveal">
    <div class="pdetail">
      <div class="pshot"><img src="{shot}" alt="{name} preview" /></div>
      <div class="pinfo">
        <span class="k"><i></i>{name} &middot; {status}</span>
        <h2 class="title">{h2}</h2>
        {paras}
      </div>
    </div>
  </div>
</section>

<div class="divider"><span class="ln"></span><span class="tag">// What It Does</span><span class="ln r"></span></div>
<section id="does">
  <div class="wrap reveal">
    <div class="cards">
      {feats}
    </div>
  </div>
</section>

<div class="divider"><span class="ln"></span><span class="tag">// {cta_k}</span><span class="ln r"></span></div>
<section id="cta">
  <div class="wrap reveal">
    <span class="k"><i></i>{cta_k}</span>
    <h2 class="title">{cta_title}</h2>
    <p class="lede">{cta_lede}</p>
    <div style="margin-top:2rem;"><a class="btn btn-p" href="{cta_href}">{cta_label}</a></div>
  </div>
</section>

<footer>
  <div class="status"><span>SYSTEM: LIONROSE // STUDIO</span><span>//</span><span>PRODUCT: {name}</span><span>//</span><span>STATUS: <span class="on">{status}</span></span></div>
  <div class="fnav"><a href="index.html">Home</a><a href="index.html#building">Products</a><a href="web.html">Web Development</a><a href="hr.html">Human Resources</a><a href="media.html">Media</a><a href="production.html">Production</a></div>
  <div class="fname">LionRose Entertainment Inc.</div>
</footer>

<script src="lionrose-green.js"></script>
</body>
</html>
'''

def card(p):
    stcls = " " + p["status_class"] if p.get("status_class") else ""
    if p.get("external"):
        href = p["href"]; attrs = ' target="_blank" rel="noopener"'
    else:
        href = "p-%s.html" % p["slug"]; attrs = ""
    return ('      <a class="card pcard" href="%s"%s>\n'
            '        <div class="thumb"><img src="%s" alt="%s preview" loading="lazy" /></div>\n'
            '        <div class="body">\n'
            '          <div class="top"><h3 class="dc">%s</h3><span class="st%s">%s</span></div>\n'
            '          <div class="tg">%s</div>\n'
            '          <p>%s</p>\n'
            '          <span class="golink">%s &#8599;</span>\n'
            '        </div>\n'
            '      </a>') % (href, attrs, p["thumb"], p["name"], p["name"], stcls,
                            p["status"], p["card_tagline"], p["card_desc"], p["cta_card"])

def build_section():
    s = DATA["section"]
    cards = "\n".join(card(p) for p in DATA["products"])
    return ('<section id="building">\n'
            '  <div class="wrap reveal">\n'
            '    <span class="k"><i></i>%s</span>\n'
            '    <h2 class="title">%s</h2>\n'
            '    <p class="lede">%s</p>\n'
            '    <div class="cards">\n%s\n    </div>\n'
            '  </div>\n'
            '</section>') % (s["k"], s["title"], s["lede"], cards)

def build_detail(p):
    url = "%s/p-%s.html" % (BASE, p["slug"])
    seo = seo_head(p["name"], p["meta_desc"], url, p["og_image"])
    plist = []
    for i, t in enumerate(p["paras"]):
        style = ' style="margin-top:1rem;"' if i else ''
        plist.append('<p class="lede"%s>%s</p>' % (style, t))
    paras = "\n        ".join(plist)
    feats = "\n      ".join('<div class="card"><h3 class="dc">%s</h3><p>%s</p></div>' % (ft, fd) for ft, fd in p["feats"])
    return DETAIL.format(name=p["name"], seo=seo, words=p["words"], tagline=p["tagline"],
        sub=p["sub"], shot=p["shot"], status=p["status"], h2=p["h2"], paras=paras, feats=feats,
        cta_href=p["cta_href"], cta_label=p["cta_label"], cta_k=p["cta_k"],
        cta_title=p["cta_title"], cta_lede=p["cta_lede"])

def main():
    # detail pages
    n=0
    for p in DATA["products"]:
        if p.get("has_detail"):
            wr(os.path.join(WEB, "p-%s.html" % p["slug"]), build_detail(p)); n+=1
    # building section into index.html
    idx_path = os.path.join(WEB, "index.html")
    idx = rd(idx_path)
    new = build_section()
    idx2 = re.sub(r'<section id="building">.*?</section>', lambda m: new, idx, count=1, flags=re.DOTALL)
    if idx2 == idx and '<section id="building">' not in idx:
        raise SystemExit("building section not found in index.html")
    wr(idx_path, idx2)
    print("generated %d detail pages + building section (%d cards)" % (n, len(DATA["products"])))

if __name__ == "__main__":
    main()
