---
name: api-abuse-and-quota-audit
description: Audit applications for API abuse, credential exposure, quota exhaustion, rate-limit failures, excessive API calls, billing surprises, and unreliable usage patterns across paid, free-tier, internal, partner, and metered APIs. Use when reviewing API keys, frontend or backend API integrations, usage spikes, quota or rate-limit issues, billing incidents, AI-generated code that calls APIs, autocomplete/search/email/maps/payment/AI integrations, or production hardening for external services.
---

# API Abuse And Quota Audit

## Purpose

Use this skill to prevent API integrations from becoming abuse, quota, reliability, or billing problems. Cover paid APIs, free-tier APIs, internal APIs, partner APIs, and any service with shared limits, account-level quotas, rate limits, or usage-based billing.

## Core Workflow

1. Inventory every API integration in the application.
2. Classify each integration as browser/client, mobile, server, background job, webhook, internal service, or third-party automation.
3. Identify credentials and access mechanisms: API keys, OAuth tokens, service accounts, webhook secrets, signed URLs, temporary tokens, or provider-managed identities.
4. If a repository is available, optionally run `scripts/find-api-risk-patterns.py <repo-path>` to build a first-pass map of likely providers, request code, retry/polling patterns, and possible credential exposure. Treat script output as leads, not proof.
5. Separate evidence into:
   - `Confirmed from repo`
   - `Confirmed from provider config`
   - `Needs verification`
6. Inspect application code for wasteful, repeated, or abusable API calls.
7. Inspect infrastructure-as-code, deployment config, environment definitions, and provider settings when available.
8. Detect available provider CLIs or APIs before claiming provider-side settings.
9. Produce prioritized findings with exact fixes and manual verification steps for anything not directly observable.

## Evidence Rules

Do not claim provider-console settings are configured or missing from repository evidence alone.

Use `Confirmed from repo` for findings visible in code or local configuration, such as exposed keys, missing debounce, public proxy endpoints, duplicate calls, or retry loops.

Use `Confirmed from provider config` only when actual provider settings are visible through a CLI, API, exported config, infrastructure-as-code source of truth, or user-provided console evidence.

Use `Needs verification` for quotas, budget alerts, enabled APIs, key restrictions, WAF/rate-limit rules, billing thresholds, and similar settings when the source of truth is unavailable.

Read `references/evidence-sources.md` when provider settings, account configuration, IaC, or evidence quality matters.

If the user asks for an audit, report, shareable result, or review summary, follow `references/audit-output-template.md`.

## What To Check

Credential controls:

- Exposed server-capable keys or tokens.
- Browser keys without domain, app, package, bundle, or origin restrictions where supported.
- Server keys without IP, network, workload identity, or environment restrictions where supported.
- Overly broad scopes, IAM permissions, enabled APIs, or service permissions.
- Same key shared across development, staging, production, CI, and local scripts.
- Stale, unused, or ownerless keys.
- Missing rotation, revocation, or break-glass process.

Quota and rate-limit controls:

- Missing daily, monthly, per-user, per-IP, or per-environment limits.
- Missing spend caps, budget alerts, quota alerts, or anomaly alerts.
- Shared production quota consumed by staging, tests, workers, or local development.
- Missing graceful handling of `429`, quota exhaustion, provider outage, or degraded-mode behavior.
- Missing server-side rate limits on public or user-triggered API paths.

Code usage patterns:

- API calls in render paths or repeatedly fired effects.
- Search, autocomplete, location lookup, email, SMS, upload, or AI calls without debounce and minimum input length.
- Details, enrichment, geocoding, classification, or AI calls before user intent is clear.
- Polling without stop conditions.
- Retries without exponential backoff, jitter, max attempts, or circuit breaking.
- No caching for repeatable lookups or deterministic results.
- Background jobs calling APIs one-by-one where batching, caching, or checkpointing is needed.
- Non-idempotent webhook retries or state-changing API calls without idempotency keys.

Abuse surfaces:

- Public forms, search, autocomplete, upload, signup, login, invite, email, SMS, AI generation, maps, geocoding, payment, or enrichment endpoints.
- Unauthenticated or weakly authenticated API proxy endpoints.
- Endpoints that forward arbitrary user input to limited, metered, or privileged APIs.
- Client-visible configuration that enables unexpected provider usage.

Read `references/frontend-patterns.md` for browser and framework call-pattern risks. Read `references/server-patterns.md` for API proxy, worker, retry, cache, webhook, and server hardening risks.

## Provider Scope

Use provider-neutral reasoning first. Then apply provider-specific checks where relevant.

Common providers include Google Maps/Places/Geocoding/Firebase/Cloud APIs, OpenAI, Anthropic, AWS, Azure, GCP, Stripe, Paddle, PayPal, Twilio, SendGrid, Mailgun, Postmark, Mapbox, Algolia, Supabase, Clerk, Auth0, Cloudflare, Vercel, Netlify, GitHub, Slack, Discord, Notion, and Airtable.

Read `references/provider-checklists.md` for provider-specific examples and settings to verify.

## Incident Mode

When the user mentions a billing spike, leaked key, quota exhaustion, provider throttling, or account suspension, switch to incident mode:

1. Identify likely active credentials and integrations.
2. Recommend immediate containment: disable, rotate, restrict, or split keys.
3. Preserve evidence from logs, usage dashboards, commits, and deploy history.
4. Add short-term caps, quotas, rate limits, and bot protection.
5. Find the code path or abuse surface that consumed usage.
6. Suggest long-term hardening.

Read `references/incident-response.md` for the incident checklist.

## Output Format

Return:

- Overall risk summary.
- APIs/providers found.
- Evidence sources used.
- Findings grouped by `Critical`, `High`, `Medium`, and `Low`.
- Evidence labels for each finding.
- File paths, config locations, or provider-setting sources where available.
- Exact recommended fixes.
- Items needing provider-console verification.
- Quick wins.
- Longer-term hardening.

Severity guidance:

- `Critical`: exposed server credential, unrestricted production key, unauthenticated public proxy to limited or metered API, or active incident containment gap.
- `High`: easy bot abuse path, missing quota or rate limit on public paths, expensive calls before user intent, missing key restrictions, or broad production permissions.
- `Medium`: duplicate calls, weak caching, unsafe retries, broad scopes, weak `429` handling, or shared quota between environments.
- `Low`: monitoring gaps, stale keys, documentation gaps, ownership ambiguity, or non-urgent cleanup.

## Plain-Language Mode

When the user is not deeply technical, explain key terms briefly:

- API key: a password-like code that lets an app use another service.
- Quota: the amount of usage allowed before the service slows, blocks, or charges more.
- Rate limit: a speed limit for how many requests can happen in a short time.
- Browser key: a key that may be visible to website visitors and therefore needs strict restrictions.
- Server key: a private key that should stay on backend servers and never ship to browsers or mobile apps unless designed for that.
- Bot protection: controls that stop automated traffic from using forms or endpoints at scale.
