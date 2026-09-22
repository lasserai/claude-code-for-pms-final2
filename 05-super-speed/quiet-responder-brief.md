# A way back from quiet

**Brief for Helen Achebe · Dispatch PM · 22 Sep 2026 · draft, not reviewed with Wen yet**

## The problem, from Kip's desk

Kip handles two responders in the same city. Since 4.2, Meteor Mite went from about 11 offers a week to 1. The Gale went from 13 to 21. Mite texts Kip asking whether something's broken, and Kip has nothing better to say than "hang in there." Aunt Dot saw the same thing happen to Vesper (14 offers a week down to 1), noticed it only as "quiet weeks," and never filed a ticket.

Here's how it works underneath. A missed or declined offer lowers a responder's standing. The only way to raise it again is to answer another offer, and responders with low standing don't get offered. So once someone goes quiet, nothing brings them back. Wen flagged exactly this in a 2019 TODO. The drafted code fix makes low standing fade back to neutral over about 20 days. That's a floor, not a product: nobody is told anything, nobody can act, and "wait three weeks" is still the answer.

## Who it's for

1. **The handler (primary).** They use the console and they field the "is it broken?" messages. Today they can't tell a quiet week from a quiet responder.
2. **The responder who's gone quiet (secondary).** Today, from their side, silence looks like being forgotten.

## What changes for them

- **Kip sees it before Mite has to ask.** A coverage card flags a responder whose offers fall well below their own usual level: *"Meteor Mite: 1 offer last week, usually ~11."* The Gale's card shows the other side: *"21 offers, about twice usual."* This compares each responder to their own history, not to the other responders, so it would have caught Vesper without an interview.
- **The card says why, in plain words, or says we don't know.** For example: "ranked lower after missed offers" versus "offers sent, none answered." Until we can confirm an offer reached the phone (the push-delivery audit), the card says so plainly and doesn't guess.
- **A way back that doesn't depend on being asked.** The responder, or the handler on their behalf, can tap **"I'm back — send me work."** A check-in raises standing to at least neutral right away (it never lowers it). It's the missing input: the responder speaks up instead of waiting to be called. It doesn't guarantee offers: after a check-in, distance decides, and the card says so.
- **The responder can see their own recent offers.** A simple list of offers received, taken, missed and declined, plus a line about where they stand now ("recovering," "normal"). Ironvale asked for exactly this, and it answers most "is my account broken" tickets before anyone files one.

## What it deliberately doesn't do

- **Doesn't touch the 4.2 proximity change.** Responders with wide territories asked for it; reverting it just makes a different group angry.
- **Doesn't show scores or rank.** People see plain-language states, never numbers. No one can game a number they can't see, and the weights stay Wen's to explain.
- **Doesn't let handlers adjust routing.** Routing still ships with releases. A check-in resets one responder's own history and nothing else.
- **Doesn't promise volume.** No quotas and no taking turns. Closest-and-capable still wins, and quiet responders just aren't locked out anymore.
- **Doesn't write to the Availability Record.** "Quiet" is not "unavailable," so Supply's maintenance scheduling isn't affected. I'll still brief the Supply PM.
- **Doesn't fix delivery.** "Phone never goes off" for Nightwell, Stormwrack and the others is a separate push-delivery track with Marcus.
- **Doesn't know who anyone is.** It uses only callout history and availability (Policy 4.1).

## How we'd know it worked

- Most responders who go quiet get flagged on the console before a ticket or a text reaches us.
- Median time from a check-in to the next accepted callout goes down.
- "Is my account broken" tickets fall.
- Acceptance rate and time-to-accept hold steady for everyone else.

## Asks

- **Helen:** Should this absorb **Availability Confidence**? That was committed for 4.2, driven by support escalations, and didn't ship. The check-in is basically that signal coming from the responder.
- **Wen:** Can a check-in safely reset standing, and should standing still fade back when nobody is offering the responder anything?
- **Sofia:** Put the card state and the history view into the console redesign.
- **Ship order:** decay fix and 75s timeout first (the floor), then this in 4.3 or 4.4.

---

# Page 2 — Engineering view: what it takes to build

*Written against `00-rook/code/dispatch-routing/` as it stands today. Sizes are PM guesses for Marcus to correct.*

## What page 1 left out

| Gap | Why it blocks building |
|---|---|
| **No offer log exists.** | `history.py` keeps only one number per responder, in an in-memory dict. The history view, the baseline and the "why" all need every offer recorded. |
| **Responders who were ranked but never reached aren't recorded.** | `offer.dispatch()` stops once someone accepts, so everyone below that point leaves no trace. That's the most common way to go quiet, and right now it's invisible. |
| **"Well below usual" had no definition.** | An engineer needs a rule, a time window and thresholds. See below. |
| **No list of possible "why" answers, or which one wins.** | Several reasons can apply at once, and the card has to pick one. |
| **Check-in behaviour wasn't specified.** | Who can trigger it, how often, what happens if the score is already above neutral, and whether they must be available first. |
| **Delivery can't be confirmed.** | `push_to_device` and `poll_device` are stubs. The quiet flag can't see the "phone never goes off" group at all: Nightwell's sent-count *rose* from 15 to 21 a week. |
| **What a check-in is actually worth.** | Standing is 0.25 of the ranking weight. Going from floor (0) to neutral (0.5) adds 0.125, about the same as being **9 minutes closer** (0.60 × 9/45). Useful, but it won't beat someone 20 minutes closer. That's why "doesn't guarantee offers" is now on page 1. |
| **No rollout, test or acceptance criteria.** | Needed before this can go on a release train. |

