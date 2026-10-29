# Using your AVV agent

What your agent does for you with the AVV network service, when its messages arrive, and what to say back. For setting your agent up, see the setup guide the AVV admin sent you.

The examples use made-up people and companies.

## The basics

- **Where:** everything comes in your private chat with your agent: Slack, WhatsApp, Telegram or Discord.
- **The service's own messages** (briefs, the evening digest, questions after meetings, reminders) reach you through your agent word for word. Your agent doesn't rewrite them.
- **Refs:** most messages end with a short ref, like `ref d4m1`, or `(undo c7k2)` after a change you can undo. It's how your agent knows which item you mean.
- **Replying:** reply to the message itself. WhatsApp, Telegram and Discord show it quoted; on Slack, reply in its thread. Then your agent knows what you're answering, even days later. If you don't reply to the message, your agent guesses from your words and recent messages, and asks you when two could fit.
- **Times:** the service checks every 15 minutes, so "9:00 am" means the first check after 9:00 am. Times follow your current time zone (see "Travelling").
- **Quiet hours:** from 10:00 pm to 7:00 am the service holds its questions and notices, and sends them at 8:00 am. Reminders you set for a time, briefs for a meeting that's about to start, and problem and spending-limit messages still come at any hour.

## What you'll get, and when

| Message | When |
|---|---|
| Evening digest: briefs for tomorrow's outside meetings, then your open items | 6:00 pm, only on days with something to brief |
| A brief for a meeting the digest didn't cover (booked later) | About an hour before it starts |
| "How did it go?" after an outside meeting | 10 to 25 minutes after it ends |
| Your follow-ups for the day | 9:00 am, only on days with something due or overdue |
| A reminder you set for a time | Within 15 minutes of that time |
| "Closed from your inbox": an email you were waiting for arrived | Within 15 minutes of the email (held overnight until 8:00 am) |
| A problem you need to fix (for example, sign in to Google again) | When it happens, at most once a day per problem |

A meeting gets a brief when at least one person on it is from outside AVV and Attio knows them, or you've emailed them. Internal meetings and meetings with no one else invited get none. The "how did it go?" question is wider: you're asked after any timed meeting on your work calendar with someone from outside AVV, up to 15 people and not marked private, even if it got no brief.

## Briefs

A brief is a short summary of who you're meeting: who they are, their background, their history with AVV, what's open between you, and questions to ask. Founders, LPs and co-investors each get their own format. A repeat meeting gets only what changed since last time.

Ask for one whenever you like:

```text
Brief me on my 3pm
```

```text
Brief me on Linh Vo at Acme
```

It usually takes under a minute. If it takes longer, your agent says it's on its way and it comes by itself.

Each brief ends with **Useful** and **Wrong** links. One tap records your rating, and "Wrong" asks what was wrong. You can also just reply "useful" or "wrong" to the brief.

To fill in a person's background, the service looks up attendees who have a LinkedIn link in Attio. It may fill blank fields on their Attio record (job title, LinkedIn, company link, location), and update an old job title when their LinkedIn shows a newer job. The brief names each change with an undo ref, and undo works for 5 days. It never creates records and never writes emails or phone numbers.

**Turning the evening digest off:** tell your agent "stop my evening digest" (and "start my evening digest" to get it back). With it off, you also get no briefs an hour before meetings, but briefs you ask for still work.

## After a meeting

10 to 25 minutes after an outside meeting ends, your agent asks how it went:

> How did Acme x AVV (10:00 am) with Linh Vo go? Anything to note or follow up? Reply skip if there's nothing. · ref d4m1

Reply to that message, by text or voice note:

```text
Went well. Linh will send the financials next week. I'll intro her to our fintech advisor by Thursday.
```

Your agent files it in Attio as a meeting note on the person (for a founder, the full note goes on the company). What you'll do becomes a follow-up you owe, and what they'll do becomes a "waiting on" item (see "Your follow-up list"). Anyone new you mention is saved too.

Good to know:
- **Nothing to say?** Reply `skip`. Nothing is filed.
- **No reply at all?** Nothing happens. The question is listed in your evening digest's open items for 2 days, then it drops off.
- **Answering late** still works, as long as you reply to the question itself, so its ref goes along.
- **Back-to-back meetings:** the question waits until your next meeting is over. After quiet hours start, it waits until 8:00 am.
- **Already told your agent?** If you saved someone from that meeting before the question went out, you won't be asked.
- **Filed the wrong thing?** Say "undo" within 24 hours, and the question opens again.

## Your follow-up list

