# Expected — Dashboard

## Pass

- Page background is `canvas` `#010102`.
- Cards/panels use `surface-1` `#0f1011` + 1px `hairline` `#23252a`; hover
  lifts to `surface-2` `#141516`.
- Title uses `ink` `#f7f8f8`; meta/axis labels use `ink-subtle` `#8a8f98`.
- KPI values are display-scale (40px/600, negative tracking); body is 400.
- The only chromatic accent is `primary` `#5e6ad2` (CTA, links, focus).
- Positive delta uses `success` `#27a644` with a text label, not color alone.
- Panels use 16px radius for screenshots, 12px for cards.

## Fail

- Any `#000000` as the page background, or a light mode.
- A drop shadow used for card depth.
- A gradient background, orb, or spotlight card.
- More than one chromatic hue.
- A pill-shaped button.
