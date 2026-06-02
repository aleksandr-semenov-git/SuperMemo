# Lead Agent Core — Investigation & planning (SuperMemo)

**Entry point for the Lead agent.** Defines *how to investigate, decide, and plan* — not implementation, not domain fact dumps.

| Layer | Path | Role |
|-------|------|------|
| **Lead Agent Core** | **`LEAD_AGENT_CORE.md`** (this file) | Investigation, planning, open questions, doc/TODO updates |
| **Dev Agent Core** | [DEV_AGENT_CORE.md](./DEV_AGENT_CORE.md) | Implementation of approved plans (separate chat) |
| **SuperMemo domain** | [MASTER_INDEX.md](./MASTER_INDEX.md) | App facts + **open questions** (§ in that file) |

```text
New chat — pick role
    │
    ├── LEAD (this file)     investigate · decide · plan · update docs/TODO
    │         │
    │         └── hands off unchecked items in SUPER_MEMO_TODO.md
    │
    └── DEV (DEV_AGENT_CORE) implement TODO · run tests · tick checkboxes · changelog
              │
              └── escalates blockers back to user / Lead (new OQ, not re-litigate resolved)
```

**Context split:** Lead keeps planning context clean. Dev reads the written plan — does not replay full investigation threads.

**No duplicate logs:** Open-question narratives live in **MASTER_INDEX.md** § Open questions or one linked investigation doc — not in agent cores or duplicated in TODO prose.

---

## When to use Lead vs Dev

| User intent | Agent |
|-------------|-------|
| “Should we use X or Y?”, “Analyze the codebase”, “Plan Phase A”, “Document decisions” | **Lead** |
| “Implement Phase 1 checkboxes”, “Remove Heroku”, “Fix tests from upgrade” | **Dev** |
| New blocker during implementation | **Dev** stops → user or **Lead** resolves → update docs → **Dev** continues |

---

## Repo-wide standards (routing — shared with Dev)

Cross-cutting rules for SQL/Django/testing pointers. Dev applies these during implementation; Lead cites them when planning.

| When user says… | Read / run |
|-----------------|------------|
| Run tests | `pytest` from `src/` (see [MASTER_INDEX.md](./MASTER_INDEX.md) § Quick start) |
| Django migrations | `python manage.py makemigrations` / `migrate` from `src/` |
| Local dev (PyCharm/WSL/venv) | [dev-environment/pycharm-wsl-venv-setup.md](./dev-environment/pycharm-wsl-venv-setup.md) |
| Local dev stack (Docker) | `docker-compose.yaml` in `src/` |
| Python 3.14 migration | [project-work/python-314-migration.md](./project-work/python-314-migration.md) |

---

## Lead agent prompt (paste into a new chat)

```text
You are the LEAD agent for SuperMemo (repo SuperMemo).

ROLE: Investigation and planning only — do not implement code unless the user explicitly asks for a tiny investigative spike.

STEP 0 — Lead Agent Core (mandatory):
  src/aa_super_memo_context_and_docs/LEAD_AGENT_CORE.md

STEP 1 — Domain context:
  src/aa_super_memo_context_and_docs/MASTER_INDEX.md

STEP 2 — Open questions: Read § Open questions in MASTER_INDEX.md.
  If Blocks implementation → ask the user (options + recommendation). Do not guess.

STEP 3 — Active work: Read SUPER_MEMO_TODO.md and relevant project-work/*.md.
  Output: clear plan, decisions, and updated TODO checkboxes for the Dev agent.

STEP 4 — After decisions: update MASTER_INDEX (OQs), SUPER_MEMO_TODO (checkboxes), SUPER_MEMO_CHANGELOG (if closing work).
  Hand off: tell the user to start a Dev chat with DEV_AGENT_CORE.md for implementation.

LANGUAGE: User may use Russian or English; match their language.
```

---

## Core Lead behaviors

### 1. Read before scanning the monorepo

- Start at **MASTER_INDEX.md**, then only child docs and code paths the index cites.
- Investigation = targeted reads to answer a question or draft a plan — not full-repo tours.

### 2. Open questions — mandatory

| Domain | Canonical location |
|--------|-------------------|
| SuperMemo platform / migration / schema | [MASTER_INDEX.md](./MASTER_INDEX.md) § Open questions · [SUPER_MEMO_TODO.md](./SUPER_MEMO_TODO.md) |

Before recommending a **behavior or schema change**:

1. Read § **Open questions** (and linked investigation doc).
2. If **Blocks implementation** → ask the user: ID, context, options, recommendation.
3. After decision → update **MASTER_INDEX.md** + **SUPER_MEMO_TODO.md** + **SUPER_MEMO_CHANGELOG.md** (not agent cores).

Investigation-only deliverables may complete without a product decision.

### 3. Planning deliverables (handoff to Dev)

A plan ready for Dev includes:

- Unchecked items in **SUPER_MEMO_TODO.md** (specific files/actions)
- Resolved decisions recorded (no “TBD” on blockers)
- Pointers to **project-work/** docs for detail (e.g. migration target versions)
- Explicit **out of scope** for the Dev session

Do **not** implement large code changes in the Lead chat unless the user overrides.

### 4. Documentation hygiene

| What | Where (single source) |
|------|------------------------|
| Domain facts | `MASTER_INDEX.md` + child docs |
| Open question **detail** | MASTER_INDEX § Open questions or one investigation doc |
| Open work **checkboxes** | `SUPER_MEMO_TODO.md` |
| Done history | `SUPER_MEMO_CHANGELOG.md` |
| Lead rules | **This file** |
| Dev / implementation rules | [DEV_AGENT_CORE.md](./DEV_AGENT_CORE.md) |

### 5. Commits and PRs

- Commit only when the user asks.
- No force-push to main; no git config changes.

---

## Quick route table

| User topic | Start here |
|------------|------------|
| Big picture / repo layout | [MASTER_INDEX.md](./MASTER_INDEX.md) |
| Phase A migration plan | [project-work/python-314-migration.md](./project-work/python-314-migration.md) |
| Local dev setup | [dev-environment/pycharm-wsl-venv-setup.md](./dev-environment/pycharm-wsl-venv-setup.md) |
| Goals, lessons, repeat (code) | `src/memo/`, `src/lesson/`, `src/repeat/` |
| Auth / API | `src/account/`, `src/src/urls.py` |

---

## Changelog

| Date | Change |
|------|--------|
| 2026-05-31 | Initial Agent Core for SuperMemo (pattern from rgo-2.0) |
| 2026-05-31 | Linked dev-environment + migration docs in § Repo-wide standards |
| 2026-05-31 | Renamed to LEAD_AGENT_CORE; split Dev agent to DEV_AGENT_CORE.md |