## Spec

**1. Offer event log (new, backend).** Add one row per responder per callout that reaches ranking:
`callout_id, responder_id, region, ranked_at, rank_position, reached (bool), offered_at, delivered_at (null until the push-delivery audit lands), outcome ∈ {accepted, declined, no_answer, not_reached}, answered_at, score_components {proximity, acceptance, capability}`.
- Write `not_reached` for everyone below the responder who accepted.
- Keep responder IDs only. No identity data (Policy 4.1).
- Retention: 13 months, to match seasonality comparisons. *Confirm with Security.*
- **Size: M.** Everything below depends on this.

**2. Quiet and surge flags (daily job).**
- Baseline is the median of the responder's offers per week over the 6 weeks before the current one. Offers count if `reached = true`.
- **Quiet** if this week is under 40% of baseline. **Surge** if it's over 140%.
- Only flag responders with a baseline of at least 4 and at least 4 weeks of history.
- Count offers per *available hour* rather than per week, so a responder who set themselves off-duty isn't flagged.
- Put the thresholds in `config.py`, following the same "tell Marcus" rule.
- *Replayed against `callout-history.csv`, the quiet rule flags exactly Farlight, Meteor Mite, The Undertow and Vesper, all in the week of 17 Aug, and nobody else. At 140%, surge catches The Gale, Captain Vantage, Sgt. Falkirk and Ironvale by 24–31 Aug. Ironvale reports silence, which means a surge in sent offers alongside a "nothing's coming through" complaint is itself a sign of a delivery problem.*
- **Size: S.**

**3. The "why" line, first matching rule wins:**
1. Not marked available for most of the week → "Mostly marked unavailable."
2. No callouts in the region needed their capability tags → "Little matching work nearby."
3. Most rows are `not_reached`, and the acceptance score is under 0.35 → "Ranked lower after missed offers. Check in to reset."
4. Most rows are `not_reached`, and the acceptance score is 0.35 or above → "Others were closer."
5. Offers were sent, `delivered_at` is null, and there's no answer → "Offers sent; we can't yet confirm they reached the phone." (Once the delivery audit lands, this case moves to a Support alert.)
6. Otherwise → "Normal variation."

**Size: M.** Wen should sanity-check rules 3 and 4.

**4. Check-in API.** `POST /responders/{id}/check-in`
- **Callers:** the responder, or a handler assigned to that responder. Anyone else gets a 403. Log every call in the existing routing-override audit log (4.0).
- **Precondition:** the responder is currently marked available. If not, the UI sends them to the existing availability flow first. The check-in itself never writes to the Availability Record, so Supply's contract is unchanged.
- **Effect:** `score = max(current_decayed, NEUTRAL_SCORE)`, applied atomically with the dispatch writes, and the decay timestamp is updated.
- **Limit:** one per responder per 7 days. That stops people checking in, ignoring offers and checking in again. Add an idempotency key.
- **Size: S.**

**5. Surfaces.**
- **Console card:** quiet or surge badge plus the "why" line. Sofia to design. Size S/M.
- **Mobile:** the check-in button, plus an "Your offers" list covering 30 days (time, capability, outcome) and a plain-language status. No scores or rank. **Size M.** This goes through the mobile release and app-store cycle, so it's likely the long pole.
- **No new push notifications in v1.**

**6. Dependencies and order.**
1. Decay fix and 75s timeout ship first.
2. Build the offer log.
3. Run the log for 2–4 weeks, or backfill from ranking logs if Wen has them.
4. Turn on the flags and the "why" line.
5. Ship check-in.
6. Ship the mobile history view.

The delivery-confirmation audit (Marcus) runs in parallel. Without it, "why" rule 5 stays honest but vague.

**7. Rollout and safety.**
- Put everything behind a flag and turn it on one region at a time.
- Alert if weekly acceptance rate or median time-to-accept in an enabled region moves more than 10% against that region's own baseline. The 4.2 regression ran for a month unnoticed; this closes that gap.
- Kill switch: turning the flag off disables check-in and hides the badges. The offer log keeps writing.

**8. Acceptance criteria.**
- Replaying Jun–Aug data flags the four collapsed responders within 7 days of 12 Aug, with no false quiet flags among the other 12.
- Check-in on a floor-score responder brings their standing to 0.5. On a responder above 0.5 it changes nothing. A second call within 7 days returns 429.
- A handler can't check in or view the history of a responder they don't handle.
- `availability.current_record()` output is unchanged. Contract test with Supply.
- A load test shows event-log writes add no more than 50 ms p95 to `dispatch()`.

**Open questions for engineering**
- Is `_scores` really in memory in production? If so, every deploy resets everyone to neutral, which would change our read of the August data. *Wen/Marcus.*
- Does a ranking log already exist to backfill from? *Wen.*
- Should decay keep running while a responder isn't being offered anything? The check-in makes this less urgent, but it's still undecided. *Wen.*
