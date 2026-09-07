# R&R Handyman

Marketing site for Renovation & Restoration Handyman Services L.L.C., Rickey's
handyman and restoration business in Orlando, Florida. 4.8 stars across 24
Google reviews.

- **Address** 6402 Beggs Rd, Orlando, FL 32810
- **Phone** (407) 401-0184
- **Hours** Open 24 hours
- **Plus code** JGGQ+52 Orlando, Florida

Static HTML, no build step, no JavaScript. Google Fonts is the only external
request.

## Pages

| File | Contents |
| --- | --- |
| `index.html` | Hero, tally, door elevation, the spine, six services, photographs, quotes, closing call |
| `services.html` | Each of the six lines in full, with its source. Anchors `#small-jobs` `#doors` `#lighting` `#irrigation` `#storm` `#reconfiguration` |
| `cases.html` | Three documented jobs written up as as-found and as-left |
| `reviews.html` | Reviews verbatim with owner replies, rating, topic counts |
| `contact.html` | Particulars, what to have ready, FAQ |

## Design

Identity: **as found, as left.** The business restores things, so the site is
built as a set of case records with a before/after spine.

### Two accents, one rule

- **oxide `#A65A32`** is the condition found
- **restoration green `#2F6B4F`** is the condition left

Green is the **only interactive colour on the site**: every link, button, focus
ring and active state. Oxide is **semantic state only** and never appears on
anything a visitor can click. Both sit on a plaster ground `#EDEDEA` with a
slate `#14181A` for bands. Dark mode lightens both accents, so `--on-green`
darkens with them to keep the primary button at AA contrast.

### Type

Inverts the usual pairing: **Bricolage Grotesque** (variable, `opsz`) as a
grotesque *display* over **Spectral** as a serif *body*. The serif is earned by
the newspaper-masthead concept rather than reached for as a shortcut to looking
editorial.

### Structure

A newspaper-style masthead (brand, a rule, then nav) over **five layout
families**, arranged so no two consecutive sections on the overview page share
a shape:

| Family | Where |
| --- | --- |
| `.hero` | asymmetric split, copy beside a photograph |
| `.plate` | one centred drawing, nothing beside it |
| `.tally` | rule-bounded numeric strip |
| `.hang` | hanging label left, content right |
| `.svc` / `.faq` | two-column peer grid, no dividers |

The signature component is `.spine`: a two-up panel with an oxide side and a
green side.

Radius is 0 everywhere. The availability dot is the single exception.

### Original drawn graphic

A **before/after door elevation**, on the overview page and again inside Case
01. It records the change Sonia Agosto describes in her review, a two-panel
slider removed and a glazed French pair fitted in the same opening, with swing
shown the way an elevation shows it and glazing bars drawn in. Its caption says
outright that it is drawn from the review rather than from a site survey.

## House rules

These are the constraints the site is built to, and the reasons for them. They
exist because a page can be technically fine and still read as machine-written.

- **No em-dash or en-dash anywhere.** Not in headlines, labels, buttons, body
  copy, quotes, attribution, captions or alt text. Sentences get restructured
  instead: a period, a comma, parentheses or a colon.
- **No middle dot as a general separator.** At most one per line, and currently
  zero site-wide. Metadata goes in columns or on its own line.
- **Eyebrows are rationed** at one per three sections. Over budget they get
  deleted, not restyled. Currently 2 of a possible 3 on the overview page.
- **No section numbering as decoration.** `01 / 02 / 03` beside a section
  label, above a list row or beside a pull quote is gone. Case numbers stay,
  because a case number is a record identifier.
- **No decorative status dots** and no infinite loops. There is exactly one dot,
  in the masthead, and it carries real state: the listing is open every hour. It
  does not pulse, because a pulse on a permanently true fact says nothing.
- **One CTA label per intent, site-wide.** Calling is always
  "Call (407) 401-0184". Each internal destination has one label and keeps it on
  every page.
