# Server Patterns

## API Proxy Risks

- Public endpoints that forward arbitrary input to paid, limited, or privileged APIs.
- Missing authentication or authorization before provider calls.
- No per-user, per-IP, per-account, or per-route rate limit.
- No input validation, size limits, timeout, or allowlist.
- Provider errors returned directly to clients.

## Retry And Resilience

- Add exponential backoff, jitter, max attempts, and timeout limits.
- Avoid retrying non-idempotent operations unless an idempotency key or deduplication guard exists.
- Add circuit breakers or temporary disable paths for provider incidents.
- Treat `429`, quota exceeded, and insufficient credits as expected operational states.

## Caching And Deduplication

- Cache deterministic or semi-stable lookups.
- Coalesce concurrent identical requests.
- Persist checkpoints for long-running background jobs.
- Batch where provider and business logic allow it.
- Avoid repeatedly enriching the same entity without freshness requirements.

## Workers, Cron, And Webhooks

- Verify scheduled jobs have bounded scope and progress checkpoints.
- Ensure queues have dead-letter handling and retry caps.
- Verify webhook handlers validate signatures before provider calls.
- Make webhook side effects idempotent.
- Avoid test/staging jobs consuming production quota.
