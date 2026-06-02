# SuperMemo — Project analysis (architecture, weaknesses, roadmap)

**Investigation deliverable** (Lead agent). Snapshot of the project as of 2026-06-02, before the Python 3.14 / Django 5.2 migration is implemented.

> **Scope decision:** Improvements here are a **separate post-migration track** — they do **not** block or merge into Phase A migration unless explicitly promoted by the user.  
> **Open questions raised:** OQ-ARCH-001/002/003, OQ-PROD-001 → tracked in [MASTER_INDEX.md](../MASTER_INDEX.md) § Open questions.  
> **Plan/agents:** [LEAD_AGENT_CORE.md](../LEAD_AGENT_CORE.md) · [DEV_AGENT_CORE.md](../DEV_AGENT_CORE.md)

Legend: **[FACT]** = observed in code · **[OPINION]** = reviewer recommendation. Severity: **High / Med / Low**.

---

## 1. Product idea & domain model

**[FACT]** Spaced-repetition learning app (SuperMemo/Anki-style). Users store Q&A cards in a hierarchy; the system schedules when each question is repeated.

```text
User ─1:1─ Profile
                └─< Goal ─< Section ─< Theme ─1:1─ Lesson ─< Question
Profile ─< RepetitionSession ─(QState)─< Question
```

**Scheduling logic** (`src/lesson/services/question_service.py`):

- `cycle` → days via fixed `settings.DAYS_DICT` (0,1,2,12,20,30,60,90,150,270,480,720,1440,2160,3960,6480).
- `calculate_new_cycle(cycle, score)`: score < 3 → cycle+1; 3–5 → cycle−1; >5 → reset to 1 (with edge handling at cycle 1).
- Repeat session serves questions due today one by one; "remember" advances cycle, "not remember" increments `QState.score`; overdue questions are pulled back to today via `renew_date_of_all_forgotten_questions`.

**[FACT] Two interfaces:**
- Server-rendered Django templates — the working app (profile, goals, lessons, repeat).
- DRF API layer (JWT/Djoser wired) — partially built and inconsistent (see §3).

---

## 2. Architecture & patterns

**[FACT]** Layered: `View` → `Service` (static-method classes) → `Model`. Consistent across `memo`, `account`, `lesson`, `repeat`, `support`.

**[OPINION] Strengths:**
- Clean **Service Layer** separating business logic from views — the project's best quality.
- Consistent naming (`get_X_by_Y`, `create_X`) and thorough docstrings.
- Per-app unit + integration test folders.
- `bulk_create` / `bulk_update` used in hot paths.

**[FACT]** Services are stateless static-method classes (namespaced functions) — Service Layer pattern, not DI/Strategy.

---

## 3. Weaknesses & risks

### Security — High

| Issue | Evidence | Severity |
|-------|----------|----------|
| Hardcoded `SECRET_KEY` in source | `src/src/settings.py:25` | High |
| `ALLOWED_HOSTS = ['*']` | `settings.py:30` | High |
| JWT `SIGNING_KEY = SECRET_KEY` (same hardcoded key) | `settings.py:97` | High |
| `DEBUG = os.getenv('DEBUG')` → truthy-string bug (`"False"` is truthy) | `settings.py:28` | High |
| `BasicAuthentication` enabled globally in DRF | `settings.py:80` | Med |

### Correctness bugs — High/Med

| Bug | Evidence | Severity |
|-----|----------|----------|
| **API data leak**: lesson/goal/section/theme list+detail return `objects.all()`, no per-user filter, no auth | `src/lesson/api/api_views.py:7-34`, `src/memo/api/api_views.py:6-13` | High |
| `find_support` compares `CharField` status to `True` (`Q(s_tickets__status=True)`) — never matches open tickets | `src/support/services/ticket_service.py:11-13` | High |
| `ISSUE_CHOICES` reuses `CLOSED`/`FREEZE` keys for issue types (copy-paste) | `src/support/models.py:17-22` | Med |
| `QState.save()` always calls `self.question.save()` — hidden coupling / extra writes | `src/repeat/models.py:26-28` | Med |
| `QStateService.save_qstate_and_question(qstate, question)` ignores `question` arg | `src/repeat/services/qstate_service.py:12-15` | Low |
| `TestMixin1.test_func` returns redirect not bool (broken, unused) | `src/memo/decorators.py:8-15` | Low |

