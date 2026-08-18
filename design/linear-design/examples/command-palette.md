# Example — Command palette (⌘K)

A Linear-style command palette. This is a floating, elevated overlay — the one
place the surface ladder runs deep.

## Layout

- **Scrim**: `overlay` `#000000` at ~50% behind the palette.
- **Palette**: `surface-3` `#18191a` panel, `lg` 12px radius, 1px
  `hairline-strong`, centered top-third of the viewport, max 640px.
- **Search input** at top: transparent bg, `body` 16px `ink`, 8×12 padding;
  placeholder `ink-subtle`.
- **Results**: grouped list — group label `caption`/`eyebrow` `ink-subtle`,
  items `body-sm` with a `mono` shortcut hint right-aligned.
- **Selected item**: `surface-2` bg (selection = surface lift, not color).

## Tokens in play

| Element | Token |
|---------|-------|
| Scrim | `overlay` `#000000` @ 50% |
| Palette | `surface-3` `#18191a` + `hairline-strong` |
| Selected row | `surface-2` `#141516` |
| Row title | `body-sm` 14/400 `ink` |
| Group label | `caption` 12px `ink-subtle` |
| Shortcut hint | `mono` 13px `ink-tertiary` |
| Highlighted match | `primary` `#5e6ad2` text |
| Radius | `lg` 12px |

## Component notes

- Selection is a **surface lift**, never a lavender background.
- The matched substring is highlighted in `primary` text — the accent's only
  appearance.
- Shortcut hints are mono; all else display/text faces.
- Keyboard nav: arrow keys move the surface-2 selection; Enter runs the
  action; Esc closes. No animation beyond a 120ms fade/scale.

## Sketch

```html
<div class="scrim">
  <div class="palette" role="dialog" aria-label="Command palette">
    <input class="search" placeholder="Type a command or search…" />

    <div class="group">
      <p class="group-label">Navigation</p>
      <div class="row selected">
        <span class="title">Go to <mark>Dashboard</mark></span>
        <kbd>G D</kbd>
      </div>
      <div class="row">
        <span class="title">Go to <mark>Settings</mark></span>
        <kbd>G S</kbd>
      </div>
    </div>

    <div class="group">
      <p class="group-label">Actions</p>
      <div class="row">
        <span class="title">Create issue</span>
        <kbd>C</kbd>
      </div>
    </div>
  </div>
</div>
```

## Verification

- Palette is `surface-3`, not pure black; selected row is `surface-2`, not
  lavender.
- Match highlight uses `primary` text; nothing else does.
- Mono only on `<kbd>` hints.
