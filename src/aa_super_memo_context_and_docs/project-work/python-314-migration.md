# Python 3.14 migration & dependency refresh

**Project work track** — upgrading SuperMemo from its original stack (~Python 3.8/3.9 era, ~2022) to **Python 3.14** and modern dependency versions so the app can run again locally and in deploy.

> **Implementation track** — Dev agent executes via [DEV_AGENT_CORE.md](../DEV_AGENT_CORE.md); Lead maintains plan via [LEAD_AGENT_CORE.md](../LEAD_AGENT_CORE.md).  
> **Open work checkboxes:** [SUPER_MEMO_TODO.md](../SUPER_MEMO_TODO.md) § Python 3.14 migration  
> **Local environment:** [dev-environment/pycharm-wsl-venv-setup.md](../dev-environment/pycharm-wsl-venv-setup.md)

---

## Goal (Phase A — current scope)

| Target | Detail |
|--------|--------|
| **Python** | 3.14 in WSL (`~/.virtualenvs/SuperMemo`) |
| **Django** | **5.2 LTS** (latest 5.2.x patch, **≥ 5.2.8** for Python 3.14) |
| **Deploy** | **Docker Compose only** — Heroku removed completely |
| **Dependencies** | Update `src/requirements.txt` to current compatible versions |
| **Outcome** | `pip install`, `migrate`, `runserver`, and `pytest` succeed on the new stack |

**Out of scope for Phase A:** Django 6.0 upgrade (see § Django 5.2 vs 6.0 — deferred as Phase B).

---

## Decisions (resolved)

| ID | Decision | Rationale |
|----|----------|-----------|
| **OQ-MIG-001** | **Django 5.2 LTS** (Phase A) | Only LTS supporting Python 3.14; djoser officially supports up to 5.2; smaller jump than 6.0 |
| **OQ-MIG-002** | **Remove Heroku completely** | Heroku no longer used; `django-heroku` only in `requirements.txt` + `settings.py`; Docker Compose is deploy path |

---

## Django 5.2 vs 6.0 (why not 6 now)

Both support Python 3.14. Phase A targets **5.2 LTS**; revisit 6.x later as optional Phase B.

| | **Django 5.2 LTS** ✅ Phase A | **Django 6.0** — defer |
|---|------------------------------|------------------------|
| **Support** | Security until **Apr 2028** | Standard release, ~shorter window |
| **Python** | 3.10 – 3.14 (3.14 from 5.2.8+) | 3.12 – 3.14 only |
| **djoser** | Supports **3.2 – 5.2** | Not declared; “probably works” only |
| **DRF** | Stable on 5.2 | Official 6.0 support in DRF 3.17+ |
| **SuperMemo fit** | Celery already covers background tasks | Django 6 Tasks framework redundant with Celery |
| **Risk** | Lower — auth/email stack tested on 5.x | Email API rewrite; more deprecations removed |

**Django 6 features not needed to revive the app:** built-in Tasks (have Celery), CSP middleware, template partials.

**When to consider Phase B (5.2 → 6.0):** djoser declares Django 6 support, tests green on 5.2, deliberate need for 6.x features.

---

## Target dependency stack (Phase A)

Pin after first green `pip install`. Starting targets for agents:

| Package | Was (~2022) | Target (Phase A) | Notes |
|---------|-------------|------------------|-------|
| Django | unpinned | `>=5.2.8,<5.3` | LTS + Py 3.14 |
| djangorestframework | unpinned | `>=3.15,<3.18` | 3.17+ if ever jumping to Django 6 |
| djoser | 2.1.0 | `>=2.3.3` | Requires simplejwt 5.x |
| djangorestframework-simplejwt | 4.8.0 | `>=5.0,<6` | Remove wrong `simplejwt` package |
| celery | 5.2.6 | `>=5.4` | Check redis broker compat |
| redis | 4.2.2 | `>=5.1` | Drop `redis-server` pip line |
| pytest | 7.1.2 | `>=8.0` | May need fixture tweaks |
| gunicorn | 20.1.0 | `>=22` | Docker/prod |
| psycopg2 | unpinned | `psycopg2-binary>=2.9.9` | Easier on 3.14 |
| python-dotenv | — | replace `django-dotenv` | Code uses `from dotenv import load_dotenv` |
| whitenoise | unpinned | latest compatible | Already in middleware |
| **django-heroku** | present | **REMOVE** | See Heroku removal checklist |
| **simplejwt** (wrong pkg) | 2.0.1 | **REMOVE** | Duplicate of DRF simplejwt |
| **redis-server** | 6.0.9 | **REMOVE** | Not an app dependency |
| **django-dotenv** | 1.4.2 | **REMOVE** | Use python-dotenv |

---

## Heroku removal checklist

Heroku footprint is minimal — no `Procfile` in repo.

