# Spec: automatic standing reset after 7 days without offers

**Rook Dispatch · feature spec · Dispatch PM · 22 Sep 2026**
**Status:** draft for review with Wen Li and Marcus Oyelaran.
**Belongs to:** `brief.md`, step 1 ("stop the damage"). It's the automatic partner to the manual check-in.
**Prototype:** `prototype.html`. Use "+1 day" to watch it happen.

---

## 1. Problem

A responder's standing only moves when they get an offer. Once missed offers push standing low enough, the responder stops getting offers, so nothing can ever move it back up. The drafted decay fix eases standing back to neutral, but slowly: about 20 days for a full recovery. That's roughly three weeks of lost income for the responder and three weeks of Kip having nothing to tell them.

**Rule we're adding:** no responder stays penalised because the system stopped asking them. If a responder hasn't received a single offer in 7 days, their standing goes back to neutral automatically.

## 2. Who it's for

| Person | What changes |
|---|---|
| **Responder who went quiet** (Meteor Mite) | A bad stretch has a known, short end date. After a week with no offers, they're back on equal terms, with no action needed. |
| **Handler** (Kip) | They can see when the reset will happen ("automatic reset on 9 Sep") and when it did. They have something true to tell Mite: "you're back to normal on Wednesday, or check in now." |
| **Support** (Nadia) | A predictable answer to "is my account broken?" |

## 3. The rule

```
IF   no offer has reached the responder in the last 7 days
AND  their standing is below neutral (0.5)
THEN set their standing to neutral (0.5)
```

**Definitions:**
- **Offer reached the responder** means an offer-log row with outcome `accepted`, `declined` or `no_answer`.
  - **`not_reached` does not count.** Being ranked below the responder who accepted isn't being asked. If it counted, the quiet loop would keep resetting the clock, and the feature would never trigger for the people it's meant for.
- **7 days** means 7 × 24 hours, rolling, measured on server time in UTC from the last reached offer. Calendar days and time zones don't matter.
- **Standing** is the recent-acceptance score in `history.py`, with a range of 0–1 and neutral at 0.5.

**The reset only ever raises standing.** A responder above neutral is untouched. We never punish someone for a quiet week.

**It applies whether or not the responder was marked available.** A week away is a fresh start too. See the open question in §10.

## 4. How it fits with the other pieces

| Piece | Relationship |
|---|---|
| **Decay** (0.05/day, drafted fix) | Stays. Decay handles the first week gradually, and the reset guarantees the end. Recovery drops from ~20 days to **7 at most**. |
| **Manual check-in** | Same effect, available any time, limited to once per 7 days. The check-in is "now"; the reset is "no later than day 7." Both call one function: `restore_to_neutral(responder, reason)`. |
| **Quiet flag** (under 40% of usual offers) | Independent. A responder can be reset and still flagged quiet if others are closer. The "why" line changes to say standing is no longer the cause. |
| **Timeout penalty and points** | Unchanged. Standing can drop again after a reset, and each new reached offer restarts the 7-day clock. |
| **Availability Record / Supply** | Not touched. The reset changes standing only. |

**Worked example (Meteor Mite, from the prototype):**

| Moment | Standing | What's happening |
|---|---|---|
| 2 Sep 21:14 | 0.10 | Mite misses an offer. That's the last reached offer, so the clock starts. |
| 6 Sep | 0.18 | Decay has eased it up a little. It's still too low to be asked, and the card shows "automatic reset on 9 Sep." |
| 9 Sep 21:14 | 0.24 → **0.50** | 7 days without an offer, so standing resets. |
| Next nearby callout | 0.50 | Mite is ranked on distance and capability again. |
| Without the reset | 0.50 on **22 Sep** | Decay alone takes 13 days longer. |
| In 4.2 today | 0.10 **forever** | Nothing ever raises it. |

## 5. What people see

**Console card (handler):**
- **Before the reset,** under the "why" line: *"Resets automatically on 9 Sep if no offers arrive. Or check in now."*
- **After the reset,**
  - the badge reads **"● Standing restored automatically"**
  - the "why" line reads *"No offers for 7 days, so Mite's standing was reset to normal. Offers now depend on who's closest."*
- **Activity feed:** *"System restored Meteor Mite's standing after 7 days without offers."*

