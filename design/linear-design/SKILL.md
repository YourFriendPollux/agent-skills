---
name: linear-design
description: "Replicate Linear's premium dark SaaS identity — near-black canvas (#010102), charcoal surface ladder, hairline borders, lavender-blue accent (#5e6ad2), negative-tracking display type, and gradient restraint. Use whenever an interface must look like Linear or a premium dark product (linear.app, Linear-style issue tracker, dark SaaS landing page)."
version: 1.0.0
license: AGPL-3.0
metadata:
  tags: [design, linear, dark-theme, saas, tokens, premium]
  related_skills: [github-design, google-design]
---

# Linear Design — premium dark SaaS identity

Replicate **Linear**'s visual identity: the dark-first, dense,
"software-craft" aesthetic that defines the premium SaaS category. This skill
covers the dark theme, the design tokens, and the gradient discipline that
make the look read as expensive rather than generic.

Values come from two sources — do not invent them:

1. **linear.app/brand** (official brand page): naming, wordmark, logomark,
   icon, brand color.
2. **DesignMD's DESIGN.md analysis of linear.app** (designmd.co/d/linear.app)
   — exact token values extracted from the live marketing site (canvas,
   surfaces, hairlines, ink, type scale, components).

---

## When to use

- Any interface that must look like Linear: issue trackers, dashboards, dark
  SaaS landing pages, pricing pages.
- A "premium dark product" brief — "Linear-style", "Linear look", "dark
  premium SaaS", "like linear.app".
- The user wants the *opposite* of the generic AI-SaaS look (no gradient
  blobs, no purple-blue gradient hero).

## Golden rules

1. **Dark-first, always.** The identity is dark; do not ship a light mode.
2. **One chromatic accent.** Lavender-blue `#5e6ad2` is the ONLY accent —
   brand mark, primary CTA, focus ring, link emphasis. Never a background fill.
3. **Depth = surface ladder + hairline, not shadows.** Canvas → surface-1/2/3/4
   with 1px hairlines. Drop shadows are essentially banned on dark.
4. **Gradient restraint.** No atmospheric gradients, no spotlight cards, no
   gradient orbs.
5. **Canvas is `#010102`, never `#000000`.** The faint blue tint is
   intentional.
6. **Display 600, body 400, negative tracking.** Linear resists 700+ display
   weights.
7. **Product screenshots are the protagonist.** Lead with high-fidelity
   product UI framed in surface-1 panels (16px radius).
8. **Color is never the only signal** (WCAG): text ≥ 4.5:1, UI ≥ 3:1.

## Quick start

1. Set the canvas `#010102` and the ink scale.
2. Build the surface ladder (surface-1..4) + hairline tokens.
3. Apply the type system: display 600 with negative tracking, body 400.
4. Spend lavender sparingly: primary CTA, focus rings, links, brand mark.
5. Compose on the ladder: every card/panel gets a surface lift + 1px hairline;
   no drop shadows.
6. Lead with product screenshots framed in surface-1 panels (16px radius).
7. Verify against the checklist in `docs/guidelines.md`.

## Where everything lives

| File | Contents |
|------|----------|
| `docs/design-system.md` | Tokens: brand, color, typography, spacing, shape, elevation, gradients + ready-to-use CSS |
| `docs/components.md` | Component catalog: buttons, cards, inputs, nav, marquee, footer |
| `docs/guidelines.md` | Golden rules in depth, workflow, verification checklist, pitfalls, out of scope |
| `examples/` | Applied examples: dashboard, settings, project-management, command-palette |
| `evals/` | Evaluation prompts and expected outputs |

## Verification (abridged)

- [ ] Page background is `#010102` (not `#000000`); no light mode shipped.
- [ ] Exactly one chromatic accent (`#5e6ad2` family); lavender never a
      background fill.
- [ ] Contrast: text ≥ 4.5:1, UI ≥ 3:1.
- [ ] No drop shadows; depth via surface ladder + hairlines.
- [ ] No atmospheric gradients, orbs, or multi-hue accents.
- [ ] Buttons and inputs 8px radius; pills only for tabs/badges.
- [ ] Display weight ≤ 600, negative tracking on display sizes.

See `docs/guidelines.md` for the full checklist and the pitfall table.
