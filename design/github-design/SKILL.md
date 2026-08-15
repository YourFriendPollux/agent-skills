---
name: github-design
description: Replicate GitHub's visual identity and Primer design system in a frontend project — Primer color tokens (light & dark), Mona Sans / Hubot Sans typography, spacing, radii, Octicons, and the component catalog (header, buttons, labels, cards, tabs, tables, code blocks, alerts, menus). Use whenever an interface must look like GitHub.
---

# GitHub Design — Primer design system

This skill reproduces **Primer**, GitHub's official design system, as a usable
web design system: color tokens (light & dark), typography, spacing, shape,
icons, and the full component catalog — not just buttons.

Values come from official sources (primer.style, github.com, the
`primer/primitives` repo). Do not invent them. Two layers apply: the **brand**
(Octocat mark, dark header) and the **product** (Primer semantic tokens).

---

## 1. General principles

- **Dense, functional, text-first.** GitHub is a developer tool: compact
  density, clear hierarchy, strong use of monospace for code and metadata.
- **Borders over shadows.** Cards and panels use 1 px `border-default` lines and
  rounded 6 px corners; shadows are rare and subtle.
- **One accent, three states.** Blue `#0969DA` for links/actions, green
  `#1F883D` for the primary (create) button, red `#CF222E` for destructive.
  Purple `#8250DF` marks "done/merged".
- **Dark header + light canvas.** The top bar is dark (`#24292F`), content is
  white/gray; in dark theme everything inverts via tokens.
- **Monospace is content.** Code, SHAs, branch names, and file paths use the
  GitHub Mono stack — it is a first-class part of the identity.
- Color is never the only signal; contrast ≥ 4.5:1 text, ≥ 3:1 UI.

---

## 2. Brand

- **Octocat mark** + "GitHub" wordmark. Mark color: GitHub black `#181717`
  (on white) or white (on black). The mark is brand-only.
- **Dark header**: `#24292F` (light theme) / `#010409` (dark theme), white text.
- Marketing font: **Hubot Sans** (headlines); product font: **Mona Sans**.

---

## 3. Color system (Primer tokens)

### 3.1 Light theme

| Token | Value | Use |
|-------|-------|-----|
| fg-default | `#1F2328` | primary text |
| fg-muted | `#59636E` | secondary text, icons |
| fg-subtle | `#6E7781` | tertiary text |
| fg-onEmphasis | `#FFFFFF` | text on accent/dark |
| canvas-default | `#FFFFFF` | page, cards |
| canvas-subtle | `#F6F8FA` | code blocks, panels |
| canvas-inset | `#F6F8FA` | inset surfaces |
| border-default | `#D1D9E0` | standard borders |
| border-muted | `#D8DEE4` | subtle borders |
| neutral-emphasis | `#6E7781` | muted emphasis |
| neutral-muted | `rgba(175,184,193,0.2)` | hover fills |
| neutral-subtle | `rgba(234,238,242,0.5)` | faint fills |
| accent-fg | `#0969DA` | links, focus, active |
| accent-emphasis | `#0969DA` | blue buttons |
| accent-subtle | `#DDF4FF` | selected backgrounds |
| success-fg | `#1A7F37` | success text |
| success-emphasis | `#1F883D` | **primary (green) button**, open state |
| success-subtle | `#DAFBE1` | success background |
| attention-fg | `#9A6700` | warning text |
| attention-emphasis | `#9A6700` | warning accents |
| attention-subtle | `#FFF8C5` | warning background |
| danger-fg | `#D1242F` | destructive text |
| danger-emphasis | `#CF222E` | destructive button, closed state |
| danger-subtle | `#FFEBE9` | destructive background |
| done-fg | `#8250DF` | purple — merged PRs, "done" |
| done-emphasis | `#8250DF` | purple accents |
| done-subtle | `#FBEFFF` | purple background |

### 3.2 Dark theme

