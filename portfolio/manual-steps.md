# Manual steps to publish the site

These steps need your accounts or credentials, so you need to do them yourself.

## 1. Create the GitHub repository

1. On GitHub, create a new **public** repository named `hookferry-docs`. Don't add a README, license, or `.gitignore`. The repo already has them.
2. In this folder, run:

   ```bash
   git add -A
   git commit -m "Initial Hookferry docs site"
   git branch -M main
   git remote add origin https://github.com/<your-username>/hookferry-docs.git
   git push -u origin main
   ```

## 2. Create a Mintlify account and connect the repo

1. Sign up at [mintlify.com](https://mintlify.com). The free plan is enough for this project.
2. During onboarding, choose **I have an existing repo**, install the Mintlify GitHub App, and give it access to `hookferry-docs` only.
3. Set the docs path to the repository root (`docs.json` is at the root).
4. Wait for the first deployment. The dashboard shows your URL, for example `https://<subdomain>.mintlify.app`.

## 3. Replace the fictional docs domain (recommended)

The pages refer to `https://docs.hookferry.dev`, a domain that doesn't exist. After deploying, choose one option:

- **Keep it.** It's clearly part of the fictional product, but links such as the MCP URL in `ai-tools.mdx` won't work for visitors.
- **Point to your real URL.** Replace `docs.hookferry.dev` with your Mintlify subdomain:

  ```bash
  grep -rl 'docs.hookferry.dev' --include='*.mdx' --include='*.md' --include='*.yaml' . \
    | xargs sed -i '' 's#docs.hookferry.dev#<subdomain>.mintlify.app#g'
  ```

  On Linux, use `sed -i` without `''`.

Leave `api.hookferry.dev`, `in.hookferry.dev`, and `app.hookferry.dev` as they are. They're part of the fictional product.

## 4. Optional: custom domain

In the Mintlify dashboard, go to **Settings → Custom domain**, enter a domain you own (for example `hookferry-docs.yourname.com`), and add the CNAME record it shows at your DNS provider. Custom domains may need a paid Mintlify plan.

## 5. Check the AI features on the live site

These only exist after deployment. They couldn't be tested on `mint dev`.

| Check | How | Expected |
| :-- | :-- | :-- |
| llms.txt | Open `<site>/llms.txt` | Every page listed with its description, plus a link to the OpenAPI spec |
| llms-full.txt | Open `<site>/llms-full.txt` | Full text of all pages |
| Markdown pages | Open `<site>/quickstart.md` | Markdown with an "Agent Instructions" block at the top |
| skill.md | Open `<site>/skill.md` | The custom skill from this repo, not a generated one |
| Skill discovery | Open `<site>/.well-known/agent-skills/index.json` | One skill named `hookferry` |
| MCP server | Run `npx @modelcontextprotocol/inspector`, connect to `<site>/mcp` with the HTTP transport, and run a search for "replay" | Results from the Hookferry pages |
| Contextual menu | Open any page and select the menu next to the title | Copy, View as Markdown, ChatGPT, Claude, Perplexity, MCP options |
| Agent-readiness score | `npx mint@latest login`, then `npx mint@latest score <site>` | A score and a list of passed checks. Add the score to the case study. |

Mintlify can take up to 24 hours to process a custom `skill.md`.

## 6. Rerun the AI question test against the live MCP server

The 10-question test in `case-study.md` used the Markdown export from the local preview. After deploying, connect Claude or Cursor to `<site>/mcp`, ask the same 10 questions, and update the results table if anything differs.
