"""Hermes plugin for the lean-code skill: mode-filtered context injection.

Reads ``SKILL.md``, filters its body by the active intensity level
(``off`` / ``lite`` / ``full`` / ``ultra``) and injects the result before
LLM turns, so the agent only sees the sections that apply.

Mode resolution order: explicit argument -> ``LEAN_CODE_DEFAULT_MODE``
env var -> ``~/.config/lean-code/config.json`` (``defaultMode``) -> ``full``.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

DEFAULT_MODE = "full"
RUNTIME_MODES = {"off", "lite", "full", "ultra"}

ROOT = Path(__file__).resolve().parent
SKILL_FILE = ROOT.parent / "SKILL.md"

_current_mode: str | None = None


def _normalize_runtime_mode(mode: str | None) -> str | None:
    if not isinstance(mode, str):
        return None
    mode = mode.strip().lower()
    return mode if mode in RUNTIME_MODES else None


def _config_dir() -> Path:
    if os.environ.get("XDG_CONFIG_HOME"):
        return Path(os.environ["XDG_CONFIG_HOME"]) / "lean-code"
    if os.name == "nt":
        base = os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming")
        return Path(base) / "lean-code"
    return Path.home() / ".config" / "lean-code"


def _default_mode() -> str:
    env_mode = _normalize_runtime_mode(os.environ.get("LEAN_CODE_DEFAULT_MODE"))
    if env_mode:
        return env_mode
    try:
        data = json.loads((_config_dir() / "config.json").read_text(encoding="utf-8"))
        file_mode = _normalize_runtime_mode(data.get("defaultMode"))
        if file_mode:
            return file_mode
    except Exception:
        pass
    return DEFAULT_MODE


def _strip_frontmatter(text: str) -> str:
    return re.sub(r"^---[\s\S]*?---\s*", "", text or "", count=1)


def _filter_skill_body_for_mode(body: str, mode: str) -> str:
    """Keep mode-tagged rows/items only when they match the active level.

    Recognized shapes, mirroring the SKILL.md authoring convention:
      - table rows:      | **lite** | ... |
      - list items:      - lite: ...
    Everything untagged (headings, prose, pitfalls) is always kept.
    """
    effective = _normalize_runtime_mode(mode) or DEFAULT_MODE
    lines = []
    for line in _strip_frontmatter(body).splitlines():
        table_label = re.match(r"^\|\s*\*\*(.+?)\*\*\s*\|", line)
        if table_label:
            label_mode = _normalize_runtime_mode(table_label.group(1))
            if label_mode and label_mode != effective:
                continue
        list_label = re.match(r"^-\s*([^:]+):\s*", line)
        if list_label:
            label_mode = _normalize_runtime_mode(list_label.group(1))
            if label_mode and label_mode != effective:
                continue
        lines.append(line)
    return "\n".join(lines)


def _fallback_instructions(mode: str) -> str:
    return (
        f"LEAN-CODE MODE ACTIVE — level: {mode}\n\n"
        "Write the minimum code that satisfies the requirement: YAGNI, stdlib "
        "first, no unrequested abstractions, no speculative scaffolding. "
        "Deletion over addition. Do not simplify away validation, error "
        "handling, security, accessibility, or explicitly requested behavior."
    )


def build_injected_context(mode: str | None = None) -> str:
    """Return the mode-filtered lean-code context injected before LLM turns."""
    effective = _normalize_runtime_mode(mode) or _default_mode()
    if effective == "off":
        return ""
    try:
        body = SKILL_FILE.read_text(encoding="utf-8")
        filtered = _filter_skill_body_for_mode(body, effective)
        return f"LEAN-CODE MODE ACTIVE — level: {effective}\n\n{filtered}"
    except OSError:
        return _fallback_instructions(effective)


def _pre_llm_call(session_id: str = "", **_: object) -> dict[str, str] | None:
    """Hook name used by the Hermes gateway: inject context before a turn."""
    context = build_injected_context()
    return {"context": context} if context else None


def _skill_prompt(command: str, args: str = "") -> str:
    tail = args.strip()
    target = f"\n\nUser arguments: {tail}" if tail else ""
    return f"Load and follow the lean-code skill `lean-code:{command}`.{target}"


def rewrite_gateway_command(event: object = None, gateway: object = None, **_: object) -> dict[str, str] | None:
    """Rewrite authorized gateway /lean-* commands into normal agent prompts."""
    text = str(getattr(event, "text", "") or "").strip()
    if not text.startswith("/"):
        return None
    head, _, rest = text[1:].partition(" ")
    command = head.replace("_", "-").lower()
    if command not in {"lean-code", "lean-review"}:
        return None
    return {"action": "rewrite", "text": _skill_prompt(command, rest)}


def _handle_mode_command(raw_args: str) -> str:
    global _current_mode
    arg = (raw_args or "").strip().lower()
    if not arg:
        mode = _current_mode or _default_mode()
        return f"Lean-code mode: {mode}. Use `/lean-code lite|full|ultra|off`."
    mode = _normalize_runtime_mode(arg)
    if not mode:
        return "Usage: /lean-code [lite|full|ultra|off]"
    _current_mode = mode
    return f"Lean-code mode set to {mode}."


if __name__ == "__main__":
    import sys

    mode = sys.argv[1] if len(sys.argv) > 1 else None
    print(build_injected_context(mode))