| Token | Value | Use |
|-------|-------|-----|
| fg-default | `#F0F6FC` | primary text |
| fg-muted | `#9198A1` | secondary text |
| fg-subtle | `#8B949E` | tertiary text |
| canvas-default | `#0D1117` | page, cards |
| canvas-subtle | `#161B22` | code blocks, panels |
| canvas-inset | `#010409` | inset surfaces |
| border-default | `#30363D` | standard borders |
| border-muted | `#21262D` | subtle borders |
| neutral-muted | `rgba(110,118,129,0.4)` | hover fills |
| accent-fg | `#4493F8` | links, focus |
| accent-emphasis | `#1F6FEB` | blue buttons |
| accent-subtle | `rgba(56,139,253,0.15)` | selected backgrounds |
| success-fg | `#3FB950` | success text |
| success-emphasis | `#238636` | primary (green) button, open state |
| success-subtle | `rgba(46,160,67,0.15)` | success background |
| attention-fg | `#D29922` | warning text |
| attention-emphasis | `#9E6A03` | warning accents |
| attention-subtle | `rgba(187,128,9,0.15)` | warning background |
| danger-fg | `#F85149` | destructive text |
| danger-emphasis | `#DA3633` | destructive button, closed state |
| danger-subtle | `rgba(248,81,73,0.15)` | destructive background |
| done-fg | `#A371F7` | purple — merged/done |
| done-emphasis | `#8957E5` | purple accents |
| done-subtle | `rgba(163,113,247,0.15)` | purple background |

### 3.3 State colors (issues / PRs)

| State | Light | Dark |
|-------|-------|------|
| open | `#1A7F37` | `#3FB950` |
| closed | `#D1242F` | `#F85149` |
| merged | `#8250DF` | `#A371F7` |

### 3.4 Semantic naming

Primer token naming: `{namespace}-{role}` → `fg-default`, `canvas-subtle`,
`border-muted`, `accent-fg`, `success-emphasis`, `danger-subtle`. `-fg` = text,
`-emphasis` = filled, `-muted`/`-subtle` = backgrounds. Follow this convention in
your own tokens.

---

## 4. Typography

- **Mona Sans** — product UI font (variable).
- **Hubot Sans** — marketing/headline font (variable).
- **System stack** — the default body fallback used across github.com.
- **Mono stack** — GitHub's "Mono" + system monospace, for code, SHAs, paths,
  branch names, and metadata.

Font stacks:

```css
/* UI / body */
font-family: 'Mona Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI',
  'Noto Sans', Helvetica, Arial, sans-serif, 'Apple Color Emoji',
  'Segoe UI Emoji';

/* Marketing / headings */
font-family: 'Hubot Sans', 'Mona Sans', -apple-system, BlinkMacSystemFont,
  'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif;

/* Code */
font-family: 'Mono', ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas,
  'Liberation Mono', monospace;
```

### Type scale

| Size | Use |
|------|-----|
| 12 px | metadata, labels, buttons (small) |
| **14 px** | **body default** |
| 16 px | titles, inputs |
| 20 px | section headings |
| 24 px | h2 |
| 32 px | h1 |
| 40–48 px | display / marketing |

Body = **14 px** (a strong GitHub-density marker), line-height 1.5. Headings
600 weight, body 400. SHAs and code in mono, 12–13 px.

---

## 5. Spacing

Base **4 px** scale (0.25rem):

| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 10 | 12 | 16 |
|---|---|---|---|---|---|---|---|---|---|---|----|
| 0 | 4 | 8 | 12 | 16 | 20 | 24 | 28 | 32 | 40 | 48 | 64 |

Cards: 16 px padding. Lists/rows: 8–16 px. Page gutters: 16–32 px.

---

## 6. Shape (border radius)

| Token | Radius | Use |
|-------|--------|-----|
| small | 4 px | code, small tags |
| medium | **6 px** | buttons, inputs, cards, tabs (default) |
| large | 8 px | menus, popovers, modals |
| xlarge | 12 px | large containers |
| full / pill | 9999px | avatars, badges, labels |

GitHub default radius is **6 px** on almost everything — a key density signal.

---

## 7. Shadow

GitHub is flat: borders do the work. Use shadows only for overlays:

```css
--shadow-resting: 0 1px 0 rgba(31,35,40,0.04);
--shadow-floating: 0 8px 24px rgba(140,149,159,0.2);
--shadow-overlay: 0 1px 3px rgba(31,35,40,0.12), 0 8px 24px rgba(66,74,83,0.12);
```

---

