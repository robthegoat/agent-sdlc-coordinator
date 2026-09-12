# Agent SDLC Coordinator

A reusable template for running significant builds as a **multi-session, GitHub-tracked, coordinator-overseen** agentic development process — instead of one large single-session build.

See [`docs/process.md`](docs/process.md) for the full process spec.

## Why this exists

Building an entire feature/page/product in one uninterrupted agent session leads to large batches of unreviewed work landing all at once, with no checkpoint to catch a wrong direction early. This template enforces:

- Work broken into **phases**, phases broken into **tasks**, tracked as GitHub Issues on a GitHub Project board.
- A **coordinator** agent that re-orients on the plan and the codebase (via Serena MCP) at the start of every session and after every context compaction, then assigns the right agent to the right issue.
- A **mandatory review-and-fix loop**: no task closes without an actual code review pass and any resulting fixes applied.
- Strict session boundaries: one task closed and documented before the next begins.

## Repository layout

- `.claude/agents/` — coordinator and worker agent definitions (Phase 1/2). Empty for now.
- `.github/ISSUE_TEMPLATE/` — phase/task issue templates (Phase 3). Empty for now.
- `docs/` — process specs and setup guides. Currently: `process.md` (the lifecycle this template enforces).

## Status

This repo is currently in its planning phase. See the Project board and open Phase issues for what's built vs. not yet built.
