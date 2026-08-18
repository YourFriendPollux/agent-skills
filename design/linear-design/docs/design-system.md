# Design system

The complete token set for Linear's premium dark identity. All values come
from linear.app/brand and DesignMD's DESIGN.md analysis of linear.app — do not
invent them. This is the single source of truth for values; the component
specs live in [`components.md`](components.md) and the rules in
[`guidelines.md`](guidelines.md).

## Brand

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

Linear's mark is a **rounded-square frame with a hollow "L"** cut into it —
*not* a solid two-bar L. Render it monochrome (`currentColor`): that is how
Linear itself ships it in its header and app sidebar (observed on the live
site: ~22px in the marketing header lockup, ~13px in the app sidebar). The
header lockup is the mark followed by the wordmark drawn as one glyph, with
the mark filling roughly the left quarter of the lockup's height.

The exact 100×100 SVG path:

```svg
<svg width="22" height="22" viewBox="0 0 100 100" fill="currentColor">
  <path d="M1.225 61.523c-.222-.949.908-1.546 1.597-.857l36.512 36.512c.69.69.092 1.82-.857 1.597-18.425-4.323-32.93-18.827-37.252-37.252M.002 46.889a1 1 0 0 0 .29.76L52.35 99.71c.201.2.478.307.76.29 2.37-.149 4.695-.46 6.963-.927.765-.157 1.03-1.096.478-1.648L2.576 39.448c-.552-.551-1.491-.286-1.648.479a50 50 0 0 0-.926 6.962M4.21 29.705a.99.99 0 0 0 .208 1.1l64.776 64.776a.99.99 0 0 0 1.1.208 50 50 0 0 0 5.185-2.684.98.98 0 0 0 .183-1.54L8.436 24.336a.98.98 0 0 0-1.541.183 50 50 0 0 0-2.684 5.185m8.448-11.631a.986.986 0 0 1-.045-1.354C21.78 6.46 35.111 0 49.952 0 77.592 0 100 22.407 100 50.048c0 14.84-6.46 28.172-16.72 37.338a.986.986 0 0 1-1.354-.045z"/>
</svg>
```

Copy it into a `<defs>` block and reference with `<use>` for consented,
clearly non-affiliated demos.

## Color

### Dark theme (the shipped theme)

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

### Inverse (rare, light moments)

| Token | HEX | Use |
|-------|-----|-----|
| inverse-canvas | `#ffffff` | inverse pill CTA |
| inverse-surface-1 | `#f5f6f6` | one step above |
| inverse-surface-2 | `#f6f7f7` | two steps above |
| inverse-ink | `#000000` | text on inverse |

**Semantic naming:** `canvas`, `surface-{1..4}`, `hairline[-strong|-tertiary]`,
`ink[-muted|-subtle|-tertiary]`, `primary[-hover|-focus]`. Follow this naming
in your own tokens.

## Typography

- **Linear Display** — display sans (fallback `SF Pro Display,
  -apple-system, system-ui, Segoe UI, Roboto`). Display-xl → subhead.
- **Linear Text** — text cut for body sizes (same fallback stack).
- **Linear Mono** — mono (fallback `ui-monospace, SF Mono, Menlo`) — code and
  ID tokens only, never marketing chrome.

Free substitutes: **Inter** (500/600/700) or **Geist Sans** for display/text;
**JetBrains Mono** / **Geist Mono** (400) for mono.

Proven stack: **Inter Tight** (600) for display sizes, **Inter** (400/500/600)
for text, **JetBrains Mono** for mono. Caveat: Inter Tight's metrics are
taller than Linear Display's, so give display line-heights a touch more air
(e.g. hero 1.12 instead of the 1.05 token) to avoid clipped
ascenders/descenders.

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

## Spacing & layout

- Base **4px**. Tokens: 4 · 8 · 12 · 16 · 24 · 32 · 48 · **96** (section).
- Card interior: 24px (feature/pricing), 32px (testimonial), 48px (CTA
  banner). Buttons: 8px × 14px. Inputs: 8px × 12px.
- Max content width ≈ **1280px**. Card grids 3-up → 2-up (1024px) → 1-up
  (768px).
- **The dark canvas IS the whitespace.** Sections separate by lifting onto
  surface-1 panels, not by white gaps. 96px between sections, 24px inside
  panels.

## Shape (border radius)

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

## Elevation & depth

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

## Gradients & the premium look

Linear's premium read is **gradient restraint** — the documented marketing
canvas has no atmospheric gradients, no spotlight cards.

- **Allowed**: subtle white edge highlight (§Elevation); a faint blue tint
  baked into the canvas; low-intensity gradients *within the lavender-blue
  family* (`#5e6ad2 → #828fff`) for a brand moment only — never as a
  background.
- **Banned**: purple-to-blue gradient backgrounds; gradient orbs/blobs as hero
  decoration (the "AI SaaS look"); multi-hue gradients; spotlight cards.
- **Masks are not gradients.** Edge fades are fine as `mask-image` masks —
  hero-grid falloff, marquee ribbon edges — they keep the canvas flat and
  never read as background decoration.

The expensive look comes from: one accent used scarcely, a four-step surface
ladder, hairline borders, dense typography with negative tracking — not from
colorful backgrounds.

## Ready-to-use CSS

Copy-paste starting point — design tokens, base styles, cards, buttons,
inputs, focus rings, the wordmark lockup, and the marquee. Adjust from here.

