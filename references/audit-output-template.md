# Audit Output Template

Use this structure for shareable API abuse and quota audit reports.

## Summary

- Overall risk: `Critical`, `High`, `Medium`, or `Low`.
- Short explanation of why.
- Most urgent action.

## APIs And Providers Found

List each provider or API and how it appears to be used:

- Provider/API:
- Usage path:
- Environment:
- Evidence:

## Evidence Sources Used

List what was inspected:

- Repository files:
- Infrastructure or deployment config:
- Provider CLI/API/console evidence:
- Logs, billing, or usage data:
- Not available:

## Findings

Group findings by severity.

### Critical

For each finding:

- Title:
- Evidence level: `Confirmed from repo`, `Confirmed from provider config`, or `Needs verification`.
- Evidence:
- Risk:
- Recommended fix:

### High

Use the same fields.

### Medium

Use the same fields.

### Low

Use the same fields.

## Needs Verification

List exact provider-console or account checks that still need to be done:

- Provider:
- Setting to check:
- Why it matters:
- Expected safe setting:

## Quick Wins

List fixes that can usually be done quickly:

- Split browser and server keys.
- Restrict browser keys to real domains/apps.
- Add per-IP and per-user rate limits.
- Add debounce and minimum input length to search/autocomplete.
- Add quotas, budget alerts, and usage alerts.
- Stop enrichment/details calls until user intent is clear.

## Longer-Term Hardening

List deeper improvements:

- Move privileged provider calls behind authenticated server endpoints.
- Add usage dashboards by route, user, provider, and environment.
- Add WAF/bot protection for public forms and high-cost endpoints.
- Add caching, batching, request coalescing, and idempotency.
- Separate projects/accounts for development, staging, and production.

## Plain-Language Explanation

If the audience is not technical, add a short version:

- What could go wrong.
- Whether it could cost money, break the feature, exhaust a free quota, or expose credentials.
- What to fix first.
