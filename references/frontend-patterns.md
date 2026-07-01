# Frontend Patterns

## Common Risks

- API calls directly in render or computed paths.
- Framework effects that rerun because dependencies are unstable.
- Autocomplete/search calls without debounce, cancellation, and minimum input length.
- Details or enrichment calls for every prediction instead of the final selection.
- No request cancellation when a user keeps typing or navigates away.
- Client-side retries that multiply provider usage.
- Server-capable keys exposed through browser bundles, source maps, mobile apps, or public config.
- Shared frontend keys used across staging, production, docs, and demos.

## React Checks

- Inspect `useEffect` dependencies for object/function values recreated every render.
- Look for API calls in component body, selectors, render helpers, or unguarded effects.
- Verify autocomplete has debounce, minimum length, stale-response handling, and abort logic.
- Verify detail calls happen after final user selection, not for each suggestion.

## Vue/Svelte/Other Browser Checks

- Inspect watchers, reactive statements, computed values, subscriptions, and lifecycle hooks.
- Look for unbounded requests from input bindings.
- Verify route changes and component remounts do not duplicate calls.

## Client Hardening

- Keep privileged calls behind server endpoints.
- Use short-lived or restricted client credentials only when the provider supports them.
- Add user-visible degraded states for rate limits and provider outages.
- Avoid surfacing provider error details that reveal keys, account ids, or internal routes.
