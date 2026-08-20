# Example — Dashboard

A Professional SaaS metrics dashboard. The goal is a dense, calm overview that
reads as *expensive*: one accent, surface lift for hierarchy, no shadows.

## Layout

- **Top nav** (56px): wordmark left, section links center (`ink-subtle`),
  primary CTA right.
- **Header band**: `display-md` title (40px/600, -1.0px tracking) + `body-sm`
  description, then a surface-1 toolbar for filters.
- **KPI row**: 4 cards, 3-up → 2-up (1024px) → 1-up (768px).
- **Main grid**: left 2/3 chart panel, right 1/3 activity list — both
  surface-1 with 1px hairline.
- **Section gap**: 96px between bands, 24px inside panels.

## Tokens in play

| Element | Token |
|---------|-------|
| Page | `canvas` `#010102` |
| Cards / panels | `surface-1` `#0f1011` + `hairline` `#23252a` |
| Hovered card | `surface-2` `#141516` + `hairline-strong` |
| Title | `ink` `#f7f8f8` |
| KPI value | `display-md` 40/600 |
| Meta / axis labels | `ink-subtle` `#8a8f98` |
| Positive delta | `success` `#27a644` |
| Primary CTA | `primary` `#5e6ad2`, hover `#828fff` |
| Panel radius | `xl` 16px (screenshot), `lg` 12px (cards) |

## Component notes

- KPI cards: value + `caption` delta; the delta uses `success` plus an arrow —
  never color alone (aria-label the trend).
- Chart: `ink-muted` line on `canvas`, with the primary series in
  `primary`. No gradients under the curve.
- Activity list: 1px `hairline` dividers between rows, `body-sm` title +
  `caption` timestamp, mono for issue IDs.

## Sketch

```html
<header class="nav">
  <a class="wordmark"><svg class="mark">…</svg> Professional SaaS</a>
  <nav>Overview · Analytics · Issues · Cycle</nav>
  <button class="btn-primary">New issue</button>
</header>

<main>
  <div class="header">
    <h1>Overview</h1>
    <p class="muted">Triaged · In Progress · Done this cycle</p>
  </div>

  <div class="kpis">
    <div class="card">
      <span class="kpi-label">Active issues</span>
      <span class="kpi-value">1,284</span>
      <span class="delta up" aria-label="down 3% this week">▼ 3%</span>
    </div>
    <!-- ×4 -->
  </div>

  <div class="grid">
    <section class="card chart">…</section>
    <section class="card activity">…</section>
  </div>
</main>
```

## Verification

- No `#000000`; no drop shadow; one accent. Chart lines, not gradient blobs.
- KPI delta communicates trend in text + color (WCAG).
