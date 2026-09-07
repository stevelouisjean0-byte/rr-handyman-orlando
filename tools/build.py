#!/usr/bin/env python3
"""Generate the R&R Handyman pages.

The deployed site is plain static HTML with no build step and no JavaScript.
This script exists only so the parts that appear on every page (head metadata,
masthead, navigation, mobile action bar, footer) are written once and cannot
drift apart. Run it, then commit the generated .html files.

    python tools/build.py

Everything factual in here traces to the Google Business profile or to a named
customer review. See FACTS below. Nothing is invented: no licensing, insurance,
years in business, project counts, awards, warranties or guarantees.
"""

import io
import math
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── FACTS ─────────────────────────────────────────────────────────────────
# Every one of these is either on the Google Business profile or in a review.
NAME_LEGAL = "Renovation &amp; Restoration Handyman Services L.L.C."
NAME = "R&amp;R Handyman"
PHONE = "(407) 401-0184"
TEL = "+14074010184"
STREET = "6402 Beggs Rd"
CITY, REGION, ZIP = "Orlando", "FL", "32810"
PLUSCODE = "JGGQ+52"
RATING, REVIEWS = "4.8", "24"
# OWNER TO CONFIRM: the Google profile lists "Open 24 hours". That is the
# owner's own published hours, so it is used verbatim and consistently in the
# header, contact page, footer, metadata and structured data. If the business
# does not in fact take calls at any hour, change HOURS here and rerun.
HOURS = "Open 24 hours"
HOURS_LONG = "Open 24 hours, every day"
BASE = "https://stevelouisjean0-byte.github.io/rr-handyman-orlando"
# OWNER TO CONFIRM: this is the search URL already present in the project, not
# a canonical Google Business profile link. Replace it with the real profile or
# place URL when available.
GOOGLE = ("https://www.google.com/search?q=Renovation+%26+Restoration"
          "+Handyman+Services+Orlando+reviews")
MAPS = ("https://www.google.com/maps/search/?api=1&amp;query="
        "Renovation%20%26%20Restoration%20Handyman%20Services%20"
        "6402%20Beggs%20Rd%20Orlando%20FL%2032810")

NAV = [
    ("index.html", "Home"),
    ("services.html", "Services"),
    ("cases.html", "Our Work"),
    ("reviews.html", "Reviews"),
    ("contact.html", "Contact"),
]


# ── icons ────────────────────────────────────────────────────────────────
# Simple geometric marks built from rects, circles, lines and short paths,
# drawn at a single 24x24 box with one stroke weight so they read as one set.
# No icon library is used because the site ships without a build step or any
# package dependency.
def ico(body, size=24, cls=None, sw="1.75"):
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true">{body}</svg>')


def star_path(cx=12, cy=12, outer=8.6, inner=3.7, points=5):
    pts = []
    for i in range(points * 2):
        r = outer if i % 2 == 0 else inner
        a = -math.pi / 2 + i * math.pi / points
        pts.append(f"{cx + r * math.cos(a):.2f} {cy + r * math.sin(a):.2f}")
    return "M" + "L".join(pts) + "Z"


I_PHONE = ('<path d="M6.6 3h3l1.5 5.2-2.1 1.5a12.5 12.5 0 0 0 5.3 5.3l1.5-2.1L21 14.4v3'
           'a2.4 2.4 0 0 1-2.6 2.4A16.8 16.8 0 0 1 3.2 5.6A2.4 2.4 0 0 1 5.6 3z"/>')
I_TICK = '<path d="M4 12.5l5 5 11-11"/>'
I_STAR = f'<path d="{star_path()}" fill="currentColor" stroke="none"/>'
I_PIN = ('<path d="M12 21.5c4.4-4.2 7-7.6 7-10.8a7 7 0 1 0-14 0c0 3.2 2.6 6.6 7 10.8z"/>'
         '<circle cx="12" cy="10.4" r="2.6"/>')
I_CHAT = '<path d="M4 5h16v11H9l-5 4z"/>'
I_NOTE = '<path d="M5 3h9l5 5v13H5z"/><path d="M14 3v5h5"/><path d="M8.5 13h7M8.5 16.5h4.5"/>'
# toolbox
I_TOOL = ('<rect x="3" y="9" width="18" height="11"/>'
          '<path d="M9 9V7a3 3 0 0 1 6 0v2"/><path d="M3 14h18"/>'
          '<path d="M10.5 12.5h3v3h-3z"/>')
# door
I_DOOR = ('<rect x="5" y="3" width="14" height="18"/>'
          '<rect x="8" y="6" width="8" height="8"/>'
          '<circle cx="15.6" cy="17" r="1"/>')
# bulb
I_BULB = ('<circle cx="12" cy="9.5" r="5"/>'
          '<path d="M10 17.5h4M10.6 20.5h2.8"/>'
          '<path d="M12 2.5v1.4M4.6 6.1l1 .8M19.4 6.1l-1 .8"/>')
# droplet
I_DROP = '<path d="M12 3.2c3.6 4.2 5.4 7 5.4 9.4a5.4 5.4 0 0 1-10.8 0c0-2.4 1.8-5.2 5.4-9.4z"/>'
# house with water inside
I_WATER = ('<path d="M3.5 10.6 12 4l8.5 6.6V20H3.5z"/>'
           '<path d="M12 11.4c1.9 2.2 2.8 3.7 2.8 4.9a2.8 2.8 0 0 1-5.6 0c0-1.2.9-2.7 2.8-4.9z"/>')
# floor plan with a doorway gap
I_PLAN = ('<rect x="3.5" y="3.5" width="17" height="17"/>'
          '<path d="M12 3.5v6M12 14v6.5"/><path d="M3.5 14h5M15.5 9.5h5"/>')
I_IMG = ('<rect x="3" y="5" width="18" height="14"/>'
         '<circle cx="8.5" cy="10" r="1.6"/><path d="m4 17 5-4 4 3 3-2 4 3"/>')
I_INFO = '<circle cx="12" cy="12" r="9"/><path d="M12 11v5.5"/><path d="M12 7.8h.01"/>'

SERVICE_ICONS = {
    "small-jobs": I_TOOL, "doors": I_DOOR, "lighting": I_BULB,
    "irrigation": I_DROP, "storm": I_WATER, "reconfiguration": I_PLAN,
}


