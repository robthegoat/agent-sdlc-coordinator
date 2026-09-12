"""One-off verification script for Task 0.2 (see docs/serena-setup.md).

Speaks the MCP stdio protocol directly to Serena's server (bypassing the
Claude Code tool layer) to prove find_symbol / find_referencing_symbols
actually work against real source, not just that the server connects.

Run with: uv run --with mcp python3 scripts/test-serena-mcp.py

Queries this script's own `main` function within this repo — the repo
had no source at all until this script existed, so this is now the
"real symbol-level query against this repo's own code" the task asks
for, not a substitute repo. Portable: TARGET_PROJECT is derived from
this file's own location, not hardcoded to one machine/user.
"""

import asyncio
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

TARGET_PROJECT = str(Path(__file__).resolve().parent.parent)
TARGET_SYMBOL = "main"
TARGET_FILE = "scripts/test-serena-mcp.py"


async def main():
    params = StdioServerParameters(
        command="uvx",
        args=[
            "--from",
            "git+https://github.com/oraios/serena",
            "serena",
            "start-mcp-server",
            "--context",
            "ide-assistant",
            "--project",
            TARGET_PROJECT,
        ],
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(
                "find_symbol",
                {
                    "name_path": TARGET_SYMBOL,
                    "relative_path": TARGET_FILE,
                    "include_body": True,
                },
            )
            for block in result.content:
                if hasattr(block, "text"):
                    print(block.text)

            print("\n--- find_referencing_symbols ---\n")
            refs = await session.call_tool(
                "find_referencing_symbols",
                {
                    "name_path": TARGET_SYMBOL,
                    "relative_path": TARGET_FILE,
                },
            )
            for block in refs.content:
                if hasattr(block, "text"):
                    print(block.text)


asyncio.run(main())
