---
name: review-checklist
description: Review a brief, spec, one-pager or proposal against the user's six standing checks before it goes any further — who decides and who does (with deadlines), how we'll know it worked (with defined metrics), scope consistent start to end, problem before fix, numbers that trace and agree, and guesses labelled as guesses. Use when the user says "review this brief", "run the review checklist", "/review-checklist <file>", or asks whether a brief is ready to send.
---

# Review checklist

Run the same six checks on a brief, every time, and report them the same way. These are the user's own checks. Don't add new ones, drop any, or soften them. For engineering handoff readiness, use the separate `eng-readiness` skill instead.

## Input

- The brief is whatever file path or pasted text comes with the request.
- If nothing is given, ask which brief to review. Don't guess. You can list candidate `.md` / `.docx` files in the working directory to help them choose.
- Read the **whole** document before judging. Checks 3 and 5 depend on how parts of it relate to each other.

## The six checks

For each check, give **Pass**, **Partial** or **Fail**. Quote the exact words that decide it, with the section heading or line number. If you can't point to text, it isn't there: that's a Fail, not a Pass by implication.

### 1. It names who owns it: who decides, who does, by when
- **Pass:** all three hold.
  - One named person is the **decider** for each decision the brief asks for.
  - A named person is the **doer** for each piece of work.
  - Every ask to the decider has a **by-when**: a date, a release, or a meeting.
- **Partial:** any of these:
  - doers are named but the decider isn't clear
  - an owner is shared ("X or Y") or is a team ("engineering", "we")
  - asks have no deadline
- **Fail:** no owner named anywhere.
- Also flag any owner marked "TBD" or "to confirm", and any open question or action with no owner.

### 2. It says how we'll know it worked, with metrics defined
- **Pass:** at least one outcome has all five of:
  - a current value, or a plan to get one
  - a target
  - a time frame or checkpoint
  - **who measures it**
  - **what exactly it counts** (a definition, or a pointer to one)
- **Partial:** any of these:
  - outcomes are named but can't be measured, like "tickets should fall"
  - there's no baseline, target or timing
  - a metric's owner or definition is missing, or the brief itself says the definition is unconfirmed
- **Fail:** no success measure at all.

### 3. The scope at the end matches the scope at the start
- Write one line for what the opening (summary, bottom line, problem framing) says is in scope.
- Write one line for what the ending (plan, decisions, asks, next steps, spec) actually commits to.
- **Pass:** the two match. Nothing is quietly added, dropped, or grown.
- **Partial:** there's small drift. For example, an extra item appears late without being flagged, or a promised item is thinner by the end.
- **Fail:** the end commits to something materially different, bigger or smaller, than the start said.
- List each specific item that appears at one end but not the other. Also catch contradictions, such as an item listed as "not doing" that later shows up in the plan.

### 4. It explains the problem before it proposes a fix
- **Pass:** the problem (who it hurts, what's happening, why it matters) is stated *before* the first proposed solution. It stands on its own, so a reader could agree it's a problem without accepting the fix.
- **Partial:** the problem is there but comes after the solution, is tangled up with it, or is only described as "the lack of <our solution>".
- **Fail:** the brief goes straight to the solution.
- Quote the first sentence that states the problem and the first sentence that proposes a fix, with where each one appears.

### 5. Numbers trace and agree
Collect every number that carries the argument: counts, percentages, ratios, dates, durations, sizes, and claims like "twice as many".

For each one:
- **Traces:** it names or clearly implies its source, whether a data file, report, or person.
- **Recalculates:** if the source is a file in the working directory, recompute the figure. Check arithmetic (sums, ratios, percentages) even when there's no file.
- **Agrees:** the same fact has the same value everywhere it appears in the document, including headings and summaries ("one page" versus the actual length).

Rating:
- **Pass:** all key numbers trace, recalculate, and agree.
- **Partial:** a minor number is off or untraced, or a figure is fine but described loosely ("twice" for 1.5×).
- **Fail:** a number the argument depends on is wrong, contradicts itself, or has no source.

List every mismatch as *stated → actual (source)*.

### 6. Guesses are labelled as guesses
- Find every estimate, target, forecast, assumption, and effort size.
- **Pass:** each one is marked as unconfirmed ("estimate", "assumption", "to confirm", "starting point") **and** names who will confirm it.
- **Partial:** it's labelled but nobody is named to confirm it, or some guesses are labelled and others aren't.
- **Fail:** guesses are presented as facts.
- Watch especially for a headline number that rests on an unconfirmed assumption without saying so near the number itself.

## Output format

Always use this layout, and keep it short:

```
## Review: <document name>

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Who decides, who does, by when | Pass/Partial/Fail | "<quote>" (<section/line>) |
| 2 | How we'll know it worked | … | … |
| 3 | Scope end matches start | … | … |
| 4 | Problem before fix | … | … |
| 5 | Numbers trace and agree | … | … |
| 6 | Guesses labelled | … | … |

**Verdict:** Ready to send · Fix first · Not ready
```

The verdict follows from the ratings:
- **Ready to send:** all six Pass.
- **Fix first:** any Partial and no Fail.
- **Not ready:** any Fail.

Then, **only for checks that aren't a Pass**, list what to fix: one line each, specific enough to act on. For example, "Line 93: 'about twice usual' → 'about 1.5× usual' (21 vs ~14)", not "check numbers".

## Rules

- **Don't edit the brief.** Only offer to apply the fixes once the review is done, and only change the file if the user says yes.
- **Judge what's written, not what the author probably meant.**
- **Keep other feedback out of the table.** If you notice something serious that isn't one of the six checks, add at most one line after the fixes under **"Outside the checklist:"**. Otherwise say nothing.
- **Reviewing several briefs** means one table per brief, then a single line comparing the verdicts.
