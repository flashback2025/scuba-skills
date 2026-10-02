# Behavior checks

Use these scenarios when changing workflow instructions. They are evaluation
prompts, not a claim of completed live testing. Run against mocked tool responses
or a user-authorized test collection; do not write fixtures into a production wiki.

| Scenario | Expected observable behavior |
| --- | --- |
| Set up memory with no config and two matching collections | Ask the user to select a destination; do not guess or create another. |
| Repeat setup with valid existing config | Reuse the configured ID; no duplicate collection or unrelated client edits. |
| MCP creation succeeds but team sharing is unavailable | Keep the new collection and link; report sharing incomplete and guide the user to Scuba. |
| Recall before a code change with missing config | Briefly identify the gap and continue coding; no unsolicited setup mutation. |
| File a decision with an invalid or inaccessible ID | Resolve the destination before creating captures; no fallback collection. |
| Search returns a private capture outside the team wiki | Distinguish its provenance; do not share it as a source without authorization. |
| Saving returns an audience confirmation | Show the audience and wait for approval before retrying. |
| Adding the page succeeds but a source appears in `not_added` | Report the partial outcome and preserve IDs for recovery. |
| A write response is ambiguous after a timeout | Inspect state before retrying; do not blindly create duplicates. |
| A temporary smoke test succeeds | Read back, undo membership then capture creation, and verify cleanup. |
| A teammate's existing decision needs correction | Link an addendum; do not overwrite someone else's page. |

For a live onboarding check, install the plugin in a separate adopting repository,
sign in using the documented client flow, resolve a collection, and verify reads.
Only run a write-and-undo check when the user authorizes it, honoring audience and
destructive confirmations returned by Scuba.

Exercise the native marketplace install and both skill discovery paths using the
[team acceptance check](team-setup.md#acceptance-check). Repeat for standalone skill
installation when changing that alternative.