Your agent keeps one list with three kinds of item:
- **You owe:** what you said you'll do, from a meeting or a note about someone. For a work contact it's also a task in Attio. With no date, it's due in 3 business days.
- **Waiting on:** what someone said they'll send or do for you.
- **Reminders:** "remind me to …", for a day or a time.

### The 9:00 am message

On a day when something is due or overdue, you get one message at 9:00 am. Items are numbered when there's more than one, with the headings "You owe", "Waiting on" and "Reminders" when there's more than one kind. Reply to it:

```text
Done 1, move 2 to Monday
```

```text
Drop 3
```

You can also say "done", "move to Friday", "move to tomorrow", or "drop it" for one item. Done, move and drop update the Attio task too. Closed a waiting-on item or a reminder by mistake? Say "reopen". If you mark a task done, delete it or move it in Attio, the list follows.

**Overdue items come back.** Anything still open after its day is in every 9:00 am message, marked "overdue since …", until you mark it done, drop it, or move it.

### Reminders

```text
Remind me to call the Acme team on Monday
```

```text
Remind me at 3 pm to send the deck to Linh
```

- **A reminder for a day** comes in that day's 9:00 am message and keeps coming back as overdue until you mark it done, drop it, or move it. After 9:00 am, a reminder for today needs a time.
- **A reminder for a time** comes within 15 minutes of it, once, and then closes. Want it to keep coming back until it's done? Say so: "remind me at 3 pm to call Linh, and keep reminding me". It then joins the 9:00 am message as overdue from the next day. You can also say "keep reminding me" about a reminder that's already set.
- **Again later:** "move it to Friday" or "again at 5 pm" sets a closed reminder again.

### Waiting on

These come from your meeting answers and notes, or from you directly:

```text
Linh owes me the financials by the 8th
```

