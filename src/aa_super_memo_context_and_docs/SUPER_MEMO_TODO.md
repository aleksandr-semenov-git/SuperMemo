# SuperMemo — Open work (TODO)

Link-only rollups and checkboxes. **Open question detail** lives in [MASTER_INDEX.md](./MASTER_INDEX.md) § Open questions — do not duplicate narratives here.

**Agent rules:** [AGENT_CORE.md](./AGENT_CORE.md)

---

## Documentation

- [ ] Add domain child docs (`01-objectives-and-domain.md`, …) and register in MASTER_INDEX
- [ ] Document repetition / scheduling algorithm once confirmed in code

## Python 3.14 migration

Detail: [project-work/python-314-migration.md](./project-work/python-314-migration.md)

### Phase 1 — Baseline
- [ ] `pip install -r requirements.txt` — capture all failures
- [ ] Clean up suspicious `requirements.txt` lines (`test`, duplicates, `redis-server`)

### Phase 2 — Core framework
- [ ] Upgrade Django + DRF + djoser/simplejwt stack
- [ ] `python manage.py check` passes

### Phase 3 — Services & tooling
- [ ] Celery + redis versions aligned
- [ ] pytest + factory-boy stack runs
- [ ] gunicorn / whitenoise / postgres driver updated

### Phase 4 — Code fixes
- [ ] `migrate` + `runserver` smoke test
- [ ] Fix test failures from upgrade

### Phase 5 — Verify
- [ ] Main user flows work (goals, lessons, repeat)
- [ ] Update Dockerfile Python version when local is green

## Open questions (from MASTER_INDEX)

- [ ] **OQ-MIG-001** — Decide Django major version (4.2 LTS vs 5.x+)
- [ ] **OQ-MIG-002** — Keep django-heroku / Heroku deploy path?

---

## Done

See [SUPER_MEMO_CHANGELOG.md](./SUPER_MEMO_CHANGELOG.md).
