# Quiet responders: the problem, and who does what

**Rook Dispatch · for Helen Achebe and the Dispatch team · from the Dispatch PM · 22 Sep 2026**
**Status:** draft. Not yet reviewed with Wen Li or Marcus Oyelaran. Replaces `brief-package.md`, and that file's Part D still holds the full engineering spec.

---

## 1. The business problem worth solving

**In one sentence:** Dispatch has no way back for a responder who goes quiet. Once someone misses a few offers, they stop being offered work, and since the only way to recover is to answer an offer, they stay switched off. No one is told: not the responder, not their handler, and not us.

**Where it came from.** The loop has been in the ranking code since 2019, when Wen questioned it in a code comment. 4.2 (12 Aug) cut the offer timeout from 90s to 60s. That turned missed offers from rare into common and set the loop off at scale for the first time.

**What it costs us now** (from `callout-history.csv`, 16 responders, 29 Jun–31 Aug):

| Cost | Evidence |
|---|---|
| **Paying customers getting no work.** We price per active responder. | 4 of 16 (25%) fell to 0–1 offers a week: Farlight, Meteor Mite, The Undertow, Vesper. Before 4.2 each got 11–14 offers a week, with healthy acceptance. |
| **Work is concentrating on fewer people.** | The top 4 responders' share of all offers rose from **32% to 48%** in three weeks. The Gale went from 13 to 21 a week, and Kip calls them "exhausted." |
| **Fewer accepted callouts.** | **~100 fewer accepted offers** in the 4 weeks after 4.2 than the prior run rate (428 vs ~529, −19%). *If one accepted offer is one filled callout, that's incidents filled late or not at all. Ravi to confirm.* |
| **Support load.** | Callout tickets at ~3× normal for five weeks. |
| **Loss of trust.** | Handlers can't explain it. Kip: "hang in there… what else do you say." |
| **We didn't know.** | The regression ran for a month unnoticed. One affected responder (Vesper) never filed a ticket. Acceptance has already climbed back to 73% (from 54%, versus 77% before), so **the headline metric will soon say "fixed" while four people are still at zero.** |

**Not yet seen, but the real risk:** a responder with no work has no reason to keep paying. No one has said they're leaving. The four handlers of the affected responders are where we'd hear it first.

**Why it's worth solving, not just patching.** The one-line code fix stops the loop, but recovery would take about 3 weeks, invisibly, and the next time something similar happens we'd miss it again. The problem isn't one number in the code. It's that no one can see a responder going quiet, and no one can do anything about it.

**What solving it is worth:**
- The four responders' seats are kept.
- Work spreads out again.
- Tickets fall.
- There's a metric that catches the next one within a week instead of a month.

**What this is *not*:**
- A reason to revert 4.2's distance change. Wide-territory responders asked for it.
- The "phone never goes off" complaints from responders whose offers *rose* (Nightwell, Ironvale and others). That's a separate push-delivery problem with its own track.

---

## 2. What we'll do, in one paragraph

**Step 1 (4.3):** stop the damage. A low score fades back to neutral on its own, a missed offer costs less than a decline, and the timeout eases to 75s. It ships with a plain note to handlers, not quietly.

**Step 2 (4.3):** start recording every offer, including the responders who were ranked but never reached.

**Step 3 (4.4):** show handlers when a responder has gone quiet, and why, on the console, and give them an **"I'm back — send me work"** check-in that restores that responder's standing.

**Step 4 (4.4–4.5):** give responders the same check-in and their own offer history on mobile.

We don't add routing settings, we don't show scores, and we don't promise anyone a volume of work.

---

## 3. By perspective: what each person owns

Each section covers: **what it means for you → what you deliver → done when → your first step this week.**

### Director (Helen Achebe)
**What it means for you:** a revenue and trust risk that our headline metric is about to hide, plus a process gap: routing changes ship everywhere at once with no alarm.
**Decide:**
1. Approve step 1 for 4.3, shipped openly.
2. Fold the unshipped 4.2 commitment "Availability Confidence" into this.
3. Make region-by-region rollout plus acceptance alerts standard for routing changes.
4. Add "responders gone quiet" as a second headline metric.

