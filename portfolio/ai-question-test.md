# AI question test: method and results

## Method

- **Corpus:** the Markdown export of every page (`<page>.md` from `mint dev`), the 13 generated API endpoint pages, and `skill.md`. That's 44 files. These are the same files an AI tool gets through the MCP server, `.md` URLs, or `llms-full.txt`.
- **Answering model:** a separate Claude Sonnet agent with no memory of writing the docs. It was allowed to search and read only those files, the way an MCP docs-search tool works. Hookferry is fictional, so the model had no prior knowledge to fall back on, and anything not in the docs would be invented.
- **Rules given to the model:** cite the source files, give a confidence level, and say "not documented" instead of guessing.
- **Grading:** each answer was compared with the facts in the source of truth (`openapi.yaml` and the concept pages), and graded as **Correct**, **Correct but fragile** (right answer, but only through inference a weaker tool could miss), or **Wrong**.

## Round 1: 10 questions

| # | Question | Grade | Notes |
| :-- | :-- | :-- | :-- |
| 1 | My Express handler returns 401 for every event, even ones I send with curl. What's wrong? | Correct | Found the `express.json()` raw-body cause first. The symptom-first troubleshooting heading matched the question. |
| 2 | I stopped `hookferry listen` overnight. Will the missed webhooks show up? | Correct | Status `undelivered`, not retried, replay after restarting listen. Five pages agreed. |
| 3 | How many retries if my HTTPS endpoint is down, and over how long? | Correct but fragile | Right numbers, but the agent flagged inconsistent wording: "8 attempts" vs "retries", and "22 hours" vs "22 h 36 min" vs "22.6 hours". |
| 4 | Exact command: source `stripe-dev`, port 8080, path `/hooks`, only `invoice.*` events | Correct but fragile | The command was correct, but no page combined the flags with `$prefix`, so the agent had to assemble it from two pages. |
| 5 | How do I use Hookferry in GitHub Actions without `hookferry login`? | Correct | The agent also flagged a race condition (`sleep 3`) in the sample workflow. |
| 6 | On the Free plan, can I replay an event from 10 days ago? | Correct | No: 3-day retention, `410 event_expired`. |
| 7 | My app runs in Docker and listen says "connection refused". | Correct | |
| 8 | What happens at the API rate limit, and how should my code handle it? | Correct | The agent noted that the docs didn't say whether the window is fixed or sliding. |
| 9 | How do I delete a source using the CLI? | Correct but fragile | Said no CLI command was documented and pointed to the API. It reached this only because a command was missing. No page said source deletion was API-only, so a less careful tool could invent `hookferry sources delete`. |
| 10 | Can my teammate and I both receive events from the same source? | Correct | The agent noted that the Team-plan requirement appeared only in the FAQ. |

**Round 1 result:** 10 of 10 correct, 0 wrong, 3 correct but fragile. The agent also reported 2 ambiguities (whether expired events still appear in lists, and the rate-limit window) and 1 broken example (the CI race condition).

## Fixes made after round 1

| Finding | Fix | Pages changed |
| :-- | :-- | :-- |
| Source deletion was only implied by a missing command | Added "Delete or rename a source", which says the CLI can't do it, plus an FAQ entry and a "don't invent one" rule in the skill | `concepts/sources-routes-destinations`, `resources/faq`, `skill.md` |
| Retry wording was inconsistent | Standardized on "up to 8 delivery attempts: the first attempt plus 7 retries, about 22 hours 36 minutes" | `concepts/retries-and-replay`, `resources/faq`, `skill.md` |
| Contradiction: expired event IDs "remain" vs "lists only show events inside retention" | Removed the "ID and status remain" claim and stated that expired events disappear from lists | `concepts/events-and-attempts`, `resources/faq` |
| No combined `--path` + `$prefix` example | Added one to the command reference | `cli/listen` |
| Team-plan requirement only in the FAQ | Added it to the command reference | `cli/listen` |
| Rate-limit window unspecified | Stated it's a sliding window and that `Retry-After` is a whole number | `api-reference/rate-limits` |
| CI sample used `sleep 3` (race) | Replaced with a loop that waits for the session line | `guides/use-hookferry-in-ci` |
| Unclear whether test keys can run `listen` | Stated it explicitly | `guides/use-hookferry-in-ci` |