## 8. Icons (Octicons)

- **Octicons** — GitHub's icon set (16 px grid, 1.5 px stroke).
- Use 16 px inline; scale to 24 px for nav. Color: `fg-muted` by default,
  `fg-default` on hover, `accent-fg` when active.

---

## 9. Component catalog

### 9.1 Navigation

| Component | Anatomy / specs |
|-----------|-----------------|
| Header | dark `#24292F` (light) / `#010409` (dark), white text, 16 px padding, search field, avatar |
| Underline tabs | text 14 px, active tab = `fg-default` + 2 px `accent`/orange bottom border, inactive = `fg-muted` |
| Secondary nav | canvas-subtle bar, bordered, small text |

### 9.2 Buttons

| Variant | Background | Text | Border |
|---------|-----------|------|--------|
| Primary (green) | `#1F883D` | white | — |
| Default | `#F6F8FA` | `fg-default` | `border-default` |
| Blue | `#0969DA` | white | — |
| Danger | `#CF222E` | white | — |
| Invisible / link | transparent | `accent-fg` | — |
| Outline | transparent | `fg-default` | `border-default` |

Height ~32 px, radius 6 px, padding 5–16 px, weight 500, font-size 14 px.
Hover: darken one step; disabled: 50% opacity.

### 9.3 Labels & badges

| Component | Anatomy / specs |
|-----------|-----------------|
| Label / badge | pill (`full`), colored: `{color}-subtle` background + `{color}-fg` text + 1 px `{color}` border; 12 px text |
| Status pill | open `success` / closed `danger` / merged `done`, with Octicon |
| Counter | `neutral-muted` pill with `fg-muted` text, 12 px |
| Avatar | circular image, 20–32 px, 1 px `border-default` ring |

### 9.4 Content

| Component | Anatomy / specs |
|-----------|-----------------|
| Card / panel | `canvas-default` bg, 1 px `border-default`, radius 6 px, 16 px padding |
| Table | header `canvas-subtle`, rows separated by `border-muted`, 13–14 px text, right-aligned numbers |
| Code block | `canvas-subtle` bg, 1 px `border-default`, radius 6 px, mono 13 px |
| Inline code | `neutral-muted` bg, radius 6 px, mono 12 px, padding 2–6 px |
| Timeline | vertical `border-muted` line with circular nodes (open/closed/merged colors) |
| File tree | rows with Octicon + mono filename, hover `canvas-subtle` |

### 9.5 Forms

| Component | Anatomy / specs |
|-----------|-----------------|
| Text input | white bg, 1 px `border-default`, radius 6 px, 14 px, focus = `accent-fg` 2 px ring + `accent-subtle` bg |
| Search field | bordered input + `/` shortcut hint + Octicon |
| Select / dropdown | bordered 6 px, custom trigger, menu = white + border + shadow |
| Checkbox / radio | 16 px, `accent-fg` when checked |

### 9.6 Feedback

| Component | Anatomy / specs |
|-----------|-----------------|
| Alert (flash) | `{color}-subtle` bg + `{color}-fg` text + `{color}` 1 px border, radius 6 px, Octicon |
| Tooltip | dark `neutral-emphasis-plus` bg, white text, radius 6 px, arrow |
| Toast | bottom-right, `canvas-overlay` bg, border + shadow |
| Progress | 8 px bar, `neutral-muted` track, `accent-fg` fill |
| Spinner | Octicon spinner, `fg-muted` |

### 9.7 Overlays

| Component | Anatomy / specs |
|-----------|-----------------|
| Menu (dropdown) | white bg, 1 px `border-default`, radius 6 px, shadow, 8 px padding |
| Dialog / modal | white bg, radius 12 px, overlay scrim `rgba(140,149,159,0.2)` |
| Popover | white bg, border, radius 8 px, arrow |

---

## 10. Component states

Every control: **default · hover · pressed · disabled · focused · selected**.

- hover: `neutral-muted` background or one-step-darkened emphasis;
- pressed: `neutral-subtle` background;
- disabled: 50% opacity, no interaction;
- focused: 2 px `accent-fg` focus ring;
- selected: `accent-subtle` background + `accent-fg` text/icon.

---

## 11. Ready-to-use CSS block

