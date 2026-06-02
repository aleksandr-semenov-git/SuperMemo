# 04 — API & URL catalog

**Domain reference (facts).** HTTP surface as wired in `src/src/urls.py` and each app's urls. Auth/permission gaps and redundancy are critiqued in [project-work/PROJECT_ANALYSIS.md](./project-work/PROJECT_ANALYSIS.md) §3.

---

## Root mounts (`src/src/urls.py`)

| Prefix | Includes |
|--------|----------|
| `admin/` | Django admin |
| `` (root) | `memo.urls` (home, goal page) |
| `account/` | `account.urls` (auth, profile pages) |
| `lesson/` | `lesson.urls` (content CRUD pages) |
| `repeat/` | `repeat.urls` (review flow) |
| `api/` | `memo.api.urls`, `account.api.urls`, `lesson.api.urls`, router `new-lessons` (`APILessons`) |
| `api/auth/`, `api/auth-token/`, `api/base-auth/` | Djoser + DRF auth |
| `api/token/`, `api/token/refresh/` | SimpleJWT |
| `api/v1/support/` | `support.api.urls` |
| `__debug__/` | django-debug-toolbar |

---

## Server-rendered page routes (HTML)

**memo** (`name`):
- `home` `/`
- `goal_page` `/goal-page/<goal_id>`

**account**:
- `login`, `logout`, `registration`
- `password_reset*` / `reset/<uidb64>/<token>/` (Django auth views)
- `profile_basic` `/account/profile/`, `profile` `/account/profile/<username>`, `profile_edit`
- `password_change` / `password_change_done`
- `add_goal`

**lesson**:
- `add_section`, `add_theme/<section_id>`
- `lesson_learn/<theme_id>`, `edit_question/<question_id>`, `delete_question/<question_id>`

**repeat**:
- `repeat_mix` `/repeat/mix/`
- `repeat` `/repeat/<rep_id>/`, `repeat_check/<question_id>`
- `remember/<question_id>`, `not_remember/<question_id>`
- `repeat_goal` / `repeat_section` / `repeat_theme` — **stubs** (render `in_progress.html`)

---

## REST API endpoints

### memo (`/api/`)
| Method(s) | Path | View |
|-----------|------|------|
| GET | `goals/` | `Goals` (ListAPIView) |
| GET/PUT/PATCH/DELETE | `goal/<pk>/` | `GoalDetails` |

### lesson (`/api/`)
| Method(s) | Path | View |
|-----------|------|------|
| GET | `lessons/` | `Lessons` |
| GET/PUT/PATCH/DELETE | `lesson/<pk>/` | `LessonDetails` |
| GET | `sections/` · GET/PUT/PATCH/DELETE `section/<pk>/` | `Sections` / `SectionDetails` |
| GET | `themes/` · GET/PUT/PATCH/DELETE `theme/<pk>/` | `Themes` / `ThemeDetails` |
| (router) | `new-lessons/` | `APILessons` (ModelViewSet — overlaps the above) |

### account (`/api/`)
| Method(s) | Path | View | Permission |
|-----------|------|------|------------|
| GET/PUT/PATCH/DELETE | `user/profile/<pk>/` | `UserProfileDetails` | `IsOwnerOrReadOnly` |
| GET/PUT/PATCH/DELETE | `profile/<pk>/` | `ProfileDetails` | `ProfileIsOwnerOrReadOnly`, `IsAuthenticated` |

### support (`/api/v1/support/`)
| Method(s) | Path | View | Permission |
|-----------|------|------|------------|
| GET (list) / POST (create) | `user/tickets/` | `TicketViewSet` | `IsAuthenticated`, `IsTicketOwnerOrReadOnly` |
| GET (list) / POST (create) | `user/ticket/<ticket_id>/messages/` | `MessageViewSet` | `IsAuthenticated`, `IsThreadParticipant` |

---

## Auth configuration (facts)

- DRF default auth classes: Basic, Token, Session, JWT (`settings.REST_FRAMEWORK`).
- JWT via SimpleJWT; `AUTH_HEADER_TYPES = ('JWT',)`; access 5 min / refresh 1 day.
- Djoser handles registration/activation/password reset over the API.

> `memo` and `lesson` API views set no `permission_classes` and query `objects.all()` (no per-user scoping) — flagged High in the analysis.
