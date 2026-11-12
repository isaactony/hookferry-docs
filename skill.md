---
name: hookferry
description: Receive, forward, inspect, and replay webhooks with the Hookferry CLI and Cloud API. Use when a user is building or debugging a webhook handler, needs webhooks on localhost, wants to verify Hookferry-Signature headers, replay failed events, or receive webhooks in CI.
license: MIT
compatibility: The hookferry CLI 2.4 runs on macOS, Linux, and Windows. The npm install needs Node.js 18 or later. The Cloud API is HTTPS at https://api.hookferry.dev/v1.
metadata:
  author: Isaac Tony
  version: "2.4"
  docs: https://tony-isaac-portfolio.mintlify.site
---

# Hookferry

Hookferry gives developers a public **source URL** for webhooks, stores every request as an **event**, and delivers it through **routes** to a **destination**: a running `hookferry listen` session (CLI destination) or a public HTTPS URL (HTTPS destination).

Full docs: https://tony-isaac-portfolio.mintlify.site. Page index: https://tony-isaac-portfolio.mintlify.site/llms.txt. Add `.md` to any page URL for Markdown.

## Before you act

- Ask whether the user is working locally (CLI) or automating (API) if it isn't clear. Steps differ.
- Never print, log, or commit API keys (`hf_live_…`, `hf_test_…`) or signing secrets (`whsec_…`). Read them from `HOOKFERRY_API_KEY` and `HOOKFERRY_SIGNING_SECRET`.
- Never invent CLI flags or API fields. If a task isn't covered here, look it up in the docs.

## Common tasks

### Forward webhooks to a local app

```bash
hookferry login
hookferry listen 3000 --source <name> --path /webhooks
```

`listen` creates the source if it doesn't exist and prints the source URL and signing secret. The source URL doesn't change between sessions with the same `--source` name. If the app binds only to IPv4, use `hookferry listen http://127.0.0.1:3000`.

### Verify the Hookferry-Signature header

Header format: `Hookferry-Signature: t=<unix seconds>,v1=<hex>`.

1. Read the **raw** request body bytes. Never parse JSON before verifying.
2. Compute HMAC-SHA256 over `<t>.<raw body>` with the full signing secret, including the `whsec_` prefix, as the key.
3. Hex-encode it and compare to `v1` in constant time.
4. Reject if `t` is more than 300 seconds from now.

Each destination has its own signing secret. Complete Express and Flask code: https://tony-isaac-portfolio.mintlify.site/guides/verify-signatures.md

### Inspect and replay events

```bash
hookferry events list --source <name> --status failed --since 2h
hookferry events get <evt_id> --attempts
hookferry replay <evt_id>
hookferry replay --source <name> --status failed --since 2h --yes
```

Up to 1,000 events per replay. For a CLI destination, start `hookferry listen` before replaying, or the events become `undelivered` again.

### Manage sources

`hookferry listen` creates sources, but **the CLI has no command to list, delete, or rename sources.** Don't invent one. Delete with the dashboard or `DELETE /sources/{source_id}` (permanent; also deletes routes and events). Sources can't be renamed.

### Run in CI

Set `HOOKFERRY_API_KEY` (use an `hf_test_` key), then run `hookferry listen <port> --source ci-<run id> --ephemeral --json &`. The first JSON line contains `source_url`. Check results with `hookferry events list --source <name> --json`.

## Rules that are easy to get wrong

- **CLI destinations are never retried automatically.** Events that arrive with no listen session become `undelivered`. Events whose local delivery fails become `failed`. Fix: replay.
- **HTTPS destinations get up to 8 delivery attempts**: the first attempt plus 7 retries, with delays of 1m, 5m, 30m, 1h, 3h, 6h, and 12h (about 22 hours 36 minutes in total). Success means a `2xx` within 30 seconds. Redirects count as failures.
- **Replays are not retried**, and they carry `Hookferry-Replay: true` and a new signature.
- **Event statuses:** `pending`, `delivered`, `failed`, `undelivered`, `filtered`.
- **Retention period:** 3 days (Free), 30 days (Team). Expired events can't be replayed (API `410 event_expired`).
- **Body limit:** 1 MB. Larger requests get `413` and aren't stored.
- Hookferry never changes the body, so the provider's own signature still verifies.

## API essentials

- Base URL `https://api.hookferry.dev/v1`, header `Authorization: Bearer $HOOKFERRY_API_KEY`.
- Resources: `/sources`, `/routes`, `/events`, `/events/{id}/attempts`, `/events/{id}/replay`, `/replays`.
- Cursor pagination: `limit` (max 100) and `cursor`; responses have `has_more` and `next_cursor`.
- Rate limit: 100 requests per 10 seconds per key; on `429`, wait for `Retry-After`.
- Errors: `{"error": {"type", "code", "message", "doc_url"}}`. Handle by `code`.
- OpenAPI spec: linked in https://tony-isaac-portfolio.mintlify.site/llms.txt, and downloadable from any API reference page.

## Troubleshooting map

| Symptom | Page |
| :-- | :-- |
| Handler returns 401 on every event | https://tony-isaac-portfolio.mintlify.site/troubleshooting/signature-errors.md |
| `✕ connection refused` in listen output | https://tony-isaac-portfolio.mintlify.site/troubleshooting/connection-refused.md |
| Provider sent it but the app never got it | https://tony-isaac-portfolio.mintlify.site/troubleshooting/missing-events.md |
