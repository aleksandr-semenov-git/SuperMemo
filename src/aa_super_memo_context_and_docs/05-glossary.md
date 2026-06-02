# 05 — Glossary

**Domain reference (facts).** Terms used across SuperMemo code and docs.

| Term | Meaning |
|------|---------|
| **Profile** | Per-user record (`account.Profile`), 1:1 with Django `User`; stores avatar photo |
| **Goal** | Top-level learning objective owned by a profile (`memo.Goal`) |
| **Section** | Subdivision of a goal (`lesson.Section`) |
| **Theme** | Subdivision of a section (`lesson.Theme`); 1:1 with a Lesson |
| **Lesson** | Container/name for a theme's questions (`lesson.Lesson`); name = `"{goal} {section} {theme}"` |
| **Question** | A Q&A card with scheduling fields (`lesson.Question`) |
| **cycle** | Integer index into `DAYS_DICT`; determines days until next review |
| **DAYS_DICT** | Settings map `cycle → days` (see [03-repetition-algorithm.md](./03-repetition-algorithm.md)) |
| **memo_index** | Coefficient field on `Question`; declared but unused in current algorithm |
| **next_repeat_at / prev_repeat_at** | Scheduled next / last review dates of a question |
| **repeated_num** | Cumulative successful repetition count (`+= score`) |
| **RepetitionSession** | A review run for a profile; status IN_PROGRESS / FINISHED / PAUSED |
| **rep_mod / mode** | Session scope: Mix (`M`), Goal (`G`), Section (`S`), Theme (`T`) |
| **QState** | Through-model linking a session and a question; holds per-session `score` |
| **score** | Attempts counter in a session; starts at 1, `+=1` on "not remember"; feeds `calculate_new_cycle` |
| **Mix session** | Review of all of today's due questions across the profile (only mode implemented) |
| **forgotten question** | Card whose `next_repeat_at` is in the past; pulled forward to today before a session |
| **Ticket** | Support thread between a user and a staff member (`support.Ticket`) |
| **Message** | A single message inside a ticket (`support.Message`) |
| **support (user)** | Staff user (`is_staff=True`) assigned to handle a ticket |
| **Service** | Stateless class of `@staticmethod`s holding business logic (e.g. `QuestionService`) |
| **Phase A** | Current migration scope: Python 3.14 + Django 5.2 LTS + Heroku removal |
