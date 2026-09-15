# 03 · Rewind — prompts

**Context:** You joined Rook two weeks ago as PM on Dispatch.
Release 4.2 shipped on 12 August, just before you arrived, and
landed badly.

Last session you read four conversations and every support ticket
since 4.2 — and found the two piles did not agree.

At the end of the session, ask Claude Code to save the prompts you
wrote yourself below — not the starter prompt. The closing slide has
the exact prompt to paste. By Module 6 this file is a prompt library
built from your own questions.

---

### 1.

```
please find the callout history somewhere in my data.

```

### 2.

```
Open 00-rook/data/callout-history.csv. Every row is one responder in one week: how many times we pinged them, and how many of those they took. Release 4.2 shipped on 12 August. Tell me what changed after that date. Show me the weekly numbers before and after, and show me the rows you used to get them.

```

### 3.

Tell the root-causes for the groups that collapsed toward zero and another group well above baseline.  What are the commanalities in those groups that explains them. How to these groups separate from each other?

### 4.

Check one Farlight's pings week by week. Explain what goes wrong?

### 5.

What is a ping?

### 6.

Can you figure it out from the ping numbers which are  incidents and which are offers?

### 7.

What does ping taken mean? Why there is difference between pings send and taken?

### 8.

```
Compare the tickets in 00-rook/feedback/tickets/ against this data file. Do they agree with each other? When did people start writing in, and when do the numbers actually move?
```

### 9.

What is the root-cause problem behind the data does not support the perception?

### 10.

Tell me in plain language in one paragraph what are the business problems worth solving here? We need better sales and better customer satisfaction. Tell the resolutions for that.

### 11.

Was the problem there before 4.2 release, what are the particular bugs related to 4.2.

### 12.

Tell a story what happened to Farlight after 4.2 release? Why it happened?

### 13.

Tell a story in plain English one paragraph

### 14.

How the report is calculated?

### 15.

Is there possibility external factors causing the low acceptance? Like a holiday? How to prove it?

### 16.

Tell the figures by week, each customer how many offers send and how many accepted. Make a rank order.

### 17.

What is the story to tell to Product Director about these tables?

### 18.

```
Before we wrap up, three things. First: look back through this session and find the prompts I wrote myself, not the starter I pasted. Save them into 03-rewind/prompts.md, one per numbered slot, exactly as I typed them. Don't tidy them up. Second: add a few lines to the Working context in CLAUDE.md, anything we figured out today that isn't in there yet and that I'd want you to already know next session. Third: commit everything that's changed with a short message describing what this session did, then push. Tell me when it's done and give me the link to my repository on GitHub.
```
