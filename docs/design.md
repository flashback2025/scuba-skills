# Packaging and configuration rationale

Reviewed on 2026-10-02. The choices below are Scuba's design, informed by these
public examples and official documentation. They are not a claim that MCP mandates
a `.scuba/config.json` file.

## Portable workflow package

The [Agent Skills specification](https://agentskills.io/specification) defines
`SKILL.md`, metadata, and supporting files. It does not define an interoperable
user-settings schema. We use `skills/<name>/SKILL.md` with resources inside each
skill so installers can copy individual skills without breaking references.

[Vercel's Skills CLI](https://github.com/vercel-labs/skills) discovers this layout
and supports selecting skills and target agents. We document that existing
installer and manual copying instead of introducing another installation script.

## Destination settings belong to the adopting project

[Anthropic's plugin-settings example](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/plugin-settings/SKILL.md)
shows agents reading explicitly documented settings from a project-local file.
Its `.claude/<plugin>.local.md` format is specific to that plugin ecosystem and
intended for untracked per-user settings. We adopt the separation from installed
instructions, while using an agent-neutral JSON path for a team's repository
destination. That path and JSON shape are our convention.

[OpenAI's Notion knowledge-capture skill](https://github.com/openai/skills/blob/main/skills/.curated/notion-knowledge-capture/SKILL.md)
locates a destination and verifies it before creating knowledge. This supports an
interactive setup step rather than shipping a vendor's internal wiki identifier.
We use a stable collection ID after selection so future runs are deterministic.
We do not copy old feature flags or host setup commands from example skills; current
client documentation governs installation.

## Native MCP connection and OAuth

The [MCP remote-server guide](https://modelcontextprotocol.io/docs/develop/connect-remote-servers)
describes adding a remote endpoint and completing authentication through the client.
The [current MCP authorization specification](https://modelcontextprotocol.io/specification/latest/basic/authorization)
defines HTTP authorization and discovery, not skill destination settings. We rely
on client OAuth and keep tokens out of project configuration. This package does not
implement a transport or pin a protocol revision; client and server negotiate that.

[Codex's skill documentation](https://developers.openai.com/codex/skills) and
[OpenAI's Linear skill metadata](https://github.com/openai/skills/blob/main/skills/.curated/linear/agents/openai.yaml)
demonstrate declaring an MCP dependency in `agents/openai.yaml`. We supply that
metadata as a host-specific convenience, while documenting manual setup through
[Codex MCP](https://developers.openai.com/codex/mcp) and
[Claude Code MCP](https://code.claude.com/docs/en/mcp).

## Boundaries

The public workflow has no team UUID, organization-specific preapproval, internal
repository paths, or private examples. Setup never assumes collection creation also
shares it. A configured destination never bypasses the server's audience confirmation.
Version 1 ships only the setup and engineering-memory skills; client-specific plugin
packaging can be added without changing their destination contract.
