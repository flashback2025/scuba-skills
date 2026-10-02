# Scuba skills

Give your coding agent access to your team's engineering memory in [Scuba](https://scuba.app).
Recall why a decision was made, avoid repeating failed approaches, and preserve useful
conclusions with their sources.

Install the **Scuba plugin** to get both skills and the hosted MCP connection:

| Skill | Use it to |
| --- | --- |
| `scuba-setup` | Connect Scuba, select a team collection, and configure a repository. |
| `scuba-codebase-memory` | Recall prior decisions and record approved decisions, findings, incidents, and PR outcomes. |

No local Scuba server is required. Each person signs in with their own Scuba account.

## Quick start

### 1. Install the plugin

**Codex** — register the marketplace and install Scuba:

```bash
codex plugin marketplace add flashback2025/scuba-skills
codex plugin add scuba@scuba
```

The marketplace also appears as a source in the desktop app's plugin directory.
If your Codex version does not offer `plugin add`, install from that directory.
Restart or open a new session after installation, then complete the Scuba sign-in
when prompted. Inspect the plugin's connection in `/mcp`; use the connection name
shown by your client when authenticating.

**Claude Code** — run from the repository where you want engineering memory:

```bash
claude plugin marketplace add flashback2025/scuba-skills
claude plugin install scuba@scuba --scope project
```

Reload plugins or start a new session, then use `/mcp` to sign in to the plugin's
Scuba connection. Project scope records the enabled plugin in `.claude/settings.json`;
teammates still install it on their own machines. Use `--scope user` for personal
installation across projects.

Already using Scuba? Check for a working connection and existing copies of these
skills before installing. When migrating, verify the plugin first, then remove only
the superseded standalone Scuba configuration and skill copies. Plugin connections
may have different names and may require their own sign-in. Do not configure both
manual setup and the plugin by default.

### 2. Configure your team's memory

In your adopting repository, ask your agent:

> Use scuba-setup to configure engineering memory for this repository. Help me
> choose an existing shared Eng Wiki collection or create one for my team.

The setup skill checks access and writes `.scuba/config.json` in that repository:

```json
{
  "version": 1,
  "engineering_memory": {
    "collection_id": "<collection-uuid>"
  }
}
```

The skill can resolve a collection link or name to its ID. Collection creation
through MCP starts private: use Scuba's sharing controls to give teammates access.
A destination file does not grant access or authorize writes.

This file is **a Scuba skills convention**, separate from MCP and plugin configuration.
Private team repositories may commit it; public repositories should ignore the real
file and commit an example instead. It stays outside the installed plugin so
upgrades preserve your team's destination. See the [configuration contract](docs/configuration.md).

### 3. Use it

> Before we change the sync architecture, use scuba-codebase-memory to look for
> previous decisions and failed approaches.

> Record why we chose this approach in our engineering wiki, with the alternatives
> and the PR link.

Claude Code also exposes `/scuba:scuba-setup` and `/scuba:scuba-codebase-memory`.
The skills offer to save valuable conclusions; an explicit filing request authorizes
that write. Scuba's sharing confirmations still apply.

## Set it up for your team

Commit the client-specific plugin configuration and your destination in the adopting
repository. Every teammate installs the same plugin, signs in separately, and verifies
access to the same collection. The [team setup guide](docs/team-setup.md) includes:

- Claude's shared marketplace and enabled-plugin settings.
- Codex's `.agents/plugins/marketplace.json` team catalog.
- Pinning a reviewed release and migrating existing local skills.
- An installation and read-access acceptance check.

Add the [agent guidance snippet](skills/scuba-setup/assets/agent-guidance.md) to your
existing `AGENTS.md` or `CLAUDE.md` when you want proactive memory recall.

## Alternatives: standalone skills and MCP

For hosts without plugin support, or teams that already manage Scuba connections,
install just the portable [Agent Skills](https://agentskills.io/specification):

```bash
npx skills add flashback2025/scuba-skills --skill scuba-setup scuba-codebase-memory
```

Choose your agent and project scope. Alternatively, copy the two `skills/` directories
with their supporting files into `.agents/skills/` for Codex or `.claude/skills/` for
Claude Code. These methods do not install or authenticate an MCP connection.

Then reuse your existing Scuba connection or follow [manual MCP setup](skills/scuba-setup/references/mcp-setup.md#manual-connection-alternative).
Claude supports a committed project `.mcp.json`; Codex supports a trusted project's
`.codex/config.toml`. Both examples and personal setup are documented there.
Collection setup is the same for plugin and standalone installations.

## Package and maintain

This repository is a single plugin and two small marketplace catalogs:

- `plugin.json`, `mcp.json`, and `skills/`: portable plugin package.
- `.agents/plugins/marketplace.json`: Codex catalog.
- `.claude-plugin/plugin.json` and `.mcp.json`: Claude-compatible package metadata and MCP configuration.
- `.claude-plugin/marketplace.json`: Claude catalog.

The catalogs distribute the same skills and endpoint. They are GitHub-hosted
catalogs, not listings in the vendors' official directories. Official directory
submission is separate. This follows [OpenAI's plugin packaging guide](https://developers.openai.com/plugins/build/plugins)
and [Claude's marketplace guide](https://code.claude.com/docs/en/plugin-marketplaces).

Validate the package, skills, references, and destination schema:

```bash
uv run scripts/validate.py
claude plugin validate . --strict
claude plugin validate .claude-plugin/plugin.json --strict
```

Python is used only for validation, not by the installed workflows. Bump the version
in both plugin manifests for a release; installed clients can cache by version.
See [behavior checks](docs/behavior-checks.md) for acceptance scenarios.

## License

[MIT](LICENSE).
