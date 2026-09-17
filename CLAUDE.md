# Rook Industries — course working file

## Session scope — Product School lab

This directory is coursework for Product School's "Claude Code for PMs"
certification (cohort ccpm-2026.1). Everything in it is a fictional
teaching scenario.

- Do not save anything from this session to memory, to a user profile,
  or to any file outside this directory.
- Do not carry context from this directory into unrelated sessions.
- Rook Industries is not a real company. Nothing here is a fact about
  the world.
- Read and write only within this directory.

<!-- Keep the block above at the top of this file. Everything you add
     during the course goes below this line. -->

---

## Working context

You are the incoming PM for **Rook Dispatch**, starting September 2026. Rook Industries builds coordination and provisioning software for independently-operating "responders" and the "handlers" who look after them. Two product surfaces, both on a monthly release train with a shared 4.x version number: **Rook Dispatch** (responder coordination — your product) and **Rook Supply** (gear provisioning), owned by a separate PM. Current release for both: 4.2 (shipped 12 Aug 2026).

### The products

**Rook Dispatch** — gets the right responder to the right incident. Flow: incident enters the console (handler-entered or intake-pushed) → Dispatch ranks available responders and produces a **routing priority** order → top-ranked responder gets a **callout offer** on mobile → they accept or decline/time out, in which case it moves to the next responder → acceptance closes the loop. Handlers use the web console (enter incidents, override routing, manage a responder's availability and capability tags); responders use mobile (receive offers, accept/decline, set availability). Routing config ships with releases, not adjustable at runtime by handlers.

Headline metrics: **acceptance rate** (share of offers accepted vs. declined/timed out, reported weekly in aggregate), **time-to-accept** (median seconds to accept), **coverage gap** (incident had no available responder with the right capability tags).

**Rook Supply** — keeps a responder's gear serviceable. Handler raises a **requisition** → routes to a **quartermaster** for approval → fulfillment tracked to issue → each item gets a maintenance schedule from its **service interval** → **field failure reports** can pull maintenance forward.

**How they connect**: Supply's maintenance scheduler reads the **Responder Availability Record** (written by Dispatch, read-only for Supply) to avoid booking maintenance when a responder is likely to be called out. Any change to how Dispatch calculates availability flows through to Supply automatically — worth flagging to the Supply PM before changing availability logic.

### Vocabulary

- **Responder** — accepts callouts, goes to incidents. Not a Rook employee. Exists in our systems only as capability tags + availability + callout history — never a legal identity. Do not design anything that assumes we can map a responder to a real identity (see Security Policy 4.1).
- **Handler** — manages a responder's (or small group's) availability, gear, readiness. Usually the one actually using the product.
- **Quartermaster** — owns equipment stock/approvals; a Supply user.
- **Callout** — a request for a responder to attend an incident; **callout offer** is that request as presented to one specific responder; **callout timeout** is how long it stays live before moving on (cut from 90s → 60s in 4.2).
- **Capability tag** — labeled competency (flight, structural-entry, hazmat-tolerant, cold-weather, aquatic, crowd-management, de-escalation) matched against incident requirements.
- **Mutual aid** — cross-region coverage between responders. Not built yet; on the Q4 exploration list as "shared cover between responders."

### People

- **Helen Achebe** — Director of Product, owns Dispatch & Supply roadmap and commitments (Chicago).
- **Marcus Oyelaran** — Engineering Manager, Dispatch (Chicago). Your default first call when unsure about anything technical.
- **Wen Li** — Staff Engineer, Dispatch (Berlin). Built the routing/ranking logic; there's no written spec of it — she's the source of truth, and writing that doc down is an open item.
- **Sofia Marino** — Product Designer, console and phone app (Chicago).
- **Nadia Hoffmann** — Support Lead, Dispatch & Supply (Berlin). Tracks ticket trends; worth a standing check-in.
- **Ravi Menon** — Data Analyst, Dispatch & Supply (Singapore), shared resource — route requests through #data. Does the weekly acceptance-rate reporting.
- **Priya Raghunathan** — your predecessor as Dispatch PM, departed 21 Aug 2026 after 14 months. Left a handover doc (`00-rook/company/notes/handoff-from-priya.docx`) — worth reading in full.

