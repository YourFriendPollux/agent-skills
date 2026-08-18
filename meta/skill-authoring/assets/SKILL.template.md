---
name: my-skill
description: "Do <outcome> — <1-2 concrete verbs and objects>. Use whenever <triggers: user phrasing, keywords, artifact names>."
version: 1.0.0
license: AGPL-3.0
metadata:
  tags: [<category>, <domain>]
  related_skills: []
---

# <Skill name> — <one-line purpose>

<1-3 sentences: what this skill does, and when it applies. Copy the firing
condition from the description into plain language.>

---

## 1. When to use

- <trigger 1 — the exact phrasing a user would type>
- <trigger 2>
- <trigger 3>

## 2. Prerequisites

- <what must already be true before step 1: installed tools, running services,
  files present, authorization granted>
- <if a prerequisite is missing: fail loudly — state what to do instead, e.g.
  "request X", "refuse", "install Y">

## 3. Golden rules

1. <non-negotiable constraint, one per line>
2. <e.g. "Never …", "Always …", "Refuse if …">
3. <each rule must be checkable — no "be careful">

## 4. Workflow

### Step 1 — <imperative action>

<what to do, with the exact command, request, or format>

### Step 2 — <imperative action>

<if a step can fail, add the failure mode and the fallback:

| Symptom | Cause | Fix |
|---------|-------|-----|
| <what goes wrong> | <why> | <what to do instead> |
>

## 5. Pitfalls

| Pitfall | Failure | Fix |
|---------|---------|-----|
| <observed failure mode> | <what breaks> | <the correction> |

## 6. Verification

After running the skill, all of these must hold:

1. <mechanically checkable condition, e.g. "exit code 0", "file exists",
   "status is stopped", "count > 0">
2. <never write "verify quality is good" — each check must be satisfiable>

## 7. Out of scope

- <what the skill explicitly does not do>
- <what it refuses, and the refusal behavior>

---

## Reference files

- `references/<file>.md` — <what it holds and when to load it> (add only if
  the body exceeds ~40 lines per section)
- `scripts/<script>` — <usage: `python3 scripts/<script> --help`>
