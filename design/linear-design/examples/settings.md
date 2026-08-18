# Example — Settings

A Linear-style settings page. Settings are the least "premium" surface to get
wrong: keep it quiet, dense, and predictable.

## Layout

- **Left sub-nav** (`surface-3` `#18191a`, 240px): account, workspace,
  notifications, billing, security. Active item = `surface-2` bg + `ink` text.
- **Content column** (max 640px): sections separated by `hairline` dividers,
  each with a `card-title` (22/500) header and `body-sm` description.
- **Sticky footer** with secondary ("Cancel") + primary ("Save") buttons
  right-aligned.

## Tokens in play

| Element | Token |
|---------|-------|
| Page | `canvas` `#010102` |
| Sub-nav | `surface-3` `#18191a` |
| Active nav item | `surface-2` `#141516` + `ink` |
| Nav label (idle) | `ink-subtle` `#8a8f98` |
| Input | `surface-1` bg, 8px radius, 8×12 padding, `hairline` border |
| Input focus | 2px `primary-focus` `#5e69d1` @ 50% |
| Section title | `card-title` 22/500 |
| Helper text | `caption` `ink-subtle` |
| Danger action | `ink-muted` + `hairline` border (never red-on-red) |
| Save button | `primary` `#5e6ad2` |

## Component notes

- Inputs: 8px radius, never pill. Labels `body-sm`; helper text `caption`.
- Toggles/pills: pill radius is allowed here (tabs/status only), never on
  buttons.
- Danger zone: a bordered `surface-1` panel with a tertiary-style button —
  reserved color, not a red fill.
- Focus ring: the only place lavender appears on the page besides the Save
  button.

## Sketch

```html
<div class="settings">
  <aside class="subnav">
    <a class="active">Account</a>
    <a>Workspace</a>
    <a>Notifications</a>
    <a>Billing</a>
    <a>Security</a>
  </aside>

  <section class="content">
    <h2>Account</h2>

    <div class="field">
      <label>Display name</label>
      <input value="Ada Lovelace" />
      <p class="helper">Shown across the workspace.</p>
    </div>

    <div class="field">
      <label>Email</label>
      <input type="email" value="ada@example.com" />
    </div>

    <div class="danger card">
      <h3>Delete account</h3>
      <p class="muted">Permanently removes your account and data.</p>
      <button class="btn-secondary">Delete…</button>
    </div>

    <footer class="actions">
      <button class="btn-secondary">Cancel</button>
      <button class="btn-primary">Save</button>
    </footer>
  </section>
</div>
```

## Verification

- Sub-nav is a surface lift (`surface-3`), not a colored sidebar.
- No pill-shaped buttons; lavender only on Save + focus.
- Danger zone uses restraint, not a red fill.
