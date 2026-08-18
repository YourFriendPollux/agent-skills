# Evals

A small harness for grading whether an output actually follows the Linear
identity — not just whether it *looks* dark.

## Layout

```
evals/
├── prompts/     # the brief given to the model
├── expected/    # acceptance criteria for each brief (same filename)
└── README.md
```

Each `prompts/<name>.md` has a matching `expected/<name>.md`. Grade by
checking the output against every item in the expected file.

## Grading

- **Tokens** — exact values must match the design system
  (`docs/design-system.md`): canvas `#010102`, accent `#5e6ad2`, hairlines,
  surface ladder.
- **Identity rules** — the golden rules from `docs/guidelines.md`: one accent,
  no drop shadows, no gradient orbs, 8px control radius, display ≤ 600.
- **Accessibility** — text ≥ 4.5:1, UI ≥ 3:1; color is never the only signal.
- **Anti-patterns** — reject outputs that ship light mode, use `#000000`
  canvas, pill CTAs, or placeholder logos.

Each expected file lists pass criteria and fail criteria separately. An output
that trips a **fail** item is a hard reject even if every pass item holds.
