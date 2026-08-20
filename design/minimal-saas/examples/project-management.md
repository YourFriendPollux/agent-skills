# Example — Project management

A Professional SaaS issue tracker / kanban board. This is the *app* surface, not
the marketing site: it inherits the same tokens but adds the richer in-app
tag palette for priorities and labels.

## Layout

- **Top nav** (56px): workspace switcher + project name left, view controls
  center (list / board / calendar), primary "New issue" right.
- **Toolbar** (surface-1, 1px hairline): filters, sort, search input.
- **Board**: horizontal columns, each a `surface-1` panel with a `caption`
  column header + issue count badge; columns scroll horizontally.
- **Issue cards** inside columns: `surface-2` bg on `canvas`, 1px `hairline`,
  12px radius, 16px padding.

## Tokens in play

| Element | Token |
|---------|-------|
| Board canvas | `canvas` `#010102` |
| Column / toolbar | `surface-1` `#0f1011` + `hairline` |
| Issue card | `surface-2` `#141516` + `hairline`, `lg` 12px |
| Card title | `body-sm` 14/500 `ink` |
| Meta / IDs | `mono` 13px, `ink-tertiary` `#62666d` |
| Count badge | `surface-2` bg, `ink-muted`, pill |
| Focus ring | 2px `primary-focus` @ 50% |
| Priorities/labels | in-app palette (red, orange, yellow, green, blue, purple) |

## Component notes

- Issue IDs (`LIN-1024`) are **mono** — the only sanctioned mono use.
- Priority and label chips use the in-app palette; those exact values are not
  in the design system, so reference real product mockups rather than
  inventing hues.
- Cards lift via `surface-2` + hairline, never via drop shadow.
- Drag-and-drop affordance: `hairline-strong` border on the drop target.

## Sketch

```html
<header class="nav">
  <span class="project">Acme · Web</span>
  <div class="views">List · <b>Board</b> · Calendar</div>
  <button class="btn-primary">New issue</button>
</header>

<div class="toolbar">
  <input placeholder="Filter…" />
  <button class="btn-secondary">Sort</button>
</div>

<div class="board">
  <section class="column">
    <header>Backlog <span class="count">12</span></header>
    <article class="issue">
      <span class="id">LIN-1024</span>
      <h4>Fix billing webhook retries</h4>
      <span class="label bug">Bug</span> <span class="label high">High</span>
    </article>
    <!-- … -->
  </section>
  <!-- Todo · In Progress · Done -->
</div>
```

## Verification

- Board columns are surface lifts, not colored backgrounds.
- Mono reserved for IDs; marketing chrome stays in display/text faces.
- No drop shadows on cards; drop target uses `hairline-strong`.
