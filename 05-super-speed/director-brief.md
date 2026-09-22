# Quiet responders: what we'd build, and what I need from you

**To:** Helen Achebe · **From:** Dispatch PM · **22 Sep 2026** · reply to your note this morning

## Bottom line

The small code fix is real, and we should ship it. But it only stops the damage; it doesn't fix the experience. What I'm proposing is a way back from quiet that people can see and use: handlers are told when a responder has gone quiet and why, and responders get one button to say "I'm back." It doesn't change the 4.2 routing change that gave distance more weight, and it doesn't add a routing setting. I need five decisions from you, listed at the bottom.

## What's happening, in one paragraph

A missed offer lowers a responder's standing. The only way to raise it again is to answer another offer, and low standing means they stop getting offers. 4.2's shorter timeout triggered this for the first time at scale. Meteor Mite went from about 11 offers a week to 1, while Kip's other responder, The Gale, went from 13 to 21 in the same city. Vesper collapsed the same way and never filed a ticket. Wen's 2019 note asked whether it should work like this. It shouldn't.

## Why this can't wait for September's numbers

- **Our headline number will soon look fine while four responders are still stuck at zero.** Overall acceptance fell from 77% to 54% the week 4.2 shipped, and it's already back to 73% by 31 Aug. September's report will probably show recovery. Meanwhile Farlight, Meteor Mite, The Undertow and Vesper are at 0 or 1 offers a week. If we only watch the headline number, we'll call this solved.
- **It isn't just a slow August.** Total offers held steady at 158–177 a week. The work didn't dry up; it moved from four responders to others.
- **It's a revenue risk.** We price per active responder. Four of 16 responders in our data (25%) are effectively switched off, and a responder who gets no work has little reason to keep paying.
- **Our tickets don't show all of it.** Vesper never filed one; we found out through a design interview.

## What we'd build

**For the handler (Kip):**
- The console card flags a responder whose offers drop far below *their own* usual level ("Meteor Mite: 1 offer last week, usually ~11"), plus one plain-language reason.
- If we don't know the reason, the card says so.
- Kip finds out before Mite has to text him.

**For the responder who's gone quiet:**
- An **"I'm back — send me work"** check-in (the handler can also do it on their behalf) that restores their standing right away.
- A simple list of their own recent offers.

Silence becomes something they can see and act on, instead of feeling forgotten.

**Checked against real data:** the "gone quiet" rule flags exactly the four collapsed responders within a week of 4.2, and nobody else.

## What it deliberately doesn't do

- Doesn't revert the 4.2 distance change, and doesn't let handlers adjust routing.
- Doesn't show scores or rank.
- Doesn't promise anyone a volume of work: closest capable responder still wins. A check-in is worth about the same as being 9 minutes closer to the incident.
- Doesn't touch the availability data Supply relies on. I'll still brief the Supply PM.
- Doesn't fix "my phone never goes off." That's a separate delivery problem. Marcus's audit covers it, and it affects different people (Nightwell, Ironvale and others whose offers *went up*).

## Plan

| Step | What | Release |
|---|---|---|
| 1 · Stop the damage | Standing fades back to neutral on its own. Missed offers cost less than a decline. Timeout eased from 60s to 75s. **With a note to handlers saying what changed and why**, not a quiet number change. | 4.3 |
| 2 · Start recording | Log every offer, including the people who were ranked but never reached. Nothing visible yet. Needs 2–4 weeks of data. | 4.3 |
| 3 · Show it | Console flag with a reason, plus the check-in. Turned on one region at a time, with an alert if acceptance rate or time-to-accept gets worse. | 4.4 |
| 4 · Responder view | Offer history on mobile. Longest lead time, because it goes through app-store review. | 4.4–4.5 |

The push-delivery audit runs in parallel with all of this.

## Risks

- **Offers could flow to people farther away.** A check-in pulls work toward the quiet responder. This is limited to once every 7 days and watched by the per-region alert.
- **We may not be able to say why for a while.** Until delivery is confirmed, some cards will honestly say "can't confirm the offer reached the phone." That's better than guessing.
- **Our read of August may be off.** Engineering needs to confirm whether standing is reset on every deploy. If it is, our August analysis shifts.

## Decisions I need from you

