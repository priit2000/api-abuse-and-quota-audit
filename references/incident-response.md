# Incident Response

## Immediate Containment

- Disable, rotate, or restrict suspected credentials.
- Split browser and server credentials if they are shared.
- Apply temporary quotas, spend caps, rate limits, and WAF/bot rules.
- Disable nonessential jobs or high-usage features if needed.
- Preserve logs, usage exports, billing reports, deploy history, and recent commits.

## Diagnosis

- Identify which provider, key, project, route, account, user segment, referrer, IP range, job, or deployment consumed usage.
- Compare usage before and after recent deploys.
- Look for public forms, autocomplete/search, signup, upload, AI, email, SMS, maps, and enrichment paths.
- Check whether test, staging, local development, or workers consumed production quota.
- Inspect retries, polling, loops, and duplicate frontend requests.

## Recovery

- Reissue least-privilege credentials.
- Add provider-side restrictions and app-side rate limits.
- Add quotas, budget alerts, usage alerts, and dashboards.
- Fix wasteful code paths and add caching.
- Add graceful user experience for provider throttling or quota exhaustion.
- Document ownership, rotation process, and emergency shutoff.
