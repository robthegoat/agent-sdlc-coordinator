# Serena MCP setup

[Serena](https://github.com/oraios/serena) gives an agent IDE-grade *semantic* code understanding — symbol-level navigation (find-references, go-to-definition, rename) backed by real language servers, plus a per-project memory system — instead of relying on grep/text search alone. The coordinator agent (Phase 1) uses it to re-orient on the actual codebase at session start and after every context compaction.

## Install

Serena is run via `uvx` (no separate install step needed once `uv` is present):

```bash
brew install uv   # provides uvx
```

## Register as an MCP server

```bash
claude mcp add --scope user serena -- uvx --from git+https://github.com/oraios/serena serena start-mcp-server --context ide-assistant
```

**Scope: `user`, not `project`.** Serena is a general-purpose dev tool, useful in any repo, not something specific to this template. Registering it at user scope means it's available in every Claude Code session for this account, and it can `activate_project` for whichever repo the current session is working in — it isn't locked to `agent-sdlc-coordinator`.

Verify registration:

```bash
claude mcp get serena
# Status: ✔ Connected
```

## Important caveat: session restart required

`claude mcp add` registers the server in config immediately, and `claude mcp list`/`get` can health-check the connection right away — but an **already-running** Claude Code session does not pick up newly-registered MCP servers or their tools. The tool list for a session is resolved at session start. If you add Serena mid-session, you won't see its tools until you start a new session.

This matters for the coordinator's own lifecycle (`docs/process.md`): the coordinator's "re-orient via Serena" step only works in a session that started *after* Serena was registered.

## Verifying it actually works (not just "connected")

Because this template repo has no real source code yet, indexing it directly proves nothing interesting:

```bash
cd ~/agent-sdlc-coordinator
uvx --from git+https://github.com/oraios/serena serena project index . --name agent-sdlc-coordinator
# → "No source files for supported language servers were found ... Indexed files per language:" (0 files)
```

That's the honest, expected result for a repo with only markdown in it.

To prove the underlying symbol-level engine genuinely works, it was exercised against a repo with real code (`kinetic-kings-data-platform`, a separate project on this machine) via a direct MCP client script (bypassing the Claude Code tool layer entirely, to test the server itself):

```python
# minimal MCP stdio client — full script at scripts/test-serena-mcp.py
result = await session.call_tool("find_symbol", {
    "name_path": "query_shopify_graphql",
    "relative_path": "etl/shopify_products.py",
    "include_body": True,
})
# → returns the real function body, lines 16-19, verbatim

refs = await session.call_tool("find_referencing_symbols", {
    "name_path": "query_shopify_graphql",
    "relative_path": "etl/shopify_products.py",
})
# → correctly finds the one real call site, at etl/shopify_products.py:71
```

Both calls returned exactly correct, verifiable results — real LSP-backed symbol retrieval and reference-finding, not a canned response. Language server used: `pyright` (Python), started automatically by Serena.

## Current state of this repo's Serena config

`serena project index .` auto-generated `.serena/project.yml` (versioned — it's Serena's standard project config, `language_servers: []` until this repo has real source code to index) and `.serena/.gitignore` (Serena's own recommended excludes: `/cache` and `/project.local.yml`, both machine-local and correctly not versioned).
