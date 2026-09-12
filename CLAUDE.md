# CLAUDE.md

This is a skeleton. Full binding rules land in Phase 5 ([issue #6](https://github.com/robthegoat/agent-sdlc-coordinator/issues/6)) — until then, treat every section below as a stub pointing at the real spec in `docs/process.md`, not as the final word.

## Project purpose

This repo is a reusable template for running significant builds as a multi-session, GitHub-tracked, coordinator-overseen agentic development process, instead of one large single-session build. See [`docs/process.md`](docs/process.md) for why this exists and what it enforces.

## Session lifecycle

Work happens in separate sessions, never in one continuous build: an idea session, then a phase-planning session per phase, then one implementation session per task. See ["The 3-stage session lifecycle"](docs/process.md#the-3-stage-session-lifecycle) in `docs/process.md` for the full spec. (Stub — Phase 5 turns this into binding instructions.)

## Review-and-fix loop policy

No task closes without an actual review pass and any resulting fixes applied — not optional, not skipped for small changes. See ["The review-and-fix loop"](docs/process.md#the-review-and-fix-loop-mandatory-every-task) in `docs/process.md` for the mechanics, and `docs/github-conventions.md` for how it's been practiced so far. (Stub — Phase 5 turns this into binding instructions.)

## Coordinator behavior

At the start of every session, and after every context compaction, the coordinator re-reads this file, re-reads the GitHub Project board's current state, and re-orients on the actual codebase via Serena MCP before assigning any work. See ["Coordinator behavior"](docs/process.md#coordinator-behavior-every-session-start-and-every-context-compaction) in `docs/process.md`. The coordinator agent itself doesn't exist yet — that's Phase 1 ([issue #2](https://github.com/robthegoat/agent-sdlc-coordinator/issues/2)). (Stub — Phase 5 turns this into binding instructions.)
