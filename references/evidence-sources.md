# Evidence Sources

## Evidence Levels

Use `Confirmed from repo` when the issue is visible in source code, package configuration, local deployment files, CI files, committed environment examples, frontend bundles, or tests.

Use `Confirmed from provider config` only when the setting is visible in a provider CLI/API response, infrastructure-as-code source of truth, exported provider configuration, or user-provided console evidence.

Use `Needs verification` when a setting likely matters but is not visible from the available sources.

## Source Priority

Prefer sources in this order:

1. Provider API or CLI output from the active account.
2. Infrastructure-as-code that is known to be applied.
3. Deployment platform configuration and CI/CD environment definitions.
4. Repository code and local config.
5. Logs, usage exports, billing reports, and monitoring dashboards.
6. Screenshots or copied provider-console settings.
7. Manual checklist items.

## Provider Settings Discovery

Check for available tools and configuration before claiming actual provider settings:

- Google: `gcloud`, Firebase CLI, Terraform, Google Cloud API Keys API, Service Usage, IAM, Monitoring, Billing.
- AWS: `aws`, Terraform, CloudFormation, IAM, Service Quotas, Budgets, CloudWatch, WAF.
- Azure: `az`, ARM/Bicep, role assignments, budgets, quotas, Application Gateway/WAF.
- Stripe: `stripe`, webhook endpoint config, restricted keys, events, idempotency usage.
- Cloudflare: API tokens, WAF rules, rate limiting rules, Turnstile, workers routes.
- Vercel/Netlify: environment variables, edge functions, deployment protection, logs.
- Supabase/Firebase: public anon keys, service role keys, rules, usage limits, auth restrictions.

## Reporting Rule

If provider-side access is unavailable, state exactly what could not be verified and give console checks. Do not imply a provider setting is absent unless it was directly inspected.