**Done when:** the decisions are recorded and the roadmap is updated.
**First step:** hold the overdue Q3 commitments conversation with the PM this week. It decides what fits in 4.3 and 4.4.

### Product (Dispatch PM)
**Owns:** the problem framing, scope, success measures and sequencing, and coordinating everyone below.
**Delivers:**
- this brief
- the release note for step 1
- the success-metric targets, agreed with Ravi
- the go/no-go for each region

**Success (8 weeks after step 3):**
- No responder quiet for more than 2 weeks.
- At least 80% of quiet responders flagged before a ticket arrives.
- Median check-in to next accepted callout of 7 days or less.
- Callout tickets back to normal once delivery is fixed.

**Guardrails:** acceptance rate, time-to-accept and coverage gaps must not get more than 10% worse in any region.
**Stop and rethink if:** most check-ins don't lead to an accepted callout within 2 weeks.
**First step:** contact the four affected handlers (Linda Pruitt, Kip, Desmond Okafor, Aunt Dot) with Nadia. Offer each responder a manual reset, and watch what they do. That tests the core assumption before we build.

### Customer: the handler (Kip)
**Today:** two cards side by side, one silent and one on fire, and nothing to say to either responder.
**After step 3:**
- The card flags *"Meteor Mite: 1 offer last week, usually ~11,"* with one plain reason, or "we can't tell yet."
- One button checks Mite back in.
- The Gale's card shows *"about twice usual."*

**What Kip won't get:** routing controls, scores, or a guarantee of work. After a check-in, distance still decides.

### Customer: the responder who's gone quiet (Meteor Mite, Vesper)
**Today:** silence, with no way to tell whether something is broken.
**After step 4:**
- An "I'm back" button.
- A 30-day list of offers received, taken, missed and declined.
- A plain status: "recovering" or "normal."

Silence becomes something they can see and act on.

### Design (Sofia Marino)
**Delivers:**
- The console card state: quiet or surge badge, the "why" line, and the handler check-in.
- The mobile check-in and "Your offers" screens.
- Plain-language copy for the six "why" answers (below), with no numbers or ranks shown.

**Done when:** a clickable mock has been tested with Kip, Aunt Dot and one large-roster handler, and the flag doesn't feel like noise at scale.
**First step:** add the card state to the console redesign now. Kip's dark mode lands on the same screen.

### Engineering (Marcus Oyelaran, Wen Li)
**What the code means for this design:**
- `history.py` keeps one in-memory score per responder and no offer history.
- `offer.dispatch()` leaves no trace of responders ranked below the one who accepted.
- `push_to_device` and `poll_device` are stubs, so delivery can't be confirmed.
- A check-in's effect is bounded: standing is 0.25 of the ranking weight, so moving from 0 to 0.5 is worth about the same as being 9 minutes closer.

**Delivers:**

| # | Item | Size* | Release |
|---|---|---|---|
| E1 | Review and ship the drafted scoring fix: decay, timeout penalty, symmetric points, 75s timeout | S | 4.3 |
| E2 | **Offer event log.** One row per responder per ranked callout. Outcome is accepted, declined, no answer, or **not reached**. Rank position, score components, and `delivered_at` (null until the delivery audit lands). Responder IDs only. | M | 4.3 |
| E3 | **Quiet/surge job**, run daily. Quiet is under 40%, and surge over 140%, of the responder's own 6-week median of reached offers per available hour. Only for responders with a baseline of 4 or more and at least 4 weeks of history. Thresholds live in `config.py`. | S | 4.4 |
| E4 | **"Why" rules**, first match wins: (1) mostly unavailable, (2) little matching work, (3) not reached and score under 0.35, "missed offers, check in," (4) not reached and score 0.35 or more, "others closer," (5) sent but delivery unconfirmed, (6) normal variation | M | 4.4 |
| E5 | **`POST /responders/{id}/check-in`.** Callable by the responder or an assigned handler, otherwise 403. Requires the responder to be available. Sets `score = max(current, 0.5)` atomically. Once per 7 days, otherwise 429. Audit-logged. Never writes the Availability Record. | S | 4.4 |
| E6 | Feature flag by region, alert on a 10% move in acceptance or time-to-accept, and a kill switch | S | 4.4 |
| E7 | Mobile check-in and offer history | M | 4.4–4.5 |

