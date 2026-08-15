---
name: linear-design
description: "Replicate Linear's premium dark SaaS identity — near-black canvas (#010102), charcoal surface ladder, hairline borders, lavender-blue accent (#5e6ad2), negative-tracking display type, and gradient restraint. Use whenever an interface must look like Linear or a premium dark product (linear.app, Linear-style issue tracker, dark SaaS landing page)."
version: 1.0.0
author: Dandl AI
license: AGPL-3.0
metadata:
  tags: [design, linear, dark-theme, saas, tokens, premium]
  related_skills: [github-design, google-design]
---

# Linear Design — premium dark SaaS identity

Replicate **Linear**'s visual identity: the dark-first, dense, "software-craft"
aesthetic that defines the premium SaaS category. This skill covers the dark
theme, the design tokens, and the gradient discipline that make the look read
as expensive rather than generic.

Values come from two sources — do not invent them:

1. **linear.app/brand** (official brand page): naming, wordmark, logomark,
   icon, brand color.
2. **DesignMD's DESIGN.md analysis of linear.app** (designmd.co/d/linear.app)
   — exact token values extracted from the live marketing site (canvas,
   surfaces, hairlines, ink, type scale, components).

---

## 1. When to use

- Any interface that must look like Linear: issue trackers, dashboards, dark
  SaaS landing pages, pricing pages.
- A "premium dark product" brief — the user says "Linear-style", "Linear
  look", "dark premium SaaS", "like linear.app".
- Styling themes, components, or full pages "in the Linear style".
- The user wants the *opposite* of the generic AI-SaaS look (no gradient
  blobs, no purple-blue gradient hero).

## 2. Golden rules

1. **Dark-first, always.** The identity is dark; do not ship a light mode.
2. **One chromatic accent.** Lavender-blue `#5e6ad2` is the ONLY accent —
   brand mark, primary CTA, focus ring, link emphasis. Never as a background
   fill or card color.
3. **Depth = surface ladder + hairline, not shadows.** Canvas → surface-1/2/3/4
   with 1px hairlines. Drop shadows are essentially banned on dark.
4. **Gradient restraint.** No atmospheric gradients, no spotlight cards, no
   gradient orbs. The premium read comes from restraint (§9).
5. **Canvas is `#010102`, never `#000000`.** The faint blue tint is
   intentional.
6. **Display 600, body 400, negative tracking.** Linear resists 700+ display
   weights; display tracking runs -3.0px → 0 as size falls.
7. **Product screenshots are the protagonist.** Lead sections with
   high-fidelity product UI framed in surface-1 panels (radius 16px).
8. **Color is never the only signal** (WCAG): text ≥ 4.5:1, UI ≥ 3:1.

## 3. Brand

| Asset | Rule |
|-------|------|
| Naming | "Linear" — one word, capital L, never "Linear app" |
| Wordmark | Preferred mark; **monochrome usage preferred** |
| Logomark | For tight layouts / logo-only grids |
| Icon | For social chips; use with an appropriate corner radius |
| Brand color | "A subtle desaturated blue" — typically reserved for backgrounds; light/dark accents for monochrome wordmark usage |

Brand assets are **proprietary**: download from linear.app/brand, do not
alter, combine, or imply affiliation. For a *replica* use the logomark-style
geometry only with the user's consent and clear non-affiliation.

### Logomark (replica geometry — consent required)

Linear's mark is a **rounded-square frame with a hollow “L”** cut into it —
*not* a solid two-bar L. Render it monochrome (`currentColor`): that is how
Linear itself ships it in its header and app sidebar (observed on the live
site: ~22px in the marketing header lockup, ~13px in the app sidebar). The
header lockup is the mark followed by the wordmark drawn as one glyph, with
the mark filling roughly the left quarter of the lockup's height.

The exact 100×100 SVG path lives in
[`references/linear.css`](references/linear.css) — copy it into a `<defs>`
block and reference with `<use>` for consented, clearly non-affiliated
demos (the `rendu.html` uses it this way).

## 4. Color system (tokens)

### 4.1 Dark theme (the shipped theme)

