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

## Simple Terms

- **API key**: a password-like code that lets your app use another service.
- **Quota**: the amount of usage you are allowed before a service slows down, blocks requests, or starts costing more.
- **Rate limit**: a speed limit for requests.
- **Browser key**: a key that may be visible to website visitors, so it needs strict restrictions.
- **Server key**: a private key that should stay on your backend and not appear in website code.
- **Bot protection**: checks that stop automated traffic from using your forms or API endpoints too much.

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

Install it from GitHub the same way you would install any other public Codex skill:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo priit2000/api-abuse-and-quota-audit \
  --path . \
  --name api-abuse-and-quota-audit
```

Restart Codex after installing so it can pick up the new skill. Then ask Codex to use it by name:

```text
Use api-abuse-and-quota-audit to review this project.
```

## Example Result

A typical audit might say:

```text
Overall risk: High

APIs found:
- Google Places in the website search box
- SendGrid in the contact form
- OpenAI in the summary endpoint

Critical findings:
- None confirmed.

High findings:
- The contact form can trigger SendGrid without a visible rate limit. Confirmed from repo.
- Google Places details lookups appear to happen before final user selection. Confirmed from repo.

Needs verification:
- Check whether the Google browser key is restricted to production and staging domains.
- Check whether daily quotas and billing alerts are set for Google Places and OpenAI.

Quick wins:
- Add debounce and a minimum input length to autocomplete.
- Add per-IP and per-user rate limits to public endpoints.
- Split browser and server API keys if they are currently shared.
```

## Files

- `SKILL.md`: the main skill instructions.
- `references/evidence-sources.md`: how to tell what is confirmed and what still needs checking.
- `references/audit-output-template.md`: a reusable structure for audit reports.
- `references/provider-checklists.md`: provider-specific things to inspect.
- `references/frontend-patterns.md`: browser and frontend patterns that cause extra API calls.
- `references/server-patterns.md`: server, worker, webhook, retry, caching, and rate-limit checks.
- `references/incident-response.md`: what to do after a leaked key, quota spike, billing issue, or provider throttling incident.
- `scripts/find-api-risk-patterns.py`: a lightweight first-pass scanner for likely API risk patterns.

## Important Limit

The skill cannot magically see private provider-console settings unless Codex has access to the right CLI, API, infrastructure files, exported settings, or screenshots. When it cannot verify a setting, it should say so clearly and give a checklist for what to check.
