# Provider Checklists

## Universal Checks

- Restrict credentials to the minimum APIs, scopes, roles, origins, apps, IPs, or workloads.
- Split browser, mobile, server, CI, staging, production, and local-development credentials.
- Add quotas, budget alerts, usage alerts, and anomaly alerts where supported.
- Add app-level rate limits even when the provider has its own limits.
- Log provider errors, `429` responses, quota exhaustion, and high-cost paths.
- Cache deterministic or semi-stable results.
- Add graceful degradation for quota exhaustion or provider outage.

## Google APIs

- Verify actual key settings in Google Cloud Console or with `gcloud services api-keys describe` when access exists.
- Browser keys: restrict by HTTP referrer, Android package/SHA, or iOS bundle where applicable.
- Server keys: restrict by IP or use service accounts/workload identity where applicable.
- Limit each key to only the required APIs.
- Verify Maps, Places, Geocoding, Directions, Routes, Vision, Translation, and Cloud APIs separately.
- For Places/autocomplete, avoid details calls before final selection and stop lookups once the place is resolved.
- Set quotas and budget alerts by project/API where possible.
- Check whether staging, local development, and production share one project or key.
- Check whether referrer restrictions include only real production/staging domains, not wildcards broader than needed.

## AI APIs

- Keep API keys server-side unless the provider explicitly supports ephemeral client tokens.
- Add per-user, per-IP, and per-session limits.
- Cap prompt, output, image, audio, and tool-call usage.
- Cache deterministic classifications, enrichments, embeddings, and repeated completions when acceptable.
- Avoid retries that regenerate expensive outputs without idempotency or deduplication.
- Log model, token/image/audio usage, user, route, and request purpose.
- Check project-level budgets, monthly caps, usage alerts, and per-route app limits where available.
- Avoid letting anonymous users trigger expensive model, image, transcription, or agent/tool workflows without controls.

## Stripe And Payments

- Use restricted keys where possible.
- Keep secret keys server-side.
- Verify webhook signing and idempotency keys on state-changing operations.
- Avoid duplicate create/charge/subscription calls on retries or refresh.
- Rate-limit public checkout/session creation endpoints.
- Ensure test and live keys are not mixed.
- Confirm webhook handlers validate signatures before doing any state change.
- Confirm retry behavior cannot create duplicate customers, sessions, subscriptions, invoices, or credits.

## SMS And Email

- Rate-limit signup, invite, password reset, OTP, contact, and notification endpoints.
- Add per-recipient, per-IP, per-account, and daily caps.
- Add bot protection to public forms.
- Avoid unlimited retries for transient provider failures.
- Monitor bounce, complaint, fraud, and abuse indicators.
- Add CAPTCHA, Turnstile, login requirements, or abuse scoring before public endpoints that send messages.
- Confirm password reset, OTP, and invite flows do not allow unlimited sends to the same recipient.

## Cloud And Hosting

- Review IAM roles for broad `*` permissions.
- Check budgets, spend alerts, service quotas, WAF/rate limits, and public endpoints.
- Separate staging and production accounts/projects where practical.
- Watch background jobs, queues, cron tasks, image/video processing, search indexing, and serverless functions for runaway usage.
- Check serverless concurrency, timeout, memory, and retry settings.
- Confirm logs and metrics make it possible to trace usage by route, job, deployment, and environment.

## Cloudflare, Vercel, And Netlify

- Check WAF, rate-limiting, bot protection, preview deployment protection, and public function routes.
- Verify environment variables are scoped correctly to development, preview/staging, and production.
- Check whether preview deployments can call production APIs or consume production quota.
- Confirm edge/serverless functions have request limits, input limits, timeouts, and observability.

## Supabase And Firebase

- Treat anon/public keys as public and rely on database rules, security rules, and backend checks.
- Keep service role, admin, and private keys server-side only.
- Review row-level security, Firebase security rules, storage rules, and callable functions.
- Check auth, database, storage, and function quotas separately.
- Confirm public clients cannot read or write high-volume tables, storage paths, or functions without intended limits.

## Search, Maps, And Enrichment

- Debounce user input and require a minimum query length.
- Do not call details/enrichment for every prediction or result.
- Cache stable lookups such as geocoding, place details, company enrichment, and search results.
- Stop lookup chains once the user-selected target is resolved.
- Avoid background enrichment on untrusted or unbounded user input.
