# Process Spec

## The 3-stage session lifecycle

This template assumes work happens across **separate Claude Code sessions**, never in one continuous build. Each stage below is a distinct session (or repeated sessions, for Stage C).

### Stage A — Idea session (one-time, per project)

1. Question the requester to flesh the idea out fully before writing anything down.
2. Turn the fleshed-out idea into a **phased implementation plan** (this document's "Phases" section is the template's own example of that output).
3. Create a GitHub Project board and one Issue per phase (high-level scope only — not yet broken into tasks).
4. End the session. Do not start implementing.

### Stage B — Phase-planning session (one per phase, when that phase's turn comes)

1. Pick the next open phase (coordinator determines this from the Project board state).
2. Break that phase into concrete, independently-closeable **task** issues.
3. Create the task issues in GitHub, linked to the phase, with acceptance criteria.
4. End the session. Do not start implementing.

### Stage C — Implementation session (repeated, one per task)

1. Pick **one task** issue.
2. Implement it.
3. Test it.
4. Document it.
5. Run the **review-and-fix loop** (see below) — this is not optional and does not get skipped for small changes.
6. Only after the loop passes clean, close the task issue with a summary of what shipped.
7. End the session (or, if continuing, treat the next task as a fresh Stage C pass — never batch multiple tasks into one implementation pass).

Repeat Stage C until every task in the current phase is closed, then return to Stage B for the next phase.

## The review-and-fix loop (mandatory, every task)

1. Implementer produces the change.
2. Reviewer (a dedicated review pass — see `.claude/agents/reviewer.md` once Phase 2 exists) reviews the actual diff for correctness and quality issues.
3. Every finding gets fixed or explicitly and visibly dismissed with a reason — never silently dropped.
4. Reviewer re-checks after fixes.
5. Only a clean pass allows the task issue to close.

## Coordinator behavior (every session start, and every context compaction)

The coordinator (`.claude/agents/coordinator.md`, once Phase 1 exists) must, before assigning any work:

1. Re-read this repo's `CLAUDE.md`.
2. Re-read the current GitHub Project board state (open phases, open tasks, in-review items).
3. Re-orient on the actual codebase via Serena MCP (not just file reads/grep) — the code may have changed since the coordinator last looked.
4. Only then decide which agent should work which GitHub issue, and assign it.

## Phases (this template's own build-out)

- **Phase 0 — Repo & Tooling Bootstrap**: repo skeleton, Serena MCP configured and verified, GitHub CLI/MCP conventions documented, `CLAUDE.md` skeleton in place.
- **Phase 1 — Coordinator Agent**: `.claude/agents/coordinator.md` — role, tool access, session-start/compaction behavior described above, actually implemented.
- **Phase 2 — Worker Agents & Review Loop**: `.claude/agents/implementer.md`, `.claude/agents/reviewer.md` (wraps the `/code-review` skill), the review-and-fix loop enforced in practice, not just on paper.
- **Phase 3 — GitHub Conventions**: Issue templates for `phase` and `task`, labels, Project v2 fields, all wired together and actually usable.
- **Phase 4 — Process Documentation**: this document, finished and accurate to what got built (not just what was planned).
- **Phase 5 — CLAUDE.md Finalization**: the hard rules (no multi-task batching, mandatory review loop, coordinator runs every session start/compaction) encoded as binding instructions, not suggestions.
- **Phase 6 — Dry Run**: one full fake task lifecycle executed end-to-end, proving the loop actually works, before this template is considered usable on a real project.