- With no date, it's due in 7 days. It's in that day's 9:00 am message, then in each morning's message as overdue until it's closed.
- **The inbox check:** if you've connected your Google account and the agent has the person's email address, the service checks your inbox every 15 minutes for mail from that exact address. When an email clearly delivers what you were waiting for, it closes the item and tells you. Reply "reopen" if it got it wrong. It reads nothing else in your inbox, and it never sends anything.
- **Nudge:** say "nudge" about a waiting-on item (it needs the person's email address), and your agent writes a short, polite email in your voice. You get it as a draft in your Gmail (if drafts are turned on for you), as a Gmail link that opens it ready to send, or as text to copy. You always send it yourself.

### Seeing your list

```text
What are my follow-ups?
```

You get everything open, in all three kinds, not only what's due soon.

Your evening digest also ends with "Open items": what's due in the next 2 days or overdue, and meeting questions you haven't answered in the last 2 days. Each brief shows what you and that person owe each other and your last meeting note with them.

## Saving people

Tell your agent about someone you met, or send a company as a deal or an LP firm:

```text
Met Linh Vo, CFO at Acme, at the fintech dinner. Sharp, raising a seed round in Q1. I'll send her our deck by Friday.
```

You can send text, a business card photo, a screenshot, a LinkedIn link, a voice note, a shared contact, a forwarded message, a website, or a deck. Your agent passes what you sent to the service; the service decides where to save it and what to ask.

**Handled without a question**, apart from a missing email or website:
- A founder of a new company: person, company, deal note, stated tasks, and deal intake.
- A new deal website or deck: company, note and deal intake. No founder is needed. A named founder is saved too.
- A founder whose named company is already in the pipeline or portfolio: notes, no intake; the reply says why.
- A new LP person or firm: person and/or company, note, stated tasks and LP intake.
- An LP whose person or firm already links to an LP record: note and stated tasks, no intake.
- A co-investor or other work contact: person, company, note and stated tasks, no intake.
- A friend or family member: Dex only, when connected.
- "Who is X?" or "look X up": a look-up, with nothing saved.

**What it asks:**
- "Who is this about?" when text reads like someone else's words.
- The service asks when personal or work, the type, or a person's role in a deal isn't clear; when your type and Attio disagree in a way that changes what is written or sent; or when a website, card or link arrives with nothing said about what to do.
- When Attio already knows someone's type, the capture is saved as work without asking personal or work. If several people's answers mix personal and work, send them separately.
- A founder named with only a company name and a personal email can get one question: "What's Acme's website? If there isn't one, say so." The service asks once when intake needs a website and neither Attio nor a work email supplies it, with no single exact company match. If there isn't one, intake goes by name and no Attio company is created.
- If a founder names another company and their linked or email company is already a deal, the service asks whether the named company is new. A yes sends it to deal intake. The old company link stays.
- It also asks for a missing email, whether to save a personal contact as work too, or whose follow-up it is when needed. All service questions come together, word for word. Nothing from that message is saved until you answer.

**Good to know:**
- Companies without a named founder are saved separately, one per capture. They get company notes and tasks, without meeting wording. An LP firm needs no person.
- A passed-on deal names who passed it on, by name only, never as the founder. They aren't saved as a contact unless you ask. "Passed on by" applies to everyone else in the same capture too.
- Only blank fields are filled. No Attio person or company is ever merged or deleted. Teammates' intake goes by a signed direct call.
- Anything you say is private stays out of Attio. A personal contact or a whole private message needs Dex, which is off unless the AVV admin has connected it for you with an API key you make in Dex. A company deal can't be private.

**Fixing and undoing:**
- **Fix:** "she's CTO, not CEO" updates the record and rewrites the note.
- For a job change, the save goes through with the existing company link and the reply offers: "Attio has Lan Pham at Acme. Reply 'Lan Pham is at Beta' to change it." Your answer changes the company link in Attio and Dex, and the title if you gave one. A different email domain alone doesn't trigger this offer. A correction never relinks a founder whose capture named another company, or whose Attio link predates the capture.
- **Undo:** "undo" within 24 hours removes what was saved. Attio records it created are listed for you to remove by hand.
- Personal or work, contact type, follow-ups and private remarks can't be fixed in place: undo and send again. A company capture also needs undo and a fresh capture for any correction.

## Looking someone up

```text
Who is Linh Vo at Acme?
```

```text
What does linkedin.com/in/linh-vo-example do now?
```

Give a LinkedIn link, an email, an Attio link, or a name with a company (a name alone isn't enough). You get their current job, past roles and education, and what Attio already has. If the match isn't certain, your agent asks "is this them?" first. Nothing is saved until you say "save". Look-ups have a monthly limit shared by the whole team.

With Happenstance connected (optional, see the setup guide), "who is" also searches your own network, and your agent says how many Happenstance credits it used.

## Talking about a person

When you mention someone, your agent first looks at what it can reach about them: your recent messages with them (with quicker.chat, once it's available), your network (with Happenstance), and what AVV holds. Then it answers. It uses what's connected for you and skips the rest.

## Investor introductions

```text
Which investors could fill Acme's seed round?
```

Your agent reads AVV's VCs list in Attio (or another company list you name), checks it against what it knows, and gives you a short list. You pick who gets an intro, the founder checks each name first, and your agent writes the drafts in chat for you to copy and send. It never sends anything itself.

## Raises

```text
Start a raise for Acme's Series A
```

Your agent asks whether to share the raise's list with AVV and when the raise should close (it proposes 3 months from today if you don't know), then makes the raise's own list in Attio, one row per investor firm. It asks for the latest blurb and deck link before drafting, picks the best way in to each firm (an AVV owner who knows them, a warm intro, an email, LinkedIn), and drafts for you to send. When the best way in is a teammate, it drafts in their voice and, after your OK, hands it to their agent; a hand-off for you arrives the same way, and you send it as yourself or say no. Tell your agent when you've sent something: it reminds you to follow up 5 business days later. Statuses change only when you say so. Each morning after your reminders, a separate raise message tells you what others changed and asks about a raise past its close date: delete the list in Attio yourself, keep it, or pick a new date.

## Recent messages after a brief

Once quicker.chat is connected and the AVV admin has turned this on for you, a brief an hour before a meeting and the evening digest can be followed by one short message: what you and the people you're meeting have said to each other recently, with the brief's ref. If there's nothing recent, nothing comes. On WhatsApp, if a follow-up didn't come (for example, your Mac was asleep), your agent tries once more at 8:15 am, for meetings still ahead.

Each follow-up opens with the meeting and the people's names, since your agent doesn't keep it in your everyday chat: if you reply to it, say which meeting you mean.

## Travelling

```text
I'm in Singapore till Sunday
```

Your digest, the 9:00 am message, reminders for a day, and the times in your messages then follow your time there. A flight on your calendar also counts once it has landed. A reminder already set for a time keeps the moment it was set for: one set for 3:00 pm in Ho Chi Minh City comes at 4:00 pm in Singapore.

## If something looks wrong

- **Is it working?** Ask "is it working?" or "status". You get the latest health check and your counts.
- **Fix a problem message.** If you get a message about a problem (for example, your Google sign-in), it tells you what to do.
- **A brief has the line "Couldn't write this one; here are the facts." under its title.** The service couldn't write it in time, or you've reached your monthly writing limit (you're told at 80% and 100%). The facts are still right. At the limit, the inbox check also pauses until the next month.
- **Anything else:** tell the AVV admin, with the ref from the message if there is one.