# ── services ──────────────────────────────────────────────────────────────
SERVICES = [
    dict(
        id="small-jobs", name="Small handyman jobs",
        short="The jobs that never quite justify calling a contractor. More reviews "
              "mention this than any other kind of work.",
        long="The jobs that never quite justify calling a contractor, and the ones "
             "most handymen quietly stop returning calls about, because they do not "
             "pay like a renovation. Ours get scheduled and finished.",
        eg=["A door that will not latch", "A light fixture swapped out",
            "A shelf that needs to hold real weight"],
        src="Named in five Google reviews",
    ),
    dict(
        id="doors", name="Door repair and replacement",
        short="Sliding doors swapped for French pairs, doors rehung, frames squared "
              "and weathersealed.",
        long="Sliding doors swapped for French pairs, doors rehung, frames squared, "
             "thresholds and weatherseals renewed. When the old unit comes out the "
             "opening itself usually needs attention, and that is part of the job "
             "rather than an extra.",
        eg=["A slider replaced with a French pair", "A door rehung so it latches",
            "Threshold and weatherseal renewed"],
        src="Named in two Google reviews",
    ),
    dict(
        id="lighting", name="Lighting installation",
        short="Replacing fixtures inside and out, plus the switching that goes with "
              "them.",
        long="Replacing fixtures inside and out, plus the switching that goes with "
             "them. Often fitted during the same visit as a larger job. One customer "
             "got a new French door and new lights on the same day.",
        eg=["Ceiling and wall fixtures replaced", "Exterior lights fitted",
            "Switches changed out"],
        src="Named in two Google reviews",
    ),
    dict(
        id="irrigation", name="Irrigation repair",
        short="Heads, valves, timers, and the slow leaks you only catch by watching "
              "the meter.",
        long="Heads, valves, timers, broken laterals, and the slow leaks you only "
             "catch by watching the meter with everything off. A Central Florida "
             "system runs most of the year, so it wears out like something that runs "
             "most of the year. A stuck zone can waste more water in a month than "
             "the repair costs.",
        eg=["Broken or blocked heads replaced", "A stuck valve or dead zone fixed",
            "Timer set to something sensible"],
        src="Named in two Google reviews",
    ),
    dict(
        id="storm", name="Storm damage and water-intrusion diagnosis",
        short="Finding where wind-driven water actually gets in, which is the part "
              "that usually survives inspection.",
        long="Wind-driven water through exterior joints is the classic Florida "
             "failure and the hardest to diagnose, because it only shows itself in "
             "weather. That is exactly why it survives inspection after inspection. "
             "We chase the path the water takes, not the stain it leaves.",
        eg=["Tracing where water actually enters", "Sealing the exterior joints at fault",
            "Making the inside good once it is dry"],
        src="From Marsha Jefferson's Google review",
    ),
    dict(
        id="reconfiguration", name="Home reconfiguration and trade coordination",
        short="Changing a layout rather than replacing it, and working alongside "
              "another vendor on the same site.",
        long="Jobs that need a layout altered rather than ripped out, or another "
             "vendor on site at the same time. One customer's job needed both, and "
             "they called the reconfiguration element tricky, meaning it was not a "
             "swap, it was a rethink.",
        eg=["A layout altered rather than replaced", "Scheduling around another vendor",
            "One point of contact for the job"],
        src="From N Roe's Google review",
    ),
]

# Careful language about regulated trades. Trade coordination itself is
# evidenced by N Roe's review. OWNER TO CONFIRM the exact wording.
REGULATED_NOTE = (
    "Work that legally requires a licensed trade, such as new electrical circuits, "
    "plumbing alterations or structural changes, is coordinated with an appropriately "
    "licensed contractor rather than carried out in place of one. Ask when you call "
    "and we will tell you which part of your job that applies to."
)

WHY = [
    ("You speak to Rickey directly",
     "One call reaches the person who does the work, not an office and not a queue. "
     "Reviewers mention the communication more than almost anything else."),
    ("The price is discussed before work starts",
     "“Fair price” and “reasonable price” are the two phrases that "
     "recur most across the reviews. Both depend on the number coming first."),
    ("Small jobs actually get scheduled",
     "Small jobs are the most mentioned kind of work in the reviews, counted five "
     "separate times. It is the work people struggle to get anyone to turn up for."),
    ("Repairs other people could not find",
     "One customer had storm water entering a two-year-old house every year, through "
     "round after round of inspections, before the path it was taking was found."),
    ("Cleaned up when the work is done",
     "“Clean up completely and charged a fair price” is a customer's own "
     "description of how their job ended. That is the standard."),
]

REVIEWS_DATA = [
    dict(name="Sonia Agosto", meta="5 reviews, 9 photos", when="Two months ago",
         body='100% recommended. Trustworthy, reasonable price and very responsible. '
              'So happy with the work that he done in my house. \U0001F60A<br>Removed '
              'my old sliding door and replaced with French door and put some lights '
              'up. <span class="trunc">… [review continues on Google]</span>',
         reply="Thank you for your review and allowing me to help you. I appreciate it "
               "very much and always ready to help with any of your needs."),
    dict(name="Marsha Jefferson", meta="9 reviews", when="A year ago",
         body='Rickey did an awesome job repairing our home. We have a new build, 2 '
              'years after hurricane winds blew water into our home from the joints '
              'outside of the house every year! After years of inspections and such- '
              'Rickey fixed the problem. He did a great job and stayed in constant '
              'communication! We definitely recommend his services!',
         reply="I appreciate your review very much glad we could help take care of issues"),
    dict(name="N Roe", meta="4 reviews", when="A year ago",
         body='Rick showed up when he said he would, stayed until the job was done, '
              'clean up completely and charged a fair price. The job required '
              'cooperation with another vendor and required a reconfiguration element '
              'that was tricky. I appreciated R&amp;R '
              '<span class="trunc">… [review continues on Google]</span>',
         reply="I appreciate the review very much appreciate you giving us the "
               "opportunity to help you look forward to helping you in the future"),
]

