# Expected — Command palette

## Pass

- Scrim is `overlay` `#000000` at ~50%.
- Palette is `surface-3` `#18191a` + `hairline-strong`, 12px radius.
- Selected row is `surface-2` `#141516` (surface lift, not color).
- Matched substring is highlighted in `primary` `#5e6ad2` text only.
- Shortcut hints are mono; group labels are `caption` `ink-subtle`.

## Fail

- A lavender background on the selected row.
- The palette rendered on pure `#000000` instead of `surface-3`.
- Lavender used anywhere other than the match highlight.
- Non-mono shortcut hints.
