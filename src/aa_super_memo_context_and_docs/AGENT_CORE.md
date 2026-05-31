# Agent Core — How to work in `aa_super_memo_context_and_docs/` (SuperMemo)

**This is the agent entry point.** It defines *how* to work — not domain facts, not a log of open questions.

| Layer | Path | Role |
|-------|------|------|
| **Agent Core** | **`aa_super_memo_context_and_docs/AGENT_CORE.md`** (this file) | Routing, TODO/changelog rules, **when to ask the user**, **repo-wide standards** |
| **SuperMemo domain** | [MASTER_INDEX.md](./MASTER_INDEX.md) | App facts + **open questions** (§ in that file) |

```text
New chat
    │
    ▼
AGENT_CORE.md  (how to work + standards)
    │
    ├──► MASTER_INDEX.md              + SUPER_MEMO_TODO.md
    └──► repo code (targeted files only)
```

**No duplicate logs:** Do not copy open-question narratives into `AGENT_CORE.md` or a root-level registry. One canonical place per question (usually **MASTER_INDEX.md** § Open questions or an investigation doc it links to).

---

## Repo-wide standards (root of `aa_super_memo_context_and_docs/`)

Cross-cutting rules — **not** app-domain-specific. Add child docs here as the repo grows (testing, migrations, API conventions).

| When user says… | Read / run |
|-----------------|------------|
| Run tests | `pytest` from `src/` (see [MASTER_INDEX.md](./MASTER_INDEX.md) § Quick start) |
| Django migrations | `python manage.py makemigrations` / `migrate` from `src/` |
| Local dev (PyCharm/WSL/venv) | [dev-environment/pycharm-wsl-venv-setup.md](./dev-environment/pycharm-wsl-venv-setup.md) |
| Local dev stack (Docker) | `docker-compose.yaml` in `src/` |
| Python 3.14 migration work | [project-work/python-314-migration.md](./project-work/python-314-migration.md) — not agent rules |

Agents: follow these by default unless the user overrides.

---

## Agent prompt (paste into a new chat)

```text
You are helping with SuperMemo at repo SuperMemo.

STEP 0 — Agent Core (mandatory):
  src/aa_super_memo_context_and_docs/AGENT_CORE.md

STEP 1 — Route domain (read MASTER_INDEX.md):
  • General SuperMemo / Django apps / API / repetition logic → src/aa_super_memo_context_and_docs/MASTER_INDEX.md

STEP 2 — Open questions: Read § Open questions in MASTER_INDEX.md.
  If a blocked item applies, STOP and ask the user (options + recommendation). Do not guess.

STEP 3 — Repo standards: Apply AGENT_CORE § Repo-wide standards.

STEP 4 — Answer from child docs + targeted code. Update MASTER_INDEX.md (and linked docs) when you learn something new.

LANGUAGE: User may use Russian or English; match their language.

TODO: Checkboxes in SUPER_MEMO_TODO.md only; done history in SUPER_MEMO_CHANGELOG.md.
  Do not duplicate open-question narratives in TODO — link to MASTER_INDEX § Open questions instead.
```

---

## Core agent behaviors

### 1. Read before you scan the repo

- Start at **MASTER_INDEX.md**, then open only child docs and code paths that index cites.
- Prefer app-level entry points: `models.py`, `urls.py`, `services/`, `api/` under each Django app.

### 2. Open questions — mandatory (where to look)

| Domain | Canonical location |
|--------|-------------------|
| SuperMemo platform / repetition / data model | [MASTER_INDEX.md](./MASTER_INDEX.md) § Open questions · [SUPER_MEMO_TODO.md](./SUPER_MEMO_TODO.md) |

Before a **behavior or schema change**:

1. Read § **Open questions** (and linked investigation doc if any).
2. If **Blocks implementation** → ask the user: ID, 1–2 sentence context, options, recommendation.
3. After decision → update **MASTER_INDEX.md** + `SUPER_MEMO_TODO.md` + `SUPER_MEMO_CHANGELOG.md` (not `AGENT_CORE.md`).

Investigation-only deliverables may complete without a product decision.

### 3. Documentation hygiene (anti-duplication)

| What | Where (single source) |
|------|------------------------|
| Domain facts | `MASTER_INDEX.md` + numbered child docs it links to |
| Open question **detail** | MASTER_INDEX § Open questions **or** one investigation doc (linked once) |
| Open work **checkboxes** | `SUPER_MEMO_TODO.md` |
| Done history | `SUPER_MEMO_CHANGELOG.md` |
| Agent rules + standards | **This file only** |

Do **not** maintain a separate root `OPEN_QUESTIONS.md` or repeat full OQ text in TODO files.

### 4. Commits and PRs

- Commit only when the user asks.
- No force-push to main; no git config changes.

---

## Quick route table

| User topic | Start here |
|------------|------------|
| Big picture / repo layout | [MASTER_INDEX.md](./MASTER_INDEX.md) |
| Goals, home, core models | `src/memo/` |
| Auth, profile, registration | `src/account/` |
| Content hierarchy (goal → question) | `src/lesson/` |
| Repetition sessions, spaced recall | `src/repeat/` |
| Support tickets API | `src/support/` |
| URL routing, settings, Celery | `src/src/` |

---

## Changelog

| Date | Change |
|------|--------|
| 2026-05-31 | Initial Agent Core for SuperMemo (pattern from rgo-2.0 `aa_rgo2_context_and_docs`) |
| 2026-05-31 | Linked dev-environment + migration docs in § Repo-wide standards (routing only) |
