# Python 3.14 migration & dependency refresh

**Project work track** — upgrading SuperMemo from its original stack (~Python 3.8/3.9 era, ~2022) to **Python 3.14** and modern dependency versions so the app can run again locally and in deploy.

> **Not in AGENT_CORE** — this is implementation work, not agent routing rules.  
> **Open work checkboxes:** [SUPER_MEMO_TODO.md](../SUPER_MEMO_TODO.md) § Python 3.14 migration  
> **Local environment:** [dev-environment/pycharm-wsl-venv-setup.md](../dev-environment/pycharm-wsl-venv-setup.md)

---

## Goal

| Target | Detail |
|--------|--------|
| **Python** | 3.14 in WSL (`~/.virtualenvs/SuperMemo`) |
| **Dependencies** | Update `src/requirements.txt` to current compatible versions where possible |
| **Outcome** | `pip install`, `migrate`, `runserver`, and `pytest` succeed on the new stack |

---

## Starting point (as of 2026-05-31)

**Original stack indicators:**

- `requirements.txt` pins many packages from ~2022 (`Django` unpinned but paired with old pins: `celery==5.2.6`, `pytest==7.1.2`, `djoser==2.1.0`, `gunicorn==20.1.0`, etc.)
- Project written for Django 3.x era (`settings.py` references Django 3.1 deployment docs)
- Some entries look suspicious or redundant (`redis-server==6.0.9`, `simplejwt==2.0.1` alongside `djangorestframework-simplejwt`, trailing `test` line)

**Environment already done:**

- WSL + Python 3.14 + venv configured (see dev-environment doc)
- Branch with initial `requirements.txt` touch may exist — treat migration as iterative

---

## Migration phases

### Phase 1 — Baseline install & inventory

- [ ] From `src/` with venv active: attempt `pip install -r requirements.txt`
- [ ] Record every install failure (package name, error: no wheel, deprecated API, conflict)
- [ ] Note Django target version (likely 4.2 LTS or 5.x — decide after first install pass)
- [ ] Remove or fix obvious bad lines in `requirements.txt` (`test`, duplicate JWT packages, `redis-server` if not needed as pip package)

### Phase 2 — Core framework upgrade

- [ ] Upgrade **Django** to a version supporting Python 3.14 (verify release notes)
- [ ] Upgrade **Django REST framework**, **djoser**, **simplejwt** together (auth stack is coupled)
- [ ] Run `python manage.py check` after each major bump
- [ ] Fix deprecations: `django.conf.urls.url` → `re_path`, `DEFAULT_AUTO_FIELD`, etc.

### Phase 3 — App services & tooling

- [ ] **Celery** + **redis** — align versions; verify `src/src/celery.py` and broker settings
- [ ] **pytest**, **factory-boy**, **pytest-factoryboy**, **Faker** — test suite runs
- [ ] **gunicorn**, **whitenoise**, **django-heroku** — deploy path (may defer if local-first)
- [ ] **psycopg2** → consider **psycopg2-binary** or **psycopg[3]** for easier installs on 3.14
- [ ] **Pillow**, **flake8**, **debug-toolbar** — bump to compatible releases

### Phase 4 — Code & config fixes

- [ ] Fix import/runtime errors surfaced by `manage.py migrate` and `runserver`
- [ ] Update middleware/settings for newer Django (CSRF, `USE_TZ`, static files, etc.)
- [ ] Review `SECRET_KEY` / `DEBUG` / env loading (`django-dotenv` vs stdlib — package may be stale)
- [ ] Docker: update `src/Dockerfile` base image Python version when local stack is green

### Phase 5 — Verification

- [ ] `python manage.py migrate` — clean on fresh DB
- [ ] `python manage.py runserver` — smoke test main URLs (`/`, account, lesson, repeat)
- [ ] `pytest` — full suite or document known failures in § Open questions below
- [ ] Optional: load fixtures from `src/fixtures/`

---

## Known risk areas (from codebase skim)

| Area | Risk | Where to look |
|------|------|----------------|
| Django version jump | URL imports, settings defaults, model fields | `src/src/settings.py`, all `urls.py` |
| djoser + simplejwt | Breaking API between 2.x and current | `account/api/`, `DJOSER` settings |
| Celery 5.2 → current | Broker API, task discovery | `src/src/celery.py`, `src/src/tasks.py` |
| psycopg2 build | May need binary wheel or psycopg3 | DB settings in `settings.py` |
| Old pytest plugins | Factory fixtures API | `*/tests/conftest.py`, `pytest.ini` |

---

## Working conventions

- **One logical bump per commit** when the user asks for commits (e.g. “Django + deps”, then “test fixes”).
- **Pin** versions in `requirements.txt` after a green install (`pip freeze` relevant packages) — avoid leaving everything unpinned once stable.
- **Document blockers** in [MASTER_INDEX.md](../MASTER_INDEX.md) § Open questions (ID `OQ-MIG-…`) instead of long notes here.

---

## Open questions (migration)

| ID | Blocks? | Summary | Detail |
|----|---------|---------|--------|
| **OQ-MIG-001** | TBD | Target Django major version (4.2 LTS vs 5.x vs 6.x) | Decide after Phase 1 install errors and Python 3.14 compatibility matrix |
| **OQ-MIG-002** | TBD | Keep `django-heroku` / Heroku deploy path or drop for local-only | User decision when touching deploy deps |

Add rows as new blockers appear. Checkboxes stay in [SUPER_MEMO_TODO.md](../SUPER_MEMO_TODO.md).

---

## Progress log

| Date | Note |
|------|------|
| 2026-05-31 | Migration track created; env on Python 3.14 + WSL documented separately |
| 2026-05-31 | Initial `requirements.txt` edit started on feature branch |

---

## Changelog

| Date | Change |
|------|--------|
| 2026-05-31 | Initial migration doc |
