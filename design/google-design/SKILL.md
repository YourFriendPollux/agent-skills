---
name: google-design
description: Replicate Google's visual identity and Material Design 3 (Material You) in a frontend project — Google brand colors, Google Sans, the tonal color system, type scale, spacing, shape, elevation, and component patterns. Use whenever an interface must look like a Google product (Search, Gmail, Drive, Docs, Android).
---

# Google Design — replicate Google's visual style

This skill styles an interface so it looks like a Google product, based on
Google's official **Material Design 3** (Material You) and the Google brand
guidelines. Use it for themes, components, or full pages "in the Google style".

Values below come from official sources (m3.material.io, fonts.google.com,
Google brand guidelines). Do not invent them — reference them as-is. There are
**two layers** to Google's look, and you almost always need both:

1. **Google product theme** — the actual look of Gmail/Drive/Docs/Search (blue
   `#1A73E8`, Google Sans, gray text on white). This is what "looks like Google".
2. **Material Design 3 tokens** — the semantic color/type/shape system Google
   ships (baseline seed `#6750A4`, `--md-sys-*` CSS variables). This is the
   engine under the hood.

---

## 1. General principles

- **Clean, airy, generous whitespace.** White background, light gray surfaces,
  one accent (Google blue). No dense interfaces.
- **Rounded everywhere.** Cards, chips, buttons, search bars use large radii
  (8–28 dp); pill/capsule shapes for inputs and FABs.
- **Subtle elevation.** Prefer tonal surface layers and thin outlines over heavy
  drop shadows.
- **Blue = the only action color.** `#1A73E8` for primary actions and links.
  Red/green/amber are reserved for destructive / positive / warning states.
- **Google Sans for the brand and headings** ("product name" look), **Roboto**
  for body text, **Material Symbols Rounded** for icons.
- **Color is never the only signal** (WCAG 1.4.1). Contrast ≥ 4.5:1 for text,
  ≥ 3:1 for UI elements.

---

## 2. Google brand (logo)

| Name | HEX | Use |
|------|-----|-----|
| Google Blue | `#4285F4` | logo, brand accents |
| Google Red | `#EA4335` | logo |
| Google Yellow | `#FBBC05` | logo |
| Google Green | `#34A853` | logo |

The wordmark letters are colored G=`#4285F4`, o=`#EA4335`, o=`#FBBC05`,
g=`#4285F4`, l=`#34A853`, e=`#EA4335`. The four-color treatment is brand-only;
do not use it for functional UI states.

---

## 3. Google product theme (Gmail / Drive / Docs web look)

These are the "Google web" grays and state colors used across Google apps:

| Role | HEX | Use |
|------|-----|-----|
| Text (primary) | `#202124` | body text on white |
| Text (secondary) | `#5F6368` | captions, hints, meta |
| Border / divider | `#DADCE0` | outlines, separators |
| Hairline | `#E8EAED` | subtle dividers |
| Background | `#FFFFFF` | page / cards |
| Light surface | `#F8F9FA` | headers, panels |
| Hover surface | `#F1F3F4` | row/button hover |
| Blue (primary) | `#1A73E8` | buttons, links, focus |
| Blue (hover) | `#1765CC` | primary button hover |
| Blue (light) | `#E8F0FE` | selected/focus backgrounds |
| Red | `#D93025` | destructive actions |
| Green | `#188038` | positive / success |
| Amber | `#F9AB00` | warning |

Interaction states: hover = one step darker/lighter, focus = color change +
**blue focus ring** (`#1A73E8`, 2–3 px), active = one more step.

---

## 4. Material Design 3 — color system

### 4.1 Tonal palettes & roles

M3 generates **6 tonal palettes** (Primary, Secondary, Tertiary, Error,
Neutral, Neutral Variant) from a seed color; each has 13 tones from `0` (black)
to `100` (white). **Color roles** are semantic tokens that map to tones
(e.g. Primary = tone 40 in light, tone 80 in dark).

CSS variables use the prefix `--md-sys-color-` (Material Web) and
`--md-ref-palette-*` for raw tones.

### 4.2 Baseline scheme (seed `#6750A4`)

