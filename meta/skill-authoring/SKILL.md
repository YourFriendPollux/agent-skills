---
name: skill-authoring
description: "Write a skill that actually works — design the trigger (name + description frontmatter), structure a lean SKILL.md body, bundle references/scripts/assets, and verify the skill loads and fires correctly before shipping. Use whenever creating, editing, or reviewing a skill, a SKILL.md, or agent instruction files."
version: 1.0.0
author: Dandl AI
license: AGPL-3.0
metadata:
  tags: [meta, skill-authoring, agent-instructions, frontmatter, workflows]
  related_skills: [leak-guard, lean-code]
---

# Skill Authoring — skills that actually work

A skill only works if three things are true: it **triggers** when it should, its
instructions are **followable** by a cold agent, and its result is
**verifiable**. This skill is the method and checklist for producing that — for
any new skill, any edit to an existing one, or any agent instruction file.

Apply [`leak-guard`](../leak-guard/SKILL.md) at the end of every authoring pass,
before the artifact is saved.

---

## 1. When to use

- Creating a new skill from scratch.
- Editing or reviewing an existing `SKILL.md`.
- Writing agent instruction files, runbooks, or prompts that an agent loads on
  demand and must act on reliably.
- Debugging a skill that triggers too often, too rarely, or whose results are
  inconsistent.

---

## 2. The runtime contract — how a skill is loaded

An agent decides to load a skill from **two fields only**: the frontmatter
`name` and `description`. The whole body — markdown, references, scripts — is
invisible until the skill triggers and is injected into context.

Three consequences:

1. **The description is the entire trigger.** Write it like a filter: it must
   fire on the requests you want and stay silent on everything else.
2. **The body must survive contact.** Once injected, it lands in a live context
   window. Dense, imperative, and complete — or it gets skimmed or truncated.
3. **Context is budget.** The skill competes with the conversation. Keep it as
   small as it can be while staying complete.

---

## 3. Frontmatter — design the trigger

```yaml
---
name: my-skill          # lowercase-hyphen-case; must match the folder name
description: "Do <outcome> — <concrete verbs and objects>. Use whenever <triggers: user phrasing, keywords, artifact names>."
version: 1.0.0          # optional but recommended
author: Dandl AI        # optional
license: AGPL-3.0       # optional
metadata:               # optional
  tags: [meta, authoring]
  related_skills: [leak-guard]
---
```

### Rules for `description`

| Rule | Why |
|------|-----|
| Start with an outcome verb: `Run`, `Operate`, `Write`, `Scan`, `Review` | Tells the agent what job it is for |
| State **when** to use it, not just what it is | "Use whenever …" is the firing condition |
| Include the literal keywords a user would type | `pentest`, `MiroFish`, `sim_*`, `GitHub-style UI` — these are what actually match |
| Keep it to 1-3 sentences, plain text, no markdown | It must be readable at a glance |
| Mention exclusions if useful | "Refuses …", "Not for …" prevents misfires |

**Weak:**

```yaml
description: Skill about penetration testing.
```

**Strong:**

```yaml
description: Run an authorized penetration test end to end — scoping, reconnaissance, enumeration, controlled exploitation, and reporting. Refuses any action outside an explicit scope. Use whenever the user asks to pentest, audit, or exploit a specific target.
```

---

## 4. Body structure — the eight sections

A SKILL.md that works reads like a runbook, not an essay. Use this order:

| # | Section | Content | Required |
|---|---------|---------|----------|
| 1 | Title + mission | 1-3 sentences: what it does, when it applies | yes |
| 2 | When to use | Explicit trigger list (expands the description) | yes |
| 3 | Prerequisites | What must be true before starting; what to do if missing — **fail loudly** | yes |
| 4 | Golden rules / hard rules | Non-negotiable constraints, numbered, one per line | yes |
| 5 | Workflow | Numbered imperative steps; decision tables for branches | yes |
| 6 | Pitfalls | Failure modes observed in the wild + their fixes | yes |
| 7 | Verification | Concrete, satisfiable checks that prove it worked | yes |
| 8 | Out of scope | What the skill does not do or refuses to do | yes |

Every section is short. If a section grows past ~40 lines, the bulk belongs in
`references/` (see §6).

---

## 5. Instruction quality — rules that get followed

- **Imperative and numbered.** "1. Run X. 2. Read Y. 3. If Z, do W." Not prose.
- **State the output contract.** Give the exact format to produce: a YAML
  block, a table, a report skeleton. An agent reproduces formats, not vibes.
- **Decision tables for branches.** `condition → action` beats paragraphs.
- **Anticipate failure.** For each step, name the failure mode and the fallback.
- **No "be careful".** Say the actual constraint: "Never run X on a production
  host", "Refuse if the scope is missing".
- **Do not re-teach the base model.** A skill earns its context by adding
  something the agent would not reliably do alone: a scope gate, an exact
  workflow, a token table, a response format.
- **Placeholders only.** Real-looking values become real leaks. Follow
  [`leak-guard`](../leak-guard/SKILL.md).

---

