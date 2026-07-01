# API Abuse And Quota Audit

This is a Codex skill for checking whether an app could run into API problems.

It is not only for paid APIs. It also covers free-tier APIs, shared quotas, rate limits, account suspensions, service slowdowns, and surprise bills.

## Origin

This skill is based on a real experience discussed in the Vibecoding Life Facebook group: an API setup that could have been safer with stricter key restrictions, separated browser and server credentials, quotas, budget alerts, bot protection, and fewer unnecessary API lookups.

Source discussion: [Vibecoding Life Facebook post](https://www.facebook.com/groups/vibecodinglife/posts/2072351953353331/?comment_id=2072381400017053&notif_id=1782909614532091&notif_t=feedback_reaction_generic&ref=notif)

## What It Helps Find

- API keys that are too exposed or too powerful.
- Browser keys that should be restricted to specific domains or apps.
- Server keys that should not appear in frontend code.
- Missing quotas, rate limits, alerts, or budget controls.
- Public forms or endpoints that bots could abuse.
- Code that makes more API calls than needed.
- Autocomplete, search, maps, AI, email, SMS, payment, and enrichment flows that may waste quota.
- Retry loops, polling, duplicate requests, or missing caching.
- Places where actual provider settings need to be checked manually.

## When To Use It

Use this skill when you want Codex to review a project before launch, after a quota or billing issue, or after adding a feature that calls external services.

Example requests:

- "Audit this app for API abuse and quota risks."
- "Check whether this Google Places implementation could waste quota."
- "Find places where AI-generated code is making too many API calls."
- "Review our API keys, rate limits, and billing-risk controls."
- "Check whether our free-tier APIs could break production."

## What Makes It Careful

The skill separates evidence into three groups:

- **Confirmed from repo**: visible in the code or local config.
- **Confirmed from provider config**: verified from a provider console, CLI, API, export, or infrastructure-as-code.
- **Needs verification**: important settings that cannot be proven from the repo alone.

This matters because source code can show that a key is used in the browser, but it usually cannot prove whether the key is correctly restricted inside Google Cloud, Stripe, AWS, OpenAI, or another provider.

## Providers It Can Cover

The skill is provider-neutral. It can be used for services such as:

- Google Maps, Places, Geocoding, Firebase, and Google Cloud
- OpenAI, Anthropic, and other AI APIs
- AWS, Azure, and GCP
- Stripe, Paddle, PayPal
- Twilio, SendGrid, Mailgun, Postmark
- Mapbox, Algolia, Supabase, Clerk, Auth0
- Cloudflare, Vercel, Netlify
- GitHub, Slack, Discord, Notion, Airtable
- Internal company APIs with quotas or shared limits

## How To Install

Copy or link this folder into your Codex skills directory:

```bash
~/.codex/skills/api-abuse-and-quota-audit
```

After that, ask Codex to use the skill by name:

```text
Use api-abuse-and-quota-audit to review this project.
```

## Files

- `SKILL.md`: the main skill instructions.
- `references/evidence-sources.md`: how to tell what is confirmed and what still needs checking.
- `references/provider-checklists.md`: provider-specific things to inspect.
- `references/frontend-patterns.md`: browser and frontend patterns that cause extra API calls.
- `references/server-patterns.md`: server, worker, webhook, retry, caching, and rate-limit checks.
- `references/incident-response.md`: what to do after a leaked key, quota spike, billing issue, or provider throttling incident.

## Important Limit

The skill cannot magically see private provider-console settings unless Codex has access to the right CLI, API, infrastructure files, exported settings, or screenshots. When it cannot verify a setting, it should say so clearly and give a checklist for what to check.
