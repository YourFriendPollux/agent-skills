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
  - [Tools](#tools)
  - [Design](#design)
- [What is a skill?](#what-is-a-skill)
- [Installation](#installation)
- [Safety & responsible use](#safety--responsible-use)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

This repository gathers skills for real engagements and product work, cleaned
up and organized by category. Each skill is a self-contained folder that an
agent loads on demand, so nothing here needs to be "installed" as a package —
you install its folder into your agent's skills directory and it becomes
available.

| Category | Skills | Purpose |
|----------|--------|---------|
| [meta/](meta) | [leak-guard](meta/leak-guard)<br>[skill-anonymizer](meta/skill-anonymizer)<br>[skill-authoring](meta/skill-authoring) | Skill hygiene, anonymization, and authoring |
| [security/](security) | [authorized-pentest](security/authorized-pentest)<br>[kali-operator](security/kali-operator) | Offensive security, scoped and authorized |
| [tools/](tools) | [mirofish](tools/mirofish) | Multi-agent simulation via REST API |
| [design/](design) | [professional-saas](design/professional-saas) | Design-system replication |

---

## Repository structure

```
.
├── meta/
│   ├── leak-guard/
│   ├── skill-anonymizer/
│   │   ├── references/
│   │   └── scripts/
│   └── skill-authoring/
│       ├── assets/
│       └── scripts/
├── security/
│   ├── authorized-pentest/
│   │   └── exploit/
│   └── kali-operator/
│       ├── references/
│       └── scripts/
├── tools/
│   └── mirofish/
│       └── references/
└── design/
    └── professional-saas/
        ├── docs/
        ├── examples/
        └── evals/
```

---

## Skills

### Meta

| Skill | Description |
|-------|-------------|
| [**leak-guard**](meta/leak-guard) | Ensure no sensitive information leaks when an AI writes a skill or other documentation — scan for credentials, secrets, PII, internal network details, and proprietary data, then redact with safe placeholders. Run it before saving any new or edited `SKILL.md`. |
| [**skill-anonymizer**](meta/skill-anonymizer) | Run an exhaustive pre-publication anonymization scan of a repo or document set — secrets, PII, internal IPs/hostnames, client names, proprietary data — classify findings, redact, and produce a sign-off report. Ships with a dependency-free scanner and a full detection catalog. |
| [**skill-authoring**](meta/skill-authoring) | Write a skill that actually works — design the trigger (frontmatter), structure the SKILL.md body, bundle `references/`/`scripts/`/`assets/`, and verify it loads and fires before shipping. Ships with a fill-in template and a validation script. |

### Security

| Skill | Description |
|-------|-------------|
| [**authorized-pentest**](security/authorized-pentest) | Run an authorized penetration test end to end — scoping, recon, enumeration, exploitation, privilege escalation, reporting. Refuses any action outside an explicit scope. |
| [**kali-operator**](security/kali-operator) | Operate Kali Linux like a senior pentester — tool selection, result interpretation, diagnostics, and Bash/Python automation, strictly within an authorized scope. |

### Tools

| Skill | Description |
|-------|-------------|
| [**mirofish**](tools/mirofish) | Operate the MiroFish swarm-intelligence prediction engine — start the backend, prepare, launch, monitor, stop, and generate reports for multi-agent social simulations (Twitter/Reddit/parallel) via its Flask REST API. |

### Design

| Skill | Description |
|-------|-------------|
| [**professional-saas**](design/professional-saas) | Premium dark SaaS identity — near-black canvas, surface ladder, hairline borders, lavender-blue accent, negative-tracking display type, and gradient restraint. Ships with full tokens and a ready-to-use CSS block. |

---

## What is a skill?

A skill is a folder containing a required `SKILL.md` plus optional bundled
resources:

```
skill-name/
├── SKILL.md        # YAML frontmatter (name + description) and markdown instructions
├── references/     # optional: documentation loaded on demand
├── scripts/        # optional: deterministic, runnable helpers
├── assets/         # optional: templates, icons, and other output files
├── docs/           # optional: extended documentation
├── examples/       # optional: usage examples
└── evals/          # optional: evaluation prompts and expected outputs
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
npx skills add YourFriendPollux/agent-skills --list

# install one skill into ./.agents/skills/
npx skills add YourFriendPollux/agent-skills --skill authorized-pentest --yes
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
| Generic | `~/.agent/skills/` | `.agent/skills/` |

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
