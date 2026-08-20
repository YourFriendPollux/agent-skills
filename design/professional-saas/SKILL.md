---
name: professional-saas
description: "Apply a premium dark SaaS identity — near-black canvas (#010102), charcoal surface ladder, hairline borders, lavender-blue accent (#5e6ad2), negative-tracking display type, and gradient restraint. Use whenever a professional SaaS product, issue tracker, dashboard, or dark landing page needs an expensive, software-craft look."
version: 1.0.0
license: AGPL-3.0
metadata:
  tags: [design, dark-theme, saas, tokens, premium, professional]
  related_skills: [github-design, google-design]
---

# Professional SaaS — premium dark identity

Build a **professional dark SaaS** identity: the dark-first, dense,
"software-craft" aesthetic for premium SaaS products. This skill covers the
dark theme, the design tokens, and the gradient discipline that make the look
read as expensive rather than generic.

Values are exact tokens (canvas, surfaces, hairlines, ink, type scale,
components) extracted as a curated professional SaaS system — do not invent
them. Source of truth is `docs/design-system.md`.

---

## When to use

- Any interface that needs a premium dark SaaS look: issue trackers,
  dashboards, dark landing pages, pricing pages.
- A "professional SaaS" or "premium dark product" brief — dark, dense,
  software-craft aesthetic.
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
6. **Display 600, body 400, negative tracking.** Resists 700+ display
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