| Token | HEX | Use |
|-------|-----|-----|
| canvas | `#010102` | page background — near-pure black, faint blue tint |
| surface-1 | `#0f1011` | feature cards, pricing cards, screenshot panels |
| surface-2 | `#141516` | featured pricing card, hovered cards |
| surface-3 | `#18191a` | sub-nav, dropdown menus |
| surface-4 | `#191a1b` | deepest lifted surface |
| hairline | `#23252a` | 1px card borders, dividers |
| hairline-strong | `#34343a` | stronger borders, input focus rings |
| hairline-tertiary | `#3e3e44` | nested-surface borders |
| ink | `#f7f8f8` | headlines, emphasized body |
| ink-muted | `#d0d6e0` | secondary type |
| ink-subtle | `#8a8f98` | tertiary type, footer columns |
| ink-tertiary | `#62666d` | disabled, footnotes |
| primary | `#5e6ad2` | lavender-blue — brand, CTA, focus, links |
| primary-hover | `#828fff` | primary CTA hover |
| primary-focus | `#5e69d1` | focus-ring tint, pressed CTA |
| on-primary | `#ffffff` | text on primary |
| success | `#27a644` | the only semantic color on marketing |
| overlay | `#000000` | modal scrim |
| brand-secure | `#7a7fad` | muted lavender-gray (security surfaces) |

### 4.2 Inverse (rare, light moments)

| Token | HEX | Use |
|-------|-----|-----|
| inverse-canvas | `#ffffff` | inverse pill CTA |
| inverse-surface-1 | `#f5f6f6` | one step above |
| inverse-surface-2 | `#f6f7f7` | two steps above |
| inverse-ink | `#000000` | text on inverse |

**Semantic naming:** `canvas`, `surface-{1..4}`, `hairline[-strong|-tertiary]`,
`ink[-muted|-subtle|-tertiary]`, `primary[-hover|-focus]`. Follow this naming
in your own tokens.

## 5. Typography

- **Linear Display** — display sans (fallback `SF Pro Display,
  -apple-system, system-ui, Segoe UI, Roboto`). Display-xl → subhead.
- **Linear Text** — text cut for body sizes (same fallback stack).
- **Linear Mono** — mono (fallback `ui-monospace, SF Mono, Menlo`) — code and
  ID tokens only, never marketing chrome.

Free substitutes: **Inter** (500/600/700) or **Geist Sans** for display/text;
**JetBrains Mono** / **Geist Mono** (400) for mono.

Proven stack from `rendu.html`: **Inter Tight** (600) for display sizes,
**Inter** (400/500/600) for text, **JetBrains Mono** for mono. Caveat:
Inter Tight's metrics are taller than Linear Display's, so give display
line-heights a touch more air (e.g. hero 1.12 instead of the 1.05 token) to
avoid clipped ascenders/descenders.

| Token | Size | Weight | Line-height | Tracking | Use |
|-------|------|--------|-------------|----------|-----|
| display-xl | 80px | 600 | 1.05 | **-3.0px** | largest hero |
| display-lg | 56px | 600 | 1.10 | -1.8px | section openers |
| display-md | 40px | 600 | 1.15 | -1.0px | sub-sections |
| headline | 28px | 600 | 1.20 | -0.6px | pricing titles, CTA banner |
| card-title | 22px | 500 | 1.25 | -0.4px | feature card titles |
| subhead | 20px | 400 | 1.40 | -0.2px | lead intro |
| body-lg | 18px | 400 | 1.50 | -0.1px | hero subhead |
| body | 16px | 400 | 1.50 | -0.05px | default |
| body-sm | 14px | 400 | 1.50 | 0 | card body, footer |
| caption | 12px | 400 | 1.40 | 0 | meta, status |
| button | 14px | 500 | 1.20 | 0 | all button labels |
| eyebrow | 13px | 500 | 1.30 | **+0.4px** | section eyebrows |
| mono | 13px | 400 | 1.50 | 0 | code in screenshots |

Principles: one continuous voice (display 600 → body 400); aggressive negative
tracking on display; the eyebrow's *positive* tracking marks it as taxonomy.

## 6. Spacing & layout

- Base **4px**. Tokens: 4 · 8 · 12 · 16 · 24 · 32 · 48 · **96** (section).
- Card interior: 24px (feature/pricing), 32px (testimonial), 48px (CTA
  banner). Buttons: 8px × 14px. Inputs: 8px × 12px.
- Max content width ≈ **1280px**. Card grids 3-up → 2-up (1024px) → 1-up
  (768px).
