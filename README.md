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
you install its folder into your agent's skills directory and it becomes
available.

| Category | Skills | Purpose |
|----------|--------|---------|
| [security/](security) | [authorized-pentest](security/authorized-pentest)<br>[kali-operator](security/kali-operator) | Offensive security, scoped and authorized |
| [meta/](meta) | [leak-guard](meta/leak-guard) | Skill hygiene and anonymization |
| [tools/](tools) | [mirofish](tools/mirofish) | Tool / API integration |
| [design/](design) | [github-design](design/github-design)<br>[google-design](design/google-design) | Design-system replication |

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

| Skill | Description |
|-------|-------------|
| [**authorized-pentest**](security/authorized-pentest) | Run an authorized penetration test end to end — scoping, recon, enumeration, threat modeling, controlled exploitation, privilege escalation, and reporting. For labs, CTFs, bug bounty, and contracted engagements; refuses any action without authorization. |
| [**kali-operator**](security/kali-operator) | Operate Kali Linux like a senior pentester / security analyst — terminal work, tool selection, result interpretation, diagnostics, and Bash/Python automation, strictly within an authorized scope. |

### Meta

| Skill | Description |
|-------|-------------|
| [**leak-guard**](meta/leak-guard) | Scan skills and documentation for credentials, secrets, PII, internal network details, and proprietary data, then redact with safe placeholders. Apply to any new or edited `SKILL.md`, prompt, or document before it is saved. |

### Tools

| Skill | Description |
|-------|-------------|
| [**mirofish**](tools/mirofish) | Operate the MiroFish swarm-intelligence prediction engine — prepare, launch, monitor, stop, and report on multi-agent social simulations (Twitter / Reddit / parallel) via its Flask REST API. |

### Design

| Skill | Description |
|-------|-------------|
| [**github-design**](design/github-design) | Replicate GitHub's visual identity and Primer design system in a frontend project — color tokens (light & dark), Mona Sans / Hubot Sans typography, spacing, radii, Octicons, and the component catalog. |
| [**google-design**](design/google-design) | Replicate Google's visual identity and Material Design 3 (Material You) — brand colors, Google Sans, the tonal color system, type scale, shape, elevation, and component patterns. |

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
3. follow the `lowercase-hyphen-case` folder naming used across the repo.

---

## License

[MIT](LICENSE)
