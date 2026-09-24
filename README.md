# Assisted Installer Agentic

Portable, reusable agentic workflows and shared skills for local coding
harnesses and hosted agent platforms.

The repository keeps skill instructions in plain Markdown. Its marketplace
catalogs expose the plugin directories directly; no build or packaging step is
required for installation.

## Included plugins

- [`assisted-installer-skills`](plugins/assisted-installer-skills/) contains
  shared, independently usable skills.
- [`assisted-installer-workflows`](plugins/assisted-installer-workflows/)
  contains interactive, multi-step workflows and depends on shared skills when
  needed.

## Use as an external plugin

Add the marketplace from Git, or use a local clone instead. While the repository
is private, your Git credentials must have read access. The same HTTPS URL works
after it becomes public; authentication is then unnecessary for read access.
For SSH authentication, substitute
`git@github.com:openshift-assisted/assisted-installer-agentic.git` for the HTTPS URL.

### Claude Code

Add the remote marketplace:

```text
/plugin marketplace add https://github.com/openshift-assisted/assisted-installer-agentic.git
```

Or add a local clone:

```text
/plugin marketplace add /path/to/assisted-installer-agentic
```

Then install the plugins:

```text
/plugin install assisted-installer-workflows@assisted-installer
/plugin install assisted-installer-skills@assisted-installer
```

See [Claude Code marketplace instructions](https://code.claude.com/docs/en/discover-plugins#add-marketplaces).

### Codex CLI

Add the remote marketplace:

```bash
codex plugin marketplace add https://github.com/openshift-assisted/assisted-installer-agentic.git
```

Or add a local clone:

```bash
codex plugin marketplace add /path/to/assisted-installer-agentic
```

Then install the desired plugins from `assisted-installer` in your harness's
plugin browser. See [Codex marketplace instructions](https://developers.openai.com/plugins/build/plugins#add-a-marketplace-from-the-cli).

### Marketplace details

The repository has native marketplace catalogs for both hosts:
`.claude-plugin/marketplace.json` is the Claude Code catalog and
`.agents/plugins/marketplace.json` is the Codex catalog. Both use the stable
marketplace name `assisted-installer` and expose both plugins under `plugins/`.
The workflows plugin declares the shared-skills plugin as a Claude dependency;
Codex users should install both plugins when a workflow requires shared skills.

If this path was previously registered under a different marketplace name,
remove the old configured name shown by `codex plugin marketplace list` before
adding the path again. Codex tracks configured marketplace sources by name, so
renaming the catalog does not migrate an existing local registration.

The plugin carries both `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json`
manifests.

## Design boundaries

- Shared skills are reusable leaf capabilities; workflows own orchestration,
  checkpoints, and end-to-end task state.
- External writes require an approval checkpoint in the applicable skill.
- Project build, test, lint, and code-generation commands are discovered from
  the target repository; they are not guessed from file extensions.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development dependencies, validation
instructions, and plugin conventions.
