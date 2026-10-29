#!/usr/bin/env python3
# Copied from the AVV secrets-manager repo (runtime/secrets_exec.py, bws 2.1.0), with only this comment changed. Don't edit here; change the original and copy it again.
"""Start a service with its secrets from Bitwarden.

Usage: secrets_exec.py <command> [args...]

With no BWS_ACCESS_TOKEN, runs the command unchanged. Otherwise reads the
secrets with `bws secret list -o json`, adds them to the environment (minus the
token), and replaces itself with the command, so the service gets stop signals
directly. Never prints a value.

AVV_SECRETS_BWS_TIMEOUT (seconds) and AVV_SECRETS_BWS_FALLBACK (the path tried
when bws isn't on PATH) exist for the tests only.
"""

import json
import os
import re
import shutil
import subprocess
import sys

EX_CONFIG = 78
TOKEN = "BWS_ACCESS_TOKEN"
ITEM_ID = re.compile(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}")  # a UUID


def fail(message):
    print(f"secrets_exec: {message}", file=sys.stderr)
    sys.exit(EX_CONFIG)


def item_id(item):
    """The Bitwarden item id (not secret), or a placeholder if it looks odd."""
    value = item.get("id")
    return value if isinstance(value, str) and ITEM_ID.fullmatch(value) else "(no id)"


def encodable(key, value):
    """True if the pair can go into the environment (a lone surrogate can't)."""
    try:
        os.fsencode(key)
        os.fsencode(value)
        return True
    except UnicodeError:
        return False


def test_setting(name):
    """A setting for tests only: ignored on Railway."""
    return None if os.environ.get("RAILWAY_ENVIRONMENT") else os.environ.get(name)


def find_bws():
    return shutil.which("bws") or test_setting("AVV_SECRETS_BWS_FALLBACK") or "/app/bin/bws"


def read_secrets():
    try:
        timeout = float(test_setting("AVV_SECRETS_BWS_TIMEOUT") or 60)
    except ValueError:
        timeout = 60.0
    try:
        result = subprocess.run(
            [find_bws(), "secret", "list", "-o", "json"],
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=timeout,
        )
        code = result.returncode
    except subprocess.TimeoutExpired:
        code = 124
    except OSError:
        code = 127
    if code < 0:
        code = 128 - code
    if code != 0:
        fail(f"could not read secrets from Bitwarden (exit {code})")
    try:
        # A byte-order mark is refused, the same as in secrets-exec.mjs.
        items = None if result.stdout.startswith(b"\xef\xbb\xbf") else json.loads(result.stdout)
    except (ValueError, RecursionError):
        items = None
    if not isinstance(items, list):
        fail("could not read secrets from Bitwarden (unexpected output)")

    loaded = {}
    for item in items:
        key = item.get("key") if isinstance(item, dict) else None
        if not isinstance(key, str) or not key:
            fail("an item with no key came back from Bitwarden")
        if "=" in key or "\0" in key:
            fail(f"item {item_id(item)} has a name that isn't a valid variable name")
        value = item.get("value")
        if not isinstance(value, str) or "\0" in value or not encodable(key, value):
            fail(f"item {item_id(item)} has a value that isn't plain text")
        if key == TOKEN:
            continue
        if key in loaded:
            fail(f"item {item_id(item)} has the same name as another item in this service's Bitwarden projects")
        loaded[key] = value
    if not loaded:
        fail("no secrets found for this token")
    return loaded


def run(argv, env):
    try:
        os.execvpe(argv[0], argv, env)
    except FileNotFoundError:
        print(f"secrets_exec: command not found: {argv[0]}", file=sys.stderr)
        return 127
    except OSError as err:
        print(f"secrets_exec: could not start {argv[0]} ({err.strerror})", file=sys.stderr)
        return 126


def main(argv):
    if not argv:
        print("usage: secrets_exec.py <command> [args...]", file=sys.stderr)
        return 64
    env = dict(os.environ)
    if env.get(TOKEN):
        loaded = read_secrets()
        del env[TOKEN]
        env.update(loaded)
        print(f"secrets_exec: loaded {len(loaded)} secrets from Bitwarden", file=sys.stderr)
        sys.stderr.flush()
    return run(argv, env)


if __name__ == "__main__":
    try:
        code = main(sys.argv[1:])
    except Exception as err:  # never a traceback, which could show a value
        print(f"secrets_exec: stopped on an unexpected error ({type(err).__name__})", file=sys.stderr)
        code = EX_CONFIG
    sys.exit(code)
