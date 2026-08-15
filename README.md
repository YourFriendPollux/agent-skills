# Skills

A curated collection of reusable, self-contained **skills** for AI coding agents —
modular instructions that give an agent specialized workflows, guardrails, and
domain knowledge for a specific task or domain.

---

## Table of contents

- [Overview](#overview)
- [Repository structure](#repository-structure)
- [Skills](#skills)
  - [Security](#security)
  - [Meta](#meta)
  - [Tools](#tools)
  - [Design](#design)
- [What is a skill?](#what-is-a-skill)
- [Installation](#installation)
- [Safety & responsible use](#safety--responsible-use)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

This repository gathers skills authored for real engagements and product work,
cleaned up and organized by category. Each skill is a self-contained folder that
an agent loads on demand, so nothing here needs to be "installed" as a package —
you drop the folder into your agent and it becomes available.

| Category   | Skills | Purpose |
|------------|--------|---------|
| [`security/`](security) | [`authorized-pentest`](security/authorized-pentest), [`kali-operator`](security/kali-operator) | Offensive security, scoped and authorized |
| [`meta/`](meta)         | [`leak-guard`](meta/leak-guard) | Skill hygiene and anonymization |
| [`tools/`](tools)       | [`mirofish`](tools/mirofish) | Tool / API integration |
| [`design/`](design)     | [`github-design`](design/github-design), [`google-design`](design/google-design) | Design-system replication |

---

## Repository structure

```
.
├── design/
│   ├── github-design/
│   └── google-design/
├── meta/
│   └── leak-guard/
├── security/
│   ├── authorized-pentest/
│   └── kali-operator/
└── tools/
    └── mirofish/
```

---

## Skills

### Security

#### authorized-pentest

Run an authorized penetration test end to end — scoping, reconnaissance,
enumeration, threat modeling, controlled exploitation with minimal proofs of
concept, privilege escalation, and a professional report.

Built for labs, CTFs, bug bounty, and contracted engagements with an explicit
scope. Refuses any action without authorization or outside scope.

- **Location:** [`security/authorized-pentest`](security/authorized-pentest)

#### kali-operator

Operate Kali Linux like a senior pentester / security analyst — terminal work,
tool selection, result interpretation, diagnostics, and Bash/Python automation —
strictly within an explicitly authorized scope.

For authorized audits, labs, CTFs, administration, forensics, and automation.
Refuses any action without authorization or outside scope.

- **Location:** [`security/kali-operator`](security/kali-operator)

### Meta

#### leak-guard

Ensure no sensitive information leaks when an AI writes a skill or other
documentation — scan for credentials, secrets, PII, internal network details,
and proprietary data, then redact with safe placeholders.

Apply to any new or edited `SKILL.md`, prompt, or document before it is saved.

- **Location:** [`meta/leak-guard`](meta/leak-guard)

### Tools

#### mirofish

Operate the MiroFish swarm-intelligence prediction engine locally — start the
backend, prepare, launch, monitor, stop, and generate reports for multi-agent
social simulations (Twitter / Reddit / parallel) via its Flask REST API.

Use whenever the user mentions MiroFish, swarm simulation, agent prediction, or
a `sim_*` ID.

- **Location:** [`tools/mirofish`](tools/mirofish)

### Design

#### github-design

Replicate GitHub's visual identity and Primer design system in a frontend
project — Primer color tokens (light & dark), Mona Sans / Hubot Sans typography,
spacing, radii, Octicons, and the component catalog (header, buttons, labels,
cards, tabs, tables, code blocks, alerts, menus).

Use whenever an interface must look like GitHub.

- **Location:** [`design/github-design`](design/github-design)

#### google-design

Replicate Google's visual identity and Material Design 3 (Material You) in a
frontend project — Google brand colors, Google Sans, the tonal color system,
type scale, spacing, shape, elevation, and component patterns.

Use whenever an interface must look like a Google product (Search, Gmail, Drive,
Docs, Android).

- **Location:** [`design/google-design`](design/google-design)

---

## What is a skill?

A skill is a folder containing a required `SKILL.md` plus optional bundled
resources:

```
skill-name/
├── SKILL.md        # YAML frontmatter (name + description) and markdown instructions
├── references/     # optional: documentation loaded on demand
├── scripts/        # optional: deterministic, runnable helpers
└── assets/         # optional: templates, icons, and other output files
```

The frontmatter `name` and `description` are what the agent reads to decide when
to load a skill. The body and bundled resources are loaded only once the skill
triggers, which keeps the agent's context lean.

---

## Installation

Skills are plain folders — there is no package to install. To use one, copy its
folder into your agent's skills directory and the agent discovers it
automatically:

- **Codex:** `~/.codex/skills/`
- **Hermes:** `~/.hermes/skills/`

```bash
# example: install authorized-pentest for Codex
cp -r security/authorized-pentest ~/.codex/skills/
```

---

## Safety & responsible use

`authorized-pentest` and `kali-operator` contain offensive-security guidance.
They are intended strictly for **authorized** engagements, isolated labs, and
CTFs. Both enforce a hard authorization gate and refuse to act without an
explicit, written scope.

Do not use these skills against systems you do not own or do not have explicit
permission to test.

---

## Contributing

Contributions are welcome. Each skill must:

1. contain a valid `SKILL.md` with a `name` and a clear, trigger-focused
   `description` frontmatter;
2. use **placeholders only** for secrets, domains, IPs, and PII — see
   [`leak-guard`](meta/leak-guard);
3. follow the `lowercase-hyphen-case` folder naming used across the repo.

---

## License

[MIT](LICENSE)
