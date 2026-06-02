# SuperMemo — Domain knowledge (Master Index)

Knowledge base for **SuperMemo**: a Django app for spaced-repetition learning — goals, lessons, questions, and repetition sessions.

> **Agents:** **Lead** (investigate/plan) → [LEAD_AGENT_CORE.md](./LEAD_AGENT_CORE.md) · **Dev** (implement) → [DEV_AGENT_CORE.md](./DEV_AGENT_CORE.md). Open questions: § [Open questions](#open-questions) in this file.

**Open work:** [SUPER_MEMO_TODO.md](./SUPER_MEMO_TODO.md)

> **Language:** You can ask questions in Russian or English. This documentation is in English to match code and repo conventions.

---

## Agent entry

**Lead agent (investigate / plan):** [LEAD_AGENT_CORE.md](./LEAD_AGENT_CORE.md)  
**Dev agent (implement TODO):** [DEV_AGENT_CORE.md](./DEV_AGENT_CORE.md)  
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

Numbered domain docs ([01](./01-objectives-and-domain.md)–[05](./05-glossary.md)) cover objectives, architecture, the repetition algorithm, the API catalog, and a glossary.

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
| — | [LEAD_AGENT_CORE.md](./LEAD_AGENT_CORE.md) | Done | Lead agent: investigation & planning |
| — | [DEV_AGENT_CORE.md](./DEV_AGENT_CORE.md) | Done | Dev agent: implement TODO / plans |
| — | [project-work/python-314-migration.md](./project-work/python-314-migration.md) | In progress | Python 3.14 + dependency upgrade track |
| — | [project-work/PROJECT_ANALYSIS.md](./project-work/PROJECT_ANALYSIS.md) | Done | Point-in-time critique: weaknesses + roadmap (opinions) |
| 01 | [01-objectives-and-domain.md](./01-objectives-and-domain.md) | Done | Purpose, domain concepts, hierarchy, user flow |
| 02 | [02-architecture-and-layers.md](./02-architecture-and-layers.md) | Done | Stack, view→service→model layering, app map |
| 03 | [03-repetition-algorithm.md](./03-repetition-algorithm.md) | Done | Cycle/`DAYS_DICT` scheduler, session lifecycle |
| 04 | [04-api-and-urls-catalog.md](./04-api-and-urls-catalog.md) | Done | HTML routes + REST endpoints + auth |
| 05 | [05-glossary.md](./05-glossary.md) | Done | Terms used across code and docs |

**Domain docs (01–05) vs PROJECT_ANALYSIS:** numbered docs are stable *facts* ("how it works"); the analysis is a point-in-time *critique* (weaknesses, severity, roadmap). Keep critique out of the numbered docs — link to the analysis instead.

When adding more domain docs, continue the numbering and register them here.

---

## Quick start paths

**“I need the big picture”**  
→ [01-objectives-and-domain.md](./01-objectives-and-domain.md) → [02-architecture-and-layers.md](./02-architecture-and-layers.md)

**“How is content organized?”**  
→ [01-objectives-and-domain.md](./01-objectives-and-domain.md) § Hierarchy · `src/lesson/models.py`

**“How does repetition work?”**  
→ [03-repetition-algorithm.md](./03-repetition-algorithm.md) · `src/repeat/`, `src/lesson/services/question_service.py`

**“What are the endpoints?”**  
→ [04-api-and-urls-catalog.md](./04-api-and-urls-catalog.md)

**“What does term X mean?”**  
→ [05-glossary.md](./05-glossary.md)

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
| **OQ-MIG-001** | ✅ Resolved | **Django 5.2 LTS** (Phase A); Django 6 deferred | [project-work/python-314-migration.md](./project-work/python-314-migration.md) § Decisions · § Django 5.2 vs 6.0 |
| **OQ-MIG-002** | ✅ Resolved | **Heroku removed**; Docker Compose deploy | [project-work/python-314-migration.md](./project-work/python-314-migration.md) § Heroku removal checklist |
| **OQ-ARCH-001** | Open | Security/settings hardening — Phase A scope vs separate track | [project-work/PROJECT_ANALYSIS.md](./project-work/PROJECT_ANALYSIS.md) § 3 · § 5 |
| **OQ-ARCH-002** | Open | Custom user model now, or stay with `User` + `Profile`? | [project-work/PROJECT_ANALYSIS.md](./project-work/PROJECT_ANALYSIS.md) § 5 |
| **OQ-ARCH-003** | Open | Frontend direction (templates+htmx vs API-first) | [project-work/PROJECT_ANALYSIS.md](./project-work/PROJECT_ANALYSIS.md) § 5 |
| **OQ-PROD-001** | Open | Keep cycle-table scheduler or implement SM-2 (`memo_index`)? | [project-work/PROJECT_ANALYSIS.md](./project-work/PROJECT_ANALYSIS.md) § 1 · § 5 |

Checkboxes: [SUPER_MEMO_TODO.md](./SUPER_MEMO_TODO.md).

---

## Maintenance

When the system changes materially (new app, new API surface, repetition algorithm change), update the relevant section here or add a child doc and register it in **Documentation map**. Record notable doc changes in **Changelog** below.

### Changelog

| Date | Change |
|------|--------|
| 2026-05-31 | Initial master index (pattern from rgo-2.0 `understand_RGO/MASTER_INDEX.md`) |
| 2026-05-31 | Added dev-environment + python-314-migration docs |
| 2026-05-31 | OQ-MIG-001/002 resolved: Django 5.2 LTS Phase A, Heroku removal |
| 2026-05-31 | Two-agent model: LEAD_AGENT_CORE + DEV_AGENT_CORE (replaces AGENT_CORE) |
| 2026-06-02 | Added PROJECT_ANALYSIS; raised OQ-ARCH-001/002/003, OQ-PROD-001 (separate post-migration track) |
| 2026-06-02 | Added domain docs 01–05 (objectives, architecture, algorithm, API catalog, glossary) |
