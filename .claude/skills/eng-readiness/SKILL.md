---
name: eng-readiness
description: Check whether a brief or spec is ready to hand to engineering — testable acceptance criteria, dependencies and data contracts, privacy and security, rollout and kill switch, owned open questions, engineer-confirmed estimates, and claims that match the actual code. Use when the user says "is this ready for engineering", "eng readiness", "/eng-readiness <file>", or before sending a spec to an engineering manager or staff engineer. For the general pre-send check, use review-checklist instead.
---

# Engineering readiness

Answer one question: **could an engineer start building from this without coming back to ask?** Run the same seven checks every time and report them the same way.

## Input

- Take the brief or spec from the file path or pasted text that comes with the request. If nothing is given, ask which document to check.
- Read the whole document.
- If the document names code, config, data files or APIs that exist in the working directory, **open them**. Check 7 depends on comparing the document with the code. If the code isn't available, say so, and rate check 7 on the document alone.

## The seven checks

For each check, give **Pass**, **Partial** or **Fail**, with a quote and its location. If you can't point to text, it isn't there.

### 1. Acceptance criteria are testable
- **Pass:** each thing to be built has criteria an engineer could turn into a test. That means specific inputs, expected outputs, and thresholds like "returns 429 on second call within 7 days" or "p95 ≤ 50 ms".
- **Partial:** there are criteria, but some are vague ("works well", "is fast") or cover only part of what's being built.
- **Fail:** there are no acceptance criteria.

### 2. Behaviour is specified, including edge cases
- **Pass:** the rules are exact. That covers thresholds, windows, the order in which rules apply, who can call what, and rate limits. Edge cases are listed with the expected behaviour: new or empty records, boundaries, repeats and idempotency, concurrency, restarts.
- **Partial:** the main path is exact but the edge cases are missing, or a rule leaves an obvious choice open, such as "reset after a week" without saying whether that's calendar days or rolling hours.
- **Fail:** the behaviour is described only as intent.

### 3. Dependencies and data contracts are named
- **Pass:** it names every system, team, data source, schema or shared record the work reads or changes. For each shared record, it says whether the contract changes and how that's verified, for example with a contract test. It also names the order the work depends on (what must ship first).
- **Partial:** some dependencies are named but their contracts or order aren't.
- **Fail:** there are dependencies, such as shared data, another team's service or a mobile release, that go unmentioned.

### 4. Data, privacy and security are covered
- **Pass:** it covers:
  - new data stored: the fields, where they're kept, and how long
  - who can see or change it, with permission checks
  - audit logging of actions
  - compliance with any stated policy
- **Partial:** new data is described but retention, access or audit is missing.
- **Fail:** the work stores or exposes new data and none of this is covered.

### 5. Rollout, monitoring and rollback are defined
- **Pass:** it covers:
  - how it's released: a flag, staged by region or percentage, or all at once, and why
  - what's monitored, and which threshold triggers an alert
  - how it's switched off, and what the off switch leaves running
- **Partial:** there's a flag or staging but no alert threshold, or no off switch.
- **Fail:** there's no rollout plan.

### 6. Open questions are owned, and estimates come from engineering
- **Pass:** every open question has one named owner and blocks a clearly stated step. Effort sizes are marked as confirmed by the engineering owner, or explicitly marked "PM estimate, <name> to confirm".
- **Partial:** some questions have no owner, or sizes are given with no indication of who produced them.
- **Fail:** there are open questions with no owners, or PM guesses presented as engineering commitments.

### 7. Claims match the code
- List every statement the document makes about how the current system works: names, values, behaviour, and what exists or doesn't.
- Check each one against the code or config in the working directory.
- **Pass:** all claims match.
- **Partial:** there's a minor mismatch, like a renamed field or an out-of-date value that doesn't change the design.
- **Fail:** the design rests on a claim the code contradicts, or on something the code shows is only a stub or doesn't exist.
- List each mismatch as *document says → code says (file:line)*.

## Output format

```
## Engineering readiness: <document name>

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Testable acceptance criteria | Pass/Partial/Fail | "<quote>" (<section/line>) |
| 2 | Behaviour and edge cases | … | … |
| 3 | Dependencies and contracts | … | … |
| 4 | Data, privacy, security | … | … |
| 5 | Rollout, monitoring, rollback | … | … |
| 6 | Owned questions, real estimates | … | … |
| 7 | Claims match the code | … | … |

**Verdict:** Ready for engineering · Ready with questions · Not ready
```

The verdict follows from the ratings:
- **Ready for engineering:** all seven Pass.
- **Ready with questions:** any Partial and no Fail. Engineering can start, but the listed gaps travel with the handoff.
- **Not ready:** any Fail.

Then, **only for checks that aren't a Pass**, list what to add, one line each, specific enough to act on. Finish with **"Questions to take to engineering:"**, at most five, each with the person to ask if the document names them.

## Rules

- **Don't edit the document or the code.** Offer the fixes, and change a file only if the user says yes.
- **Don't design the solution.** Point out what's missing, not what the answer should be. The exception is when the code makes the answer factual; then state it and cite the file.
- **Leave product questions to `review-checklist`.** Whether the problem is worth solving, and whether success metrics exist, belong there, not here.
