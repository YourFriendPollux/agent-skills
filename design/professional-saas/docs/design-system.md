# Design system

The complete token set for a premium dark SaaS identity. This is the single source of truth for values; the component specs live in [`components.md`](components.md) and the rules in [`guidelines.md`](guidelines.md).

## Brand

| Asset | Rule |
|-------|------|
| Wordmark | Preferred mark; **monochrome usage preferred** |
| Logomark | For tight layouts / logo-only grids |
| Icon | For social chips; use with an appropriate corner radius |
| Brand color | Use your own subtle desaturated hue for backgrounds; monochrome wordmark preferred |

Create your own wordmark/logomark — do not replicate a third-party proprietary mark. Render any mark monochrome (`currentColor`) and keep the header lockup simple (mark ~22px, wordmark ~19px/600, -0.4px tracking).

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

- - **Display Sans** — display sans (`Inter Tight` 600 recommended, fallback `SF Pro Display, -apple-system, system-ui, Segoe UI, Roboto`). Display-xl → subhead.
- **Text Sans** — text cut for body sizes (fallback `Inter` 400/500 + same stack).
- **Mono** — mono (`JetBrains Mono` 400, fallback `ui-monospace, SF Mono, Menlo`) — code and ID tokens only, never marketing chrome.

Recommended stack: **Inter Tight** (600) for display, **Inter** (400/500/600) for text, **JetBrains Mono** (400) for mono. Or **Geist Sans / Geist Mono** as alternative.

Proven stack: **Inter Tight** (600) for display sizes, **Inter** (400/500/600) for text, **JetBrains Mono** for mono. Note: give display line-heights a touch more air (e.g. hero 1.12 instead of 1.05) to avoid clipped ascenders/descenders.

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

The premium read is **gradient restraint** — the documented marketing
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
  --ps-canvas: #010102;
  --ps-surface-1: #0f1011;
  --ps-surface-2: #141516;
  --ps-surface-3: #18191a;
  --ps-surface-4: #191a1b;
  --ps-hairline: #23252a;
  --ps-hairline-strong: #34343a;
  --ps-hairline-tertiary: #3e3e44;
  --ps-ink: #f7f8f8;
  --ps-ink-muted: #d0d6e0;
  --ps-ink-subtle: #8a8f98;
  --ps-ink-tertiary: #62666d;
  --ps-primary: #5e6ad2;
  --ps-primary-hover: #828fff;
  --ps-primary-focus: #5e69d1;
  --ps-on-primary: #ffffff;
  --ps-success: #27a644;
  --ps-overlay: #000000;

  /* Substitute stack: Inter Tight (display), Inter (text), JetBrains Mono.
     Inter Tight: add ~0.07
     line-height on display sizes (e.g. hero 1.12 instead of 1.05). */
  --ps-font-display: 'Inter Tight', 'Inter', 'SF Pro Display',
    -apple-system, system-ui, 'Segoe UI', Roboto, sans-serif;
  --ps-font-text: 'Inter', 'SF Pro Text', -apple-system, system-ui,
    'Segoe UI', Roboto, sans-serif;
  --ps-font-mono: 'JetBrains Mono', ui-monospace, 'SF Mono', Menlo, monospace;

  --ps-radius-xs: 4px;
  --ps-radius-sm: 6px;
  --ps-radius-md: 8px;
  --ps-radius-lg: 12px;
  --ps-radius-xl: 16px;
  --ps-radius-xxl: 24px;
  --ps-radius-pill: 9999px;

  --ps-space-1: 4px;  --ps-space-2: 8px;  --ps-space-3: 12px;
  --ps-space-4: 16px; --ps-space-6: 24px; --ps-space-8: 32px;
  --ps-space-12: 48px; --ps-space-section: 96px;
}

body {
  font-family: var(--ps-font-text);
  font-size: 16px;
  line-height: 1.5;
  letter-spacing: -0.05px;
  color: var(--ps-ink);
  background: var(--ps-canvas);
}

h1, h2, h3, h4 {
  font-family: var(--ps-font-display);
  font-weight: 600;
  letter-spacing: -0.02em;   /* display tracking */
}

.card {
  background: var(--ps-surface-1);
  border: 1px solid var(--ps-hairline);
  border-radius: var(--ps-radius-lg);
  padding: var(--ps-space-6);
}

.btn-primary {
  background: var(--ps-primary);
  color: var(--ps-on-primary);
  border-radius: var(--ps-radius-md);
  padding: 8px 14px;
  font-size: 14px;
  font-weight: 500;
}
.btn-primary:hover { background: var(--ps-primary-hover); }
.btn-primary:active { background: var(--ps-primary-focus); }

.btn-secondary {
  background: var(--ps-surface-1);
  color: var(--ps-ink);
  border: 1px solid var(--ps-hairline);
  border-radius: var(--ps-radius-md);
  padding: 8px 14px;
}

input, textarea {
  background: var(--ps-surface-1);
  color: var(--ps-ink);
  border: 1px solid var(--ps-hairline);
  border-radius: var(--ps-radius-md);
  padding: 8px 12px;
}

:focus-visible {
  outline: 2px solid var(--ps-primary-focus);
  outline-offset: 2px;
}

/* ----- wordmark lockup (monochrome logomark + name) ----- */
.wordmark {
  display: inline-flex; align-items: center; gap: 8px;
  font-family: var(--ps-font-display); font-size: 19px; font-weight: 600;
  letter-spacing: -0.4px; color: var(--ps-ink); text-decoration: none;
}
.wordmark .mark { width: 22px; height: 22px; color: var(--ps-ink); transition: color 140ms ease; }
.wordmark:hover .mark { color: var(--ps-primary); }

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
  font-family: var(--ps-font-display); font-size: 19px; font-weight: 600;
  letter-spacing: -0.4px; color: var(--ps-ink-subtle); opacity: .8;
  white-space: nowrap; transition: color 160ms ease, opacity 160ms ease;
}
.logo-item:hover { color: var(--ps-ink); opacity: 1; }
@media (prefers-reduced-motion: reduce) {
  .marquee-track { animation: none; width: auto; flex-wrap: wrap; justify-content: center; }
  .marquee-group[aria-hidden="true"] { display: none; }
}
```

## Sources

- Curated professional SaaS token set — no third-party brand extraction.
- Reference inspiration: premium dark SaaS systems (near-black canvas, surface ladder, lavender-blue accent).
