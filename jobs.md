# Scheduled jobs for your agent

These jobs run a small script on a schedule without using the model ("no-agent" jobs). Hermes sends you what the script prints, on the platform you chat with your agent on (WhatsApp, Telegram or Discord), word for word. When it prints nothing, nothing is sent.

You can add a job in two ways:

- ask your agent to run the commands below in its terminal, or run them there yourself;
- or use your agent's dashboard: on the Cron page, tick "no_agent", put the script's file name in Script, choose your platform (whatsapp, telegram or discord) to deliver to, and use the schedule shown below.

A job's script must be in your agent's scripts folder, so the commands first copy it there from this repo.

## The weekly skills update (add it once)

If your agent messages you on Telegram or Discord, write `--deliver telegram` or `--deliver discord` instead of `--deliver whatsapp` in the last line: the same platform you chose on your setup link.

```bash
scripts_dir="${HERMES_HOME:-$HOME/.hermes}/scripts"
mkdir -p "$scripts_dir"
curl -fsSL https://raw.githubusercontent.com/binh/avv-agent/main/scripts/update_skills.sh -o "$scripts_dir/update_skills.sh"
hermes cron create "0 9 * * 1" --no-agent --script update_skills.sh --deliver whatsapp --name avv-skills-update
```

- It runs on Mondays at 9:00 am, your agent's time. It checks the four AVV skills and updates the ones that changed in this repo.
- When everything is fine, you hear nothing. When something goes wrong, you get one plain line saying what.
- A skill you changed on your agent is left as it is, and the line says so. AVV's version replaces your change only when you ask your agent to run `hermes skills update <name> --force`.
- To see your jobs: `hermes cron list`.

## The fallback: fetching AVV messages (only when the AVV admin asks)

Normally the AVV network service posts its messages to your agent's `network` route, which you set up from your setup link. If that route ever stops working for good, the AVV admin switches your messages to "fetch" on the service and asks you to add this job. Don't add it before then.

1. On your agent's Keys page, add `NETWORK_DUE_URL`, with the address the AVV admin gives you (it isn't secret).

2. Add these lines to your settings file (config.yaml), the same way as the AVV settings. If the file already has a line that starts with `cron:`, put the two lines under that one instead of adding a second `cron:` line.

   ```yaml
   cron:
     wrap_response: false
     mirror_delivery: true
   ```

   - `wrap_response: false`: the messages arrive exactly as the service wrote them, without Hermes's "Cronjob Response" header and footer.
   - `mirror_delivery: true`: they're copied into your chat's history, so your agent knows what you're replying to.
   - Both apply to your other scheduled jobs too.

3. Restart your agent, then add the job. If your agent messages you on Telegram or Discord, write `--deliver telegram` or `--deliver discord` instead of `--deliver whatsapp` in the last line: the same platform you chose on your setup link.

   ```bash
   scripts_dir="${HERMES_HOME:-$HOME/.hermes}/scripts"
   mkdir -p "$scripts_dir"
   curl -fsSL https://raw.githubusercontent.com/binh/avv-agent/main/scripts/network_fetch.py -o "$scripts_dir/network_fetch.py"
   hermes cron create "* * * * *" --no-agent --script network_fetch.py --deliver whatsapp --failure-deliver local --name avv-network-fetch
   ```

- Every minute it asks the service for the messages that are due, and you get them on your platform, exactly as the service wrote them. When nothing is due, nothing is sent.
- It reads NETWORK_TOOLS_KEY and NETWORK_DUE_URL from your Keys page. Without NETWORK_DUE_URL, it works the address out from your settings file (the `network` tools server's `url`).
- If the service can't be reached for 10 minutes, you get one plain line, then at most one an hour while it lasts.
- `--failure-deliver local` stops Hermes from sending its own failure notice every minute if the script itself breaks. A broken script then shows only as messages that stop arriving: tell the AVV admin if they do.

When the AVV admin switches you back, remove the job: `hermes cron list` shows its id, then run `hermes cron remove <id>`. You can leave the two `cron:` lines and `NETWORK_DUE_URL`.
