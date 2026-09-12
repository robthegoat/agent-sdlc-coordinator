# GitHub conventions

This documents the actual conventions used so far in this repo (Phase 0's own issues), so future sessions don't reinvent them. If a later phase changes something here, update this file to match — it describes real practice, not aspiration.

## Labels

Two labels exist, both created once via `gh label create`:

| Label | Color | Meaning |
|---|---|---|
| `phase` | `#5319E7` | A phase-level tracking issue (one per row in `docs/process.md`'s phase list). Scoped, but not broken into tasks. |
| `task` | `#0E8A16` | A concrete, independently-closeable implementation task, created during a phase's Stage B (phase-planning) session. |

Default GitHub labels (`bug`, `documentation`, `enhancement`, etc.) are left as-is and unused by this template — they're not part of this convention.

Phase 3 may add more labels (e.g. `needs-review`, `review-passed`) — when it does, this table gets updated, not duplicated elsewhere.

## Issue title conventions

- Phase issues: `Phase N — <name>`, e.g. `Phase 0 — Repo & Tooling Bootstrap`. N matches the phase's position in `docs/process.md`.
- Task issues: `Task N.M — <name>`, e.g. `Task 0.2 — Install and verify Serena MCP`. N is the phase number, M is a 1-based sequence within that phase, in the order the phase-planning session created them (not necessarily implementation order).

## Cross-referencing phase and task issues

Every task issue's body opens with a line like:

```
Part of Phase 0 (#1).
```

This is a plain GitHub issue-number reference (auto-linked by GitHub), not a special API relationship — there's no native GitHub Issues parent/child hierarchy in use here (see "Not currently used" below). It's enough for a human or a coordinator agent reading the issue to know which phase it belongs to.

## Acceptance criteria and closing

Every task issue body ends with an explicit `**Acceptance criteria:**` list, always including "Reviewed and merged via the review-and-fix loop before closing." Task issues are closed with `gh issue close <N> --comment "..."`, and that comment always includes:

- Which commit(s) implemented the task
- A short rundown of what was actually done, matched against the acceptance criteria
- What the review-and-fix loop found (even if "no findings") and, if anything was found, what changed between the reviewed commit and the fix commit

This comment is the durable record of what shipped — written so a future session can trust the issue's closed state without re-reading every commit.

## GitHub Project board

One Project (v2), created once via:

```bash
gh project create --owner "@me" --title "Agent SDLC Coordinator"
```

Every phase and task issue is added to it via:

```bash
gh project item-add <project-number> --owner "@me" --url <issue-url>
```

To read the board's current state (what a coordinator does at session start / after compaction, per `docs/process.md`):

```bash
gh project item-list <project-number> --owner "@me" --limit 20
```

`--limit` defaults to a small number that silently truncates — always pass an explicit `--limit` comfortably above the current issue count, or you'll think an item is missing when it's just off the end of the default page.

**Custom fields (Phase, Status beyond the default, etc.) are not set up yet.** Only the default Project v2 fields exist right now (Title, Status, Assignees, Labels, and GitHub's built-in issue metadata fields). Phase 3 is explicitly responsible for adding and wiring up custom fields — this doc will be updated when that lands, not before.

## Review-and-fix loop, in practice

Every task so far has followed this exact sequence, which is what "the review-and-fix loop" in `docs/process.md` concretely means:

1. Implement the change, commit and push it.
2. Invoke the `/code-review` skill (medium effort has been sufficient so far) scoped explicitly to the one commit and the originating issue's acceptance criteria — not a general "review my code" ask.
3. Read the findings. Every finding gets fixed, not dismissed, unless there's a clear reason it doesn't apply (none have been dismissed so far — every finding raised has been a real issue).
4. Commit and push the fixes, referencing what was fixed and why in the commit message.
5. Re-invoke `/code-review`, scoped to confirming the specific prior findings are resolved (not a generic re-review) — this catches "fixed on paper but not actually" mistakes.
6. Only on a clean re-review does the task issue close, with the summary described above.

## GitHub CLI reference used so far

```bash
gh label create <name> --color <hex> --description "<text>"
gh issue create --title "<title>" --body "<body>" --label "<phase|task>"
gh issue close <number> --comment "<summary>"
gh issue list --state all --limit 20
gh project create --owner "@me" --title "<title>"
gh project item-add <project-number> --owner "@me" --url <issue-url>
gh project item-list <project-number> --owner "@me" --limit 20
gh project field-list <project-number> --owner "@me"
```

No GitHub MCP server is configured for this repo yet — everything above goes through the `gh` CLI directly.
