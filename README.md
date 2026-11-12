# Hookferry docs

Created by **[Isaac Tony](https://github.com/isaactony)**, technical writer. Live site: https://tony-isaac-portfolio.mintlify.site

An AI-ready documentation site, built with [Mintlify](https://mintlify.com), for **Hookferry**: a fictional CLI and REST API for receiving, forwarding, inspecting, and replaying webhooks.

> Hookferry is not a real product. Its domains (`hookferry.dev`), npm package, and Homebrew tap don't exist. The site is a portfolio project that shows information architecture, technical writing, and AI-readiness work on a realistic product.

## Run the site locally

Prerequisites: Node.js 20 or later.

```bash
npx mint@latest dev
```

Open http://localhost:3000. If port 3000 is busy, add `--port 3333`.

## Check the site

Run these before every commit:

```bash
npx mint@latest validate       # MDX, navigation, and OpenAPI rules, then a strict build
npx mint@latest broken-links   # internal links, including generated API pages
npx mint@latest a11y           # color contrast and alt text
```

After deploying, run `mint score <your-docs-url>` for Mintlify's agent-readiness score. It requires `mint login`.

## Repository structure

```text
docs.json                    Site config: navigation, theme, contextual menu, agent instructions
skill.md                     Custom agent skill (overrides Mintlify's generated one)
index.mdx                    What Hookferry does
quickstart.mdx               First webhook in five minutes
installation.mdx
ai-tools.mdx                 MCP server, skill install prompt, Markdown, llms.txt
concepts/                    Explanation: the mental model (4 pages)
guides/                      How-to: one task per page (5 pages)
cli/                         Reference: one command per page (6 pages)
troubleshooting/             Organized by symptom (3 pages)
resources/                   FAQ, glossary, AI readiness checklist
changelog.mdx
api-reference/
  openapi.yaml               OpenAPI 3.1 spec. Mintlify generates the 13 endpoint pages from it.
  authentication.mdx, errors.mdx, pagination.mdx, rate-limits.mdx
logo/, favicon.svg
```

## Information architecture

The **Documentation** tab follows the [Diátaxis](https://diataxis.fr) split, so every page has a single job:

| Section | Answers | Example |
| :-- | :-- | :-- |
| Get started | "How do I get it working?" | Quickstart |
| Concepts | "How does it work?" | Retries and replay |
| How-to guides | "How do I do X?" | Replay failed events |
| CLI reference | "What exactly does this flag do?" | hookferry listen |
| Troubleshooting | "Why am I seeing Y?" | Fix "connection refused" |
| Resources | Lookup | Glossary, FAQ |

The **API reference** tab puts four hand-written pages (auth, errors, pagination, rate limits) ahead of endpoint pages generated from `openapi.yaml`. Field names, types, and limits therefore come from one source of truth.

## Writing decisions

- **Every page has a specific `title` and a one-sentence `description`.** The description is what `llms.txt` and search results show, so it states the page's answer, not just its topic.
- **One topic per page.** Signatures, retries, and replay are separate pages, so search, and AI retrieval, returns the page that actually answers the question.
- **Descriptive headings.** No "Overview" or "More info". AI tools split pages into chunks at headings, and a heading is often the only context a chunk keeps.
- **Prerequisites at the top of every task.** No page assumes the reader came from another page.
- **Links, not positions.** No "as mentioned above". Every cross-reference names and links the target page.
- **Numbers, not adjectives.** "Up to 8 attempts over about 22 hours 36 minutes", not "several retries".
- **Controlled vocabulary.** Each term in the [glossary](resources/glossary.mdx) has one meaning everywhere. For example, *retry* (automatic) and *replay* (on request) are never used interchangeably.
- **Troubleshooting by symptom.** Pages open with what the user sees, such as `401` on every event or `✕ connection refused`, because that is what they paste into an AI tool.
- **Tested code.** The Express and Flask verification samples in `guides/verify-signatures.mdx` were extracted and run against valid, tampered, and stale requests.
- **Developer-focused tone.** Second person, present tense, short sentences, code first.

Mintlify components are used only where they help a reader: `Steps` for ordered procedures, `Tabs` for OS or interface choices, `CodeGroup` for the same code in several languages, and callouts for warnings that change what the reader does.

## AI-readiness features

| Feature | Where |
| :-- | :-- |
| Contextual menu: copy page, view Markdown, open in ChatGPT, Claude, or Perplexity, MCP connect for Cursor and VS Code, download the spec | `docs.json` → `contextual` |
| Site-wide agent instructions in every Markdown page | `docs.json` → `markdown.instructions` |
| Custom agent skill | `skill.md` |
| Install-the-skill prompt (Prompt component, with an agent-only Markdown version) | `ai-tools.mdx` |
| `llms.txt`, `llms-full.txt`, `/mcp`, `.md` pages | Generated by Mintlify on deploy |
| Reusable checklist for clients | `resources/ai-readiness-checklist.mdx` |

The results of the 10-question AI test are in `portfolio/case-study.md`.