| Role | Light | Dark |
|------|-------|------|
| primary | `#6750A4` | `#D0BCFF` |
| on-primary | `#FFFFFF` | `#381E72` |
| primary-container | `#EADDFF` | `#4F378B` |
| on-primary-container | `#21005D` | `#EADDFF` |
| inverse-primary | `#D0BCFF` | `#6750A4` |
| secondary | `#625B71` | `#CCC2DC` |
| on-secondary | `#FFFFFF` | `#332D41` |
| secondary-container | `#E8DEF8` | `#4A4458` |
| on-secondary-container | `#1D192B` | `#E8DEF8` |
| tertiary | `#7D5260` | `#EFB8C8` |
| on-tertiary | `#FFFFFF` | `#492532` |
| tertiary-container | `#FFD8E4` | `#633B48` |
| on-tertiary-container | `#31111D` | `#FFD8E4` |
| error | `#B3261E` | `#F2B8B5` |
| on-error | `#FFFFFF` | `#601410` |
| error-container | `#F9DEDC` | `#8C1D18` |
| on-error-container | `#410E0B` | `#F9DEDC` |
| background | `#FEF7FF` | `#141218` |
| on-background | `#1D1B20` | `#E6E0E9` |
| surface | `#FEF7FF` | `#141218` |
| on-surface | `#1D1B20` | `#E6E0E9` |
| surface-variant | `#E7E0EC` | `#49454F` |
| on-surface-variant | `#49454F` | `#CAC4D0` |
| outline | `#79747E` | `#938F99` |
| outline-variant | `#CAC4D0` | `#49454F` |
| inverse-surface | `#322F35` | `#E6E0E9` |
| inverse-on-surface | `#F5EFF7` | `#322F35` |
| surface-dim | `#DED8E1` | `#141218` |
| surface-bright | `#FEF7FF` | `#3B383E` |
| surface-container-lowest | `#FFFFFF` | `#0F0D13` |
| surface-container-low | `#F7F2FA` | `#1D1B20` |
| surface-container | `#F3EDF7` | `#211F26` |
| surface-container-high | `#ECE6F0` | `#2B2930` |
| surface-container-highest | `#E6E0E9` | `#36343B` |
| shadow | `#000000` | `#000000` |
| scrim | `#000000` | `#000000` |
| surface-tint | `#6750A4` | `#D0BCFF` |

**To look like a Google product**, override `primary` with `#1A73E8` (Google
blue), keep `error` `#D93025`, and keep the neutral surfaces. The baseline
purple is the M3 *default*; Google apps use their own brand seed.

---

## 5. Typography

- **Google Sans** — brand/product typeface (variable font; axes: weight, grade,
  optical size). Use for product names, headings, and brand moments.
- **Roboto** — the default UI typeface for body and controls.
- **Material Symbols Rounded** — the icon font (ligature-based).
- **Roboto Mono** — for code, IDs, and technical values.

Font stacks:

```css
/* Brand / headings */
font-family: 'Google Sans', 'Product Sans', 'Roboto', -apple-system,
  BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;

/* Body / UI */
font-family: 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial,
  sans-serif;

/* Mono */
font-family: 'Roboto Mono', 'SFMono-Regular', 'Consolas', 'Liberation Mono',
  monospace;

/* Icons */
font-family: 'Material Symbols Rounded';
```

### Material 3 type scale (Roboto defaults)

| Style | Size / line-height | Weight | Letter-spacing |
|-------|--------------------|--------|----------------|
| Display Large | 57 / 64 | 400 | -0.25px |
| Display Medium | 45 / 52 | 400 | 0 |
| Display Small | 36 / 44 | 400 | 0 |
| Headline Large | 32 / 40 | 400 | 0 |
| Headline Medium | 28 / 36 | 400 | 0 |
| Headline Small | 24 / 32 | 400 | 0 |
| Title Large | 22 / 28 | 400 | 0 |
| Title Medium | 16 / 24 | **500** | 0.15px |
| Title Small | 14 / 20 | **500** | 0.1px |
| Body Large | 16 / 24 | 400 | 0.5px |
| Body Medium | 14 / 20 | 400 | 0.25px |
| Body Small | 12 / 16 | 400 | 0.4px |
| Label Large | 14 / 20 | **500** | 0.1px |
| Label Medium | 12 / 16 | **500** | 0.5px |
| Label Small | 11 / 16 | **500** | 0.5px |

Google-product feel: body **14px** (Roboto), product name in **Google Sans 500**,
secondary text `#5F6368`.

---

## 6. Spacing

Base **4 dp**. Component padding uses 4 dp increments:

| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 10 | 12 | 14 | 16 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 4 | 8 | 12 | 16 | 20 | 24 | 28 | 32 | 40 | 48 | 56 | 64 |

Cards: 16 dp inner padding. Page gutters: 24–32 dp. Buttons: 8–24 dp horizontal.

---

## 7. Shape (corner radii)

| Token | Radius | Use |
|-------|--------|-----|
| none | 0 | — |
| extra-small | 4 dp | text fields, snackbars |
| small | 8 dp | chips, cards, dialogs |
| medium | 12 dp | cards, sheets |
| large | 16 dp | FABs, large cards |
| extra-large | 28 dp | large cards, bottom sheets |
| full | 9999px | pills, capsules, inputs |

Google look = **large radii**; search bars, text fields, and FABs are pill-shaped
(`full`), cards are 8–12 dp.

---

## 8. Elevation

M3 prefers **tonal elevation** (surface containers) over shadows. If shadows are
needed, levels 0–5 = `0, 1, 3, 6, 8, 12` dp with a soft, low-opacity shadow.
Cards usually sit on `surface-container-low` with a 1 px `outline-variant`
border instead of a hard drop shadow.

---

## 9. Component patterns (Google look)

- **Filled button** — `primary` background, `on-primary` text, `full` radius,
  40 dp height, weight 500. Hover: tone darker.