```css
:root {
  /* Primer light */
  --fg-default: #1F2328; --fg-muted: #59636E; --fg-subtle: #6E7781;
  --fg-on-emphasis: #FFFFFF;
  --canvas-default: #FFFFFF; --canvas-subtle: #F6F8FA; --canvas-inset: #F6F8FA;
  --border-default: #D1D9E0; --border-muted: #D8DEE4;
  --neutral-muted: rgba(175,184,193,0.2); --neutral-subtle: rgba(234,238,242,0.5);
  --accent-fg: #0969DA; --accent-emphasis: #0969DA; --accent-subtle: #DDF4FF;
  --success-fg: #1A7F37; --success-emphasis: #1F883D; --success-subtle: #DAFBE1;
  --attention-fg: #9A6700; --attention-emphasis: #9A6700; --attention-subtle: #FFF8C5;
  --danger-fg: #D1242F; --danger-emphasis: #CF222E; --danger-subtle: #FFEBE9;
  --done-fg: #8250DF; --done-emphasis: #8250DF; --done-subtle: #FBEFFF;
  --header-bg: #24292F;
  --brand-black: #181717;

  /* Shape */
  --radius-small: 4px; --radius-medium: 6px; --radius-large: 8px;
  --radius-xlarge: 12px; --radius-full: 9999px;

  /* Shadow */
  --shadow-floating: 0 8px 24px rgba(140,149,159,0.2);

  /* Type */
  --font-ui: 'Mona Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI',
    'Noto Sans', Helvetica, Arial, sans-serif, 'Apple Color Emoji',
    'Segoe UI Emoji';
  --font-display: 'Hubot Sans', 'Mona Sans', -apple-system, BlinkMacSystemFont,
    'Segoe UI', Helvetica, Arial, sans-serif;
  --font-mono: 'Mono', ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas,
    'Liberation Mono', monospace;
}

@media (prefers-color-scheme: dark) {
  :root {
    --fg-default: #F0F6FC; --fg-muted: #9198A1; --fg-subtle: #8B949E;
    --canvas-default: #0D1117; --canvas-subtle: #161B22; --canvas-inset: #010409;
    --border-default: #30363D; --border-muted: #21262D;
    --neutral-muted: rgba(110,118,129,0.4);
    --accent-fg: #4493F8; --accent-emphasis: #1F6FEB; --accent-subtle: rgba(56,139,253,0.15);
    --success-fg: #3FB950; --success-emphasis: #238636; --success-subtle: rgba(46,160,67,0.15);
    --attention-fg: #D29922; --attention-emphasis: #9E6A03; --attention-subtle: rgba(187,128,9,0.15);
    --danger-fg: #F85149; --danger-emphasis: #DA3633; --danger-subtle: rgba(248,81,73,0.15);
    --done-fg: #A371F7; --done-emphasis: #8957E5; --done-subtle: rgba(163,113,247,0.15);
    --header-bg: #010409;
  }
}

body {
  font-family: var(--font-ui);
  font-size: 14px;
  line-height: 1.5;
  color: var(--fg-default);
  background: var(--canvas-default);
}
h1,h2,h3,h4,h5,h6 { font-family: var(--font-display); font-weight: 600; }
a { color: var(--accent-fg); }
code, pre, kbd { font-family: var(--font-mono); }

.btn-primary { background: var(--success-emphasis); color: #fff; border-radius: var(--radius-medium); }
.btn-default { background: var(--canvas-subtle); color: var(--fg-default); border: 1px solid var(--border-default); border-radius: var(--radius-medium); }
.btn-danger { background: var(--danger-emphasis); color: #fff; border-radius: var(--radius-medium); }
.card { background: var(--canvas-default); border: 1px solid var(--border-default); border-radius: var(--radius-medium); padding: 16px; }
.label { border-radius: var(--radius-full); padding: 0 8px; font-size: 12px; font-weight: 500; }
```

---

## 12. Official sources

- Primer design system: https://primer.style
- Color: https://primer.style/foundations/color
- Typography: https://primer.style/foundations/typography
- Icons (Octicons): https://primer.style/foundations/icons
- Primitives (tokens): https://github.com/primer/primitives
- GitHub brand: https://github.com/logos
