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

`scripts/test-serena-mcp.py` (added by this same task) is a direct MCP client — it speaks the stdio protocol to Serena's server itself, bypassing the Claude Code tool layer entirely, so it tests the server rather than Claude Code's integration with it. Run it with:

```bash
uv run --with mcp python3 scripts/test-serena-mcp.py
```

It queries its own `main` function, within this same repo:

```python
result = await session.call_tool("find_symbol", {
    "name_path": "main",
    "relative_path": "scripts/test-serena-mcp.py",
    "include_body": True,
})
# → returns the real function body verbatim, starting at (0-indexed) line 26
#   — line 27 in a normal 1-indexed editor/grep view, i.e. `async def main():`

refs = await session.call_tool("find_referencing_symbols", {
    "name_path": "main",
    "relative_path": "scripts/test-serena-mcp.py",
})
# → correctly finds the one real call site, at (0-indexed) line 68
#   — line 69 in a 1-indexed view, i.e. `asyncio.run(main())`
```

Both calls returned exactly correct, verifiable results against this repo's own code — real LSP-backed symbol retrieval and reference-finding, not a canned response. Language server used: `pyright` (Python), started automatically by Serena.

**Note on line numbers:** Serena's tool output uses 0-indexed line numbers (LSP convention). Every number quoted above has been cross-checked against `grep -n` (1-indexed) on the actual file — don't assume the two match without converting.

## Current state of this repo's Serena config

Once `scripts/test-serena-mcp.py` existed, re-running `serena project index . --language python` picked it up (`Indexed files per language: python=1`) and generated `.serena/project.yml` with `language_servers: [python]` — versioned, since Serena's own `.serena/.gitignore` only excludes `/cache` and `/project.local.yml` (both machine-local).
