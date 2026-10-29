"""Post a deploy notice from .github/workflows/announce.yml after each merge to main.

Teammates' agents pick up the change at their weekly skills update. This mirrors
avv-status's version_alert.py: chore:, docs:, ci: and build: titles aren't announced,
and commit text can't ping the channel or add a link. For a merge commit, the title
is the pull request's. Run as `python3 .github/scripts/deploy_notice.py`.
"""

from __future__ import annotations

import http.client
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

SKIP_PREFIXES = frozenset({"chore", "docs", "ci", "build"})
_PREFIX = re.compile(r"^([A-Za-z]+)(?:\([^)]*\))?!?:")
_MERGE = re.compile(r"^Merge pull request #(\d+) from \S+$")


class FetchError(Exception):
    """The POST could not reach the host or read its response."""


def http_post_json(url: str, payload: dict, headers: dict | None = None, timeout: float = 20):
    """POST JSON, returning (status, body_text, headers). Errors name only the host."""
    body = json.dumps(payload).encode("utf-8")
    all_headers = {"Content-Type": "application/json; charset=utf-8", "User-Agent": "avv-agent"}
    all_headers.update(headers or {})
    req = urllib.request.Request(url, data=body, headers=all_headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read().decode("utf-8", "replace"), dict(resp.headers)
    except urllib.error.HTTPError as exc:
        try:
            return exc.code, exc.read().decode("utf-8", "replace"), dict(exc.headers or {})
        finally:
            exc.close()
    except (urllib.error.URLError, TimeoutError, ConnectionError, http.client.HTTPException) as exc:
        host = urllib.parse.urlsplit(url).hostname
        raise FetchError(f"{type(exc).__name__} posting to {host}") from None


def escape(text: str) -> str:
    """Escape Slack's three special characters ('&' first)."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def title(commit_message: str) -> str:
    """The commit's title; for a pull request's merge commit, its title and number."""
    lines = [line.strip() for line in (commit_message or "").splitlines()]
    first = lines[0] if lines else ""
    merge = _MERGE.match(first)
    if merge:
        pr_title = next((line for line in lines[1:] if line), "")
        if pr_title:
            return f"{pr_title} (#{merge.group(1)})"
    return first


def is_internal(title_text: str, skip_prefixes=SKIP_PREFIXES) -> bool:
    match = _PREFIX.match(title_text)
    return bool(match) and match.group(1).lower() in skip_prefixes


def message(sha: str, title_text: str, author: str, branch: str) -> str:
    header = ":rocket: *avv-agent — new version deployed*"
    if branch:
        header += f"  (`{branch}`)"
    by = escape(author.strip() or "unknown")
    tail = f"`{sha[:7]}` · by {by}" if sha else f"by {by}"
    return f"{header}\n{escape(title_text.strip() or '(no commit message)')}\n{tail}"


def main(env=None, post=http_post_json) -> int:
    env = os.environ if env is None else env
    title_text = title(env.get("COMMIT_MESSAGE", ""))
    if is_internal(title_text):
        print(f"internal change, not announced: {title_text[:80]}")
        return 0
    token, channel = env.get("SLACK_BOT_TOKEN", ""), env.get("AGENT_ALERTS_CHANNEL", "")
    if not token or not channel:
        print("error: SLACK_BOT_TOKEN and AGENT_ALERTS_CHANNEL must both be set", file=sys.stderr)
        return 1
    sha = env.get("COMMIT_SHA", "")
    text = message(sha, title_text, env.get("COMMIT_AUTHOR", ""), env.get("BRANCH", ""))
    try:
        status, body, _ = post(
            "https://slack.com/api/chat.postMessage",
            {"channel": channel, "text": text},
            {"Authorization": f"Bearer {token}"},
        )
    except FetchError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # e.g. a token with a line break: the error text would hold it
        print(f"error: {type(exc).__name__} posting to slack.com", file=sys.stderr)
        return 1
    try:
        data = json.loads(body)
    except ValueError:
        data = {}
    if status != 200 or not data.get("ok"):
        err = data.get("error") or f"HTTP {status}"
        hint = " (invite Khoa: /invite @Khoa in #agent-alerts)" if err == "not_in_channel" else ""
        print(f"error: Slack chat.postMessage failed: {err}{hint}", file=sys.stderr)
        return 1
    print(f"announced {sha[:7]} in #agent-alerts")
    return 0


if __name__ == "__main__":
    sys.exit(main())