- **The dark canvas IS the whitespace.** Sections separate by lifting onto
  surface-1 panels, not by white gaps. 96px between sections, 24px inside
  panels.

## 7. Shape (border radius)

| Token | Value | Use |
|-------|-------|-----|
| xs | 4px | chips, status badges |
| sm | 6px | inline tags |
| md | **8px** | all buttons, inputs |
| lg | 12px | pricing / feature / testimonial cards |
| xl | 16px | product screenshot panels |
| xxl | 24px | oversized CTA banners (rare) |
| pill | 9999px | pricing tabs, status pills |

Rule: **buttons and inputs are 8px, never pill.** Pills are reserved for tab
toggles and status.

## 8. Elevation & depth

| Level | Treatment |
|-------|-----------|
| 0 | flat — no border, no shadow (hero text, footer) |
| 1 | surface-1 on canvas + 1px hairline (default cards) |
| 2 | surface-2 + 1px hairline-strong (featured, hover) |
| 3 | surface-3 (sub-nav, menus) |
| focus | 2px `primary-focus` outline at 50% opacity |

No drop shadows on dark. A **subtle white edge highlight** on the top edge of
lifted panels gives the dark surface a faint "pixel-rendered" feel — the only
allowed glow.

## 9. Gradients & the premium look

Linear's premium read is **gradient restraint** — the documented marketing
canvas has no atmospheric gradients, no spotlight cards. If your "premium dark"
brief drifts toward gradient decoration, this is the section to enforce.

- **Allowed**: subtle white edge highlight (§8); a faint blue tint baked into
  the canvas; low-intensity gradients *within the lavender-blue family*
  (`#5e6ad2 → #828fff`) for a brand moment only — never as a background.
- **Banned**: purple-to-blue gradient backgrounds; gradient orbs/blobs as hero
  decoration (the "AI SaaS look"); multi-hue gradients; spotlight cards.
- **Masks are not gradients.** Edge fades are fine as `mask-image` masks —
  hero-grid falloff, marquee ribbon edges — they keep the canvas flat and
  never read as background decoration.

The expensive look comes from: one accent used scarcely, a four-step surface
ladder, hairline borders, dense typography with negative tracking — not from
colorful backgrounds.

## 10. Component catalog

- **Primary button** — bg `primary`, text `on-primary`, 14/500, 8px radius,
  padding 8×14. Hover → `primary-hover`; pressed → `primary-focus`.
- **Secondary button** — bg `surface-1`, text `ink`, 1px `hairline`.
- **Tertiary button** — text-only on `canvas`.
- **Inverse button** — white bg, black text (rare, section openers).
- **Pricing tab** — pill; default `canvas` bg + `ink-subtle` text; selected =
  `surface-2` bg + `ink` text (selection = surface lift).
- **Cards** — `surface-1`, 12px radius, 1px `hairline`, 24px padding.
  Featured = `surface-2`. Screenshot panels = 16px radius.
- **Text input** — `surface-1` bg, 8px radius, 8×12 padding; focus = 2px
  `primary-focus` ring at 50%.
