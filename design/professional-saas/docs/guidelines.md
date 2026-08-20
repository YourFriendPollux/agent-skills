# Guidelines

The rules that keep the look *premium* rather than generic. Values live in
[`design-system.md`](design-system.md); component specs in
[`components.md`](components.md). This file is the enforcement layer.

## When to use

- Any interface that needs a premium dark SaaS look: issue trackers, dashboards, dark
  landing pages, pricing pages.
- A "premium dark product" or "professional SaaS" brief — dark, dense, software-craft aesthetic.
- Styling themes, components, or full pages in the professional dark style.
- The user wants the *opposite* of the generic AI-SaaS look (no gradient
  blobs, no purple-blue gradient hero).

## Golden rules

1. **Dark-first, always.** The identity is dark; do not ship a light mode.
2. **One chromatic accent.** Lavender-blue `#5e6ad2` is the ONLY accent —
   brand mark, primary CTA, focus ring, link emphasis. Never as a background
   fill or card color.
3. **Depth = surface ladder + hairline, not shadows.** Canvas → surface-1/2/3/4
   with 1px hairlines. Drop shadows are essentially banned on dark.
4. **Gradient restraint.** No atmospheric gradients, no spotlight cards, no
   gradient orbs.
5. **Canvas is `#010102`, never `#000000`.** The faint blue tint is
   intentional.
6. **Display 600, body 400, negative tracking.** The system resists 700+ display
   weights; display tracking runs -3.0px → 0 as size falls.
7. **Product screenshots are the protagonist.** Lead sections with
   high-fidelity product UI framed in surface-1 panels (radius 16px).
8. **Color is never the only signal** (WCAG): text ≥ 4.5:1, UI ≥ 3:1.

## Workflow

1. **Set the canvas** (`#010102`) and ink scale; never `#000000` as the page
   background.
2. **Build the surface ladder** (surface-1..4) + hairline tokens.
3. **Apply the type system**: display 600 with negative tracking, body 400,
   eyebrow +0.4px.
4. **Spend lavender sparingly**: primary CTA, focus rings, links, brand mark.
5. **Compose on the ladder**: every card/panel gets a surface lift + 1px
   hairline; no drop shadows.
6. **Lead with product screenshots** framed in surface-1 panels (16px radius).
7. **Verify** against the checklist below before calling it done.

## Verification checklist

- [ ] Page background is `#010102` (not `#000000`); no light mode shipped.
- [ ] Exactly one chromatic accent (`#5e6ad2` family); lavender never a
      background fill.
- [ ] Contrast: text ≥ 4.5:1, UI ≥ 3:1 (ink `#f7f8f8` on canvas ≈ 19:1;
      `ink-subtle` `#8a8f98` on surface-1 ≈ 4.6:1 — tertiary only).
- [ ] No drop shadows; depth via surface ladder + hairlines.
- [ ] No atmospheric gradients, orbs, or multi-hue accents.
- [ ] Buttons and inputs 8px radius; pills only for tabs/badges.
- [ ] Display weight ≤ 600, negative tracking on display sizes.
- [ ] Type family fallbacks per the design system; mono only for code/IDs.
- [ ] Trusted-by band shows *real* brand shapes (Simple Icons / official
      SVG), monochrome on dark — no invented placeholder marks.
- [ ] Marquee honors `prefers-reduced-motion`: static row, duplicate group
      hidden, no looping animation.

## Pitfalls

| Pitfall | Failure | Fix |
|---------|---------|-----|
| Shipping light mode | Loses the identity | Dark-first, always |
| Lavender as card/section fill | Accent stops being scarce | Primary = CTA/focus/links only |
| Gradient hero / orbs | Instant "generic AI SaaS" | Restraint (design-system §Gradients) |
| `#000000` canvas | Flatter, colder | `#010102` with blue tint |
| Pill-shaped CTAs | Wrong radius language | `md` 8px for buttons/inputs |
| Drop shadows on dark | Muddy depth | Surface ladder + hairline |
| Display weight 700+ | Shouts, breaks the voice | 600 max, 400 body |
| Multiple accents | Dilutes the single hue | One chromatic color |
| Mono in marketing chrome | Noise | Mono for code/IDs only |
| Invented placeholder marks in trusted-by bands | Logos read as fake | Real brand shapes (Simple Icons CC0, official SVGs), monochrome on dark |
| Gradient fades on marquee edges | Breaks gradient restraint | `mask-image` fades — masks are allowed, background gradients are not |

## Out of scope

- Do not replicate third-party proprietary logo assets — create your own mark; never imply affiliation.
- Replicating in-app status/priority tag palettes (values not documented).
- Legal advice on brand usage; do not imply affiliation or endorsement.