# Work records. Every stage is drawn from the named review, nothing is
# reconstructed. Photographs are placeholder stock and labelled as such.
PROJECTS = [
    dict(
        no="01", kind="Sliding door replaced", when="Two months ago",
        title="A slider out, a glazed French pair in, same opening and same day.",
        problem="An old two-panel sliding door between the house and the garden. The "
                "customer wanted it gone.",
        found="A single opening that had to take a completely different door, so the "
              "frame and the fixings had to change with it.",
        did="Removed the slider, fitted a French door in the same opening, and put up "
            "lights while on site.",
        result="Finished the same day. The customer called the price reasonable and the "
               "work trustworthy.",
        img="french-left", w=960, h=1516, ratio="fig-3x2",
        alt="A glazed French door pair standing open onto a garden",
        cap="A glazed French pair, the usual replacement for a worn slider",
        rev=0,
    ),
    dict(
        no="02", kind="Water intrusion", when="A year ago",
        title="Two years of storm water, and rounds of inspections that found nothing.",
        problem="A two-year-old new build. Every year, hurricane winds drove water into "
                "the house through the joints on the outside.",
        found="Years of inspections had not located it, because the leak only appears in "
              "wind-driven rain. The path mattered, not the stain.",
        did="Traced the route the water was actually taking and repaired it, keeping the "
            "customer informed throughout.",
        result="The problem stopped. The customer recommends the service without "
               "qualification.",
        img="exterior-found", w=960, h=1427, ratio="fig-3x2",
        alt="A worker on a ladder repairing the exterior joints of a house",
        cap="Exterior joints, the usual route for wind-driven water",
        rev=1,
    ),
    dict(
        no="03", kind="Reconfiguration", when="A year ago",
        title="Two trades on one site, and a reconfiguration that was not straightforward.",
        problem="A job that needed cooperation with another vendor, and a layout change "
                "the customer described as tricky.",
        found="Not a like-for-like swap. The reconfiguration had to be worked out rather "
              "than simply installed.",
        did="Coordinated with the other vendor, carried out the reconfiguration, and "
            "stayed until the job was finished.",
        result="Showed up when promised, cleaned up completely, and charged a fair price.",
        img="reno-found", w=960, h=640, ratio="fig-3x2",
        alt="A room part-way through renovation with ladders and materials",
        cap="A room mid-reconfiguration",
        rev=2,
    ),
]

FAQS = [
    ("Are you really open 24 hours?",
     "Those are the hours listed on our Google profile. Water coming into a house does "
     "not wait for business hours, and neither does the phone."),
    ("Will you take a job that is genuinely small?",
     "Yes. Small jobs are the most mentioned kind of work across our reviews, counted "
     "five times. It is the work most people struggle to get anyone to turn up for."),
    ("What if other people have already failed to fix it?",
     "That is often the better job to call about. One customer's house had taken on "
     "storm water for two years, through rounds of inspections, before we found the "
     "path it was taking."),
    ("Can you work with another contractor on site?",
     "Yes, and we have. One job required exactly that, plus a reconfiguration the "
     "customer described as tricky."),
    ("Do you quote before starting?",
     "Yes. “Fair price” and “reasonable price” are the two phrases "
     "that recur most across the reviews, and both depend on the number coming first."),
    ("Where do you work?",
     "Orlando and the surrounding area, working out of Beggs Road in 32810. Confirm "
     "your address with us when you call."),
]


# ── shared chrome ─────────────────────────────────────────────────────────
def head(page, title, desc, extra=""):
    canon = f"{BASE}/{page}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta name="theme-color" content="#EDEDEA" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#101416" media="(prefers-color-scheme: dark)">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="assets/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">

<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{BASE}/assets/og-card.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{NAME}, renovation and restoration handyman services in Orlando, Florida">
<meta name="twitter:card" content="summary_large_image">

<!-- Only the body serif is preloaded. It renders the hero paragraph, which is
     the largest-contentful-paint element on most pages. Preloading the 77KB
     Bricolage variable file alongside it made the two compete and pushed LCP
     out, so the display face loads at its normal priority. -->
<link rel="preload" href="assets/fonts/spectral-400-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/site.css?v=7">
{extra}</head>
<body>

<a class="skip" href="#main">Skip to content</a>
"""


def masthead(current):
    items = "\n".join(
        f'      <li><a href="{h}"{" aria-current=\"page\"" if h == current else ""}>{t}</a></li>'
        for h, t in NAV)
    return f"""
<header class="masthead">
  <div class="mast-top">
    <a class="mast-brand" href="index.html">
      <span class="mast-rr">R&amp;R</span>
      <span class="mast-full">{NAME_LEGAL}</span>
    </a>
    <div class="mast-meta">
      <a class="ph" href="tel:{TEL}">{PHONE}</a>
      <span class="mast-open">{HOURS}</span>
      <span class="mast-where">{CITY}, Florida</span>
    </div>
  </div>
  <nav class="mast-nav" aria-label="Main">
    <ul>
{items}
    </ul>
  </nav>
</header>
"""


def mobile_bar():
    """Fixed bottom actions under 768px. Calling takes the filled half."""
    return f"""
<nav class="mobile-bar" aria-label="Quick actions">
  <a class="mb-call" href="tel:{TEL}">{ico(I_PHONE, 18)}Call Now</a>
  <a class="mb-est" href="contact.html#estimate">{ico(I_NOTE, 18)}Request Estimate</a>
</nav>
"""


def footer():
    return f"""
<footer class="foot">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <h2>{NAME}</h2>
        <p>{NAME_LEGAL}</p>
        <p>{CITY}, Florida. {HOURS_LONG}.</p>
      </div>
      <div>
        <h2>Pages</h2>
        <ul>
          <li><a href="services.html">Services</a></li>
          <li><a href="cases.html">Our Work</a></li>
          <li><a href="reviews.html">Reviews</a></li>
          <li><a href="contact.html">Contact</a></li>
          <li><a href="contact.html#estimate">Request an Estimate</a></li>
        </ul>
      </div>
      <div>
        <h2>Reach us</h2>
        <ul>
          <li><a href="tel:{TEL}">{PHONE}</a></li>
          <li><a href="{MAPS}" target="_blank" rel="noopener">{STREET}<br>{CITY}, {REGION} {ZIP}</a></li>
          <li>{HOURS_LONG}</li>
          <li><a href="{GOOGLE}" target="_blank" rel="noopener">Read all Google reviews</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-legal">
      <p>{NAME_LEGAL} Plus code {PLUSCODE}.</p>
      <p>Reviews quoted verbatim from our Google Business profile, rating and counts current as of September 2026. Photographs are representative of the work, not records of the jobs described.</p>
    </div>
  </div>