## Round 2: retest on the fixed docs

A new agent, with no memory of round 1, answered the fragile questions and two questions that targeted the fixed ambiguities.

| # | Question | Grade | Notes |
| :-- | :-- | :-- | :-- |
| 1 | How do I delete a source using the CLI? | Correct | "You can't." Found it stated in 3 places (concept page, FAQ, skill) and gave the dashboard and API alternatives. |
| 2 | `stripe-dev`, port 8080, `/hooks`, `invoice.*` only | Correct | Found the combined example directly on the command reference. |
| 3 | API rate limit: what happens, how to handle it, fixed or sliding window? | Correct | Gave the sliding window and the whole-number `Retry-After`. |
| 4 | Free plan: does an event from 10 days ago still show in `hookferry events list`? | Correct | "No." The contradiction is gone. |
| 5 | Exactly how many times does Hookferry retry an HTTPS delivery? | Correct | "8 delivery attempts: the first plus 7 retries", worded the same on every page. |

**Round 2 result:** 5 of 5 correct with high confidence, and no contradictions between pages.

### Backlog: remaining gaps the agent noted

These didn't cause wrong answers. They're candidates for the next docs iteration:

- How the CLI handles `429` responses internally (backoff, maximum retries).
- Whether retention is measured from when the event was received.
- Whether retry delays have jitter, and whether Hookferry honors a destination's `Retry-After`.

## Round 3: retrieval test on the live MCP server

After deployment, each of the 10 round 1 questions went to the live docs MCP server's search tool (`search_hookferry` at `https://tony-isaac-portfolio.mintlify.site/mcp`). This tests retrieval, the first step for any MCP client: does the page with the answer come back near the top? The script is `retrieval.py`. It sends each question and records where the answer page ranks.

| # | Question | Before fixes | Notes |
| :-- | :-- | :-- | :-- |
| 1 | Express handler returns 401 for every event | Partial | Top result was the code guide, which covers the fix only in a code comment. The troubleshooting page ranked 6th because its headings never said "Express" or "Flask". |
| 2 | Stopped `hookferry listen` overnight: will missed webhooks show up? | Miss | No top-3 result explained `undelivered` events. The answer was spread across concept pages, and no heading matched how users ask. |
| 3 | Retry count and duration for HTTPS | Found (rank 1) | |
| 4 | `$prefix` filter command | Found (rank 1) | |
| 5 | GitHub Actions without login | Found (rank 1) | |
| 6 | Replay a 10-day-old event on Free | Found (rank 1) | The rank 1 page (Replay failed events) states the 3-day limit and `event_expired`. |
| 7 | Docker "connection refused" | Found (rank 1) | |
| 8 | API rate limit behavior | Found (rank 1) | |
| 9 | Delete a source with the CLI | Found (rank 1) | The FAQ entry added after round 1 ranks first. |
| 10 | Teammates sharing a source | Found (rank 1) | |

**Before fixes:** 8 of 10 found, 1 partial, 1 missed.

### Fixes made after round 3

| Finding | Fix |
| :-- | :-- |
| Q2 had no page worded the way users ask | Added the FAQ entry "I stopped hookferry listen. Do I lose webhooks that arrive while it's off?" |
| Q1's troubleshooting page didn't use the words people search with | Renamed it "Fix 401 signature verification errors", added Express and Flask to the description and first heading |
| The live MCP and skill-install commands pointed at the placeholder `docs.hookferry.dev` | Switched every docs link to `tony-isaac-portfolio.mintlify.site` |

**Lesson:** a reading test (rounds 1 and 2) checks that the answer exists. A retrieval test (round 3) checks that a search can find it. The FAQ ranked first for 3 questions, which shows that question-shaped headings help retrieval.

**After fixes:** RETEST_PENDING
