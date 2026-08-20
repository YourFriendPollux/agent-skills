# minimal-saas

A skill for a **minimal premium dark SaaS identity** — the
dark-first, dense, "software-craft" aesthetic for professional SaaS
products.

The skill covers the dark theme, the design tokens, and the gradient
discipline that make the look read as *expensive* rather than generic. Values
are a curated token set — nothing is invented.

## Structure

```
repo/
├── README.md
├── SKILL.md               # entry point: identity, golden rules, quick start
├── LICENSE                # AGPL-3.0
├── CHANGELOG.md
├── docs/
│   ├── design-system.md   # tokens: color, type, spacing, shape, elevation, gradients + CSS
│   ├── components.md      # component catalog (buttons, cards, nav, marquee, …)
│   └── guidelines.md      # rules, workflow, verification, pitfalls, scope
├── examples/              # applied examples
│   ├── dashboard.md
│   ├── settings.md
│   ├── project-management.md
│   └── command-palette.md
└── evals/                 # evaluation harness
    ├── prompts/           # graded prompts
    ├── expected/          # acceptance criteria per prompt
    └── README.md
```

## Usage

Load `SKILL.md` and follow the quick start. Pull token values from
`docs/design-system.md`, component specs from `docs/components.md`, and the
verification checklist from `docs/guidelines.md`. Use `examples/` as concrete
starting points and `evals/` to grade an output against the identity.

## License

[AGPL-3.0](LICENSE)
