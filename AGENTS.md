# AGENTS.md

This repository contains standalone agent skills. Skill instructions are
executable guidance, so changes require the same care as code changes.

## Repository layout

```text
plugins/
  assisted-installer-skills/
    .claude-plugin/plugin.json
    .codex-plugin/plugin.json
    skills/
      <skill>/SKILL.md              # shared, independently usable skill
.agents/plugins/marketplace.json
.claude-plugin/marketplace.json
scripts/                     # deterministic validation and isolation tests
```

## Authoring rules

- Keep shared skills independently usable with documented inputs, outputs, and
  capability boundaries. Allow normal skill discovery, instruction loading, and
  invocation; do not couple workflows to private installation paths or on-disk
  handoffs.
- When a workflow explicitly names a skill for a step, it must discover, load,
  and use that skill for the step. Do not silently substitute another skill or
  recreate its procedure. If the required skill is unavailable or ambiguous,
  stop the dependent step and report the missing prerequisite. Delegated steps
  must pass this requirement to the worker.
- Keep shared skills in `assisted-installer-skills` and end-to-end orchestration
  in separate workflow plugins. Declare required shared-plugin dependencies in
  the Claude manifest; do not invent unsupported cross-plugin dependency fields
  for Codex.
- Keep plugin Markdown references relative and inside their plugin so they
  work after installation. Refer to other plugins' skills through discovery and
  invocation, not filesystem links. Repository documentation may link across plugins.
- Keep `SKILL.md` files concise; put substantial detail in references.
- Each skill must define its inputs, outputs, checkpoint behavior, and terminal
  failure conditions.
- Treat external systems as capability providers. Describe semantic operations
  first and use a provider-specific CLI only as a fallback.
- Do not add permissions, remote writes, or autonomous loops implicitly.
- Preserve project instructions from the target repository and discover its
  validation commands instead of inventing them.

## Validation

Run:

```bash
make validate
make test
```

Behavioral changes to distributed skills should update the plugin and
marketplace release metadata when a new plugin release is intended.
