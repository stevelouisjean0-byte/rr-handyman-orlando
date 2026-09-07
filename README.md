# R&R Handyman

Marketing site for Renovation & Restoration Handyman Services L.L.C., Rickey's
handyman and restoration business in Orlando, Florida.

- **Address** 6402 Beggs Rd, Orlando, FL 32810
- **Phone** (407) 401-0184
- **Hours** Open 24 hours (as published on the Google Business profile)
- **Plus code** JGGQ+52 Orlando, Florida
- **Rating** 4.8 across 24 Google reviews, current as of September 2026

Live at <https://stevelouisjean0-byte.github.io/rr-handyman-orlando/>

The deployed site is plain static HTML and CSS. No JavaScript, no runtime
dependencies, no third-party requests at all.

## Goal

Make it easy for an Orlando homeowner to understand what R&R does, trust it,
and get in touch. **Calling is the primary action**, so it is the filled green
button in the hero, in every closing band, on every service card, and in the
left half of the mobile action bar. **Requesting an estimate is secondary**, and
every one of those links lands on `contact.html#estimate`.

## Pages

| File | Contents |
| --- | --- |
| `index.html` | Hero with trust row, six service cards, Before & After, Why Choose R&R, work photographs, customer quotes, closing call |
| `services.html` | The six services in full with sources. Anchors `#small-jobs` `#doors` `#lighting` `#irrigation` `#storm` `#reconfiguration` |
| `cases.html` | "Our Work". Three projects as problem, what we found, work completed, result, plus the customer's review |
| `reviews.html` | Rating, review topics, three reviews verbatim with the owner's replies |
| `contact.html` | Contact details, the Request an Estimate form, what to have ready, FAQ |
| `404.html` | Served by GitHub Pages for any unknown path |

`robots.txt` and `sitemap.xml` are generated alongside them.

## Editing

The pages are **generated**. Shared markup (head metadata, masthead,
navigation, mobile action bar, footer) is written once in `tools/build.py`, so
it cannot drift apart across six files, which is what the brief means by
consistent footer information.

```
python tools/build.py     # rewrites the six .html files, robots.txt, sitemap.xml
```

Edit `tools/build.py` (copy, services, reviews, projects, FAQ) or
`assets/site.css` (all styling), then rerun it and commit the output. Do not
hand-edit the `.html` files; the next build overwrites them.

All facts live in one block at the top of `tools/build.py` under `# FACTS`.
Change the phone number or hours there and every page, the footer, the metadata
and the structured data update together.

## Design

Identity: **before and after.** The business restores things, so the site is
built around paired before/after panels.

### Two accents, one rule

- **oxide `#A65A32`** marks a condition that is not right yet: the Before
  panel, the problem stages on a work record, the not-yet-connected form
  notice. It is **never** used on anything clickable.
- **green `#2F6B4F`** is the only interactive colour on the site. Every link,
  button, focus ring and active state.

On a plaster ground `#EDEDEA`, with slate `#14181A` for bands.

`--green` splits three ways because one green cannot do all three jobs at AA:

| Token | Job | Contrast |
| --- | --- | --- |
| `--green` | interactive text and fills on light | 5.4:1 on plaster |
| `--green-hover` `#245A40` | hover on light, so it goes *darker* | 6.9:1 on plaster |
| `--green-slate` `#4E9E77` | green text on a slate ground, so it goes *lighter* | 5.5:1 on slate |

The single earlier `--green-hi` failed both ways at once: 4.3:1 as a footer
heading on slate, and 3.5:1 as a link hover on plaster.

### Type

Inverts the usual pairing: **Bricolage Grotesque** (variable, `opsz` axis) as a
grotesque *display* over **Spectral** as a serif *body*.

Both are **self-hosted** from `assets/fonts/`, latin subsets, `font-display:
swap`. The previous linked Google Fonts stylesheet was a render-blocking
third-party request costing roughly 930ms of render delay and was the single
largest component of LCP. Only `spectral-400` is preloaded, because it renders
the hero paragraph that is the LCP element; preloading the 77KB Bricolage
variable file alongside it made the two compete and pushed LCP back out.

Both families are SIL Open Font License 1.1. Full licences are in
`assets/fonts/`.

### Layout families

Arranged so no two consecutive sections share a shape: `.hero` (asymmetric
split), `.trust` (verified-claim row), `.cards` (two-column service cards),
`.spine` (paired Before/After panels), `.why` (two-column icon list), `.hang`
(hanging label), `.project` (four-stage record), `.form` (stacked fields).