- **Long lists get the right component.** Six services and six questions are
  two-column peer grids, not rows with a hairline under each one.
- **Only figures that are figures.** A postcode set in 44px display type is not
  a statistic, and neither is repeating the opening hours already in the
  masthead. The three tally figures all trace to the Google profile.
- **The rating is set as type, not as stars.** Five filled stars cannot
  represent 4.8, and drawing five anyway overstates the rating. Individual
  reviews keep five stars, because each of those genuinely is five.

## Honesty

Everything factual traces to the Google Business profile:

| Claim | Source |
| --- | --- |
| 4.8 / 24 reviews | Google profile |
| small jobs, five times | Google review topic, most counted |
| sliding door replacement, twice | Google review topic |
| irrigation repair & maintenance, twice | Google review topic |
| lighting installation, twice | Google review topic |
| Storm damage & water intrusion | Marsha Jefferson's review |
| Reconfiguration & trade coordination | N Roe's review |

Reviews are quoted verbatim including original spelling. The highlight quote
"The quality **if** his work makes him worth every penny" keeps its typo,
because correcting a customer's words would be falsifying them. Truncations are
marked. Rickey's three replies are shown in full.

No star distribution is displayed: Google publishes the 4.8 average and the 24
total but not the per-star counts.

**No `aggregateRating` in the structured data**, on purpose. The figure is real,
but it was collected on Google, and Google's structured-data guidelines
disallow marking up reviews gathered on another platform as your own. It earns
no rich result and risks a manual action, so the number is stated in the visible
copy instead. `index.html` and `contact.html` carry
`HomeAndConstructionBusiness`; `contact.html` also carries `FAQPage`.

### Photography

**All photography is placeholder stock from Pexels** in `assets/img/`. Because
of that:

- Captions describe what a photograph *shows*. None of them assert that it is
  the job in the record beside it.
- `cases.html` deliberately carries **no photographs at all**, and says so. It
  previously paired two unrelated stock images as one job's before and after,
  which is a false claim to make to a homeowner.
- Both the photograph sections and the footer carry a standing line: photographs
  are representative of the work, not records of the jobs described.

`drywall-work.jpg`, `exterior-found.jpg`, `reno-found.jpg` and
`slider-found.jpg` are currently unreferenced. They are the reserved slots for
real job photographs.

**Real before/after photographs from Rickey would transform this site**, and are
the single highest-value thing left to do. Drop them in, restore the paired
images inside `.spine` on `cases.html`, and write captions that do assert what
they show. Grade and crop are CSS: `.side-found img` desaturates and darkens the
found side, `.side-left img` leaves the left side alone.

## Before launch

- Replace the placeholder photography, per the section above.
- No licensing or insurance claims appear anywhere by design. Add them only
  once verified.
- Confirm the service-area boundary.
- Rating and review counts are current as of September 2026.
- Consider self-hosting the two webfonts to drop the third-party request.

## Checking it

Two scripts were used to verify this build and are worth re-running after edits:
a static pass over the markup (dash ban, dot budget, eyebrow budget, banned
patterns, link and asset integrity, JSON-LD validity, dead CSS, tag balance, CTA
label inventory) and a render pass in a real browser (horizontal overflow,
above-the-fold fit, headline line count, nav on one line, button wrap, and
gutters at 390 / 768 / 1024px, in both colour schemes).

Two bugs that only the render pass caught, both worth knowing about:

- `width` and `height` attributes on `<img>` land as presentational hints, so a
  `height="1500"` survived `width: 100%` and forced the hero photograph to
  1500px tall, cropping it to a ceiling vent. Fixed by `height: auto` on the
  global `img, svg` rule.
- `.section` and `.hero` set padding with the shorthand, which zeroed the inline
  padding `.wrap` supplies, so section content ran to the screen edge at every
  width under 1180px. This one predates the redesign. Fixed by switching those
  rules to `padding-block`.