</footer>

{mobile_bar()}
</body>
</html>
"""


def ldjson_business():
    """Only verified fields. No aggregateRating: the 4.8 is real but was
    collected on Google, and marking up reviews gathered on another platform is
    against Google's structured-data guidelines, which the brief also requires
    compliance with."""
    return f"""
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "HomeAndConstructionBusiness",
  "@id": "{BASE}/#business",
  "name": "Renovation & Restoration Handyman Services L.L.C.",
  "alternateName": "R&R Handyman",
  "url": "{BASE}/",
  "telephone": "+1-407-401-0184",
  "address": {{
    "@type": "PostalAddress",
    "streetAddress": "{STREET}",
    "addressLocality": "{CITY}",
    "addressRegion": "{REGION}",
    "postalCode": "{ZIP}",
    "addressCountry": "US"
  }},
  "areaServed": {{ "@type": "City", "name": "Orlando" }},
  "sameAs": ["{GOOGLE.replace('&amp;', '&')}"],
  "openingHoursSpecification": [{{
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
    "opens": "00:00",
    "closes": "23:59"
  }}],
  "makesOffer": [
{chr(10).join('    { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "%s" } }%s'
              % (s["name"], "," if i < len(SERVICES) - 1 else "")
              for i, s in enumerate(SERVICES))}
  ]
}}
</script>
"""


def picture(stem, widths, jpg_w, jpg_h, alt, cls, sizes, eager=False, cap=None, rep=False):
    """<picture> with WebP sources and the resized JPEG as fallback. Explicit
    width and height on the <img> so nothing shifts while it loads."""
    srcset = ", ".join(f"assets/img/{stem}-{w}.webp {w}w" for w in widths)
    load = ('fetchpriority="high" decoding="async"' if eager
            else 'loading="lazy" decoding="async"')
    inner = (f'<picture>\n'
             f'    <source type="image/webp" srcset="{srcset}" sizes="{sizes}">\n'
             f'    <img src="assets/img/{stem}.jpg" width="{jpg_w}" height="{jpg_h}" '
             f'alt="{alt}" {load}>\n'
             f'  </picture>')
    if cls is None:
        return inner
    bits = [f'<figure class="{cls}">', "  " + inner]
    if cap:
        bits.append(f'  <figcaption>{cap}</figcaption>')
    if rep:
        bits.append(f'  <p class="repflag">{ico(I_INFO, 13)}Representative photo, '
                    f'not this customer\'s home</p>')
    bits.append("</figure>")
    return "\n".join(bits)


def service_cards(long=False, level=3):
    """`level` keeps the heading order unbroken: on the home page the cards sit
    under an h2 so they are h3, while on the services page the h1 is the
    section heading so the cards are h2."""
    out = ['<div class="cards">']
    for s in SERVICES:
        egs = "\n".join(f"          <li>{e}</li>" for e in s["eg"])
        out.append(f"""      <article class="card" id="{s['id']}">
        {ico(SERVICE_ICONS[s['id']], 34, cls="card-ico")}
        <h{level}>{s['name']}</h{level}>
        <p>{s['long'] if long else s['short']}</p>
        <ul class="card-eg">
{egs}
        </ul>
        <p class="card-src">{s['src']}</p>
        <a class="card-call" href="tel:{TEL}">{ico(I_PHONE, 16)}Call About This Service</a>
      </article>""")
    out.append(f'      <p class="card-note">{REGULATED_NOTE}</p>')
    out.append("    </div>")
    return "\n".join(out)


def why_list():
    items = "\n".join(
        f"""      <li>{ico(I_TICK, 22)}<div>
        <h3>{t}</h3>
        <p>{b}</p>
      </div></li>""" for t, b in WHY)
    return f'<ul class="why">\n{items}\n    </ul>'


def trust_row():
    return f"""<ul class="trust">
          <li>{ico(I_STAR, 17)}<a href="{GOOGLE}" target="_blank" rel="noopener">{RATING}-star Google rating</a></li>
          <li>{ico(I_CHAT, 17)}{REVIEWS} customer reviews</li>
          <li>{ico(I_PIN, 17)}Serving {CITY}, Florida</li>
          <li>{ico(I_TICK, 17)}Small jobs welcome</li>
        </ul>"""


def cta_band(img, heading, body, second_label, second_href):
    return f"""
  <section class="band-photo">
    <picture>
      <source type="image/webp" srcset="assets/img/{img}-1000.webp">
      <img src="assets/img/{img}.jpg" width="1000" height="667" alt="" aria-hidden="true" loading="lazy" decoding="async">
    </picture>
    <span class="veil"></span>
    <div class="wrap section">
      <h2 class="h-section measure-tight">{heading}</h2>
      <p class="lede measure-tight" style="margin-top: 18px">{body}</p>
      <div class="btn-row" style="margin-top: 30px">
        <a class="btn btn-green" href="tel:{TEL}">{ico(I_PHONE, 17)}Call {PHONE}</a>
        <a class="btn btn-line-light" href="{second_href}">{second_label}</a>
      </div>
    </div>
  </section>
"""


# ── pages ─────────────────────────────────────────────────────────────────
def page_index():
    hero_img = picture(
        "hero", [480, 700, 900], 900, 1200,
        "A sunlit living room with glass doors opening onto a lawn",
        None, "(min-width: 900px) 42vw, calc(100vw - 2 * clamp(18px, 5vw, 60px))",
        eager=True)
    return (
        head("index.html",
             f"Handyman in Orlando, FL | {NAME}",
             "Reliable handyman repairs in Orlando: doors, lighting, irrigation, water "
             f"intrusion and small jobs. {RATING} stars across {REVIEWS} Google reviews. "
             f"Call {PHONE}.",
             extra=ldjson_business())
        + masthead("index.html")
        + f"""
