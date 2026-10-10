#!/usr/bin/env bash
# The weekly AVV skills update, for an AVV teammate's Hermes agent (see jobs.md).
#
# Hermes runs it as a no-agent job and sends you on WhatsApp whatever it prints. It checks the
# four AVV skills and updates the ones that changed in the AVV agent repo. When everything is
# fine it prints nothing, so you hear nothing. When something goes wrong it prints one plain
# line. It always ends with exit code 0, so Hermes sends that line as it is instead of its own
# failure notice.

SKILLS="commitments contact-capture meeting-brief meeting-debrief"

if ! command -v hermes >/dev/null 2>&1; then
  echo "The weekly AVV skills update couldn't run: the hermes command isn't available to scheduled jobs on this agent."
  exit 0
fi

failed=""
edited=""
for name in $SKILLS; do
  # A wide line, so Hermes's table never shortens the status words.
  if ! checked="$(COLUMNS=200 hermes skills check "$name" 2>&1)"; then
    failed="$failed $name"
    continue
  fi
  case "$checked" in
    *update_available*) ;;
    *up_to_date*) continue ;;
    # Not installed from the AVV repo, or the repo couldn't be reached.
    *) failed="$failed $name"; continue ;;
  esac
  if ! updated="$(COLUMNS=200 hermes skills update "$name" 2>&1)"; then
    failed="$failed $name"
    continue
  fi
  case "$updated" in
    *Skipping:*) edited="$edited $name" ;;
  esac
done

note=""
if [ -n "$failed" ]; then
  note="The weekly AVV skills update couldn't check or update:${failed}. Ask your agent to run \"hermes skills check\" and show you what it says."
fi
if [ -n "$edited" ]; then
  note="${note:+$note }These AVV skills were changed on this agent, so they were left as they are:${edited}. To take AVV's version, ask your agent to run \"hermes skills update <name> --force\"."
fi
if [ -n "$note" ]; then
  echo "$note"
fi
exit 0
