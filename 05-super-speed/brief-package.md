# A way back from quiet: brief package

**Rook Dispatch · for Helen Achebe · from the Dispatch PM · 22 Sep 2026**
**Status:** draft. Not yet reviewed with Wen Li or Marcus Oyelaran. Replaces `quiet-responder-brief.md` and `director-brief.md`.

| Part | For | Read if you want to know… |
|---|---|---|
| **A. Decision brief** | Helen | what we propose, and what I need from you (1 page) |
| **B. The experience** | Helen, Sofia, Nadia | what changes for Kip and for a quiet responder |
| **C. Product case** | Helen, Ravi | why now, how we'll measure it, options we rejected, cost |
| **D. Engineering spec** | Marcus, Wen | what gets built, and the rules it follows |
| **E. Delivery plan** | everyone | order, owners, risks, open questions |

---

## A. Decision brief

**Bottom line.** The small code fix is real, and we should ship it. But it only stops the damage; it doesn't fix the experience. We propose a way back from quiet that people can see and use. Handlers are told when a responder has gone quiet and why, and responders (or their handler) get one "I'm back" check-in that restores their standing. We don't revert 4.2's change to weight distance more heavily, and we don't add a routing setting.

**What's happening.** A missed offer lowers a responder's standing. The only way to raise it again is to answer another offer, and low standing means they stop being offered. That loop has been in the code since Wen's 2019 note questioned it. 4.2's shorter timeout triggered it at scale for the first time. Meteor Mite fell from about 11 offers a week to 1 while Kip's other responder, The Gale, rose from 13 to 21 in the same city. Vesper collapsed the same way and never filed a ticket.

**Why it can't wait for September's numbers.**
- **Our headline number will look healed while four people stay at zero.** Acceptance fell from 77% to 54% the week of release and was back to 73% by 31 Aug. Farlight, Meteor Mite, The Undertow and Vesper are at 0–1 offers a week.
- **It isn't just a slow August.** Total offers held steady at 158–177 a week. The work moved between responders; it didn't dry up.
- **It's a revenue risk.** We price per active responder, and 4 of 16 responders (25%) are effectively switched off.

**Decisions I need from you.**
1. **Approve step 1 for 4.3, shipped openly with a note to handlers.** Standing fades back to neutral on its own, a missed offer costs less than a decline, and the timeout goes from 60s to 75s. The code is drafted in our working copy. It isn't deployed and still needs Wen's review.
2. **Fold "Availability Confidence" into this.** It was committed for 4.2 and didn't ship. The check-in is that signal, coming from the responder.
3. **Hold the Q3 commitments conversation this week.** It decides what fits in 4.3 and 4.4.
4. **Make region-by-region rollout with acceptance-rate alerts standard for routing changes.** Without it, 4.2's regression ran unnoticed for a month.
5. **Add "responders gone quiet" as a second headline metric,** reported weekly by Ravi next to acceptance rate.

**This week, before anything ships:**
- Nadia or I contact the four affected handlers: Linda Pruitt, Kip, Desmond Okafor and Aunt Dot.
- Support gets an honest script for "is my account broken?"
- The Supply PM is briefed.

---

## B. The experience

**Who it's for.**
1. **The handler (primary).** They use the console and field the "is it broken?" texts. Today they can't tell a quiet week from a quiet responder.
2. **The responder who's gone quiet (secondary).** Today, silence feels like being forgotten.

**What changes.**
- **Kip sees it before Mite has to ask.** The console card flags a responder who has fallen far below *their own* usual level: *"Meteor Mite: 1 offer last week, usually ~11."* The other extreme shows too: *"The Gale: 21 offers, about twice usual."*
- **The card says why, in plain words, or says we don't know.** For example: "Ranked lower after missed offers. Check in to reset." or "Offers sent; we can't yet confirm they reached the phone."
- **A way back that doesn't depend on being asked.** **"I'm back — send me work"** raises standing to at least neutral right away and never lowers it. It isn't a guarantee: after a check-in, distance decides, and the card says so.
- **Responders can see their own recent offers.** Offers received, taken, missed and declined over 30 days, with a plain status ("recovering," "normal"). Ironvale asked for exactly this.

