# Components

The component catalog built on the [design system](design-system.md) tokens.
Every component follows the same discipline: surface lift + 1px hairline for
depth, 8px radius for controls, and lavender reserved for the primary action.

## Buttons

- **Primary button** — bg `primary`, text `on-primary`, 14/500, 8px radius,
  padding 8×14. Hover → `primary-hover`; pressed → `primary-focus`.
- **Secondary button** — bg `surface-1`, text `ink`, 1px `hairline`.
- **Tertiary button** — text-only on `canvas`.
- **Inverse button** — white bg, black text (rare, section openers).

```css
.btn-primary  { background: var(--ps-primary); color: var(--ps-on-primary); }
.btn-primary:hover  { background: var(--ps-primary-hover); }
.btn-primary:active { background: var(--ps-primary-focus); }
.btn-secondary { background: var(--ps-surface-1); color: var(--ps-ink); border: 1px solid var(--ps-hairline); }
```

All button labels: 14px / 500 / line-height 1.2 / tracking 0, 8px radius,
8×14 padding.

## Pricing tab

Pill-shaped toggle; default `canvas` bg + `ink-subtle` text; selected =
`surface-2` bg + `ink` text (selection = surface lift, not color).

## Cards

- `surface-1`, 12px radius, 1px `hairline`, 24px padding.
- Featured = `surface-2`. Screenshot panels = 16px radius.
- Interior padding by role: 24px (feature/pricing), 32px (testimonial), 48px
  (CTA banner).

```css
.card {
  background: var(--ps-surface-1);
  border: 1px solid var(--ps-hairline);
  border-radius: var(--ps-radius-lg);
  padding: var(--ps-space-6);
}
```

## Text input

`surface-1` bg, 8px radius, 8×12 padding; focus = 2px `primary-focus` ring at
50%.

```css
input, textarea {
  background: var(--ps-surface-1);
  color: var(--ps-ink);
  border: 1px solid var(--ps-hairline);
  border-radius: var(--ps-radius-md);
  padding: 8px 12px;
}
:focus-visible { outline: 2px solid var(--ps-primary-focus); outline-offset: 2px; }
```

## Status badge

`surface-2` bg, `ink-muted` text, pill radius, 2×8 padding.

## Top nav

56px tall, `canvas` bg with a subtle blur, wordmark left (monochrome logomark
+ name; on hover the mark tints lavender — the accent's one sanctioned
brand-mark moment), links center 16px/400 `ink-subtle` with a hairline
underline on hover/active, secondary + primary CTA right.

```css
.wordmark {
  display: inline-flex; align-items: center; gap: 8px;
  font-family: var(--ps-font-display); font-size: 19px; font-weight: 600;
  letter-spacing: -0.4px; color: var(--ps-ink); text-decoration: none;
}
.wordmark .mark { width: 22px; height: 22px; color: var(--ps-ink); transition: color 140ms ease; }
.wordmark:hover .mark { color: var(--ps-primary); }
```

## Trusted-by logo band

Monochrome *real* logos (`ink-subtle` → `ink` on hover) in an infinite
marquee.

Loop mechanics:
1. Duplicate the logo set in two identical groups, each self-contained
   (internal gap + equal trailing padding).
2. Animate the track `translateX(0 → -50%)`.
3. Fade the edges with a `mask-image` (masks are allowed, background gradients
   are not).
4. Pause on hover.
5. Under `prefers-reduced-motion`, fall back to a static wrapping row with the
   duplicate group hidden.

Define each logo once in `<defs>` and reference it with `<use>` so markup
stays light. Source real shapes from Simple Icons (CC0) or official
favicon/wordmark SVGs — never invent placeholder marks.

```css
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

## Footer

`canvas` bg, `ink-subtle` caption text, 64×32 padding.

## Product-UI note

The in-app product uses a richer tag palette (red, orange, yellow, green,
blue, purple) for issue priorities and labels. Those exact values are not
documented here — reference product mockups when replicating the app, not the
marketing system. See `examples/project-management.md` for the app-side
patterns.