\*PM estimates, about 2–3 sprints in total. Marcus to confirm.

**Done when:**
- Replaying Jun–Aug data flags exactly the four collapsed responders within 7 days of 12 Aug. The rule has already been checked against the CSV, and it does.
- The check-in tests pass: floor score goes to 0.5, a score above 0.5 is unchanged, and a repeat call gets 429.
- A handler can't act on another handler's responder.
- The Supply contract test on `availability.current_record()` shows no change.
- Offer-log writes add no more than 50 ms at p95 to dispatch.

**First step:** Wen reviews E1 and answers the three open questions in section 5.

### Data (Ravi Menon, via #data)
**Delivers:**
- a written definition of `pings_sent`: ranked, sent, or delivered?
- the "responders gone quiet" weekly metric
- confirmation of whether accepted offers equal filled callouts, which sizes the ~100-callout gap above
- per-region baselines for the rollout alerts

**Done when:** the new metric appears in the weekly report next to acceptance rate.
**First step:** the `pings_sent` definition. Every number in this brief depends on it.

### Support (Nadia Hoffmann)
**Delivers:**
- an honest script for "is my account broken?"
- a guide to reading the new flag and "why" line
- tagging to separate "never arrived" tickets (the delivery problem) from "gone quiet" tickets

**Done when:** the ticket trend can be split by cause.
**First step:** join the PM on the four handler calls. Pass any mention of leaving straight to the PM.

### Supply PM
**What it means for you:** nothing changes in the Responder Availability Record. The check-in doesn't write to it, and a contract test guards it.
**First step:** a 15-minute briefing before 4.3.

### Security
**Delivers:** sign-off that offer-level history (responder IDs, no identity) fits Policy 4.1, and a retention period. 13 months is proposed.
**First step:** review the E2 schema.

---

## 4. Timeline

| When | Director | Product | Design | Engineering | Data | Support |
|---|---|---|---|---|---|---|
| **This week** | Decisions 1–4, Q3 talk | Handler calls, manual reset trial | Card state into redesign | Wen reviews E1 | `pings_sent` definition | Script, join calls |
| **4.3** | — | Release note | Mock testing | E1, E2 | Quiet metric live | Ticket tagging |
| **4.4** | Region go/no-go | Measure against targets | Console ships | E3–E6, region by region | Region baselines | Flag guide |
| **4.4–4.5** | — | 8-week review | Mobile ships | E7 | Report | — |

In parallel, Marcus's push-delivery audit covers Nightwell, Cindermark, The Drift, Ironvale, Stormwrack, Sgt. Falkirk and The Longcast.

---

## 5. Risks and open questions

| Item | Owner |
|---|---|
| **Risk:** check-ins could pull work toward farther-away responders. *Mitigation:* once per 7 days, plus the per-region alerts. | Marcus, PM |
| **Risk:** the "why" line stays vague until delivery can be confirmed. *Mitigation:* it says so rather than guessing. | Marcus |
| **Risk:** mobile is the long pole. *Mitigation:* the handler check-in ships first, on the console. | Sofia |
| Are scores held in memory in production, and reset on every deploy? If so, our August analysis shifts. | Wen, Marcus |
| Is there a ranking log to backfill the offer log from? | Wen |
| Should decay run while a responder isn't being offered anything? | Wen |
| Does one accepted offer equal one filled callout? | Ravi |

*Evidence: `00-rook/data/callout-history.csv`, tickets T-001–T-025, Sofia's console interviews (2–5 Sep), and `00-rook/code/dispatch-routing/`.*