1. **Approve step 1 for 4.3**, shipped openly with a handler note. The fix is drafted in our working copy and hasn't been deployed; it needs Wen's review first.
2. **Fold "Availability Confidence" into this.** It was a committed 4.2 item, driven by support escalations, and didn't ship. The check-in is essentially that signal, coming from the responder.
3. **Hold the Q3 commitments conversation this week.** Priya flagged it as overdue, and this work affects what fits in 4.3 and 4.4.
4. **Make region-by-region rollout with acceptance-rate alerts standard for routing changes**, not just this one. It's why 4.2 ran for a month unnoticed.
5. **Add a second headline metric: "responders gone quiet."** That's the weekly count of responders under 40% of their own usual offers. Ravi would report it next to acceptance rate, so an overall average can't hide a few people at zero again.

## This week, before anything ships

- **Nadia, or I, contact the four affected handlers directly:** Linda Pruitt (Farlight), Kip (Meteor Mite), Desmond Okafor (The Undertow) and Aunt Dot (Vesper). Tell them it's our issue, not their responder's, and what's coming.
- **Nadia gets a support script** for "is my account broken?" that gives the honest answer.
- **I brief the Supply PM** that step 1 changes nothing in the availability record they read.

---

# Page 2 — The product case

## How we'll know it worked

| Measure | Now | Target (8 weeks after step 3) |
|---|---|---|
| Responders gone quiet (new metric) | 4 of 16 | 0 stuck for more than 2 weeks |
| Time from going quiet → next accepted callout | Never, in practice (the loop doesn't close) | Median ≤ 7 days after a check-in |
| Quiet responders flagged *before* a ticket or text reaches us | ~0 (we found Vesper by accident) | ≥ 80% |
| "Is my account broken / nothing's coming through" tickets | ~3× normal | Back to normal, *once the delivery fix also lands* |

**Guardrails.** None of these may get worse by more than 10% in any enabled region:
- overall acceptance rate
- median time-to-accept
- coverage gaps

**Also watch the busiest responders' load.** The Gale went from 13 to 21 offers a week, and fairness cuts both ways.

**When we'd stop and rethink:**
- if check-ins don't lead to accepted callouts within 2 weeks for most responders, or
- if a guardrail breaks in two regions.

## What we'd need to be true, and how we'll check before building

| Assumption | How we check | When |
|---|---|---|
| Handlers will act on a flag, not tune it out | Sofia runs a clickable mock with Kip, Aunt Dot and one large-roster handler (flag noise at scale) | During step 2, before step 3 is built |
| Quiet responders will check in rather than churn | Offer the check-in by hand via Support to the four affected, and watch what they do | This month |
| The reason we show matches reality | Compare it against Wen's reading of the ranking logs for The Undertow | Step 2 |
| One check-in a week isn't gamed | Watch check-in → decline patterns in the first region | Step 3 |

## Options we considered

| Option | Why not |
|---|---|
| Revert 4.2 | Trades one angry group, wide-territory responders, for another. The flaw that stops quiet responders recovering predates 4.2. |
| Ship only the code fix | Recovery takes about 3 invisible weeks. Nobody is told, and Kip still has nothing to say to Mite. |
| Quotas or rotation ("everyone gets N offers") | Sends callouts to farther-away responders on purpose, which slows response. That's a policy change, not a fix. |
| Let handlers adjust routing | Breaks the rule that routing ships with releases. It also turns a system flaw into a handler workload. |
| Notify quiet responders automatically | Tells them about the problem but gives them nothing to do about it. The check-in both tells and resolves. |

## What this costs, and what it moves

- **Engineering:** roughly 2–3 sprints of Dispatch capacity across 4.3–4.4, mostly the offer log and the mobile work. Marcus needs to confirm.
- **Design:** Sofia's console redesign, where the card state lands. Kip's dark-mode request rides along; it isn't in scope, but the same screen is being redesigned.
- **Likely displaced:** some of the work squeezed out of 4.2, until we have the Q3 conversation. This should also inform Q4 "shared cover between responders": the offer log is the data that work would need.

## Deliberately left for later

- **Protecting overloaded responders (The Gale side).** v1 flags it; it doesn't act on it.
- **Different alert sounds per responder** (Kip's ask). It's real, but separate.

## Who needs to hear what

| Who | What | When |
|---|---|---|
| Affected handlers (4) | Personal note: what happened, what's coming | This week |
| All handlers | Release note on step 1, in plain words | 4.3 release morning |
| Support (Nadia) | Script plus how to read the new flag | Before each step ships |
| Supply PM | No change to the availability record, confirmed by contract test | Before 4.3 |
| Data (Ravi, via #data) | New metric definition. Also, what `pings_sent` actually counts | Now |

*Detail for engineering is on page 2 of `quiet-responder-brief.md`. A clickable mock of Kip's cards and the check-in can follow if useful.*