**Responder phone:**
- **Before:** *"Quiet lately… Resets automatically on 9 Sep, or tap I'm back now."*
- **After:** *"● Back to normal. It's been a week without offers, so we reset your standing. Nothing you need to do."*

**Not shown anywhere:** the numeric score, or the countdown in hours. Show dates only.

**No push notification in v1,** in line with the brief.

## 6. Data and events

- **Config** (`config.py`): `RESET_AFTER_IDLE_DAYS = 7`, with the file's usual "tell Marcus" rule.
- **Event** (`standing_restored`): `responder_id, at, reason ∈ {auto_idle, check_in}, score_before, score_after, last_reached_offer_at`. Actor is `system` for automatic resets. It's written to the routing-override audit log.
- **Idempotent:** at most one `auto_idle` event per idle period, keyed on `(responder_id, last_reached_offer_at)`.
- **Where it runs:**
  - The rule is applied on read, in `history.recent_acceptance()`, so ranking is correct the moment day 7 passes.
  - A daily sweep writes the stored score and emits the event for anyone who crossed day 7 without being read.
  - Whichever happens first persists the reset.

Reference shape for `history.py`:

```python
def recent_acceptance(responder):
    score = _decayed(responder)
    if score < NEUTRAL_SCORE and _days_since_last_reached_offer(responder) >= RESET_AFTER_IDLE_DAYS:
        return restore_to_neutral(responder, reason="auto_idle")   # persists + emits once
    return score
```

**Prerequisite:** `history.py` today tracks the last *score change*, not the last *reached offer*. It needs `last_reached_offer_at`, which comes from the offer event log (brief item E2). Until E2 exists, last-score-change is a usable stand-in: scores only change on reached offers or check-ins.

## 7. Edge cases

| Case | Behaviour |
|---|---|
| New responder, no history | Already neutral. No event. |
| Standing at or above neutral after 7 idle days | No change and no event. |
| Checked in on day 3 | Already neutral, so no auto event on day 7. The check-in's own 7-day limit still applies. |
| Reset, then a missed offer | Standing drops to 0.45 and the clock restarts. Another reset needs another 7 days with no reached offer. |
| Responder offered but ranked below the one who accepted (`not_reached`) every day | Clock keeps running. The reset triggers on day 7. This is the main case. |
| Deploy or restart during the window | The clock is based on the stored `last_reached_offer_at`, so it survives restarts. |
| Region rollout flag off | No auto reset for that region. Decay only. |

## 8. Deliberately not doing

- **No reset for responders who are getting offers but declining them.** That's real feedback, not the system's silence.
- **No resets above neutral, and no "bonus" for having been quiet.**
- **No shorter window for "good" responders.** One rule for everyone.
- **No change to how anyone is ranked on distance or capability.**
- **No identity data** (Policy 4.1).

## 9. How we'll know it works

**Acceptance criteria:**
1. A responder with standing 0.10 and no reached offers for 7 days + 1 minute is read as 0.50, and exactly one `standing_restored` event exists.
2. Only `not_reached` rows for 7 days still trigger the reset.
3. A reached offer on day 6 means no reset on day 7, and the clock restarts.
4. Standing of 0.62 after 7 idle days stays 0.62, with no event.
5. Replaying Jun–Aug data: Farlight, Meteor Mite, The Undertow and Vesper would each have been reset within 7 days of their last reached offer, rather than staying down through 31 Aug.
6. `availability.current_record()` output is unchanged (Supply contract test).
7. Card and phone show the reset date before it happens, and the restored state after, with no numbers.

**Metrics** (weekly, Ravi):
- **Auto-resets per week.** A rising count is an early warning that something is pushing people down, like 4.2 did.
- **Share of resets followed by an accepted offer within 7 days.**
- **Repeat resets for the same responder.** More than 3 in 6 weeks points to a different problem, such as delivery or distance, and should go to Support.

## 10. Open questions

| Question | Owner |
|---|---|
| Should days marked *unavailable* count toward the 7? Proposed: yes, for simplicity. The gaming risk is low, since going offline for a week costs a week of work. | Wen, PM |
| Is 7 days right? It matches the check-in limit and a weekly handler rhythm. Revisit after 6 weeks of reset data. | PM, Ravi |
| Does decay stay once the reset exists? Proposed: yes, because it makes days 1–6 gentler. | Wen |
