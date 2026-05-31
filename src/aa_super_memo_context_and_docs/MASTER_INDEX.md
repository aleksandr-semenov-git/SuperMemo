# SuperMemo — Domain knowledge (Master Index)

Knowledge base for **SuperMemo**: a Django app for spaced-repetition learning — goals, lessons, questions, and repetition sessions.

> **Agents:** start at **[AGENT_CORE.md](./AGENT_CORE.md)** (how to work). Open questions: § [Open questions](#open-questions) in this file.

**Open work:** [SUPER_MEMO_TODO.md](./SUPER_MEMO_TODO.md)

> **Language:** You can ask questions in Russian or English. This documentation is in English to match code and repo conventions.

---

## Agent entry

**How to work / ask user:** [AGENT_CORE.md](./AGENT_CORE.md)  
**Open questions:** § [Open questions](#open-questions) below

---

## Coverage map (for humans and agents)

| Area | Documented here? | Where in code |
|------|------------------|---------------|
| Project settings, URLs, Celery | Pointers only | `src/src/` (`settings.py`, `urls.py`, `celery.py`) |
| Goals & home | Pointers only | `src/memo/` |
| Auth, profile, JWT/Djoser API | Pointers only | `src/account/` |
| Content hierarchy (Goal → Section → Theme → Lesson → Question) | Pointers only | `src/lesson/` |
| Repetition sessions & QState (scores, modes) | Pointers only | `src/repeat/` |
| Support tickets (API) | Pointers only | `src/support/` |
| Tests | Pointers only | `*/tests/` under each app; `src/pytest.ini` |
| Docker / deploy | Pointers only | `src/Dockerfile`, `src/docker-compose.yaml` |
| Local dev (PyCharm/WSL/venv) | Yes | [dev-environment/pycharm-wsl-venv-setup.md](./dev-environment/pycharm-wsl-venv-setup.md) |
| Python 3.14 migration | Yes (in progress) | [project-work/python-314-migration.md](./project-work/python-314-migration.md) |

Child docs (numbered `01-…`, `02-…`) will be added under this folder as the knowledge base grows.

---

## Objectives of this folder

| Goal | How this helps |
|------|----------------|
| Onboard to the system | Start with repo structure, then data model |
| Trace a user flow end-to-end | Goal → lesson content → repeat session |
| Know which app owns what | Django app map below |
| Avoid context waste | Read this index first; open targeted files only |

---

## Repo layout (high level)

```text
SuperMemo/
└── src/                          # Django project root (manage.py lives here)
    ├── src/                      # Project package: settings, urls, celery, wsgi
    ├── memo/                     # Goals, home views, goal API
    ├── account/                  # Login, registration, profile, auth API
    ├── lesson/                   # Section, Theme, Lesson, Question + CRUD/API
    ├── repeat/                   # RepetitionSession, QState, repeat flow
    ├── support/                  # Support tickets (REST API)
    ├── templates/                # Shared templates (base.html, …)
    ├── fixtures/                 # JSON fixtures for dev/tests
    └── aa_super_memo_context_and_docs/   # This knowledge base
```

---

## Django apps & domain model

| App | Responsibility | Key models / concepts |
|-----|----------------|------------------------|
| **memo** | User goals, landing/home | `Goal` → linked to `Profile` |
| **account** | Authentication, user profile | `Profile`, forms, Djoser/JWT endpoints |
| **lesson** | Content hierarchy & editing | `Goal` → `Section` → `Theme` → `Lesson` → `Question` |
| **repeat** | Spaced repetition sessions | `RepetitionSession` (modes: Mix, Goal, Section, Theme), `QState` (per-question score in session) |
| **support** | Help desk / tickets | Ticket models & API under `support/api/` |

**Question scheduling fields** (`lesson.Question`): `prev_repeat_at`, `next_repeat_at`, `cycle`, `memo_index` (coefficient — noted as not fully used in current version), `repeated_num`.

**Repetition session modes** (`repeat.RepetitionSession`): Mix (`M`), Goal (`G`), Section (`S`), Theme (`T`).

---

## API & auth (summary)

| Concern | Location |
|---------|----------|
| REST framework setup | `src/src/settings.py` → `REST_FRAMEWORK` |
| JWT tokens | `/api/token/`, `/api/token/refresh/` |
| Djoser auth | `/api/auth/` |
| Goal API | `memo/api/` |
| Account API | `account/api/` |
| Lesson API | `lesson/api/` (+ `new-lessons` router in root urls) |
| Support API | `/api/v1/support/` |

---

## Documentation map

| # | Document | Status | Contents |
|---|----------|--------|----------|
| — | [dev-environment/pycharm-wsl-venv-setup.md](./dev-environment/pycharm-wsl-venv-setup.md) | Done | Reusable PyCharm + WSL + venv + `.bashrc` setup |
| — | [project-work/python-314-migration.md](./project-work/python-314-migration.md) | In progress | Python 3.14 + dependency upgrade track |
| 01+ | *(domain docs not yet created)* | Planned | Architecture, repetition algorithm, API catalog, glossary |

When adding domain docs, use numbered filenames (`01-objectives-and-domain.md`, …) and register them in this table.

---

## Quick start paths

**“I need the big picture”**  
→ This file (§ Repo layout, § Django apps) → `src/src/urls.py`

**“How is content organized?”**  
→ `src/lesson/models.py` (Goal → Section → Theme → Lesson → Question)

**“How does repetition work?”**  
→ `src/repeat/models.py`, `src/repeat/views/`, `src/repeat/services/`

**“Set up PyCharm + WSL + venv”**  
→ [dev-environment/pycharm-wsl-venv-setup.md](./dev-environment/pycharm-wsl-venv-setup.md)

**“Upgrade Python / dependencies”**  
→ [project-work/python-314-migration.md](./project-work/python-314-migration.md)

**“Run locally / tests”**  
→ dev-environment doc first · `src/docker-compose.yaml` · from `src/`: `pytest` · `python manage.py runserver`

**“Where are API endpoints?”**  
→ `src/src/urls.py` and each app's `api/urls.py`

---

## Related paths elsewhere in repo

| Topic | Location |
|-------|----------|
| Dependencies | `src/requirements.txt` |
| Test config | `src/pytest.ini`, `src/.coveragerc` |
| Lint/format | `setup.cfg` (repo root) |

---

## Open questions

Canonical for **SuperMemo platform** (product / algorithm / schema decisions).

| ID | Blocks? | Summary | Detail |
|----|---------|---------|--------|
| **OQ-MIG-001** | TBD | Target Django major for Py 3.14 | [project-work/python-314-migration.md](./project-work/python-314-migration.md) |
| **OQ-MIG-002** | TBD | Keep Heroku/deploy path vs local-only | [project-work/python-314-migration.md](./project-work/python-314-migration.md) |

Checkboxes: [SUPER_MEMO_TODO.md](./SUPER_MEMO_TODO.md).

---

## Maintenance

When the system changes materially (new app, new API surface, repetition algorithm change), update the relevant section here or add a child doc and register it in **Documentation map**. Record notable doc changes in **Changelog** below.

### Changelog

| Date | Change |
|------|--------|
| 2026-05-31 | Initial master index (pattern from rgo-2.0 `understand_RGO/MASTER_INDEX.md`) |
| 2026-05-31 | Added dev-environment + python-314-migration docs |
