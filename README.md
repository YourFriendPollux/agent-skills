# Skills

A curated collection of reusable, self-contained **skills** for AI coding agents —
modular instructions that give an agent specialized workflows, guardrails, and
domain knowledge for a specific task or domain.

---

## Table of contents

- [Overview](#overview)
- [Repository structure](#repository-structure)
- [Skills](#skills)
  - [Meta](#meta)
  - [Security](#security)
  - [Coding](#coding)
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
you install its folder into your agent's skills directory and it becomes
available.

| Category | Skills | Purpose |
|----------|--------|---------|
| [meta/](meta) | [leak-guard](meta/leak-guard)<br>[skill-anonymizer](meta/skill-anonymizer)<br>[skill-authoring](meta/skill-authoring) | Skill hygiene and anonymization<br>Exhaustive pre-publication leak scan<br>How to write skills that actually work |
| [security/](security) | [authorized-pentest](security/authorized-pentest)<br>[kali-operator](security/kali-operator) | Offensive security, scoped and authorized |
| [coding/](coding) | [lean-code](coding/lean-code) | Code minimalism and review, mode-filtered |
| [tools/](tools) | [mirofish](tools/mirofish) | Tool / API integration |
| [design/](design) | [github-design](design/github-design)<br>[google-design](design/google-design)<br>[linear-design](design/linear-design) | Design-system replication |

---

## Repository structure

```
.
├── meta/
│   ├── leak-guard/
│   ├── skill-anonymizer/
│   └── skill-authoring/
├── security/
│   ├── authorized-pentest/
│   └── kali-operator/
├── coding/
│   └── lean-code/
├── tools/
│   └── mirofish/
└── design/
    ├── github-design/
    ├── google-design/
    └── linear-design/
```

---

## Skills

### Meta

| Skill | Description |
|-------|-------------|
| [**leak-guard**](meta/leak-guard) | Scan skills and documentation for credentials, secrets, and PII, then redact them with safe placeholders. Run it before saving any new or edited `SKILL.md`. |
| [**skill-anonymizer**](meta/skill-anonymizer) | Run an exhaustive pre-publication anonymization scan of a repo or document set — secrets, PII, internal IPs/hostnames, client names, proprietary data — classify findings, redact, and produce a sign-off report. Ships with a dependency-free scanner and a full detection catalog. |
| [**skill-authoring**](meta/skill-authoring) | Write a skill that actually works — design the trigger (frontmatter), structure the SKILL.md body, bundle `references/`/`scripts/`/`assets/`, and verify it loads and fires before shipping. Ships with a fill-in template and a validation script. |

### Security

| Skill | Description |
|-------|-------------|
| [**authorized-pentest**](security/authorized-pentest) | Run an authorized penetration test end to end — recon, enumeration, exploitation, privilege escalation, reporting. Refuses any action outside an explicit scope. |
| [**kali-operator**](security/kali-operator) | Operate Kali Linux like a senior pentester — tool selection, result interpretation, diagnostics, and Bash/Python automation, strictly within an authorized scope. |

### Coding

| Skill | Description |
|-------|-------------|
| [**lean-code**](coding/lean-code) | Write minimal, efficient code and review diffs for over-engineering, with intensity levels (lite / full / ultra) and a Hermes plugin that injects only the sections matching the active mode. |

### Tools

| Skill | Description |
|-------|-------------|
| [**mirofish**](tools/mirofish) | Operate the MiroFish swarm-intelligence prediction engine — prepare, launch, monitor, stop, and report on multi-agent social simulations via its Flask REST API. |

### Design

| Skill | Description |
|-------|-------------|
| [**github-design**](design/github-design) | Replicate GitHub's visual identity and Primer design system — color tokens (light & dark), typography, spacing, Octicons, and the component catalog. |
| [**google-design**](design/google-design) | Replicate Google's visual identity and Material Design 3 — brand colors, Google Sans, the tonal system, type scale, and component patterns. |
| [**linear-design**](design/linear-design) | Replicate Linear's premium dark SaaS identity — near-black canvas, surface ladder, hairline borders, lavender-blue accent, Linear typography with negative tracking, and gradient restraint. Ships with full tokens and a ready-to-use CSS block. |

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

Skills are plain folders — there is no package to install. An agent discovers a
skill as soon as its folder lands in the agent's skills directory. Pick the
method that fits your setup.

### With the skills CLI (recommended)

Install individual skills straight from this repository without cloning it:

```bash
# preview the skills available in this repo
npx skills add Dandl-ai/agent-skills --list

# install one skill into ./.agents/skills/
npx skills add Dandl-ai/agent-skills --skill authorized-pentest --yes
```

### Copy the folder

Clone or download the repo, then copy a skill folder into your agent's skills
directory. The agent discovers it automatically:

| Agent | User directory | Project directory |
|-------|----------------|-------------------|
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| Codex | `~/.codex/skills/` | — |
| Cursor | `~/.cursor/skills/` | `.cursor/skills/` |
| Windsurf | `~/.windsurf/skills/` | `.windsurf/skills/` |
| Hermes | `~/.hermes/skills/` | — |

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
3. follow the `lowercase-hyphen-case` folder naming used across the repo;
4. pass `python3 meta/skill-authoring/scripts/check_skill.py <skill-folder>`
   with zero errors — see [`skill-authoring`](meta/skill-authoring) for the
   full authoring method and a fill-in template.

---

## License

Released under the [GNU Affero General Public License v3.0](LICENSE).
