# Incident Response

Use this flow when the user mentions a billing spike, leaked key, exhausted quota, provider throttling, account suspension, or unexpected usage jump.

## Immediate Containment

- Disable, rotate, or restrict suspected credentials.
- Split browser and server credentials if they are shared.
- Apply temporary quotas, spend caps, rate limits, and WAF/bot rules.
- Disable nonessential jobs or high-usage features if needed.
- Preserve logs, usage exports, billing reports, deploy history, and recent commits.
- If production is affected, prefer reducing blast radius over finding the perfect root cause first.

## Diagnosis

- Identify which provider, key, project, route, account, user segment, referrer, IP range, job, or deployment consumed usage.
- Compare usage before and after recent deploys.
- Look for public forms, autocomplete/search, signup, upload, AI, email, SMS, maps, and enrichment paths.
- Check whether test, staging, local development, or workers consumed production quota.
- Inspect retries, polling, loops, and duplicate frontend requests.
- Look for anonymous users, suspicious referrers, unusual IP ranges, high-cardinality user agents, and sudden traffic source changes.
- Check recent AI-generated or rushed code for missing debounce, duplicate effects, or broad proxy endpoints.

## Recovery

- Reissue least-privilege credentials.
- Add provider-side restrictions and app-side rate limits.
- Add quotas, budget alerts, usage alerts, and dashboards.
- Fix wasteful code paths and add caching.
- Add graceful user experience for provider throttling or quota exhaustion.
- Document ownership, rotation process, and emergency shutoff.

## Communication

For a non-technical audience, explain:

- What was exposed or overused.
- Whether the issue was abuse, inefficient code, missing restrictions, or unknown.
- What has already been contained.
- What still needs provider-console verification.
- What will prevent the same issue from recurring.
