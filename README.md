# Scuba skills

Give your coding agent access to your team's engineering memory in [Scuba](https://scuba.app).
Recall why a decision was made, avoid repeating failed approaches, and preserve useful
conclusions with their sources.

| Skill | Use it to |
| --- | --- |
| `scuba-setup` | Connect Scuba, select a team collection, and configure a repository. |
| `scuba-codebase-memory` | Recall prior decisions and record approved decisions, findings, incidents, and PR outcomes. |

These are portable [Agent Skills](https://agentskills.io/specification). Start with
Codex or Claude Code; other hosts need skill loading, repository file access, and a
remote HTTP MCP connection with OAuth. No local Scuba server is required.

## Quick start

### 1. Install the skills

From the code repository where you want engineering memory, use the
[Vercel Skills CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add flashback2025/scuba-skills --skill scuba-setup scuba-codebase-memory
```

Choose your coding agent and project scope in the installer. This installs workflow
instructions; it does not authenticate Scuba or choose a collection for you.

Alternatively, copy the two directories under `skills/` into your host's skill
directory: `.agents/skills/` for Codex or `.claude/skills/` for Claude Code. Keep each
directory's `agents`, `assets`, and `references` alongside its `SKILL.md`. Check for
existing installations before copying. Follow your host's reload instructions if the
skills do not appear.

### 2. Connect Scuba

**Codex**:

```bash
codex mcp add scuba --url https://api.scuba.app/mcp/
codex mcp login scuba
```

**Claude Code**:

```bash
claude mcp add --transport http --scope user scuba https://api.scuba.app/mcp/
```

Then run `/mcp` in Claude Code and complete the browser login. Each teammate signs
in with their own Scuba account. Existing working Scuba connectors can be reused.

See [MCP setup](skills/scuba-setup/references/mcp-setup.md) for project-scoped
configuration and troubleshooting. The Codex skill metadata also declares the MCP
dependency; support for dependency installation varies by host.

### 3. Configure your team's memory

In your adopting repository, ask your agent:

> Use scuba-setup to configure engineering memory for this repository. Help me
> choose an existing shared Eng Wiki collection or create one for my team.

The setup skill helps you select a collection, check access, and create
`.scuba/config.json` in that repository:

```json
{
  "version": 1,
  "engineering_memory": {
    "collection_id": "<collection-uuid>"
  }
}
```

Replace the placeholder with the actual collection ID. The setup skill can resolve
a collection link or name through Scuba. Collection creation through MCP starts
private: use Scuba's sharing controls to give your teammates access. Collection
access must be checked for each person; a working config does not grant access.

This file is **a Scuba skills convention**, not an MCP or Agent Skills standard.
The skills explicitly read it; no client automatically substitutes these values.
It contains a destination, never tokens or credentials. Keep it outside installed
skill directories so skill upgrades preserve team settings.

Private team repositories may commit it. In a public repository, keep real team
configuration untracked and ignore `.scuba/config.json`; commit an example instead.
Several repositories may point at the same collection. See the
[configuration contract](docs/configuration.md) and
[example config](skills/scuba-setup/assets/scuba-config.example.json).

### 4. Use it

> Before we change the sync architecture, use scuba-codebase-memory to look for
> previous decisions and failed approaches.

> Record why we chose this approach in our engineering wiki, with the alternatives
> and the PR link.

Reads retrieve historical context and check it against the current code. The skill
offers to save valuable conclusions; an explicit filing request authorizes that
write. Sharing confirmations from Scuba still apply. It reports what was saved,
what became shared, and undo information when available.

For recurring use, add the [agent guidance snippet](skills/scuba-setup/assets/agent-guidance.md)
to your repository's existing `AGENTS.md` or `CLAUDE.md`.

## Configuration and setup

- [Configuration contract](docs/configuration.md)
- [MCP connection examples](skills/scuba-setup/references/mcp-setup.md)

## Development

Validate the skill metadata, packaged references, configuration schema, and examples:

```bash
uv run scripts/validate.py
```

The workflow instructions have no Python runtime dependency. Python is used only
for repository validation. See [behavior checks](docs/behavior-checks.md) for manual
scenarios to exercise with your agent. Full client OAuth and team sharing should be
verified in your own account before rollout.

## License

[MIT](LICENSE).