- **Status badge** — `surface-2` bg, `ink-muted`, pill, 2×8 padding.
- **Top nav** — 56px (`rendu.html` uses 80px for a taller lockup), `canvas`
  bg with a subtle blur, wordmark left (monochrome logomark + name; on hover
  the mark tints lavender — the accent's one sanctioned brand-mark moment),
  links center 16px/400 `ink-subtle` with a hairline underline on
  hover/active, secondary + primary CTA right.
- **Trusted-by logo band** — monochrome *real* logos (`ink-subtle` → `ink`
  on hover) in an infinite marquee. Loop mechanics: duplicate the logo set
  in two identical groups, each self-contained (internal gap + equal
  trailing padding), and animate the track `translateX(0 → -50%)`; fade the
  edges with a `mask-image` (§9), pause on hover, and under
  `prefers-reduced-motion` fall back to a static wrapping row with the
  duplicate group hidden. Define each logo once in `<defs>` and reference it
  with `<use>` so markup stays light. Source real shapes from Simple Icons
  (CC0) or official favicon/wordmark SVGs — never invent placeholder marks.
- **Footer** — `canvas`, `ink-subtle` caption text, 64×32 padding.

Product-UI note: the in-app product uses a richer tag palette (red, orange,
yellow, green, blue, purple) for issue priorities and labels. Those exact
values are not documented here — reference product mockups when replicating
the app, not the marketing system.

## 11. Workflow

1. **Set the canvas** (`#010102`) and ink scale; never `#000000` as the page
   background.
2. **Build the surface ladder** (surface-1..4) + hairline tokens.
3. **Apply the type system**: display 600 with negative tracking, body 400,
   eyebrow +0.4px.
4. **Spend lavender sparingly**: primary CTA, focus rings, links, brand mark.
5. **Compose on the ladder**: every card/panel gets a surface lift + 1px
   hairline; no drop shadows.
6. **Lead with product screenshots** framed in surface-1 panels (16px radius).
7. **Verify** against §12 before calling it done.

## 12. Verification

- [ ] Page background is `#010102` (not `#000000`); no light mode shipped.
- [ ] Exactly one chromatic accent (`#5e6ad2` family); lavender never a
      background fill.
- [ ] Contrast: text ≥ 4.5:1, UI ≥ 3:1 (ink `#f7f8f8` on canvas ≈ 19:1;
      `ink-subtle` `#8a8f98` on surface-1 ≈ 4.6:1 — tertiary only).
- [ ] No drop shadows; depth via surface ladder + hairlines.
- [ ] No atmospheric gradients, orbs, or multi-hue accents.
- [ ] Buttons and inputs 8px radius; pills only for tabs/badges.
- [ ] Display weight ≤ 600, negative tracking on display sizes.
- [ ] Type family fallbacks per §5; mono only for code/IDs.
- [ ] Trusted-by band shows *real* brand shapes (Simple Icons / official
      SVG), monochrome on dark — no invented placeholder marks.
- [ ] Marquee honors `prefers-reduced-motion`: static row, duplicate group
      hidden, no looping animation.

## 13. Pitfalls

| Pitfall | Failure | Fix |
|---------|---------|-----|
| Shipping light mode | Loses the identity | Dark-first, always (§2.1) |
| Lavender as card/section fill | Accent stops being scarce | Primary = CTA/focus/links only |
| Gradient hero / orbs | Instant "generic AI SaaS" | Restraint (§9) |
| `#000000` canvas | Flatter, colder than Linear | `#010102` with blue tint |
| Pill-shaped CTAs | Wrong radius language | `md` 8px for buttons/inputs |
| Drop shadows on dark | Muddy depth | Surface ladder + hairline |
| Display weight 700+ | Shouts, breaks the voice | 600 max, 400 body |
| Multiple accents | Dilutes the single hue | One chromatic color |
| Mono in marketing chrome | Noise | Mono for code/IDs only |
| Invented placeholder marks in trusted-by bands | Logos read as fake | Real brand shapes (Simple Icons CC0, official SVGs), monochrome on dark |
| Gradient fades on marquee edges | Breaks gradient restraint | `mask-image` fades — masks are allowed, background gradients are not |

## 14. Out of scope

- Reproducing Linear's proprietary logo assets — download from
  linear.app/brand; never alter or combine. (The logomark path shipped in
  references/linear.css is a *replica* for consented, clearly
  non-affiliated demos only — see §3.)
- Replicating in-app status/priority tag palettes (values not documented).
- Legal advice on brand usage; do not imply affiliation or endorsement.

## 15. Ready-to-use CSS

Full copy-paste starting point — design tokens, base styles, cards, buttons,
inputs, and focus rings — lives in
[`references/linear.css`](references/linear.css). Load it when you need the
ready-to-use CSS; adjust from there.

A complete visual render of the identity — hero, color tokens, type scale,
components, product screenshot mock, pricing, and footer — lives in
[`rendu.html`](rendu.html). Open it in a browser (or screenshot it) to see the
skill applied end to end before writing your own markup.

A **semi-functional SaaS interface** built on the same tokens — kanban board
with drag & drop, list view, filters, ⌘K command palette, issue create/detail
modals, and localStorage persistence — lives in
[`app.html`](app.html). Use it as the working-app starting point for
"build me a Linear-style app" briefs.

## 16. Sources

- Official brand guidelines: https://linear.app/brand
- DesignMD analysis (token values from the live site):
  https://designmd.co/d/linear.app — also mirrored at
  github.com/voltagent/awesome-design-md (`design-md/linear.app/DESIGN.md`)
