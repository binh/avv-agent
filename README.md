# AVV agent

What an AVV teammate's Hermes agent needs to work with the AVV network service: the AVV skills, the settings your setup link fills in for you, the rules for your agent's persona, and two small scripts for scheduled jobs.

The AVV network service sends you, through your agent on WhatsApp, Telegram or Discord (in a private chat with only you, never a group or a server channel), briefs before outside meetings, an evening digest, a question after each outside meeting, and follow-up reminders. It also gives your agent tools to save the people you tell it about to Attio, file your answers about meetings, keep your follow-up list, look people up, and run a portfolio company's raise: its own Attio list of investor firms, drafts for you to send, hand-offs to teammates, and follow-ups.

To start or change a raise, your Attio key needs list read and write (`list_configuration:read-write` and `list_entry:read-write`). With read only, your agent can read raise lists but can't change them: ask the AVV admin for a key with those.

**How to use your agent day to day:** `GUIDE.md` covers briefs, questions after meetings, your follow-up list and reminders, saving and looking up people, and what to say back.

Nothing here is secret: your keys live only on your agent's Keys page (or your agent's `.env` file, if you run it yourself).

## What's here

| Path | What it is |
|---|---|
| `GUIDE.md` | How to use your agent: what the service sends you, when, and what to say back. |
| `skills/` | The AVV skills: `commitments`, `contact-capture`, `investor-introductions`, `meeting-brief`, `meeting-debrief`, `message-context`, `person-context`. They tell your agent how to use the AVV tools. |
| `context-route-snippet.yaml` | Optional settings for message context after briefs, added only once quicker.chat is connected. |
| `settings-snippet.yaml` | The template of the settings you add to your agent once. Your setup link shows it filled in for you: use that one. |
| `standing-rules.md` | Rules for your agent's persona file. Your setup link shows them too. |
| `jobs.md` | How to add the weekly skills update, and the fallback job (only if you're asked). |
| `scripts/update_skills.sh` | The weekly skills update's script. |
| `scripts/network_fetch.py` | The fallback job's script. |
| `.github/` | The deploy notice to #agent-alerts after each merge to main. You don't need it. |

## Setting up your agent

The AVV admin sends you the setup guide and your setup link. In short:

1. Add the AVV skills, once. Ask your agent to run this in its terminal, or run it there yourself:

   ```bash
   for s in commitments contact-capture investor-introductions meeting-brief meeting-debrief message-context person-context; do hermes skills install "binh/avv-agent/skills/$s" --yes; done
   ```

2. Add the weekly job that keeps them up to date: `jobs.md`, "The weekly skills update".
3. Open your setup link and follow it: it shows your two keys once, the settings to add, and the rules for your persona file.

**Already set up?** AVV added three skills (`investor-introductions`, `message-context`, `person-context`), and the copy of `update_skills.sh` on your agent doesn't update itself. Run these once in your agent's terminal: the first installs the three skills, the second downloads the weekly update's script again, so it installs any of these seven that's missing; a skill AVV adds later needs this script downloaded again.

```bash
for s in investor-introductions message-context person-context; do hermes skills install "binh/avv-agent/skills/$s" --yes; done
curl -fsSL https://raw.githubusercontent.com/binh/avv-agent/main/scripts/update_skills.sh -o "${HERMES_HOME:-$HOME/.hermes}/scripts/update_skills.sh"
```

## Adding the settings

Your setup link shows the settings filled in for you. Add them to your agent's settings file (config.yaml) once, from your agent's dashboard (its Files page), or paste them to your agent and ask it to merge them into config.yaml without removing anything and to show you the result.

- If the file already has a line that starts with `mcp_servers:` or `platforms:`, don't add a second one: put the new lines under the one that's there, at the same indent. A second one would wipe out what's under the first, such as your WhatsApp, Telegram or Discord settings.
- The settings read your two keys from the Keys page (or your agent's `.env` file, if you run it yourself) by name: `NETWORK_TOOLS_KEY` and `NETWORK_ROUTE_SECRET`. Add both keys there first, with exactly those names. Never type a key into the settings file or a chat.
- Restart your agent afterwards, so it reads them.

The rules (`standing-rules.md`) go below what's already in your agent's persona file (SOUL.md).

## Plugins

Plugins are your choice, and AVV doesn't check or limit them. We suggest Hermes's official plugins, maintained by Nous: in Hermes's plugin catalog (hermes-agent.nousresearch.com/docs/plugins), filter by Official, then install one with `hermes plugins install <name>`.

## Keeping up to date

- Skills update themselves through the weekly job. To update one now, ask your agent to run `hermes skills update <name>`.
- The settings and the rules don't update themselves. If AVV changes them, the AVV admin asks you to add the new version.

## Deploy notices

After each merge to `main`, Khoa posts a notice to #agent-alerts (`.github/workflows/announce.yml`). It shows the title, the short commit id and who merged it. Titles starting with `chore:`, `docs:`, `ci:` or `build:` get no notice. Khoa must be in #agent-alerts (`/invite @Khoa`). The Slack token is read from Bitwarden at run time, using the repo's `BWS_ACCESS_TOKEN` Actions secret, and is never stored here.

## About this repo

- Nothing secret or personal ever goes here: no keys, no names, no phone numbers, and no email addresses.
- Don't change files here by hand. They're copied from the AVV network service's own repo, and the next copy replaces any change.