Service cards are **two** columns rather than three: six cards in a 3-wide grid
is the stock template look, and two columns leaves room for a real description,
real examples and a call link per card.

Radius is 0 everywhere. Icons are simple geometric marks drawn from rects,
circles and short paths at a single 24x24 box and one stroke weight, because
the site ships with no build step for the deployed assets and therefore no icon
package.

### Accessibility

- Every standalone link, button and control is at least 44px tall. Links
  sitting inline inside a sentence keep their text size, which WCAG 2.5.8
  explicitly permits, and a radio's wrapping `<label>` is the real target.
- Focus is always visible. The primary button takes an ink ring rather than the
  default green one, because green-on-green is invisible.
- Form inputs use `--field-border`, 3.6:1 against the field background, to
  satisfy the 1.4.11 non-text contrast rule.
- Labels sit above their control, hints are in the markup, error text is below.
  No placeholder is ever used as a label.
- One `<h1>` per page and unbroken heading order. Card headings are `<h2>` on
  the services page, where the `<h1>` is the section heading, and `<h3>` on the
  home page, where they sit under an `<h2>`.
- Skip link, semantic landmarks, `prefers-reduced-motion`, light and dark modes.

## Honesty

Everything factual traces to the Google Business profile or a named review:

| Claim | Source |
| --- | --- |
| 4.8 / 24 reviews | Google profile |
| small jobs, five times | Google review topic, the most counted |
| sliding door replacement, twice | Google review topic |
| irrigation repair, twice | Google review topic |
| lighting installation, twice | Google review topic |
| storm damage and water intrusion | Marsha Jefferson's review |
| reconfiguration and trade coordination | N Roe's review |

Reviews are quoted verbatim including original spelling. The highlight quote
"The quality **if** his work makes him worth every penny" keeps its typo,
because correcting a customer's words would be falsifying them, and no
explanation is bolted on to it. Truncations are marked. Rickey's replies appear
in full.

No star distribution is shown: Google publishes the average and the total but
not the per-star counts. **The 4.8 aggregate is set as type, not as five filled
stars**, because five stars cannot represent 4.8 and drawing five anyway would
overstate the rating. Individual reviews keep five stars, because each of those
genuinely is five.

### Nothing here is invented

No licensing, bonding, insurance, background checks, certifications, awards,
warranties, guarantees, years in business, project counts, employee
photographs, or fabricated reviews or service areas.

Careful wording is used where trades are regulated: the site says that work
legally requiring a licensed trade is *coordinated with* an appropriately
licensed contractor rather than performed in place of one. Trade coordination
itself is evidenced by N Roe's review.

### No aggregateRating in the structured data

Deliberate. The 4.8 is real, but it was collected on Google, and Google's
structured-data guidelines disallow marking up reviews gathered on another
platform as your own. It earns no rich result and risks a manual action. The
brief also conditions the markup on complying with search-engine requirements,
which it would not. The number is stated in the visible copy instead.

`index.html` and `contact.html` carry `HomeAndConstructionBusiness`;
`contact.html` also carries `FAQPage`.

### Photography

**All photography is placeholder stock from Pexels.** Because of that:

- Captions describe what a photograph *shows*. None claims to be a customer's
  home.
- Every photograph on `cases.html` and in the work sections carries a visible
  **"Representative photo, not this customer's home"** label, placed under the
  image rather than over it.
- The footer carries a standing line saying photographs are representative of
  the work, not records of the jobs described.

Once real photographs exist, label them "Actual R&R project" **only** after the
owner confirms which job each one is from.

### The estimate form is deliberately inert

There is no form-processing endpoint, so:

- The submit button is `disabled` and the `<form>` has no `action`. Nothing can
  be sent.
- A visible notice says the form is not accepting submissions yet and points to
  the phone number.
- A long comment in `tools/build.py` next to the form lists exactly what to do
  to enable it, including not committing keys or tokens to this public repo.
- The optional photograph upload is omitted, per the brief, until a form
  service with secure uploads is chosen. The markup to add is in that comment.

No "free estimate" is promised anywhere, because that has not been confirmed.

## Needed from the owner

Marked with `OWNER TO CONFIRM` in `tools/build.py` where applicable.

