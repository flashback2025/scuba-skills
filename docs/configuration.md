# Configuration contract

This is an application convention defined by Scuba skills, not a configuration
standard supplied by MCP, Codex, Claude Code, or Agent Skills.

## Location and scope

Read `.scuba/config.json` from the root of the repository being worked on. Skill
installation paths do not select the target repository. If several repositories
are in scope, identify the one the user means before choosing a destination.

There are no user-global settings, environment-variable overrides, or implicit
fallback destinations in version 1. A team can use the same collection ID across
repositories. Configuration changes do not require rewriting installed skills.

## Fields

| Field | Required | Meaning |
| --- | --- | --- |
| `version` | Yes | Integer `1`. Reject unsupported versions instead of guessing. |
| `engineering_memory.collection_id` | Yes | UUID of the explicitly selected Scuba collection. |

Use the [example](../skills/scuba-setup/assets/scuba-config.example.json) and
[JSON Schema](../skills/scuba-setup/assets/scuba-config.schema.json). The example's
placeholder is deliberately not a valid destination; setup replaces it with a
verified UUID. The schema rejects unknown fields so misspelled settings do not
silently appear to work. Setup preserves an existing file and reports unexpected
fields instead of deleting them to make validation pass.

This file must not contain credentials. Native MCP client configuration owns the
endpoint and each person's OAuth session. A destination ID neither grants access
nor authorizes a write or audience expansion. Search remains library-wide unless
the current tool offers and receives an explicit filter; this configuration does
not add a server-side search filter.

## Sharing the configuration

A private team code repository can commit the destination file for teammates.
For a public code repository, ignore `.scuba/config.json` and distribute a template
without the real team ID. A collection ID is not a credential, but it is unnecessary
internal destination information to publish. With unknown repository visibility,
keep real configuration untracked until the user decides.

Creating a collection through MCP starts private. Sharing with teammates is a
separate operation in Scuba. Do not infer team access from a collection's name, a
successful read by one account, or its private/public type.

## Failure behavior

Missing, malformed, unsupported, or inaccessible configuration never redirects
writes. An incidental memory lookup reports the gap briefly and does not block
unrelated work. An explicit setup or memory request resolves the missing information
with the user. Repeated setup reuses an existing verified destination.

## MCP configuration

See [client-specific setup](../skills/scuba-setup/references/mcp-setup.md). Codex uses
`config.toml`; Claude Code can use project `.mcp.json`. The supplied Codex
`agents/openai.yaml` files declare a tool dependency, not team settings. A root
`.mcp.json` is intentionally absent from this distribution: installing a skill is
not the same as installing a client-specific plugin or configuring a connection.
