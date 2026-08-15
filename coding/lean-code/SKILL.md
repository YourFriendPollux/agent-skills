---
name: lean-code
description: "Write minimal, efficient code and review diffs for over-engineering. Supports intensity levels: lite, full (default), ultra. Use on any coding or code-review task."
version: 1.0.0
author: Dandl AI
license: AGPL-3.0
metadata:
  tags: [coding, efficiency, minimalism, code-review, over-engineering]
  related_skills: [leak-guard, github-design]
---

# Lean Code

Think like a pragmatic senior engineer: **the best code is the code never
written**. Write the minimum that satisfies the requirement, then review the
result for what can be deleted. This skill has two faces — writing efficient
code and reviewing code for over-engineering — driven by an intensity level:
`lite`, `full` (default) or `ultra`.

The skill body is mode-filtered: only the sections matching the active level are
injected (see [Runtime plugin](#runtime-plugin)).

## Golden Rules (always active)

1. **YAGNI** — build only what is requested; nothing speculative, no "we might
   need it later".
2. **Deletion over addition** — prefer removing lines to adding them.
3. **Boring over clever** — stdlib and native platform patterns before any
   dependency; an installed dependency before a new one.
4. **Never simplify away safety** — validation, error handling, security,
   accessibility, and explicitly requested behavior are never over-engineering.
5. **One small runnable check** — non-trivial logic gets a minimal verification
   that it actually runs.

## Intensity levels

| **mode** | Behavior |
|----------|----------|
| **lite** | Light discipline: apply the golden rules, prefer fewer lines, skip obvious gold-plating. Keep existing abstractions and dependencies as they are. |
| **full** | Default. Question every new abstraction, dependency, and configuration option. Prefer one-liners; delete dead code you notice; add a runnable check for non-trivial logic. |
| **ultra** | Ruthless. Challenge existing abstractions too: propose deletions, module merges, and inlined helpers. Only stdlib or already-installed dependencies. No scaffolding, ever. |

## When writing code

- lite: Write the shortest correct version that meets the request.
- full: Stop at the first rung that holds — YAGNI → stdlib → installed
  dependency → one line → minimum code. Do not add unrequested abstractions.
- ultra: Climb the same ladder, then re-read the diff afterwards and delete
  anything not strictly needed, including your own scaffolding.

## When reviewing code

- lite: Flag unnecessary complexity introduced by the changed lines.
- full: Review the diff for reinvented wheels, speculative abstraction, unused
  parameters, and dead code. Suggest concrete deletions with reasons.
- ultra: Review the whole file or module, not just the diff. Propose merging or
  deleting modules and helpers. Quantify the win: lines removed, dependencies
  dropped, complexity reduced.

## Pitfalls

- Minimalism is a means, not a goal: never drop error handling, validation,
  security, accessibility, or requested behavior to save lines.
- Deleting code you do not understand is not minimalism — trace the usage first.
- Do not refactor working code just to make it smaller; review time is budgeted.
- The intensity level is sticky: state the active mode in your first reply and
  when it changes.

## Runtime plugin

`scripts/lean_code_plugin.py` is a Hermes-style plugin that:

- reads this `SKILL.md` and **filters its body by the active mode** — table rows
  tagged `| **lite** | … |` and list items tagged `- lite: …` are kept only when
  they match the active level; everything else is always included;
- **injects the filtered context before LLM turns** (`build_injected_context` /
  `_pre_llm_call`), prefixed with `LEAN-CODE MODE ACTIVE — level: <mode>`;
- resolves the mode from, in order: explicit argument → `LEAN_CODE_DEFAULT_MODE`
  env var → `~/.config/lean-code/config.json` (`defaultMode`) → `full`;
- rewrites gateway slash commands (`/lean-code`, `/lean-review`) into agent
  prompts.

```bash
# set a default level
export LEAN_CODE_DEFAULT_MODE=ultra
# or in ~/.config/lean-code/config.json
# {"defaultMode": "lite"}
```

## Out of scope

- Language/framework-specific linting and style rules (use the project's own
  linter).
- Architectural design: this skill optimizes within a chosen design, it does not
  choose the architecture.
- Performance tuning beyond removing unnecessary work.
