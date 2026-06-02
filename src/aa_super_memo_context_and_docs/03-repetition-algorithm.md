# 03 — Repetition / scheduling algorithm

**Domain reference (facts).** The current scheduling logic as implemented in `src/lesson/services/question_service.py` and the repeat flow in `src/repeat/`. Whether to replace it with SM-2 is **OQ-PROD-001** (see [project-work/PROJECT_ANALYSIS.md](./project-work/PROJECT_ANALYSIS.md)).

---

## Core idea

Each `Question` has a `cycle` (an integer). The `cycle` maps to an interval in **days** via a fixed lookup table; after each review the `cycle` moves up or down based on how the user performed, which changes when the card is next due.

`memo_index` exists on the model but is **not** used by this algorithm.

---

## The interval table (`settings.DAYS_DICT`)

```python
DAYS_DICT = {0: 0, 1: 1, 2: 2, 3: 12, 4: 20, 5: 30, 6: 60, 7: 90,
             8: 150, 9: 270, 10: 480, 11: 720, 12: 1440, 13: 2160,
             14: 3960, 15: 6480}
```

`QuestionService.cycle_to_days(cycle)` → `DAYS_DICT[cycle]`.

---

## Score → cycle transition

`score` comes from `QState.score` (starts at 1; incremented each time the user marks "not remember" in the session).

`QuestionService.calculate_new_cycle(cycle, score)`:

| Condition | New cycle |
|-----------|-----------|
| `cycle > 1` and `score < 3` | `cycle + 1` (longer interval) |
| `cycle > 1` and `3 ≤ score ≤ 5` | `cycle - 1` (shorter interval) |
| `cycle > 1` and `score > 5` | `1` (reset — repeat soon) |
| `cycle == 1` and `score < 3` | `2` |
| `cycle == 1` and `score ≥ 3` | unchanged (`1`) |
| otherwise (`cycle == 0`) | `1` |

**Interpretation:** fewer wrong attempts → the interval grows; many wrong attempts → it collapses back to daily review.

---

## Scheduling a remembered card

`QuestionService.save_remembered_question(question, score)`:

1. `new_cycle = calculate_new_cycle(question.cycle, score)`
2. `prev_repeat_at = question.next_repeat_at` (today's due date becomes the new "previous")
3. `next_repeat_at = prev_repeat_at + timedelta(days=cycle_to_days(new_cycle))`
4. `repeated_num += score`
5. `question.save()`

> Note: the persisted `question.cycle` update path is centralized here; see analysis §3 for observed coupling in `QState.save()`.

---

## Selecting what to review

| Helper | Behavior |
|--------|----------|
| `get_today_questions_by_profile(profile)` | First renews forgotten cards, then returns questions where `next_repeat_at == today` for that profile |
| `renew_date_of_all_forgotten_questions(profile)` | Any card with `next_repeat_at <= yesterday` is pulled forward to today (`bulk_update`) |
| `get_next_question_by_rep_session(rep_session)` | From the session, cards due today ordered by `edited_at`, returns the first |

---

## Session lifecycle (Mix mode)

```text
RepeatMix.get
   │  active session for profile?
   ├─ yes → redirect to repeat:<rep_id>
   └─ no  → questions due today?
             ├─ none → redirect to profile
             └─ some → create RepetitionSession + QState rows → redirect to repeat:<rep_id>

Repeat.get(rep_id)
   │  next due question in session?
   ├─ yes → render repeat.html (show question)
   └─ no  → finish session (status=FINISHED, finished_at=today) → redirect to profile

repeat_check → show answer
  ├─ Remember.post     → save_remembered_question(question, qstate.score) → reschedule
  └─ NotRemember.post  → QStateService: qstate.score += 1 (harder; stays due today)
```

Modes **Goal / Section / Theme** are defined on `RepetitionSession` but their views/services are not implemented yet (render `in_progress.html`).