**What it deliberately doesn't do.**
- It doesn't revert the 4.2 distance change or let handlers adjust routing. Routing still ships with releases.
- It doesn't show scores or rank, only plain-language states.
- It doesn't promise volume: no quotas and no taking turns. A check-in is worth about the same as being 9 minutes closer.
- It doesn't write to the Availability Record. "Quiet" is not "unavailable," so Supply is unaffected.
- It doesn't fix "my phone never goes off" (Nightwell, Ironvale and others, whose sent offers *rose*). That's the separate push-delivery audit.
- It doesn't know who anyone is. It uses only callout history and availability (Policy 4.1).
- Not in v1: protecting overloaded responders (flag only), and different alert sounds per responder (Kip's ask).

---

## C. Product case

**How we'll know it worked** (measured 8 weeks after the console launch):

| Measure | Now | Target |
|---|---|---|
| Responders gone quiet (under 40% of their own usual) | 4 of 16 | 0 stuck for more than 2 weeks |
| Time from check-in to next accepted callout | Never, in practice | Median ≤ 7 days |
| Quiet responders flagged before a ticket or text reaches us | ~0 | ≥ 80% |
| "Nothing's coming through" tickets | ~3× normal | Back to normal, once delivery is also fixed |

**Guardrails.** None of these may get more than 10% worse in any enabled region:
- acceptance rate
- median time-to-accept
- coverage gaps

We also watch the busiest responders' load.

**When we'd stop and rethink:**
- if most check-ins don't lead to an accepted callout within 2 weeks, or
- if a guardrail breaks in two regions.

*The targets are starting points to agree with Ravi.*

**What has to be true, and how we check before building:**

| Assumption | How we check | When |
|---|---|---|
| Handlers act on a flag rather than tuning it out | Clickable mock with Kip, Aunt Dot and one large-roster handler (Sofia) | Before the console build |
| Quiet responders will check in rather than leave | Offer the reset by hand, through Support, to the four affected | This month |
| The "why" line matches reality | Check it against Wen's reading of The Undertow's ranking logs | During offer-log build |
| Check-ins aren't gamed | Watch for check-ins followed by declines in the first region | First region live |

**Options we rejected:**

| Option | Why not |
|---|---|
| Revert 4.2 | Trades one angry group for another, and the loop is older than 4.2 |
| Ship the code fix only | Recovery takes about 3 weeks, invisibly. Kip still has nothing to tell Mite |
| Quotas or rotation | Deliberately sends callouts to responders farther away. That's a policy change |
| Handler-tunable routing | Breaks the rule that routing ships with releases, and shifts our flaw onto handlers |
| Just notify quiet responders | Tells them the problem without giving them anything to do about it |

**Cost and what it moves.**
- **Engineering:** roughly 2–3 sprints across 4.3–4.4. This is my estimate; Marcus to confirm.
- **Design:** lands in Sofia's console redesign.
- **Displaced:** some of the work squeezed out of 4.2, pending the Q3 conversation.
- **Future work:** the offer log is the data Q4 "shared cover between responders" will need.

---

## D. Engineering spec

*Written against `00-rook/code/dispatch-routing/` as it is today.*

**What the code means for this design:**
- **No offer history is kept.** `history.py` holds one score per responder in an in-memory dict.
- **Responders ranked below the one who accepted leave no trace.** `offer.dispatch()` stops at the first accept, and that's the most common way to go quiet.
- **Delivery can't be confirmed yet.** `push_to_device` and `poll_device` are stubs.
- **A check-in has a limited effect.** Standing is 0.25 of the ranking. Moving from 0 to 0.5 adds 0.125, about the same as being 9 minutes closer (0.60 × 9/45).

**D1. Offer event log** (backend, **M**, everything else depends on it).
- One row per responder per callout that reaches ranking: `callout_id, responder_id, region, ranked_at, rank_position, reached, offered_at, delivered_at (null until the delivery audit lands), outcome ∈ {accepted, declined, no_answer, not_reached}, answered_at, score_components`.
- Write `not_reached` for everyone below the responder who accepted.
- Responder IDs only.
- Keep rows for 13 months, pending Security.

**D2. Quiet and surge flags** (daily job, **S**).
- Baseline is the median of weekly reached offers over the previous 6 weeks, normalised per available hour.
- **Quiet** when a responder is under 40% of their baseline. **Surge** when they're over 140%.
- Only flag responders with a baseline of 4 or more and at least 4 weeks of history.
- Thresholds live in `config.py`.
- *Replayed on the Jun–Aug data, the quiet rule flags exactly the four collapsed responders in the week of 17 Aug, and nobody else. Surge flags The Gale, Captain Vantage, Sgt. Falkirk and Ironvale. Ironvale also reports silence, so a surge in sent offers combined with a silence ticket is a delivery signal.*

**D3. "Why" line** (**M**; Wen to check rules 3 and 4). The first rule that matches wins:
1. Mostly unavailable
2. Little matching work nearby
3. Mostly `not_reached` and acceptance score under 0.35: "Ranked lower after missed offers. Check in to reset"
4. Mostly `not_reached` and acceptance score 0.35 or above: "Others were closer"
5. Sent, not delivered and not answered: "Can't yet confirm offers reached the phone"
6. Otherwise: normal variation

**D4. Check-in API.** `POST /responders/{id}/check-in` (**S**)
- **Who can call it:** the responder, or an assigned handler. Anyone else gets a 403. Every call is written to the routing-override audit log.
- **Precondition:** the responder is marked available. If not, the UI routes them to the existing availability flow. The check-in itself never writes the Availability Record.
- **Effect:** `score = max(current_decayed, NEUTRAL_SCORE)`, applied atomically with dispatch writes, and the decay timestamp resets.
- **Limits:** once per responder per 7 days (429 after that). Requests carry an idempotency key.

**D5. Surfaces.**
- **Console:** badge, "why" line, and a handler check-in on the responder's behalf (**S/M**, Sofia).
- **Mobile:** responder check-in and a 30-day "Your offers" list, with no scores or rank (**M**, goes through app-store review).
- No new push notifications in v1.

**D6. Rollout and safety.**
- Everything sits behind a feature flag and is turned on one region at a time.
- An alert fires if acceptance rate or time-to-accept moves more than 10% against that region's own baseline.
- A kill switch hides the badges and disables check-in. The offer log keeps writing.

**D7. Acceptance criteria.**
- Replaying Jun–Aug data flags the four collapsed responders within 7 days of 12 Aug, and no one else.
- Check-in takes a floor-score responder to 0.5. A score already above 0.5 is unchanged. A second call within 7 days returns 429.
- A handler can't view or check in a responder they don't handle.
- `availability.current_record()` output is unchanged, verified by a contract test with Supply.
- Offer-log writes add no more than 50 ms at p95 to `dispatch()`.

---

## E. Delivery plan

| Step | What | Release | Owner |
|---|---|---|---|
| 0 · Now | Contact the four handlers, write the Support script, brief the Supply PM, ask Ravi to define the new metric and what `pings_sent` counts | this week | PM, Nadia |
| 1 · Stop the damage | Decay, timeout penalty, symmetric points, 60s → 75s timeout, handler release note | 4.3 | Wen (review), Marcus |
| 2 · Start recording | D1 offer log. Collect 2–4 weeks of data, or backfill from ranking logs if they exist | 4.3 | Marcus |
| — Validate | Clickable mock with handlers, plus the manual check-in trial | during step 2 | Sofia, PM |
| 3 · Show it to handlers | D2 flags, D3 "why" line, D4 API, console check-in, rolled out region by region | 4.4 | Marcus, Sofia |
| 4 · Show it to responders | Mobile check-in and offer history | 4.4–4.5 | Mobile, Sofia |
| In parallel | Push-delivery audit (Nightwell, Cindermark, The Drift, Ironvale, Stormwrack, Sgt. Falkirk, The Longcast) | — | Marcus |

*Change from the earlier drafts: the handler check-in ships in the console at step 3, so the recovery path doesn't wait for the app-store cycle.*

**Risks.**
- **Offers could flow to people farther away.** Limited by the 7-day check-in limit and the per-region alerts.
- **The "why" line stays vague until delivery is confirmed.** It says so rather than guessing.
- **Our read of August may shift.** If scores reset on every deploy, the analysis changes.
- **The mobile release is the long pole.** That's why the console check-in comes first.

**Open questions:**

| Question | Owner |
|---|---|
| Are scores really held in memory in production, and reset on each deploy? | Wen, Marcus |
| Is there a ranking log to backfill the offer log from? | Wen |
| Should decay run while a responder isn't being offered anything? | Wen |
| What exactly does `pings_sent` count: ranked, sent, or delivered? | Ravi, Marcus |
| How long can we keep offer-level history under Policy 4.1? | Security |

**Who hears what.**
- **Affected handlers:** this week.
- **All handlers:** release note on 4.3 morning.
- **Support:** script and flag guide before each step.
- **Supply PM:** before 4.3, backed by the contract test.
- **Ravi (via #data):** now.

*Evidence: `00-rook/data/callout-history.csv` (weekly offers, 16 responders, 29 Jun–31 Aug), tickets T-001–T-025, Sofia's console interviews (2–5 Sep), and `00-rook/code/dispatch-routing/`.*