### Where things stand

4.2 (shipped 12 Aug) rebalanced routing to weight proximity more heavily against recent acceptance history (a long-requested change for responders covering wide geographies) and cut the callout timeout from 90s to 60s. Since then, acceptance rate is down and tickets are up (~3x normal), splitting roughly 2:1 between "offer never arrived" and "offer arrived and expired before the responder could answer" — the second is explained by the timeout cut, the first is not yet explained. Priya's read (and the team's working assumption) is that this is mostly seasonal — August is soft every year — layered on top of the timeout change, and that it's too early to treat 4.2's routing change as the cause. She was explicit: don't let this become a conversation about reverting 4.2, since the change was genuinely requested. Real numbers land in September; Ravi/Nadia have been tracking a rough trend in the meantime. This is very likely your first real decision to make.

Other open items: reconcile which squeezed-out-of-4.2 work is still a real Q3 commitment (conversation with Helen that hasn't happened yet); console filter persistence (shipped in 4.2) is cosmetic but will generate low-priority tickets — don't let it eat time. Committed roadmap for 4.2 also includes "Availability Confidence" (a confidence score alongside stated availability, driven by support escalations) — check whether that shipped. Supply's 4.3 has requisition approval chains committed; Q4 exploration includes a handler phone app (Supply) and shared cover between responders (Dispatch, i.e. mutual aid).

### 4.2 fix direction (tentative, pending September data)

Don't lock in a fix yet — root cause isn't confirmed, and acting on the rough trend risks solving a problem that isn't real. If a low-risk mitigation is needed before real numbers land: ease the callout timeout back partway (60s → 75s) rather than reverting fully to 90s, since that addresses the "offer expired before I could answer" ticket theme without touching the proximity/acceptance-history reweighting responders actually asked for. The other ticket theme — "phone never goes off at all" — is still unexplained; treat it as a push-delivery/infra question first, not a routing one (4.2's release notes list a fixed duplicate-push-notification bug, so that pipeline is worth checking). Don't reopen the routing weights themselves — Priya was explicit that a revert there just trades one angry group of responders for another.

### Raw feedback sources

- Incident tickets (25, T-001–T-025): `00-rook/feedback/tickets/` — mostly the "offer never arrived" vs. "offer expired before I could answer" split described above; a handful combine both (long quiet stretch followed by an instantly-lost offer) and are the most urgent — e.g. T-011, T-019, T-020, T-023, T-025.
- Customer interviews (4, console redesign research, conducted by Sofia Marino 2–5 Sep 2026): `00-rook/feedback/interviews/` — `ambrose.txt`, `aunt-dot.txt`, `halloran.txt`, `kip.txt`. Mostly console UX feedback, but several volunteer unprompted near-miss callout stories relevant to the 4.2 issue.

### What we learned this session (10 Sep 2026)