## 6. Context economy — lean SKILL.md, rich folder

```
skill-name/
├── SKILL.md        # trigger + runbook, readable in one pass (≤ ~300 lines)
├── references/     # bulk knowledge loaded on demand: API maps, token tables, long formats
├── scripts/        # deterministic, runnable helpers (stdlib-first, usage header, safe defaults)
└── assets/         # templates and output artifacts
```

- Move big tables, endpoint maps, and reference docs to `references/`, and link
  them from SKILL.md with a one-line "load when needed" pointer.
- Scripts must be runnable and non-destructive by default: no side effects
  without an explicit flag, a `--help` usage block, exit code 0/1.
- If different audiences need different sections, use mode-filtering (see
  [`lean-code`](../../coding/lean-code/SKILL.md) for a working pattern) instead
  of one bloated file.

---

## 7. Authoring workflow

1. **Pin the job.** Task? Output? Who triggers it? One sentence each.
2. **Write the description first.** It is the contract. Draft it, then test it
   against sample prompts (§8.1) before writing a single body line.
3. **Draft the body** in the §4 order. Write the workflow steps as if you were
   executing them cold.
4. **Split the bulk.** Anything over ~40 lines per section goes to `references/`.
   Write scripts with usage headers; write templates as `assets/`.
5. **Hygiene pass.** Run leak-guard over every artifact: no secrets, no PII,
   placeholders only.
6. **Mechanical check.** Run `scripts/check_skill.py <folder>`: frontmatter,
   naming, structure, secret scan.
7. **Dry-run.** Walk the workflow yourself on a realistic input. Fix any step
   you could not complete from the text alone.
8. **Ship, then iterate.** Skills improve from recorded use — add every real
   failure mode you hit to the Pitfalls section.

---

## 8. Verification — does it actually work

### 8.1 Trigger test

Take three prompts the skill should fire on and three it should ignore:

- Good: `"pentest 192.0.2.10"` → the description matches → it fires.
- Bad: `"explain how TCP works"` → the description does NOT fire.

If a good prompt does not fire, or a bad one does, rewrite the description.

### 8.2 Load test

- Can the SKILL.md be read in one pass (≤ ~300 lines)?
- Would a cold agent complete step 1 without asking what to do?

### 8.3 Execution test

- Dry-run the workflow end to end. Every step actionable?
- Every failure mode has a stated fallback?

### 8.4 Verification test

Run the skill's own Verification section against a real output. Every check
must be mechanically satisfiable — never "verify quality is good".

### 8.5 Hygiene test

- leak-guard clean: zero real secrets, zero PII, placeholders only.
- `check_skill.py` exits 0.

---

## 9. Pitfalls & anti-patterns

| Pitfall | Failure | Fix |
|---------|---------|-----|
| Vague description (`Skill about pentesting`) | Never triggers, or triggers everywhere | Outcome verb + explicit triggers |
| Description without user keywords | Right request, no match | Include the words users actually type |
| Essay-style body | Skimmed, acted on vibes | Imperative steps + tables |
| 2000-line SKILL.md | Truncated, burns context | Push bulk to references/ |
| No output contract | Unverifiable, inconsistent results | Give exact output formats |
| Examples with real-looking secrets | Leak | leak-guard + placeholders |
| Re-teaching the base model | Wasted context, no added value | Only encode what the agent won't do alone |
| No exit condition | Agent keeps going past the job | Out of scope + stop criteria |
| Assumed tools or paths | Agent cannot follow | Prerequisites + fail loudly |

---

## 10. Readiness checklist

- [ ] `name` is lowercase-hyphen-case and matches the folder name
- [ ] `description` starts with an outcome verb and ends with "Use whenever …"
- [ ] Description fires on 3 good prompts and ignores 3 bad ones (§8.1)
- [ ] Body has all eight §4 sections; none over ~40 lines
- [ ] Workflow is numbered and imperative, with failure modes and fallbacks
- [ ] Verification section is concrete and satisfiable
- [ ] Bulk content lives in `references/`; scripts and assets are runnable
- [ ] leak-guard clean; `check_skill.py` exits 0
- [ ] Folder follows `lowercase-hyphen-case` and sits in the right category dir

---

## 11. Out of scope

- Writing the domain content of a specific skill (weather alerts, payment
  flows, a design system…): this skill teaches the method, not the subject
  matter.
- Enforcing a specific agent toolchain: the guidance is agent-agnostic; the
  validation script is stdlib Python only.
- Replacing [`leak-guard`](../leak-guard/SKILL.md): hygiene is a required
  companion pass, not a subsection of this skill.

---

## 12. References

- `assets/SKILL.template.md` — the §4 skeleton, ready to fill.
- `scripts/check_skill.py` — mechanical validation: frontmatter, naming,
  structure, secret scan. Run: `python3 scripts/check_skill.py <skill-folder>`.
- [`leak-guard`](../leak-guard/SKILL.md) — required hygiene pass.
- [`lean-code`](../../coding/lean-code/SKILL.md) — working example of a
  mode-filtered skill with a bundled runtime script.
