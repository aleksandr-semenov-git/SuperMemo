# Dev Agent Core — Implementation (SuperMemo)

**Entry point for the Dev agent.** Defines *how to implement approved plans* — not open-ended investigation or re-deciding resolved questions.

| Layer | Path | Role |
|-------|------|------|
| **Lead Agent Core** | [LEAD_AGENT_CORE.md](./LEAD_AGENT_CORE.md) | Investigation & planning (separate chat) |
| **Dev Agent Core** | **`DEV_AGENT_CORE.md`** (this file) | Execute TODO · code · tests · checkbox updates |
| **Plan source** | [SUPER_MEMO_TODO.md](./SUPER_MEMO_TODO.md) + [project-work/](./project-work/) | What to build (written by Lead / user) |

```text
Dev chat
    │
    ▼
DEV_AGENT_CORE.md
    │
    ├──► SUPER_MEMO_TODO.md     (unchecked items = your queue)
    ├──► project-work/*.md      (detail: versions, checklists, decisions)
    ├──► MASTER_INDEX.md        (domain context only — do not re-open resolved OQs)
    └──► repo code              (minimal targeted edits)
```

**Context split:** Dev trusts the plan on disk. If something is missing or contradictory, **stop and ask** — do not silently replan.

---

## When to use Dev vs Lead

| Situation | Agent |
|-----------|-------|
| TODO has clear unchecked items; decisions in migration doc are **Resolved** | **Dev** |
| “Which Django version?”, “Analyze options”, “Update the plan” | **Lead** (new chat) |
| Implementation hits unknown blocker | **Dev** stops → user or **Lead** → update docs → **Dev** resumes |

---

## Repo-wide standards (implementation)

Apply by default unless the user overrides. Full routing table: [LEAD_AGENT_CORE.md § Repo-wide standards](./LEAD_AGENT_CORE.md#repo-wide-standards-routing--shared-with-dev).

| Task | Command / path |
|------|----------------|
| Install deps | From `src/` with venv: `pip install -r requirements.txt` |
| Django check | `python manage.py check` |
| Migrations | `python manage.py migrate` |
| Run server | `python manage.py runserver` |
| Tests | `pytest` (from `src/`) |
| Docker stack | `src/docker-compose.yaml` |
| WSL / venv | [dev-environment/pycharm-wsl-venv-setup.md](./dev-environment/pycharm-wsl-venv-setup.md) |

**Phase A migration (current):** Follow [project-work/python-314-migration.md](./project-work/python-314-migration.md) and **SUPER_MEMO_TODO.md** top to bottom. Do not skip Heroku removal before chasing runtime errors.

**Resolved — do not re-debate:**

- **OQ-MIG-001:** Django **5.2 LTS** (≥5.2.8)
- **OQ-MIG-002:** Heroku **removed**; Docker Compose deploy

---

## Dev agent prompt (paste into a new chat)

```text
You are the DEV agent for SuperMemo (repo SuperMemo).

ROLE: Implement approved plans — minimal scope, match existing code style, run tests.

STEP 0 — Dev Agent Core (mandatory):
  src/aa_super_memo_context_and_docs/DEV_AGENT_CORE.md

STEP 1 — Read the plan:
  src/aa_super_memo_context_and_docs/SUPER_MEMO_TODO.md (unchecked items)
  + linked project-work/*.md for the active track (e.g. python-314-migration.md)

STEP 2 — Do NOT re-open resolved open questions (see DEV_AGENT_CORE § Resolved).
  If blocked → STOP, report blocker, ask user or refer to Lead agent.

STEP 3 — Implement: smallest correct diff · run check/migrate/pytest as relevant · tick TODO checkboxes when done.

STEP 4 — Update SUPER_MEMO_CHANGELOG.md for completed phases; note blockers in migration doc Progress log if needed.

LANGUAGE: User may use Russian or English; match their language.

COMMITS: Only when the user asks.
```

---

## Core Dev behaviors

### 1. Plan-first, code-second

1. Read **SUPER_MEMO_TODO.md** — identify the current phase and next unchecked items.
2. Read linked **project-work/** doc for versions, file paths, and checklists.
3. Open only code files required for those items.

### 2. Implementation discipline

- **Minimal scope** — only what the TODO item requires; no drive-by refactors.
- **Match conventions** — naming, structure, and patterns of surrounding code.
- **One logical unit per user-requested commit** (e.g. “requirements cleanup”, then “Heroku removal”).
- Pin `requirements.txt` after a green install when the plan says so.

### 3. Verification before marking done

| Change type | Minimum check |
|-------------|----------------|
| `requirements.txt` | `pip install -r requirements.txt` succeeds |
| `settings.py` | `python manage.py check` |
| Models / migrations | `migrate` |
| Behavior change | relevant `pytest` or manual smoke path from TODO |

Tick the TODO checkbox only after the check passes (or document known failure in Progress log and leave unchecked).

### 4. Documentation updates (Dev-owned)

| Action | Update |
|--------|--------|
| Completed phase / notable work | [SUPER_MEMO_CHANGELOG.md](./SUPER_MEMO_CHANGELOG.md) |
| Phase milestone | [project-work/python-314-migration.md](./project-work/python-314-migration.md) § Progress log |
| New blocker needing product decision | **Do not guess** — leave TODO unchecked; user → **Lead** adds OQ to MASTER_INDEX |

Dev **does not** rewrite domain architecture docs unless the implementation revealed an error — then one-line fix + changelog note.

### 5. Escalation template

When blocked:

```text
BLOCKER: [1 sentence]
TODO item: [checkbox text]
Need: [decision / Lead investigation / user input]
Options: [A / B] — recommend [X] if obvious
```

### 6. Commits and PRs

- Commit only when the user asks.
- No force-push to main; no git config changes.

---

## Active work queue

**Current track:** Python 3.14 migration — Phase A  
→ [SUPER_MEMO_TODO.md § Python 3.14 migration](./SUPER_MEMO_TODO.md)  
→ [project-work/python-314-migration.md](./project-work/python-314-migration.md)

---

## Changelog

| Date | Change |
|------|--------|
| 2026-05-31 | Created DEV_AGENT_CORE for implementation agent (split from Lead) |
