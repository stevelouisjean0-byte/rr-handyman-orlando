# R&R Handyman

Marketing site for Renovation & Restoration Handyman Services L.L.C. — Rickey's
handyman and restoration business in Orlando, Florida. 4.8 stars across 24
Google reviews.

- **Address** 6402 Beggs Rd, Orlando, FL 32810
- **Phone** (407) 401-0184
- **Hours** Open 24 hours
- **Plus code** JGGQ+52 Orlando, Florida

## Pages

| File | Contents |
| --- | --- |
| `index.html` | Opener, before/after door elevation, tally, the spine, six services, highlights |
| `services.html` | Each of the six lines in full, with its source |
| `cases.html` | Three documented jobs written up as as-found / as-left |
| `reviews.html` | Reviews verbatim with owner replies, rating, topic counts |
| `contact.html` | Particulars, what to have ready, FAQ |

## Design

Identity: **as found → as left.** The business restores things, so the site is
built as a set of case records with a before/after spine — and the palette
carries the concept rather than decorating it:

- **oxide `#A65A32`** = the condition found
- **restoration green `#2F6B4F`** = the condition left
- on a plaster ground `#EDEDEA` with a slate `#14181A` for bands

Type inverts the usual pairing: **Bricolage Grotesque** (variable, `opsz`) as a
grotesque *display* over **Spectral** as a serif *body*.

Structure is a newspaper-style masthead (brand, then a rule, then nav) over a
hanging-heading grid — labels in a narrow left column, content in a wide right
one. The signature component is `.spine`: a two-up panel with an oxide side and
a green side, used for both prose and photograph pairs.

Original drawn graphic: a **before/after door elevation** on the overview page,
taken from a real documented job — a two-panel slider removed and a glazed
French pair fitted in the same opening, with swing shown the way an elevation
shows it (dashed chevrons to the latch edge) and glazing bars drawn in.

Photographs are chosen as as-found / as-left pairs and graded per side:
the "found" side is desaturated and slightly darkened, the "left" side is not.

Static HTML, no build step, no JavaScript. Google Fonts is the only external
request.

## Reviews and sourcing

Everything factual traces to the Google Business profile:

| Claim | Source |
| --- | --- |
| 4.8 / 24 reviews | Google profile |
| small jobs ×5 | Google review topic (most counted) |
| sliding door replacement ×2 | Google review topic |
| irrigation repair & maintenance ×2 | Google review topic |
| lighting installation ×2 | Google review topic |
| Storm damage & water intrusion | Marsha Jefferson's review |
| Reconfiguration & trade coordination | N Roe's review |

Reviews are quoted verbatim including original spelling — the highlight quote
"The quality **if** his work makes him worth every penny" keeps its typo,
because correcting a customer's words would be falsifying them. Truncations are
marked. Rickey's three replies are shown in full.

No star distribution is displayed: Google publishes the 4.8 average and the 24
total but not the per-star counts.

## Before launch

- Photography is placeholder stock from Pexels in `assets/img/`. Real
  before/after job photos would transform the case records — replace the files
  keeping the filenames; grade and crop are CSS.
- No licensing or insurance claims appear anywhere by design. Add them only
  once verified.
- Confirm the service-area boundary.
- Rating and review counts are current as of September 2026.
