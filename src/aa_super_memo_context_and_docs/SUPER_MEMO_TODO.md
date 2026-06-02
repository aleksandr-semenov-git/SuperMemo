# SuperMemo — Open work (TODO)

Link-only rollups and checkboxes. **Migration detail:** [project-work/python-314-migration.md](./project-work/python-314-migration.md). **Resolved decisions:** same doc § Decisions.

**Lead agent (planning):** [LEAD_AGENT_CORE.md](./LEAD_AGENT_CORE.md)  
**Dev agent (implementation):** [DEV_AGENT_CORE.md](./DEV_AGENT_CORE.md) — work TODO top to bottom; do not skip Heroku removal (Phase 2) before chasing runtime errors.

---

## Documentation

- [ ] Add domain child docs (`01-objectives-and-domain.md`, …) and register in MASTER_INDEX
- [ ] Document repetition / scheduling algorithm once confirmed in code

---

## Python 3.14 migration — Phase A

**Targets:** Python 3.14 · **Django 5.2 LTS (≥5.2.8)** · Heroku **removed** · Docker Compose deploy

### Phase 1 — Requirements cleanup & install

- [ ] `src/requirements.txt` — remove `django-heroku`
- [ ] `src/requirements.txt` — remove `simplejwt==2.0.1` (wrong package)
- [ ] `src/requirements.txt` — remove `redis-server==6.0.9`
- [ ] `src/requirements.txt` — remove `django-dotenv`; add `python-dotenv`
- [ ] `src/requirements.txt` — pin Django `>=5.2.8,<5.3`
- [ ] `src/requirements.txt` — pin `djoser>=2.3.3`, `djangorestframework-simplejwt>=5.0,<6`, `djangorestframework>=3.15`
- [ ] From `src/` with `(SuperMemo)` venv: `pip install -r requirements.txt` — fix conflicts until clean

### Phase 2 — Remove Heroku from settings

- [ ] `src/src/settings.py` — remove `import django_heroku`
- [ ] `src/src/settings.py` — remove `django_heroku.settings(locals())`
- [ ] `src/src/settings.py` — add `STATIC_ROOT = BASE_DIR / 'staticfiles'`
- [ ] `src/src/settings.py` — remove `USE_L10N = True`
- [ ] `python manage.py check` passes (from `src/`)

### Phase 3 — Auth stack & framework

- [ ] Verify installed Django is 5.2.x (`python -c "import django; print(django.VERSION)"`)
- [ ] Fix any `manage.py check` warnings (deprecations, system checks)
- [ ] Smoke-test auth: register/login/JWT if server starts

### Phase 4 — Services & tooling

- [ ] Bump `celery`, `redis` in requirements; celery worker starts via docker-compose or local
- [ ] Bump `pytest`, `pytest_factoryboy`, `factory-boy`, `Faker`; run `pytest`
- [ ] Bump `gunicorn`, `whitenoise`, `psycopg2-binary`, `Pillow`, `django-debug-toolbar`, `flake8`

### Phase 5 — Run app & fix code

- [ ] `python manage.py migrate` succeeds
- [ ] `python manage.py runserver` — smoke `/`, account, lesson, repeat URLs
- [ ] Fix import/runtime errors and test failures from upgrade

### Phase 6 — Verify & pin

- [ ] Auth email flows still configured (SMTP env vars; Djoser activation/reset)
- [ ] Main user flows: goals → lessons → repeat session
- [ ] `src/Dockerfile` — update base image to Python 3.14
- [ ] Pin all working versions in `requirements.txt` (from `pip freeze`)
- [ ] Update migration doc § Progress log when phase completes

---

## Resolved (no action)

- [x] **OQ-MIG-001** — Django **5.2 LTS** (Phase A); not 4.x (no Py 3.14), not 6.0 yet
- [x] **OQ-MIG-002** — Heroku **removed completely**; Docker Compose is deploy path

---

## Done

See [SUPER_MEMO_CHANGELOG.md](./SUPER_MEMO_CHANGELOG.md).