1. **Business hours.** The site says "Open 24 hours" everywhere because that is
   what the Google profile publishes, and it is used consistently in the header,
   contact page, footer, metadata and `openingHoursSpecification`. If the
   business does not actually take calls at any hour, change `HOURS` and
   `HOURS_LONG` in `tools/build.py` and rerun. The FAQ answer about 24-hour
   availability needs changing with it.
2. **Real project photographs**, and which job each belongs to. The highest
   value item on this list.
3. **A professional photograph of Rickey.** The "You speak to Rickey directly"
   point would carry far more weight beside a face.
4. **A canonical Google Business profile URL.** Every "Read All Google Reviews"
   link currently points at a Google *search* for the business, which is what
   already existed in the project, not a profile or place URL.
5. **A form endpoint**, then remove the `disabled` attribute and the notice.
6. **Licensing and insurance details**, if any, before any such claim is added.
7. **Years of experience**, if it should be stated.
8. **Cities and ZIP codes served.** The site says "Orlando and nearby
   communities" and asks the visitor to confirm on the call. No specific
   outlying cities or ZIPs are claimed.
9. **Payment methods.**
10. **Confirmation of the regulated-trade wording** described above.

## Performance

Images are resized to their display dimensions and served as WebP through
`<picture>` with a resized JPEG fallback, `srcset`/`sizes`, explicit `width` and
`height`, and `loading="lazy"` below the fold. The hero is never lazy and
carries `fetchpriority="high"`.

The hero went from a single 443KB JPEG to a 37KB / 75KB / 116KB WebP ladder; a
phone now downloads 75KB where it previously took 443KB.

Measured with Lighthouse 12.8.2, mobile, simulated slow 4G with 4x CPU
throttling, against a local server:

| Page | Perf | A11y | Best practices | SEO | LCP | CLS |
| --- | --- | --- | --- | --- | --- | --- |
| index | 96 | 100 | 100 | 100 | 2.41s | 0.051 |
| services | 98 | 100 | 100 | 100 | 2.05s | 0.019 |
| cases | 98 | 100 | 100 | 100 | 2.13s | 0.000 |
| reviews | 98 | 100 | 100 | 100 | 2.21s | 0.019 |
| contact | 98 | 100 | 100 | 100 | 2.11s | 0.019 |
| 404 | 99 | 100 | 100 | 100 | 1.68s | 0.019 |

Inlining the stylesheet was tried and reverted: it removed the last
render-blocking request but a 60KB `<style>` block delayed parsing more,
dropping the home page from 96 to 75 and pushing total blocking time to 880ms.

## Testing

Two scripts were used and are worth rerunning after any change.

**Functional**, across all six pages at 320x568, 390x844, 768x1024, 1366x768
and 1920x1080, in light and dark: every image loads, no broken or 4xx requests,
no console errors, no horizontal scrolling, every image has intrinsic
dimensions and alt text, no empty image frames, every call link is exactly
`tel:+14074010184`, every internal link and `#anchor` target resolves,
navigation stays on one line at desktop, no button label wraps, no text spills
its box, tap targets clear 44px, one `<h1>` per page, unique titles and
descriptions, canonical URLs with no query string, Open Graph tags present,
skip link and landmarks present, footers byte-identical across pages, the form
has no action and a disabled submit with every control labelled, the mobile bar
appears below 768px and is hidden above it with matching body padding, and
`#estimate` exists.

**Contrast**, computed for 19 foreground/background pairs in both colour
schemes, including hover states, which Lighthouse does not test.

Two bugs that only the render pass caught, both worth knowing about:

- `width` and `height` attributes on `<img>` land as presentational hints, so a
  `height="1500"` survived `width: 100%` and forced the hero to 1500px tall,
  cropping it to a ceiling vent. Fixed with `height: auto` on the global
  `img, svg` rule.
- `.section` set padding with the shorthand, which zeroed the inline padding
  `.wrap` supplies, so section content ran to the screen edge at every width
  under 1180px. Fixed by switching to `padding-block`.

## Still open

- CLS on the home page is 0.051, within the 0.1 target but the highest on the
  site. It is webfont swap: the fallback and the real face have different
  metrics. A metrics-matched fallback with `size-adjust` would take it to near
  zero.
- Eight placeholder photographs are in use and every one is labelled
  representative. Two of the original ten (`drywall-work.jpg`,
  `slider-found.jpg`) were deleted rather than left unreferenced, because
  nothing on the site needed them and real photographs will replace the rest
  anyway. `assets/img/` is 1.9MB across 8 JPEG fallbacks and 15 WebP variants.