- **Tonal button** — `secondary-container` background, `on-secondary-container`
  text.
- **Outlined button** — transparent background, 1 px `outline` border.
- **Text button** — no background, `primary` text.
- **Card** — `surface-container-low` background, 12 dp radius, optional 1 px
  `outline-variant` border, 16 dp padding.
- **Chip / pill / token** — `surface-variant` background, 8 dp radius, label
  text 14 px.
- **Text field** — **filled** (`surface-variant` bg) or **outlined** (1 px
  `outline`, 4 dp radius); 56 dp height; floating label; focus ring `primary`.
- **Search bar** — pill (`full`) shape, `surface-variant`/`#F1F3F4` background,
  centered, Material search icon.
- **FAB** — 16 dp radius, `primary-container` background, 56 dp size.
- **Navigation bar / rail** — `surface-container`, active item = pill of
  `secondary-container`.
- **App / top bar** — `surface` or white, product name in Google Sans 500, 64 dp.
- **Snackbar / toast** — `inverse-surface` background, `inverse-on-surface`
  text, 4 dp radius.
- **Focus ring** — `primary` (`#1A73E8`), 2–3 px, always paired with the state
  color change.
- **Icons** — Material Symbols Rounded, 24 dp, `#5F6368` default / `#1A73E8`
  active.

---

## 10. Ready-to-use CSS block

```css
:root {
  /* Google product theme */
  --google-blue: #1A73E8;
  --google-blue-hover: #1765CC;
  --google-blue-light: #E8F0FE;
  --google-red: #D93025;
  --google-green: #188038;
  --google-amber: #F9AB00;

  /* Google web grays */
  --google-text: #202124;
  --google-text-subtle: #5F6368;
  --google-border: #DADCE0;
  --google-hairline: #E8EAED;
  --google-surface: #F8F9FA;
  --google-hover: #F1F3F4;

  /* Material 3 baseline (light) — key roles */
  --md-sys-color-primary: #1A73E8;      /* Google override of the M3 purple seed */
  --md-sys-color-on-primary: #FFFFFF;
  --md-sys-color-primary-container: #E8F0FE;
  --md-sys-color-on-primary-container: #174EA6;
  --md-sys-color-secondary: #5F6368;
  --md-sys-color-on-secondary: #FFFFFF;
  --md-sys-color-secondary-container: #F1F3F4;
  --md-sys-color-on-secondary-container: #202124;
  --md-sys-color-tertiary: #7D5260;
  --md-sys-color-error: #D93025;
  --md-sys-color-on-error: #FFFFFF;
  --md-sys-color-error-container: #FCE8E6;
  --md-sys-color-on-error-container: #A50E0E;
  --md-sys-color-background: #FFFFFF;
  --md-sys-color-on-background: #202124;
  --md-sys-color-surface: #FFFFFF;
  --md-sys-color-on-surface: #202124;
  --md-sys-color-surface-variant: #F1F3F4;
  --md-sys-color-on-surface-variant: #5F6368;
  --md-sys-color-outline: #DADCE0;
  --md-sys-color-outline-variant: #E8EAED;
  --md-sys-color-inverse-surface: #202124;
  --md-sys-color-inverse-on-surface: #FFFFFF;
  --md-sys-color-shadow: #000000;
  --md-sys-color-scrim: #000000;

  /* Shape */
  --md-shape-extra-small: 4px;
  --md-shape-small: 8px;
  --md-shape-medium: 12px;
  --md-shape-large: 16px;
  --md-shape-extra-large: 28px;
  --md-shape-full: 9999px;

  /* Type */
  --google-font-sans: 'Google Sans', 'Roboto', -apple-system, BlinkMacSystemFont,
    'Segoe UI', Arial, sans-serif;
  --google-font-body: 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI',
    Arial, sans-serif;
  --google-font-mono: 'Roboto Mono', 'Consolas', 'Liberation Mono', monospace;
  --google-font-icons: 'Material Symbols Rounded';
}

body {
  font-family: var(--google-font-body);
  font-size: 0.875rem;           /* 14px — Google web body */
  line-height: 1.4286;           /* 20px */
  color: var(--google-text);
  background: var(--md-sys-color-background);
}
h1, h2, h3, h4, h5, h6 {
  font-family: var(--google-font-sans);
  font-weight: 500;
  color: var(--google-text);
}
a { color: var(--google-blue); }
code, pre, kbd { font-family: var(--google-font-mono); }
```

---

## 11. Official sources

- Material Design 3: https://m3.material.io
- Color roles: https://m3.material.io/styles/color/roles
- Typography: https://m3.material.io/styles/typography
- Shape: https://m3.material.io/styles/shape
- Elevation: https://m3.material.io/styles/elevation
- Google Sans: https://fonts.google.com/specimen/Google+Sans
- Roboto: https://fonts.google.com/specimen/Roboto
- Material Symbols: https://fonts.google.com/icons
- Google brand colors: https://about.google/brand-resource-center/
