# SuperMemo — Open work (TODO)

Link-only rollups and checkboxes. **Migration detail:** [project-work/python-314-migration.md](./project-work/python-314-migration.md). **Resolved decisions:** same doc § Decisions.

**Lead agent (planning):** [LEAD_AGENT_CORE.md](./LEAD_AGENT_CORE.md)  
**Dev agent (implementation):** [DEV_AGENT_CORE.md](./DEV_AGENT_CORE.md) — work TODO top to bottom; do not skip Heroku removal (Phase 2) before chasing runtime errors.

---

## Documentation

- [x] Add domain child docs 01–05 (objectives, architecture, algorithm, API catalog, glossary) and register in MASTER_INDEX
- [x] Document repetition / scheduling algorithm (→ [03-repetition-algorithm.md](./03-repetition-algorithm.md))
- [ ] Keep domain docs 01–05 in sync as Phase A migration changes settings/deps

---

## Python 3.14 migration — Phase A

**Targets:** Python 3.14 · **Django 5.2 LTS (≥5.2.8)** · Heroku **removed** · Docker Compose deploy

### Phase 1 — Requirements cleanup & install

- [x] `src/requirements.txt` — remove `django-heroku`
- [x] `src/requirements.txt` — remove `simplejwt==2.0.1` (wrong package)
- [x] `src/requirements.txt` — remove `redis-server==6.0.9`
- [x] `src/requirements.txt` — remove `django-dotenv`; add `python-dotenv`
- [x] `src/requirements.txt` — pin Django `>=5.2.8,<5.3`
- [x] `src/requirements.txt` — pin `djoser>=2.3.3`, `djangorestframework-simplejwt>=5.0,<6`, `djangorestframework>=3.15`
- [x] From `src/` with `(SuperMemo)` venv: `pip install -r requirements.txt` — fix conflicts until clean

### Phase 2 — Remove Heroku from settings

- [x] `src/src/settings.py` — remove `import django_heroku`
- [x] `src/src/settings.py` — remove `django_heroku.settings(locals())`
- [x] `src/src/settings.py` — add `STATIC_ROOT = BASE_DIR / 'staticfiles'`
- [x] `src/src/settings.py` — remove `USE_L10N = True`
- [x] `python manage.py check` passes (from `src/`)

### Phase 3 — Auth stack & framework

- [x] Verify installed Django is 5.2.x (`python -c "import django; print(django.VERSION)"`)
- [x] Fix any `manage.py check` warnings (deprecations, system checks)
- [x] Smoke-test auth: register/login/JWT if server starts

### Phase 4 — Services & tooling

- [x] Bump `celery`, `redis` in requirements; celery worker starts via docker-compose or local
- [x] Bump `pytest`, `pytest_factoryboy`, `factory-boy`, `Faker`; run `pytest`
- [x] Bump `gunicorn`, `whitenoise`, `psycopg2-binary`, `Pillow`, `django-debug-toolbar`, `flake8`

### Phase 5 — Run app & fix code

- [x] `python manage.py migrate` succeeds
- [x] `python manage.py runserver` — smoke `/`, account, lesson, repeat URLs
- [x] Fix import/runtime errors and test failures from upgrade

### Phase 6 — Verify & pin

- [ ] Auth email flows still configured (SMTP env vars; Djoser activation/reset)
- [ ] Main user flows: goals → lessons → repeat session
- [x] `src/Dockerfile` — update base image to Python 3.14
- [x] Pin all working versions in `requirements.txt` (from `pip freeze`)
- [x] Update migration doc § Progress log when phase completes

---

## Post-migration improvements (separate track — NOT Phase A)

Source: [project-work/PROJECT_ANALYSIS.md](./project-work/PROJECT_ANALYSIS.md). **Do not start until Phase A migration is green**, unless the user promotes an item. Open decisions: OQ-ARCH-001/002/003, OQ-PROD-001 (MASTER_INDEX § Open questions).

### Security & settings (OQ-ARCH-001)
- [ ] Move `SECRET_KEY` to env; fix `DEBUG` truthy-string parsing; real `ALLOWED_HOSTS`
- [ ] Separate JWT `SIGNING_KEY` from `SECRET_KEY`; review global `BasicAuthentication`
- [ ] Split settings dev/prod; env-driven Redis/DB

### Correctness & API
- [ ] Fix API data leak: per-user querysets + auth on lesson/goal/section/theme endpoints
- [ ] Consolidate redundant lesson API (generics vs `APILessons` viewset); add pagination
- [ ] Fix `find_support` status comparison bug; fix `support` `ISSUE_CHOICES` keys
- [ ] Profile creation via signal/manager (not view `get_or_create`); decide custom user model (OQ-ARCH-002)

### Tests & tooling
- [ ] Standardize on pytest + factory-boy + real test DB; reduce ORM mocking; fix `pytest.ini` collection
- [ ] Add ruff + mypy + pre-commit

### Product & polish
- [ ] Decide scheduler: cycle table vs SM-2 / `memo_index` (OQ-PROD-001)
- [ ] Implement Goal/Section/Theme repetition modes
- [ ] Add `select_related`/`prefetch_related` + query-count tests
- [ ] Frontend direction decision (OQ-ARCH-003)

---

## Resolved (no action)

- [x] **OQ-MIG-001** — Django **5.2 LTS** (Phase A); not 4.x (no Py 3.14), not 6.0 yet
- [x] **OQ-MIG-002** — Heroku **removed completely**; Docker Compose is deploy path

---

## Done

See [SUPER_MEMO_CHANGELOG.md](./SUPER_MEMO_CHANGELOG.md).
