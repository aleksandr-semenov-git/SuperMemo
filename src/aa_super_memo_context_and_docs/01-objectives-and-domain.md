# 01 — Objectives & domain

**Domain reference (facts).** What SuperMemo is and the concepts it models. For weaknesses/roadmap see [project-work/PROJECT_ANALYSIS.md](./project-work/PROJECT_ANALYSIS.md); for "how to work" see [LEAD_AGENT_CORE.md](./LEAD_AGENT_CORE.md) / [DEV_AGENT_CORE.md](./DEV_AGENT_CORE.md).

---

## Purpose

SuperMemo is a **spaced-repetition learning app**. A user stores question/answer cards and the system decides **when** each card should be reviewed, so material is repeated just before it is likely to be forgotten.

---

## Domain concepts

| Concept | Model | Meaning |
|---------|-------|---------|
| Profile | `account.Profile` | Per-user data (1:1 with Django `User`), holds avatar photo |
| Goal | `memo.Goal` | A top-level learning objective owned by a profile |
| Section | `lesson.Section` | Subdivision of a goal |
| Theme | `lesson.Theme` | Subdivision of a section |
| Lesson | `lesson.Lesson` | 1:1 with a theme; container/name for its questions |
| Question | `lesson.Question` | A Q&A card with scheduling fields |
| RepetitionSession | `repeat.RepetitionSession` | A review run (modes: Mix/Goal/Section/Theme) |
| QState | `repeat.QState` | Per-question state within a session (`score`) |
| Ticket / Message | `support.*` | Help-desk thread between user and staff |

---

## Hierarchy & relationships

```text
User ─1:1─ Profile
                └─< Goal ─< Section ─< Theme ─1:1─ Lesson ─< Question
Profile ─< RepetitionSession ─(through QState)─< Question
```

- A `Goal` belongs to a `Profile`; `Section → Theme → Lesson → Question` chain hangs off it.
- `Lesson` is `OneToOne` with `Theme`; its `name` is built as `"{goal} {section} {theme}"` (`LessonService.get_or_create_lesson`).
- `RepetitionSession.questions` is a `ManyToMany` to `Question` **through** `QState`.

---

## Question scheduling fields (`lesson.Question`)

| Field | Role |
|-------|------|
| `prev_repeat_at` / `next_repeat_at` | Last and next scheduled review dates |
| `cycle` | Index into `settings.DAYS_DICT` → interval in days |
| `repeated_num` | Cumulative count of successful repetitions (`+= score`) |
| `memo_index` | Declared coefficient — **not used** in the current algorithm |

Algorithm detail: [03-repetition-algorithm.md](./03-repetition-algorithm.md).

---

## Primary user flow

1. Register / log in → `Profile` ensured.
2. Create a `Goal`, then `Section` → `Theme` (creates the `Lesson`).
3. Add `Question`s to a lesson.
4. Start a **Mix** repetition session → review due cards one by one, marking "remember" / "not remember".
5. Scheduler updates each card's next review date.

UI is server-rendered Django templates; a partial DRF API also exists ([04-api-and-urls-catalog.md](./04-api-and-urls-catalog.md)).
