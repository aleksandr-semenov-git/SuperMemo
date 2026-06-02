# 02 — Architecture & layers

**Domain reference (facts).** How the code is organized. Critique/roadmap live in [project-work/PROJECT_ANALYSIS.md](./project-work/PROJECT_ANALYSIS.md).

---

## Stack

| Concern | Tech |
|---------|------|
| Web framework | Django (project package `src/src/`) |
| API | Django REST Framework + Djoser + SimpleJWT |
| Async tasks | Celery + Redis broker |
| DB | PostgreSQL (SQLite optional via `USE_SQLITE`) |
| Static | WhiteNoise |
| Templates | Django template language (server-rendered UI) |

Target runtime after migration: Python 3.14 + Django 5.2 LTS — see [project-work/python-314-migration.md](./project-work/python-314-migration.md).

---

## Layering

```text
HTTP request
   │
   ▼
View (class-based django.views.View)   ← thin: parse request, call services, render/redirect
   │
   ▼
Service (static-method class)          ← business logic; one service area per concern
   │
   ▼
Model (django.db.models.Model)         ← data + minimal behavior
```

- **Views** are class-based `View`s, mostly guarded by `@method_decorator(login_required, ...)`.
- **Services** are stateless classes of `@staticmethod`s (e.g. `QuestionService`, `RepSessionService`, `GoalService`). They own queries and business rules.
- **Models** hold fields and small helpers.

This Service Layer separation is consistent across all apps.

---

## App map

| App | Owns | Key service(s) |
|-----|------|----------------|
| `memo` | Home page, `Goal`, goal API | `GoalService` |
| `account` | Auth (login/register/reset), `Profile`, profile API | `ProfileService` |
| `lesson` | `Section`/`Theme`/`Lesson`/`Question` CRUD + content API | `LessonService`, `SectionService`, `ThemeService`, `QuestionService` |
| `repeat` | Repetition sessions & review flow | `RepSessionService`, `QStateService`, `QuestionService` |
| `support` | Help-desk tickets & messages (API only) | `TicketService`, `MessageService`, `TicketAdminService` |

---

## Project package (`src/src/`)

| File | Role |
|------|------|
| `settings.py` | Single settings module (no dev/prod split); installed apps, DRF/JWT, DB, Celery, `DAYS_DICT` |
| `urls.py` | Root URL conf; mounts app urls + DRF/Djoser/JWT auth routes |
| `celery.py` | Celery app `src`, autodiscovers tasks |
| `tasks.py` | `celery_send_email_change_status` (support email) |
| `wsgi.py` / `asgi.py` | Server entrypoints |

---

## Cross-cutting conventions

- Service method naming: `get_X_by_Y`, `create_X`, `get_or_create_X`.
- `get_object_or_404` used in read services to surface HTTP 404.
- Inter-view state for the "current goal" is passed via `request.session['goal_id']`.
- Bulk DB ops (`bulk_create`, `bulk_update`) used in repetition hot paths.
