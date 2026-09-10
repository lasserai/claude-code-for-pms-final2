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