```css
:root {
  --lin-canvas: #010102;
  --lin-surface-1: #0f1011;
  --lin-surface-2: #141516;
  --lin-surface-3: #18191a;
  --lin-surface-4: #191a1b;
  --lin-hairline: #23252a;
  --lin-hairline-strong: #34343a;
  --lin-hairline-tertiary: #3e3e44;
  --lin-ink: #f7f8f8;
  --lin-ink-muted: #d0d6e0;
  --lin-ink-subtle: #8a8f98;
  --lin-ink-tertiary: #62666d;
  --lin-primary: #5e6ad2;
  --lin-primary-hover: #828fff;
  --lin-primary-focus: #5e69d1;
  --lin-on-primary: #ffffff;
  --lin-success: #27a644;
  --lin-overlay: #000000;

  /* Substitute stack: Inter Tight (display), Inter (text), JetBrains Mono.
     Inter Tight's metrics are taller than Linear Display's: add ~0.07
     line-height on display sizes (e.g. hero 1.12 instead of 1.05). */
  --lin-font-display: 'Linear Display', 'Inter Tight', 'Inter', 'SF Pro Display',
    -apple-system, system-ui, 'Segoe UI', Roboto, sans-serif;
  --lin-font-text: 'Linear Text', 'Inter', 'SF Pro Text', -apple-system, system-ui,
    'Segoe UI', Roboto, sans-serif;
  --lin-font-mono: 'Linear Mono', 'JetBrains Mono', ui-monospace, 'SF Mono', Menlo, monospace;

  --lin-radius-xs: 4px;
  --lin-radius-sm: 6px;
  --lin-radius-md: 8px;
  --lin-radius-lg: 12px;
  --lin-radius-xl: 16px;
  --lin-radius-xxl: 24px;
  --lin-radius-pill: 9999px;

  --lin-space-1: 4px;  --lin-space-2: 8px;  --lin-space-3: 12px;
  --lin-space-4: 16px; --lin-space-6: 24px; --lin-space-8: 32px;
  --lin-space-12: 48px; --lin-space-section: 96px;
}

body {
  font-family: var(--lin-font-text);
  font-size: 16px;
  line-height: 1.5;
  letter-spacing: -0.05px;
  color: var(--lin-ink);
  background: var(--lin-canvas);
}

h1, h2, h3, h4 {
  font-family: var(--lin-font-display);
  font-weight: 600;
  letter-spacing: -0.02em;   /* display tracking */
}

.card {
  background: var(--lin-surface-1);
  border: 1px solid var(--lin-hairline);
  border-radius: var(--lin-radius-lg);
  padding: var(--lin-space-6);
}

.btn-primary {
  background: var(--lin-primary);
  color: var(--lin-on-primary);
  border-radius: var(--lin-radius-md);
  padding: 8px 14px;
  font-size: 14px;
  font-weight: 500;
}
.btn-primary:hover { background: var(--lin-primary-hover); }
.btn-primary:active { background: var(--lin-primary-focus); }

.btn-secondary {
  background: var(--lin-surface-1);
  color: var(--lin-ink);
  border: 1px solid var(--lin-hairline);
  border-radius: var(--lin-radius-md);
  padding: 8px 14px;
}

input, textarea {
  background: var(--lin-surface-1);
  color: var(--lin-ink);
  border: 1px solid var(--lin-hairline);
  border-radius: var(--lin-radius-md);
  padding: 8px 12px;
}

:focus-visible {
  outline: 2px solid var(--lin-primary-focus);
  outline-offset: 2px;
}

/* ----- wordmark lockup (monochrome logomark + name) ----- */
.wordmark {
  display: inline-flex; align-items: center; gap: 8px;
  font-family: var(--lin-font-display); font-size: 19px; font-weight: 600;
  letter-spacing: -0.4px; color: var(--lin-ink); text-decoration: none;
}
.wordmark .mark { width: 22px; height: 22px; color: var(--lin-ink); transition: color 140ms ease; }
.wordmark:hover .mark { color: var(--lin-primary); }

/* ----- trusted-by logo band (infinite marquee) ----- */
.marquee {
  overflow: hidden;
  -webkit-mask-image: linear-gradient(to right, transparent, #000 10%, #000 90%, transparent);
  mask-image: linear-gradient(to right, transparent, #000 10%, #000 90%, transparent);
}
.marquee-track { display: flex; width: max-content; animation: marquee 60s linear infinite; }
.marquee:hover .marquee-track { animation-play-state: paused; }
.marquee-group { display: flex; align-items: center; gap: 48px; padding-right: 48px; }
@keyframes marquee { from { transform: translateX(0); } to { transform: translateX(-50%); } }
.logo-item {
  display: inline-flex; align-items: center; gap: 12px;
  font-family: var(--lin-font-display); font-size: 19px; font-weight: 600;
  letter-spacing: -0.4px; color: var(--lin-ink-subtle); opacity: .8;
  white-space: nowrap; transition: color 160ms ease, opacity 160ms ease;
}
.logo-item:hover { color: var(--lin-ink); opacity: 1; }
@media (prefers-reduced-motion: reduce) {
  .marquee-track { animation: none; width: auto; flex-wrap: wrap; justify-content: center; }
  .marquee-group[aria-hidden="true"] { display: none; }
}
```

## Sources

- Official brand guidelines: https://linear.app/brand
- DesignMD analysis (token values from the live site):
  https://designmd.co/d/linear.app — also mirrored at
  github.com/voltagent/awesome-design-md (`design-md/linear.app/DESIGN.md`)