<main id="main">

  <section class="wrap hero">
    <div class="hero-grid">
      <div>
        <h1 class="display">We fix what other people already tried to fix.</h1>
        <p class="lede measure" style="margin-top: 22px">Reliable handyman repairs for doors, lighting, irrigation, water intrusion, and the small jobs others will not schedule. Serving Orlando and nearby communities.</p>
        <div class="btn-row" style="margin-top: 28px">
          <a class="btn btn-green" href="tel:{TEL}">{ico(I_PHONE, 17)}Call {PHONE}</a>
          <a class="btn btn-line" href="contact.html#estimate">Request an Estimate</a>
        </div>
        {trust_row()}
      </div>
      <figure class="hero-fig">
        {hero_img}
      </figure>
    </div>
  </section>

  <div class="rule"></div>

  <section class="wrap section">
    <h2 class="h-section measure-tight">Handyman Services We Provide</h2>
    <p class="prose measure" style="margin-top: 16px; margin-bottom: 32px">Six kinds of work. Each one is something customers have named in a Google review, not a list of things we would like to be asked for.</p>
    {service_cards()}
    <div class="btn-row" style="margin-top: 30px">
      <a class="btn btn-line" href="services.html">View All Services</a>
    </div>
  </section>

  <section class="band">
    <div class="wrap section">
      <h2 class="h-section measure-tight">Before &amp; After</h2>
      <p class="lede measure" style="margin-top: 16px; margin-bottom: 30px">Renovation is a choice. Restoration is a repair. Both are in the name because both are in the work.</p>
      <div class="spine">
        <div class="side side-found">
          <p class="side-head">Before</p>
          <div class="side-body">
            <p>Water coming in at the joints every storm. Inspections that found nothing. A slider that sticks. Lights that were never wired. The small job that has sat on the list for two years.</p>
          </div>
        </div>
        <div class="side side-left">
          <p class="side-head">After</p>
          <div class="side-body">
            <p>The cause fixed, not just the symptom. Cleaned up completely. A fair price, agreed first. And steady communication while it happens, which is what reviewers mention most.</p>
          </div>
        </div>
      </div>
      <div class="btn-row" style="margin-top: 28px">
        <a class="btn btn-line-light" href="cases.html">View Our Work</a>
      </div>
    </div>
  </section>

  <section class="wrap section">
    <h2 class="h-section measure-tight">Why Choose R&amp;R?</h2>
    <p class="prose measure" style="margin-top: 16px; margin-bottom: 32px">Five things our customers wrote about us, and nothing we cannot point at.</p>
    {why_list()}
  </section>

  <div class="rule"></div>

  <section class="wrap section">
    <div class="hang">
      <div class="hang-label"><span class="kicker">The work</span></div>
      <div>
        <div class="figs-asym">
          {picture("french-left", [480, 960], 960, 1516,
                   "A glazed French door pair standing open onto a garden",
                   "fig fig-3x2", "(min-width: 820px) 44vw, 100vw",
                   cap="A glazed French pair, the usual replacement for a worn slider",
                   rep=True)}
          {picture("irrigation", [400, 700], 700, 435,
                   "A lawn sprinkler running on green grass",
                   "fig fig-4x3", "(min-width: 820px) 30vw, 100vw",
                   cap="Irrigation, which in Central Florida runs most of the year",
                   rep=True)}
        </div>
      </div>
    </div>
  </section>

  <section class="band">
    <div class="wrap section">
      <h2 class="h-section measure-tight">What customers say</h2>
      <div class="quotes" style="margin-top: 30px">
        <blockquote class="q">“The quality if his work makes him worth every penny.”
          <span class="qby">Google review <span>via our Google Business profile</span></span></blockquote>
        <blockquote class="q">“Fair prices I would recommend him to all my friends and family no question!!”
          <span class="qby">Google review <span>via our Google Business profile</span></span></blockquote>
        <blockquote class="q">“He did a great job and stayed in constant communication!”
          <span class="qby">Marsha Jefferson <span>Google review</span></span></blockquote>
      </div>
      <div class="btn-row" style="margin-top: 28px">
        <a class="btn btn-green" href="{GOOGLE}" target="_blank" rel="noopener">Read All Google Reviews</a>
        <a class="btn btn-line-light" href="reviews.html">Reviews on this site</a>
      </div>
    </div>
  </section>
"""
        + cta_band("interior-left", "Start with the part that has not worked yet.",
                   "One call reaches Rickey. What has already been tried, and what it "
                   "did, is usually the most useful thing you can say.",
                   "Request an Estimate", "contact.html#estimate")
        + "</main>\n" + footer())


def page_services():
    return (
        head("services.html",
             f"Handyman Services in Orlando | {NAME}",
             "Small jobs, door repair and replacement, lighting installation, irrigation "
             "repair, storm damage and water-intrusion diagnosis, and home "
             f"reconfiguration in Orlando, FL. Call {PHONE}.")
        + masthead("services.html")
        + f"""
<main id="main">

  <section class="wrap section-sm">
    <h1 class="h-section measure-tight">Handyman Services We Provide</h1>
    <p class="prose measure" style="margin-top: 16px">Each service below says where it comes from: a customer who named it in a Google review, or one of the topics Google counts across all {REVIEWS}. Nothing here is a service we simply decided to advertise.</p>
  </section>

  <section class="wrap section-sm">
    {service_cards(long=True, level=2)}
  </section>

  <div class="rule"></div>

  <section class="wrap section">
    <div class="hang">
      <div class="hang-label"><span class="kicker">The work</span></div>
      <div>
        <div class="figs-asym">
          {picture("ceiling-work", [480, 900], 900, 1350,
                   "A ceiling being sanded smooth before finishing",
                   "fig fig-3x2", "(min-width: 820px) 44vw, 100vw",
                   cap="Making a ceiling good, the step after a leak is stopped",
                   rep=True)}
          {picture("tools", [400, 700], 700, 1050,
                   "Hand tools and materials laid out on a floor",
                   "fig fig-4x3", "(min-width: 820px) 30vw, 100vw",
                   cap="Small jobs, the list that never justifies a contractor",
                   rep=True)}
        </div>
      </div>
    </div>
  </section>

  <section class="wrap section">
    <h2 class="h-section measure-tight">Why Choose R&amp;R?</h2>
    <p class="prose measure" style="margin-top: 16px; margin-bottom: 32px">Five things our customers wrote about us, and nothing we cannot point at.</p>
    {why_list()}
  </section>
