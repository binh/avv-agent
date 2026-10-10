"""The fallback for an AVV teammate's Hermes agent: fetch the AVV network service's messages.

Used only when the AVV admin switches your messages to "fetch" (see jobs.md); normally the
service posts them to your agent's network route instead. Hermes runs this every minute as a
no-agent job and sends you on WhatsApp whatever it prints, word for word.

- It asks the service for the messages that are due: GET <service>/agent/<id>/due, with your
  tools key (NETWORK_TOOLS_KEY, from your Keys page) as "Authorization: Bearer <key>".
- 200: it prints the messages exactly as the service wrote them, nothing added. The service
  counts them as delivered once it has handed them out.
- 204: nothing is due, so it prints nothing and nothing is sent.
- The address is NETWORK_DUE_URL, from your Keys page (the AVV admin gives it to you). Without
  it, the address comes from your settings file: the network tools server's url,
  <service>/mcp/<id>, gives <service>/agent/<id>/due.
- Anything else (no answer, a refused key, another answer) is a problem. A problem that has
  lasted 10 minutes gets one plain line, then at most one an hour while it lasts. A short
  one, such as the service restarting, says nothing, and so does the end of a problem.
- It always ends with exit code 0, so Hermes sends that line as it is instead of its own
  failure notice every minute.

It uses only Python's standard library and PyYAML, which Hermes has. It never prints the key,
and never follows a redirect, so the key only ever goes to the service's own address.
"""

import http.client
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

TIMEOUT_SECONDS = 20
TELL_AFTER_SECONDS = 10 * 60
TELL_EVERY_SECONDS = 60 * 60
STATE_FILE = Path(__file__).with_name(".network_fetch_state.json")
MCP_URL = re.compile(r"^(https://[^/\s]+)/mcp/([a-z][a-z0-9-]{1,31})/?$")


class _NoRedirects(urllib.request.HTTPRedirectHandler):
    """A redirect is answered as it is, never followed."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def due_url(mcp_url: str) -> str | None:
    """<service>/mcp/<id> gives <service>/agent/<id>/due; anything else gives None."""
    found = MCP_URL.match(mcp_url.strip())
    return f"{found.group(1)}/agent/{found.group(2)}/due" if found else None


def settings_path() -> Path:
    home = os.environ.get("HERMES_HOME")
    if home:
        return Path(home) / "config.yaml"
    return Path(__file__).resolve().parent.parent / "config.yaml"  # <home>/scripts/this file


def find_url() -> str | None:
    """The address to ask: NETWORK_DUE_URL from the Keys page (network people set <id>
    hermes-mode fetch prints it for the AVV admin to give you), or, without it, the one the
    settings file's network tools server gives. None when neither is there, or the given one
    isn't https."""
    given = os.environ.get("NETWORK_DUE_URL", "").strip()
    if given:
        return given if given.startswith("https://") else None
    try:
        import yaml

        settings = yaml.safe_load(settings_path().read_text(encoding="utf-8"))
    except Exception:
        return None
    servers = settings.get("mcp_servers") if isinstance(settings, dict) else None
    server = servers.get("network") if isinstance(servers, dict) else None
    url = server.get("url") if isinstance(server, dict) else None
    return due_url(url) if isinstance(url, str) else None


def fetch(url: str, key: str) -> tuple[int, bytes]:
    """The service's answer as (status, raw bytes). Raises OSError when it doesn't answer."""
    request = urllib.request.Request(
        url, headers={"Authorization": f"Bearer {key}", "Accept": "text/plain"}
    )
    opener = urllib.request.build_opener(_NoRedirects)
    try:
        with opener.open(request, timeout=TIMEOUT_SECONDS) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as e:
        return e.code, b""


def _read_state() -> dict:
    try:
        state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return state if isinstance(state, dict) else {}


def _write_state(state: dict) -> None:
    try:
        STATE_FILE.write_text(json.dumps(state), encoding="utf-8")
    except OSError:
        pass


def _number(value) -> float | None:
    return float(value) if isinstance(value, int | float) else None


def problem(reason: str, now: float) -> int:
    """Note a problem. Once it has lasted 10 minutes, print one plain line, then at most one
    an hour while it lasts."""
    state = _read_state()
    since = _number(state.get("since"))
    since = now if since is None else since
    told = _number(state.get("told"))
    lasted = now - since
    if lasted >= TELL_AFTER_SECONDS and (told is None or now - told >= TELL_EVERY_SECONDS):
        print(
            f"Your AVV messages couldn't be fetched for {int(lasted // 60)} minutes: {reason}. "
            "Tell the AVV admin if this keeps coming; it repeats at most once an hour."
        )
        told = now
    _write_state({"since": since, "told": told})
    return 0


def clear_problem() -> None:
    """Forget a problem once the service answers again. Nothing is printed: on 200 the output
    is exactly the service's messages, and on 204 it's nothing (D321)."""
    try:
        STATE_FILE.unlink()
    except OSError:
        pass


def main(now: float | None = None) -> int:
    now = time.time() if now is None else now
    key = os.environ.get("NETWORK_TOOLS_KEY", "").strip()
    if not key:
        return problem("NETWORK_TOOLS_KEY isn't on your agent's Keys page", now)
    url = find_url()
    if url is None:
        return problem(
            "NETWORK_DUE_URL isn't on your agent's Keys page, and the network tools address "
            "isn't in your agent's settings file",
            now,
        )
    try:
        status, raw = fetch(url, key)
    except (OSError, http.client.HTTPException, ValueError):
        return problem("the AVV network service didn't answer", now)
    if status in (200, 204):
        clear_problem()
        if status == 200 and raw.strip():
            # Exactly as the service wrote it, nothing added (D321). Raw bytes, so an output
            # that can't take UTF-8 never fails after the service counted them delivered.
            try:
                sys.stdout.buffer.write(raw)
                sys.stdout.buffer.flush()
            except (OSError, ValueError):
                pass
        return 0
    if status == 401:
        return problem("the AVV network service turned down your tools key", now)
    return problem(f"the AVV network service answered with code {status}", now)


if __name__ == "__main__":
    sys.exit(main())
