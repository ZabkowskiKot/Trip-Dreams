# Trip Dreams — GitHub backlog guide

Backlog lives in [GitHub Issues](https://github.com/ZabkowskiKot/Trip-Dreams/issues) on this repo.

## Structure

| GitHub feature | Used for |
|----------------|----------|
| **Milestones** | Iterations / releases (what to ship next) |
| **Labels `epic:*`** | Which product area (groups, calendar, …) |
| **Labels `priority:*`** | What to pick up first within an iteration |
| **Issues** | PBIs / user stories with acceptance criteria |
| **Project board** | Kanban view (Backlog → Next → In progress → Done) |

## Milestones (iterations)

1. **Done — Foundation** — closed issues #1–#4
2. **Next — Groups & invites** ← **current focus** (#5–#8)
3. **Dream Planner polish** (#9–#12)
4. **Calendar sync (Stage 2)** (#13–#15)
5. **Trip Organizer (Stage 3)** (#16–#17)
6. **Trip Summary (Stage 4)** (#18)

## Suggested project board columns

| Column | What goes here |
|--------|----------------|
| **Backlog** | All open issues not started |
| **Next** | Current iteration (`Next — Groups & invites`) |
| **In progress** | What you are building now (max 1–2) |
| **Done** | Closed issues |

## Link issues to your GitHub Project

1. Open your [Trip Dreams project](https://github.com/users/ZabkowskiKot/projects) (or repo → **Projects** tab).
2. **Add items** → search `repo:ZabkowskiKot/Trip-Dreams` → select all open issues.
3. Drag **#5** and **#6** to **Next** (invite codes + join UI).
4. When you start coding, move one issue to **In progress**.
5. Close the issue when the PR merges (`Closes #5` in PR description auto-closes).

## Workflow with Cursor

```
Implement GitHub issue #5 — group invite codes
```

Or paste the issue acceptance criteria into chat.

## Create new PBIs

Use **New issue** → **Feature** template (epic + priority + acceptance criteria).