"""
        + cta_band("interior-left", "Not sure which of these it is?",
                   "Then describe what it does and when it does it. Working out which "
                   "service it falls under is our job, not yours.",
                   "View Our Work", "cases.html")
        + "</main>\n" + footer())


def page_cases():
    blocks = []
    for p in PROJECTS:
        r = REVIEWS_DATA[p["rev"]]
        quote = re.sub(r'<span class="trunc">.*?</span>', "", r["body"])
        quote = quote.replace("<br>", " ").strip()
        blocks.append(f"""      <article class="project">
        <div class="pj-head">
          <p class="pj-meta">Project {p['no']} &nbsp;{p['kind']}, {p['when'].lower()}</p>
          <h2 class="h-sub">{p['title']}</h2>
        </div>
        <div class="pj-body">
          <div>
            <dl class="stages">
              <div class="stage is-before">
                <dt>The problem</dt>
                <dd>{p['problem']}</dd>
              </div>
              <div class="stage is-before">
                <dt>What we found</dt>
                <dd>{p['found']}</dd>
              </div>
              <div class="stage">
                <dt>Work completed</dt>
                <dd>{p['did']}</dd>
              </div>
              <div class="stage">
                <dt>Result</dt>
                <dd>{p['result']}</dd>
              </div>
            </dl>
            <blockquote class="quote-card" style="margin-top: 26px">
              {quote}
              <cite>{r['name']}<span class="gsrc">Google review, {r['meta']}</span></cite>
            </blockquote>
          </div>
          {picture(p['img'], [480, 960], p['w'], p['h'], p['alt'],
                   f"fig {p['ratio']}", "(min-width: 900px) 30vw, 100vw",
                   cap=p['cap'], rep=True)}
        </div>
      </article>""")
    body = "\n\n      <div class=\"rule\"></div>\n\n".join(blocks)
    return (
        head("cases.html",
             f"Our Work: Handyman Projects in Orlando | {NAME}",
             "Three Orlando handyman projects written up as the problem, what we found, "
             "the work completed and the result, each with the customer's own Google "
             "review.")
        + masthead("cases.html")
        + f"""
<main id="main">

  <section class="wrap section-sm">
    <h1 class="h-section measure-tight">Our Work</h1>
    <p class="prose measure" style="margin-top: 16px">Three jobs our customers described in enough detail to write up. Every stage below comes from the customer's own Google review, and each record carries that review underneath it.</p>
    <p class="prose measure" style="margin-top: 14px">The photographs on this page are stock images that show the kind of work described. They are not photographs of these customers' homes, and each one says so. Real project photographs will replace them.</p>
  </section>

  <div class="rule-heavy"></div>

  <section class="wrap section">
    <div class="projects">
{body}
    </div>
  </section>

  <div class="rule-heavy"></div>

  <section class="wrap section-sm">
    <p class="prose measure">Three of {REVIEWS} reviews described their job in enough detail to record. The other twenty-one are just as real, and mostly say “great work, fair price” and leave it there. All of them are on the <a href="reviews.html">reviews page</a>.</p>
  </section>
"""
        + cta_band("interior-left", "Got one that nobody has solved yet?",
                   "Those are the ones worth calling about. Tell us what it does, when "
                   "it does it, and what has already been tried.",
                   "Request an Estimate", "contact.html#estimate")
        + "</main>\n" + footer())


def page_reviews():
    entries = []
    for r in REVIEWS_DATA:
        entries.append(f"""      <article class="entry">
        <div class="entry-by">
          <h3 class="entry-name">{r['name']}</h3>
          <p class="entry-stars" aria-label="Rated 5 out of 5">★★★★★</p>
          <p class="entry-meta">{r['meta']}<br>{r['when']}</p>
          <p class="gsrc">Google review</p>
        </div>
        <div class="entry-body">
          <p>{r['body']}</p>
          <div class="reply">
            <p class="rl">Response from the owner, {r['when'].lower()}</p>
            <p>{r['reply']}</p>
          </div>
        </div>
      </article>""")
    topics = [("reviews mention small jobs", "5"),
              ("mention sliding door replacement", "2"),
              ("mention irrigation repair and maintenance", "2"),
              ("mention lighting installation", "2")]
    tp = "\n".join(f'      <div class="topic"><dt>{t}</dt><dd class="num">{n}</dd></div>'
                   for t, n in topics)
    return (
        head("reviews.html",
             f"Reviews: {RATING} Stars from {REVIEWS} Customers | {NAME}",
             f"{RATING} stars across {REVIEWS} Google reviews for our Orlando handyman "
             "service, quoted exactly as written, with the owner's replies in full.")
        + masthead("reviews.html")
        + f"""
<main id="main">

  <section class="wrap section-sm">
    <h1 class="h-section measure-tight">Customer Reviews</h1>
    <p class="prose measure" style="margin-top: 16px">Quoted exactly as written, typos included. Where Google shortens a long review we mark the cut rather than papering over it, and Rickey's replies are shown in full underneath each one.</p>

    <!-- The rating is set as type. Five filled stars cannot represent 4.8,
         and drawing five anyway would overstate it. -->
    <div class="rating" style="margin-top: 36px">
      <div style="display: flex; align-items: flex-end; gap: 12px">
        <p class="rating-score num">{RATING}</p>
        <p class="rating-of">out of 5</p>
      </div>
      <p class="rating-meta">Across {REVIEWS} Google reviews. Google publishes the average and the total but not the count for each star, so no distribution is shown here.</p>
    </div>
    <div class="btn-row" style="margin-top: 28px">
      <a class="btn btn-green" href="{GOOGLE}" target="_blank" rel="noopener">Read All Google Reviews</a>
    </div>
  </section>

  <div class="rule"></div>

  <section class="wrap section-sm">
    <h2 class="h-sub">What comes up most</h2>
    <dl class="topics" style="margin-top: 24px">
{tp}
    </dl>
    <p class="fine" style="margin-top: 22px">Google lists six further topics beyond these four.</p>
  </section>

  <section class="band">
    <div class="wrap section-sm">
      <h2 class="h-sub" style="margin-bottom: 26px">The lines Google pulls out</h2>
      <div class="quotes">
        <blockquote class="q">“The quality if his work makes him worth every penny.”
          <span class="qby">Google review <span>via our Google Business profile</span></span></blockquote>
        <blockquote class="q">“Fair prices I would recommend him to all my friends and family no question!!”
          <span class="qby">Google review <span>via our Google Business profile</span></span></blockquote>
        <blockquote class="q">“He did a great job and stayed in constant communication!”
          <span class="qby">Marsha Jefferson <span>Google review</span></span></blockquote>
      </div>
    </div>
  </section>

  <section class="wrap section">
    <h2 class="h-sub">Three reviews in full</h2>
    <div class="entries" style="margin-top: 24px">

