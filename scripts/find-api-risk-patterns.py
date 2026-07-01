#!/usr/bin/env python3
"""Find likely API abuse, quota, and credential-risk patterns in a repo.

This script produces review leads, not confirmed vulnerabilities. It avoids
printing full candidate secrets and should be followed by human/Codex review.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
from typing import Iterable


SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "vendor",
    "dist",
    "build",
    ".next",
    ".nuxt",
    ".venv",
    "venv",
    "__pycache__",
    ".cache",
    "coverage",
}

TEXT_EXTENSIONS = {
    ".astro",
    ".bash",
    ".cjs",
    ".conf",
    ".css",
    ".env",
    ".example",
    ".go",
    ".graphql",
    ".html",
    ".java",
    ".js",
    ".json",
    ".jsx",
    ".mjs",
    ".php",
    ".py",
    ".rb",
    ".rs",
    ".sh",
    ".svelte",
    ".toml",
    ".ts",
    ".tsx",
    ".vue",
    ".yaml",
    ".yml",
}


@dataclass(frozen=True)
class Pattern:
    label: str
    severity: str
    regex: re.Pattern[str]
    guidance: str


PATTERNS = [
    Pattern(
        "Possible Google API key",
        "High",
        re.compile(r"\bAIza[0-9A-Za-z_-]{20,}\b"),
        "Verify key restrictions, enabled APIs, quotas, and whether this key is browser-safe.",
    ),
    Pattern(
        "Possible OpenAI key",
        "Critical",
        re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b"),
        "Keep secret keys server-side; rotate if committed or exposed.",
    ),
    Pattern(
        "Possible Stripe secret key",
        "Critical",
        re.compile(r"\bsk_(?:live|test)_[0-9A-Za-z]{16,}\b"),
        "Secret keys must stay server-side; verify restricted keys and rotation.",
    ),
    Pattern(
        "Possible Stripe publishable key",
        "Medium",
        re.compile(r"\bpk_(?:live|test)_[0-9A-Za-z]{16,}\b"),
        "Publishable keys are client-safe, but verify matching environment and endpoint rate limits.",
    ),
    Pattern(
        "Possible AWS access key id",
        "Critical",
        re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
        "Rotate if exposed; review IAM scope, budgets, quotas, and CloudTrail usage.",
    ),
    Pattern(
        "Frontend-exposed environment variable",
        "Medium",
        re.compile(r"\b(?:NEXT_PUBLIC|VITE|PUBLIC|REACT_APP)_[A-Z0-9_]*(?:KEY|TOKEN|SECRET|API)[A-Z0-9_]*\b"),
        "Client-prefixed variables are usually bundled into browser code; ensure they are safe and restricted.",
    ),
    Pattern(
        "HTTP request code",
        "Info",
        re.compile(r"\b(fetch|axios|got|request|superagent)\s*(?:\(|\.)"),
        "Review request paths for auth, rate limits, retries, caching, and user-triggered loops.",
    ),
    Pattern(
        "Polling or interval",
        "Medium",
        re.compile(r"\b(setInterval|setTimeout|pollingInterval|refetchInterval)\b"),
        "Check for stop conditions, backoff, visibility handling, and quota impact.",
    ),
    Pattern(
        "Retry logic",
        "Medium",
        re.compile(r"\b(retry|retries|maxRetries|backoff|exponential)\b", re.IGNORECASE),
        "Verify retry caps, backoff, jitter, idempotency, and handling for 429/quota errors.",
    ),
    Pattern(
        "Autocomplete or search",
        "Medium",
        re.compile(r"\b(autocomplete|getPlacePredictions|PlacesService|getDetails|search|suggestions?)\b", re.IGNORECASE),
        "Check debounce, minimum query length, cancellation, and whether detail lookups wait for final selection.",
    ),
    Pattern(
        "AI API usage",
        "High",
        re.compile(r"\b(openai|anthropic|chat\.completions|responses\.create|embeddings|images\.generate)\b", re.IGNORECASE),
        "Check auth, per-user limits, token/image caps, caching, logging, and anonymous access.",
    ),
    Pattern(
        "Email or SMS API usage",
        "High",
        re.compile(r"\b(sendgrid|mailgun|postmark|twilio|sendSms|sendEmail|otp|password reset)\b", re.IGNORECASE),
        "Check bot protection, per-recipient limits, per-IP limits, and abuse monitoring.",
    ),
]


def iter_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.name == "find-api-risk-patterns.py":
            continue
        if path.suffix.lower() in TEXT_EXTENSIONS or path.name.startswith(".env"):
            yield path


def mask_line(line: str) -> str:
    line = re.sub(r"(AIza[0-9A-Za-z_-]{6})[0-9A-Za-z_-]+", r"\1...", line)
    line = re.sub(r"(sk-(?:proj-)?[A-Za-z0-9_-]{6})[A-Za-z0-9_-]+", r"\1...", line)
    line = re.sub(r"(sk_(?:live|test)_[0-9A-Za-z]{6})[0-9A-Za-z]+", r"\1...", line)
    line = re.sub(r"((?:AKIA|ASIA)[0-9A-Z]{4})[0-9A-Z]{12}", r"\1...", line)
    return line.strip()[:220]


def scan(root: Path, max_file_bytes: int) -> list[tuple[str, str, Path, int, str, str]]:
    findings: list[tuple[str, str, Path, int, str, str]] = []
    for path in iter_files(root):
        try:
            if path.stat().st_size > max_file_bytes:
                continue
            text = path.read_text(errors="ignore")
        except OSError:
            continue
        rel = path.relative_to(root)
        for line_no, line in enumerate(text.splitlines(), start=1):
            for pattern in PATTERNS:
                if pattern.regex.search(line):
                    findings.append(
                        (
                            pattern.severity,
                            pattern.label,
                            rel,
                            line_no,
                            mask_line(line),
                            pattern.guidance,
                        )
                    )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Find likely API risk patterns.")
    parser.add_argument("path", nargs="?", default=".", help="Repository path to scan")
    parser.add_argument("--max-file-bytes", type=int, default=500_000)
    args = parser.parse_args()

    root = Path(args.path).resolve()
    if not root.exists():
        parser.error(f"path does not exist: {root}")
    if not root.is_dir():
        parser.error(f"path is not a directory: {root}")

    findings = scan(root, args.max_file_bytes)
    if not findings:
        print("No common API risk patterns found. This does not prove the project is safe.")
        return 0

    print("# API Risk Pattern Scan")
    print()
    print("These are review leads, not confirmed vulnerabilities.")
    print()

    order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3, "Info": 4}
    for severity, label, rel, line_no, snippet, guidance in sorted(
        findings, key=lambda item: (order.get(item[0], 99), str(item[2]), item[3], item[1])
    ):
        print(f"- [{severity}] {label} - {rel}:{line_no}")
        print(f"  Snippet: `{snippet}`")
        print(f"  Review: {guidance}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
