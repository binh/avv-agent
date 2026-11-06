#!/usr/bin/env bash
# The weekly AVV skills update, for an AVV teammate's Hermes agent (see jobs.md).
#
# Hermes runs it as a no-agent job and sends you on WhatsApp whatever it prints. It reads AVV's
# list of skills from the AVV agent repo, installs any that aren't on this agent yet, and
# updates the ones that changed there, so a skill AVV adds later needs nothing done on this
# agent. When everything is fine it prints nothing, so you hear nothing. When it installs a
# skill or something goes wrong, it prints one plain line. It always ends with exit code 0, so
# Hermes sends that line as it is instead of its own failure notice.

SKILLS_URL="https://raw.githubusercontent.com/binh/avv-agent/main/skills.txt"
NO_LIST="The weekly AVV skills update couldn't read AVV's list of skills, so it checked nothing this week. It tries again next Monday. If this keeps happening, tell the AVV admin."

if ! command -v hermes >/dev/null 2>&1; then
  echo "The weekly AVV skills update couldn't run: the hermes command isn't available to scheduled jobs on this agent."
  exit 0
fi
if ! command -v curl >/dev/null 2>&1; then
  echo "The weekly AVV skills update couldn't run: the curl command isn't available to scheduled jobs on this agent. Tell the AVV admin."
  exit 0
fi

# Names only: anything else (a web page in place of the list, say) never reaches a command.
set -f
if ! list="$(curl -fsSL --max-time 30 "$SKILLS_URL" 2>/dev/null)"; then
  echo "$NO_LIST"
  exit 0
fi
SKILLS=""
for name in $list; do
  case "$name" in
    -* | *[!a-z0-9-]*)
      echo "$NO_LIST"
      exit 0
      ;;
  esac
  SKILLS="$SKILLS $name"
done
if [ -z "$SKILLS" ]; then
  echo "$NO_LIST"
  exit 0
fi

failed=""
edited=""
installed=""
for name in $SKILLS; do
  # A wide line, so Hermes's table never shortens the status words.
  if ! checked="$(COLUMNS=200 hermes skills check "$name" 2>&1)"; then
    failed="$failed $name"
    continue
  fi
  case "$checked" in
    *update_available*) ;;
    *up_to_date*) continue ;;
    # A skill AVV added after this agent was set up: install it.
    *"No hub-installed skills"* | *"not installed"* | *"not found"*)
      # hermes skills install exits 0 even when it fails, so only its "Installed:" line, and a
      # check that now finds the skill, count.
      result="$(COLUMNS=200 hermes skills install "binh/avv-agent/skills/$name" --yes 2>&1)"
      again="$(COLUMNS=200 hermes skills check "$name" 2>&1)"
      case "$result" in
        *Installed:*)
          case "$again" in
            *"No hub-installed skills"*) failed="$failed $name" ;;
            *) installed="$installed $name" ;;
          esac
          ;;
        *) failed="$failed $name" ;;
      esac
      continue
      ;;
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
if [ -n "$installed" ]; then
  note="The weekly AVV skills update installed new AVV skills:${installed}."
fi
if [ -n "$failed" ]; then
  note="${note:+$note }The weekly AVV skills update couldn't check or update:${failed}. Ask your agent to run \"hermes skills check\" and show you what it says."
fi
if [ -n "$edited" ]; then
  note="${note:+$note }These AVV skills were changed on this agent, so they were left as they are:${edited}. To take AVV's version, ask your agent to run \"hermes skills update <name> --force\"."
fi
if [ -n "$note" ]; then
  echo "$note"
fi
exit 0