{chr(10).join(entries)}

    </div>
    <p class="fine" style="margin-top: 26px">Twenty-one more are on the Google listing.</p>
    <div class="btn-row" style="margin-top: 20px">
      <a class="btn btn-green" href="{GOOGLE}" target="_blank" rel="noopener">Read All Google Reviews</a>
      <a class="btn btn-line" href="cases.html">View Our Work</a>
    </div>
  </section>
"""
        + cta_band("interior-left", "Make it twenty-five.",
                   "One call reaches Rickey, any hour. A fair price agreed first, and "
                   "cleaned up after.",
                   "Request an Estimate", "contact.html#estimate")
        + "</main>\n" + footer())


def page_contact():
    faq_html = "\n".join(f"""      <div class="faq-item">
        <h3>{q}</h3>
        <p>{a}</p>
      </div>""" for q, a in FAQS)
    faq_ld = ",\n".join("""    {
      "@type": "Question",
      "name": %s,
      "acceptedAnswer": { "@type": "Answer", "text": %s }
    }""" % (_json(q), _json(a)) for q, a in FAQS)
    opts = "\n".join(f'            <option value="{s["name"]}">{s["name"]}</option>'
                     for s in SERVICES)
    extra = ldjson_business() + f"""
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
{faq_ld}
  ]
}}
</script>
"""
    return (
        head("contact.html",
             f"Contact and Request an Estimate | {NAME}",
             f"Call {PHONE}, {HOURS.lower()}. {STREET}, {CITY}, {REGION} {ZIP}. Request "
             "an estimate, see what to have ready, and read answers to common questions.",
             extra=extra)
        + masthead("contact.html")
        + f"""
<main id="main">

  <section class="band">
    <div class="wrap section">
      <h1 class="h-section measure-tight">Tell us what it is doing.</h1>
      <p class="lede measure" style="margin-top: 18px">One call reaches Rickey, not an office and not a queue. Say what the problem does, when it does it, and what has already been tried. That last part is usually the most useful thing you can tell us.</p>
      <div class="btn-row" style="margin: 28px 0 42px">
        <a class="btn btn-green" href="tel:{TEL}">{ico(I_PHONE, 17)}Call {PHONE}</a>
        <a class="btn btn-line-light" href="{MAPS}" target="_blank" rel="noopener">Get directions</a>
      </div>

      <div class="particulars">
        <div><p class="k">Address</p><p class="v">{STREET}<br>{CITY}, {REGION} {ZIP}</p></div>
        <div><p class="k">Telephone</p><p class="v"><a href="tel:{TEL}">{PHONE}</a></p></div>
        <div><p class="k">Hours</p><p class="v">{HOURS_LONG}</p></div>
        <div><p class="k">Plus code</p><p class="v">{PLUSCODE} {CITY}, Florida</p></div>
        <div><p class="k">Rating</p><p class="v">{RATING} across {REVIEWS} Google reviews</p></div>
        <div><p class="k">Service area</p><p class="v">{CITY} and nearby communities</p></div>
      </div>
    </div>
  </section>

  <section class="wrap section" id="estimate">
    <h2 class="h-section measure-tight">Request an Estimate</h2>
    <p class="prose measure" style="margin-top: 16px">Tell us what needs repair and what has already been tried. We will contact you to discuss the next step.</p>

    <div class="notice" style="margin-top: 26px; max-width: 660px">
      <strong>This form is not accepting submissions yet</strong>
      <p>It is not connected to anything, so nothing you type here is sent or stored. To reach us now, <a href="tel:{TEL}">call {PHONE}</a>. The phone is answered directly.</p>
    </div>

    <!-- ══════════════════════════════════════════════════════════════════
         DEVELOPER: NO FORM ENDPOINT IS CONFIGURED.

         The interface below is complete and accessible, but deliberately
         inert. Before relying on it:

           1. Add a form-handling endpoint. Any service that posts a plain
              HTML form works, for example Formspree, Basin, Netlify Forms
              or a small serverless function.
           2. Put the endpoint on the <form> tag:
                <form action="https://ENDPOINT" method="post" ...>
           3. Remove the `disabled` attribute from the submit button and
              delete the .notice block above.
           4. Add server-side validation and a spam check. Do not rely on
              the client-side `required` attributes alone.
           5. Confirm where submissions are delivered and that the address
              is monitored, given the 24-hour hours claim.

         DO NOT commit API keys, tokens or private email addresses into this
         repository. It is a public GitHub Pages repo. Use an endpoint URL
         that is safe to expose, or move submission behind a function that
         keeps the secret server-side.

         PHOTOGRAPH UPLOAD: intentionally omitted. The brief allows an upload
         field only if the chosen form service supports secure uploads. Once
         one is configured, add:
           <div class="field field-wide">
             <label for="photos">Photographs <span class="opt">(optional)</span></label>
             <input type="file" id="photos" name="photos" accept="image/*" multiple>
             <p class="hint" id="photos-hint">A photo of the stain, gap, fitting or
               model plate helps a lot.</p>
           </div>
         and add enctype="multipart/form-data" to the <form> tag.
         ══════════════════════════════════════════════════════════════════ -->
    <form class="form" novalidate>
      <div class="form-grid">
        <div class="field">
          <label for="name">Your name</label>
          <input type="text" id="name" name="name" autocomplete="name" required aria-describedby="name-err">
          <p class="err" id="name-err" hidden>Please enter your name.</p>
        </div>
        <div class="field">
          <label for="phone">Phone number</label>
          <input type="tel" id="phone" name="phone" autocomplete="tel" required aria-describedby="phone-hint">
          <p class="hint" id="phone-hint">The fastest way for us to reach you.</p>
        </div>
        <div class="field">
          <label for="email">Email address <span class="opt">(optional)</span></label>
          <input type="email" id="email" name="email" autocomplete="email" aria-describedby="email-hint">
          <p class="hint" id="email-hint">Only needed if you would rather not be called.</p>
        </div>
        <div class="field">
          <label for="where">Service address or ZIP code</label>
          <input type="text" id="where" name="where" autocomplete="street-address" required aria-describedby="where-hint">
          <p class="hint" id="where-hint">So we can confirm the job is in our area.</p>
        </div>
        <div class="field field-wide">
          <label for="service">Type of service</label>
          <select id="service" name="service" required>
            <option value="">Choose the closest match</option>
{opts}
            <option value="Not sure">Not sure, please advise</option>
          </select>
        </div>
        <div class="field field-wide">
          <label for="details">What needs repair, and what has already been tried</label>
          <textarea id="details" name="details" required aria-describedby="details-hint"></textarea>
          <p class="hint" id="details-hint">What it does, when it does it, and anything anyone has already attempted. If inspections found nothing, that is useful information.</p>
        </div>
        <fieldset class="fieldset">
          <legend>Preferred contact method</legend>
          <div class="radios">
            <label><input type="radio" name="contact" value="Phone call" required> Phone call</label>
            <label><input type="radio" name="contact" value="Text message"> Text message</label>
            <label><input type="radio" name="contact" value="Email"> Email</label>
          </div>
        </fieldset>
      </div>
      <div class="btn-row">
        <button class="btn btn-green" type="submit" disabled>Send Estimate Request</button>
        <a class="btn btn-line" href="tel:{TEL}">{ico(I_PHONE, 17)}Call {PHONE}</a>
      </div>
      <p class="hint">If you have photographs of the problem, mention it when we speak and we will tell you where to send them.</p>
    </form>
  </section>

  <div class="rule"></div>

  <section class="wrap section">
    <h2 class="h-sub measure-tight">Four things worth having ready</h2>
    <p class="prose measure" style="margin-top: 14px; margin-bottom: 28px">None of these are required, so call and we will work it out. But having them shortens the visit, and sometimes removes the need for a first visit at all.</p>
    <ul class="ticks measure">
      <li>{ico(I_TICK, 20)}<span><b>What it does, and when.</b> “Only after heavy rain” or “only when the sprinklers run” narrows a diagnosis faster than anything else.</span></li>
      <li>{ico(I_TICK, 20)}<span><b>What has already been tried.</b> Including by other people. If inspections found nothing, that is information, not embarrassment.</span></li>
      <li>{ico(I_TICK, 20)}<span><b>A photo, if you can.</b> The stain, the gap, the fitting, or the model plate on the unit.</span></li>
      <li>{ico(I_TICK, 20)}<span><b>Whether anyone else is involved.</b> Another vendor, a builder still under warranty, or an insurer. We have worked alongside all three.</span></li>
    </ul>
  </section>

  <div class="rule"></div>

  <section class="wrap section">
    <h2 class="h-sub" style="margin-bottom: 30px">Questions we get most</h2>
    <div class="faq">
{faq_html}
    </div>
    <p class="fine" style="margin-top: 28px">Confirm the exact service-area boundary with us before relying on it.</p>
  </section>