| Step | File | Action |
|------|------|--------|
| 1 | `src/requirements.txt` | Remove `django-heroku` |
| 2 | `src/src/settings.py` | Remove `import django_heroku` and `django_heroku.settings(locals())` |
| 3 | `src/src/settings.py` | Add `STATIC_ROOT = BASE_DIR / 'staticfiles'` (was implicit via heroku) |
| 4 | `src/src/settings.py` | Remove `USE_L10N = True` (no-op/removed in Django 5+) |
| 5 | Docker / prod | Add `collectstatic` to deploy command if serving static via gunicorn (optional for local dev) |

**Keep:** WhiteNoise middleware (already configured), explicit `DATABASES` from env, `docker-compose.yaml`.

---

## Starting point (as of 2026-05-31)

**Original stack indicators:**

- `requirements.txt` pins many packages from ~2022
- Project written for Django 3.x era (`settings.py` references Django 3.1 deployment docs)
- Suspicious lines: `redis-server`, `simplejwt==2.0.1`, `django-dotenv`, `django-heroku`

**Environment already done:**

- WSL + Python 3.14 + venv configured (see dev-environment doc)

---

## Migration phases (Phase A)

### Phase 1 — Baseline install & requirements cleanup

- [x] Remove bad lines from `requirements.txt`: `django-heroku`, `simplejwt`, `redis-server`, `django-dotenv`
- [x] Add `python-dotenv`; pin Django 5.2.x + coupled auth stack (see target table)
- [x] From `src/` with venv active: `pip install -r requirements.txt`
- [x] Record and fix any remaining install failures (`psycopg2` → `psycopg2-binary` for Py 3.14)

### Phase 2 — Heroku removal + settings

- [x] Apply [Heroku removal checklist](#heroku-removal-checklist) in `settings.py`
- [x] `python manage.py check` passes

### Phase 3 — Core framework & auth stack

- [x] Confirm Django **5.2.x** installed; bump DRF, djoser, simplejwt if not done in Phase 1
- [x] Fix deprecations if any: URL imports, settings warnings
- [x] Retest Djoser/JWT endpoints after auth stack bump

### Phase 4 — App services & tooling

- [x] Celery + redis versions aligned; worker starts (`celery -A src worker`)
- [x] pytest + factory-boy + Faker — test suite runs
- [x] gunicorn, whitenoise, psycopg2-binary, Pillow, debug-toolbar bumped

### Phase 5 — Code & config fixes

- [x] `python manage.py migrate` succeeds
- [x] `python manage.py runserver` — smoke test URLs
- [x] Fix runtime/test failures from upgrade
- [x] Update `src/Dockerfile` to `python:3.14` (or `-slim`) when local stack is green

### Phase 6 — Verification

- [ ] Main flows: goals, lessons, repeat sessions
- [ ] Auth flows: register, login, password reset (email settings)
- [x] `pytest` green or known failures documented below
- [x] Pin all versions in `requirements.txt` from working venv (`pip freeze` subset)

---

## Known risk areas

| Area | Risk | Where to look |
|------|------|----------------|
| Django 3.x → 5.2 jump | Settings, removed APIs (`USE_L10N`), CSRF | `src/src/settings.py` |
| djoser 2.1 → 2.3 + simplejwt 5.x | Auth API, JWT settings | `account/api/`, `DJOSER`, `SIMPLE_JWT` |
| Heroku removal | Missing `STATIC_ROOT`, static files | `settings.py`, whitenoise |
| Celery 5.2 → current | Broker API | `src/src/celery.py`, `docker-compose.yaml` |
| pytest 7 → 8 | Factory fixtures | `*/tests/conftest.py`, `pytest.ini` |

---

## Working conventions

- **One logical bump per commit** when the user asks for commits.
- **Pin** versions in `requirements.txt` after green install.
- **New blockers** → add `OQ-MIG-00x` here + checkbox in TODO; resolved decisions stay in § Decisions.

---

## Open questions (migration)

| ID | Status | Summary |
|----|--------|---------|
| **OQ-MIG-001** | ✅ **Resolved** | Django **5.2 LTS** (Phase A); Django 6 deferred |
| **OQ-MIG-002** | ✅ **Resolved** | Heroku **removed completely**; Docker Compose deploy |

Add new rows for blockers discovered during implementation.

---

## Progress log

| Date | Note |
|------|------|
| 2026-05-31 | Migration track created; env on Python 3.14 + WSL documented |
| 2026-05-31 | OQ-MIG-001/002 resolved: Django 5.2 LTS + Heroku removal; 5 vs 6 analysis added |
| 2026-06-02 | Dev: Phases 1–5 + partial 6 complete on WSL Py 3.14 venv. `manage.py check` OK, migrate OK, pytest 2 passed, celery worker starts. Added `pytest-django` (was missing). Remaining: manual SMTP + main UI flows. |

---

## Changelog

| Date | Change |
|------|--------|
| 2026-05-31 | Initial migration doc |
| 2026-05-31 | Phase A decisions, Django 5 vs 6 analysis, Heroku checklist, target dependency table |