### Incomplete / dead code — Med

- Repetition by **Goal/Section/Theme** are stubs rendering `in_progress.html`; `get_or_create_rep_session_*` are placeholders (`src/repeat/services/repeat_session_service.py:47-63`, `src/repeat/views/repeat.py:92-111`).
- `Question.memo_index` declared but unused — real SM-style coefficient never implemented.
- Redundant API: `generics.*` views **and** an `APILessons` `ModelViewSet` for lessons.

### Config / infra smells — Med

| Issue | Evidence |
|-------|----------|
| Redis hardcoded `0.0.0.0:6380` in settings vs `redis://redis:6380` in compose | `settings.py:220-224`, `src/docker-compose.yaml` |
| Single `settings.py`, no dev/prod split | `settings.py` |
| `STATIC_ROOT` only implicit via `django_heroku` (breaks on Heroku removal — see migration plan) | `settings.py:215` |
| Deprecated `USE_L10N`; Django 3.1 doc URLs throughout | `settings.py:196` |

### Performance — Low/Med

- No `select_related` / `prefetch_related` on `lesson__goal__profile` traversals — N+1 risk.
- API has no pagination.
- `goal_id` passed between views via `request.session` instead of URL — fragile, breaks multi-tab.

---

## 4. Test strategy assessment

**[FACT]** 36 test files; unit + integration per app.

**[OPINION] Concerns:**
- Unit tests heavily **mock the ORM** with `SimpleTestCase` (`@patch('...objects.get')`), asserting call args, not behavior — brittle and blind to real query bugs (e.g. `find_support`). Example: `src/repeat/tests/unit/test_services/test_repeat_session_service.py:9-31`.
- **Style mismatch:** most apps use `unittest`/`SimpleTestCase`; `support` uses `pytest_*` + factories. `pytest.ini` only collects `pytest_*` files, so much of the unittest suite may not run under pytest.

---

## 5. Roadmap (prioritized)

### Now — security/settings (candidate to fold into Phase A if user promotes)
1. Move `SECRET_KEY` to env; fix `DEBUG` parsing; real `ALLOWED_HOSTS`; separate JWT signing key; drop global BasicAuth. → **OQ-ARCH-001**
2. Settings split dev/prod + env-driven Redis/DB (pairs with Heroku removal).

### Next — correctness & API
3. Fix API data leak: per-user querysets + `IsAuthenticated`; consolidate redundant viewsets; add pagination.
4. Fix `find_support` and `support` choices bugs.
5. Profile creation via signal/manager instead of view `get_or_create`; consider custom user model. → **OQ-ARCH-002**
6. Test modernization: standardize on pytest + factory-boy + real test DB; reduce ORM mocking; fix collection config.

### Later — product & polish
7. Decide scheduler: keep cycle table or implement SM-2 via `memo_index`. → **OQ-PROD-001**
8. Complete Goal/Section/Theme repetition modes.
9. Add `select_related`/`prefetch_related` + query-count tests.
10. Tooling: ruff + mypy + pre-commit; modern typing / `match` on 3.14.
11. Frontend direction: templates+htmx vs API-first. → **OQ-ARCH-003**

---

## Open questions raised (detail in MASTER_INDEX § Open questions)

| ID | Decision needed |
|----|-----------------|
| OQ-ARCH-001 | Security/settings hardening — Phase A scope vs separate track |
| OQ-ARCH-002 | Custom user model now, or stay with `User` + `Profile`? |
| OQ-ARCH-003 | Frontend direction (templates+htmx vs API-first) |
| OQ-PROD-001 | Keep cycle-table scheduler or implement SM-2 (`memo_index`)? |

---

## Changelog

| Date | Change |
|------|--------|
| 2026-06-02 | Initial full-project analysis; raised OQ-ARCH-001/002/003, OQ-PROD-001 |