"""
        + cta_band("interior-left", "Clean up completely, charge a fair price.",
                   "A customer's own description of how their job ended. That is the "
                   "standard.",
                   "View Our Work", "cases.html")
        + "</main>\n" + footer())


def page_404():
    links = "\n".join(f'      <li><a href="{h}">{t}</a></li>' for h, t in NAV)
    return (
        head("404.html", f"Page not found | {NAME}",
             "That page does not exist. Find our handyman services, work, reviews and "
             f"contact details, or call {PHONE}.")
        + masthead("")
        + f"""
<main id="main">
  <section class="wrap oops">
    <p class="code num">404</p>
    <h1 class="h-section measure-tight">That page does not exist.</h1>
    <p class="lede measure">The link may be out of date, or the address may have a typo in it. Everything on the site is one of these:</p>
    <ul class="oops-links">
{links}
    </ul>
    <div class="btn-row" style="margin-top: 10px">
      <a class="btn btn-green" href="tel:{TEL}">{ico(I_PHONE, 17)}Call {PHONE}</a>
      <a class="btn btn-line" href="index.html">Back to the home page</a>
    </div>
  </section>
</main>
"""
        + footer())


def _json(s):
    """Minify entity-bearing copy into a JSON string literal."""
    t = (s.replace("&amp;", "&").replace("&quot;", '"')
          .replace("“", '"').replace("”", '"'))
    return '"' + t.replace("\\", "\\\\").replace('"', '\\"') + '"'


def robots():
    return f"""User-agent: *
Allow: /

Sitemap: {BASE}/sitemap.xml
"""


def sitemap():
    urls = "\n".join(
        f"  <url>\n    <loc>{BASE}/{h}</loc>\n    <changefreq>monthly</changefreq>\n"
        f"    <priority>{'1.0' if h == 'index.html' else '0.8'}</priority>\n  </url>"
        for h, _ in NAV)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
"""


PAGES = {
    "index.html": page_index,
    "services.html": page_services,
    "cases.html": page_cases,
    "reviews.html": page_reviews,
    "contact.html": page_contact,
    "404.html": page_404,
}

if __name__ == "__main__":
    for fn, fx in PAGES.items():
        p = os.path.join(ROOT, fn)
        io.open(p, "w", encoding="utf-8", newline="\n").write(fx())
        print(f"wrote {fn} ({os.path.getsize(p) / 1024:.1f} KB)")
    for fn, fx in (("robots.txt", robots), ("sitemap.xml", sitemap)):
        p = os.path.join(ROOT, fn)
        io.open(p, "w", encoding="utf-8", newline="\n").write(fx())
        print(f"wrote {fn}")