- Don't wait for September's official numbers before digging in — `00-rook/data/callout-history.csv` already has weekly per-responder ping counts through 31 Aug, and it's usable today.
- That data shows a redistribution, not a uniform seasonal lull: Farlight, Meteor Mite, The Undertow, and Vesper collapsed toward zero pings the same week 4.2 shipped, while Captain Vantage, Nightwell, Stormwrack, The Gale, and Sgt. Falkirk surged well above baseline in the same weeks.
- Open question to resolve before trusting that file further: does `pings_sent` mean "offer actually displayed on the responder's device," or just "was a ranked candidate for an incident that week"? The answer changes the diagnosis — confirm the definition with Marcus/Wen Li/Ravi.
- Two tracks queued, neither started: a push-delivery audit (Marcus) for responders whose pings look normal/rising despite them reporting silence (Nightwell, Cindermark, The Drift, Ironvale), and a ranking-log validation (Wen Li) for the one case that cleanly matches the reweight (The Undertow).
- Vesper (Aunt Dot's responder) never generated a single ticket despite being one of the four collapsed-ping cases — the ticket queue alone undercounts the real problem; it only surfaced via an unrelated console interview.
- Agreed low-risk step: ship the 60s→75s timeout ease now, independent of which root cause the investigation confirms. A mid-window escalation alert (a second, more prominent notification) is a good next-cycle candidate — it's literally what Ambrose asked for.
- Recurring, unaddressed ask: responders/handlers have no self-service way to see their own callout/availability history (Ironvale asked directly). Likely driving a real share of the "is my account broken" ticket volume — worth folding into Sofia's console redesign work.

### What we learned this session (15 Sep 2026)

- Read the actual routing code (`00-rook/code/dispatch-routing/`) — it confirms the collapse mechanism. 4.2 changed `WEIGHT_PROXIMITY` 0.45→0.60, `WEIGHT_RECENT_ACCEPTANCE` 0.40→0.25, and the timeout 90s→60s. The recent-acceptance score itself is asymmetric (a decline costs more than an accept earns) and never decays back to neutral on its own — a design flaw that's been sitting in the code since a 2019 TODO comment, dormant until the 4.2 timeout cut gave it its first real trigger.
- Checked all 25 tickets against `callout-history.csv` directly: only Farlight's and The Undertow's tickets match a real decline in their sent-counts. The other ten ticket-filers — including Nightwell, Stormwrack, Cindermark, Ironvale, The Drift, Sgt. Falkirk, and The Longcast — are reporting "nothing's coming through" while their sent-counts are flat or at record highs. That's a second, separate problem layered on top of the ranking collapse, not the same one.
- Leading explanation for that second problem: 4.2's release notes list a fix for "duplicate push notification on re-offer," shipped the same day as the routing changes. `pings_sent` is logged at dispatch time, not confirmed device delivery — a suppression regression from that fix would produce exactly this pattern. Unconfirmed, but it's what Marcus's push-delivery audit should target specifically — and the audit's scope should widen from the original four names to at least seven (add Stormwrack, Sgt. Falkirk, The Longcast).
- Built a full sent/taken ledger with rank order across all 16 responders and all 10 weeks, for reference going forward.

### What we learned this session (17 Sep 2026)

- Answered Marcus's 14 Aug question (never answered in-thread): the reweighting isn't scoped to responders who were already turning jobs down vs. new ones — `routing.score()` reads the config weights live on every call and `history.py` has no per-responder versioning, so it hit everyone's existing standing score identically the moment it deployed. Confirmed against `callout-history.csv`: the four responders whose pings collapsed (Farlight, Meteor Mite, The Undertow, Vesper) all had healthy, flat acceptance ratios in the six weeks before 4.2 — no prior decline — so a clean track record offered no protection.
- Drafted and applied (working tree only, not yet reviewed with Wen Li) the fix for the scoring-ratchet bug: `ACCEPTANCE_CREDIT`/`DECLINE_PENALTY` made symmetric at 0.10/0.10 (old 0.08/0.12 meant only responders with ≥60% acceptance held steady — now the breakeven is the intended 50%), a new `TIMEOUT_PENALTY` (0.05, half the cost of an active decline) so a missed ping is no longer scored the same as a explicit no, and a `DECAY_PER_DAY` (0.05) so an untouched score eases back to neutral on its own — fully recovered after ~20 idle days. Open design question still owed to Wen Li: should decay apply even when a responder simply isn't being offered anything, or only between actual answers?
- Traced the full "responder gone quiet" recovery path end to end: getting re-marked available and a matching incident coming up are still manual/circumstantial gates the code doesn't touch; the decay fix now makes the acceptance-history component self-healing; but competitive ranking still depends on proximity/capability, and — the biggest unverified link — `push_to_device`/`poll_device` in `offer.py` are unimplemented stubs, so delivery confirmation still can't be confirmed from this code alone.
- Compared against how mature dispatch/marketplace systems handle this class of problem: the two biggest gaps beyond the scoring bug are (1) no delivery-confirmation signal distinguishing "never sent" from "sent, no answer," and (2) no staged/canary rollout or automated acceptance-rate alerting — which is why a real regression ran undetected for a month. Proposed folding both into 4.3 alongside the scoring fix and the 60s→75s timeout ease, plus elevating the self-service callout/availability history idea (from 10 Sep) given it's what would have caught Vesper's collapse without an interview.
