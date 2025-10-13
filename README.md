# IssuePing

IssuePing watches GitHub repositories for issues that match labels you care about and notifies you (Telegram, Email) so you can jump in quickly.

This README covers local setup, running, dry-run testing, Windows scheduling, and features implemented in this fork.

## Problem Statement

For many developers, especially beginners, contributing to open source is exciting but overwhelming. They spend endless time refreshing repositories, scanning for the right labels, and checking if issues are already taken. During Hacktoberfest and other open source drives, this becomes even more frustrating because by the time you find the right issue, someone else might already be assigned. The result: lost motivation and wasted time.

## Inspiration

This project was born from the same struggle. As students and new contributors, we wanted to help but found ourselves chasing issues instead of solving them. The idea was simple: what if there was a way to **bring the issues to you**, instead of you chasing them? A tool that works quietly in the background, filters issues by your preferences, and instantly notifies you when something relevant appears.

I wanted to design something minimal, something that could be set up in minutes, without the complexity of running servers or managing heavy infrastructure. GitHub Actions gave me the perfect platform: free, reliable, and already familiar to developers.

## How IssuePing Helps

* Saves you time by automatically watching your chosen repositories.
* Ensures you never miss a **good first issue** or a label you care about.
* Notifies you instantly on **Telegram** or **Email**, wherever you prefer.
* Filters out noise by skipping already assigned issues.
* Prevents duplicates so you only get one notification per issue.

The result: less searching, more contributing. You can spend your energy where it matters most: **writing code and making meaningful contributions**.

## Features

* Polls your selected repositories every 10 minutes
* Filters issues by labels you choose (e.g. `good-first-issue`, `frontend`, `hacktoberfest`)
* Sends notifications to:

  * **Email** (via SendGrid)
  * **Telegram** (via Telegram Bot)
* Skips already assigned issues
* Prevents duplicate notifications by storing state

## Quick Setup

### 1. Fork this Repository

Click **Fork** on the top right of this repo.

### 2. Configure Secrets

Go to your forked repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Add the following:

* `TELEGRAM_BOT_TOKEN` (create new bot using @BotFather)
* `TELEGRAM_CHAT_ID` (your chat ID)
* `SENDGRID_API_KEY` (if using email)
* `EMAIL_TO` (your email address)
* `EMAIL_FROM` (verified sender email in SendGrid)

### 3. Edit Config

In `config/repos.json`, list the repositories and labels you want to track.

Example:

```json
{
  "repos": [
    {
      "name": "facebook/react",
      "labels": ["good-first-issue"]
    },
    {
      "name": "vercel/next.js",
      "labels": ["frontend"]
    },
    {
      "name": "someuser/cool-project",
      "labels": ["hacktoberfest","frontend"]
    }
  ]
}
```

### 4. Enable GitHub Actions

Go to your fork → **Actions** → enable workflows. The default schedule runs every 10 minutes. You can also run it manually via the **Run workflow** button.

### 5. Receive Notifications

Whenever a new issue matches your filters, you will get a Telegram message or an email.

---

## Local development & testing

Follow these steps to run IssuePing locally on Windows. Commands assume the project root is `E:\IssuePing`.

1) Create and activate a virtual environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2) Install dependencies and the package

```powershell
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
python -m pip install -e .
```

3) Create a `.env` for local testing

Copy `.env.example` to `.env` and fill values you want to test. Only fill the channels you plan to use (Telegram or SendGrid). Keep `.env` private.

```powershell
Copy-Item .env.example .env
code .env
```

Example entries:

```
GITHUB_TOKEN=ghp_xxx...
TELEGRAM_BOT_TOKEN=123456:ABCDEF
TELEGRAM_CHAT_ID=987654321
SENDGRID_API_KEY=SG.xxxxx
EMAIL_TO=you@example.com
EMAIL_FROM=sender@example.com
```

4) Dry-run (safe)

This prints notifications without sending them. Useful to verify matching and formatting.

```powershell
python -m issueping --dry-run
```

5) Real run (sends notifications)

```powershell
python -m issueping
```

6) Reset state (re-send previously seen issues)

```powershell
Remove-Item -Force .issueping_cache\state.json
```

---

## Windows: Schedule IssuePing every 10 minutes (Task Scheduler)

Two quick options are provided in the repo:

- `run_issueping.ps1` — wrapper that activates the venv & runs the app.
- `scripts\register_task_safe.ps1` and `scripts\register_task_nonadmin.ps1` — helper scripts to register a scheduled task (use the non-admin `schtasks` version if you don't want to run PowerShell as admin).

Manual Task Scheduler steps (GUI):

1. Open Task Scheduler
2. Create Task → Name: IssuePing Auto Run
3. Triggers → New → Daily, Repeat task every: 10 minutes, for a duration: Indefinitely
4. Actions → New → Start a program: `E:\IssuePing\.venv\Scripts\python.exe` → Add arguments: `-m issueping` → Start in: `E:\IssuePing`
5. Conditions/Settings: adjust restart on failure and allow task on demand

Or run the non-admin schtasks command (from project root):

```powershell
schtasks /Create /SC MINUTE /MO 10 /TN "IssuePing" /TR "Powershell -NoProfile -ExecutionPolicy Bypass -File \"E:\IssuePing\run_issueping.ps1\"" /F
```

To test immediately:

```powershell
schtasks /Run /TN "IssuePing"
```

To remove the task:

```powershell
schtasks /Delete /TN "IssuePing" /F
```

---

## Implemented improvements in this workspace

- `.env` auto-loading using python-dotenv
- `--dry-run` CLI flag to print notifications instead of sending
- `run_issueping.ps1` wrapper to run from Task Scheduler
- `register_task_safe.ps1` and `register_task_nonadmin.ps1` helper scripts for scheduling
- `.env.example` file

## Feature ideas / next steps

If you want me to implement a feature next, here are recommended starters:
- `--verbose` logging (prints HTTP request/response)
- `--test-telegram` one-off message sender
- Digest mode (daily summary)
- Unit tests and GitHub Actions CI

---

If you'd like, I can: create the scheduled task for you (already added helper scripts), add `--verbose` logging, or implement any other feature from the list above.


## Local testing (using .env and dry-run)

If you want to run IssuePing locally to test configuration and message formatting without sending real notifications, use a `.env` file and the `--dry-run` flag.

1. Create a `.env` file in the project root with any secrets you want to test. Example:

```dotenv
GITHUB_TOKEN=ghp_xxx...    # optional, increases rate limits
TELEGRAM_BOT_TOKEN=12345:ABCDEF
TELEGRAM_CHAT_ID=987654321
SENDGRID_API_KEY=SG.xxxxx
EMAIL_TO=you@example.com
EMAIL_FROM=sender@example.com
```

2. Activate your virtualenv and run in dry-run mode:

```powershell
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip install -e .
python -m issueping --dry-run
```

This will print the notifications the tool would send, without calling Telegram or SendGrid. It's a safe way to check formatting and matching issues.

## Example Notification

**Telegram:**

```
[facebook/react] New issue: Fix component crash (#12345)
Labels: good-first-issue
https://github.com/facebook/react/issues/12345
```

**Email:**
Subject: New issue in facebook/react: Fix component crash

Body:

```
Repo: facebook/react
Title: Fix component crash
Labels: good-first-issue

Link: https://github.com/facebook/react/issues/12345
```

## Troubleshooting

### Workflow not running automatically?
- Make sure your repository has recent activity (make an empty commit)
- Check if Actions are enabled in your fork
- Verify the cron schedule is correct
- **Note**: Private repos have 2000 minutes/month Actions limit. Make your fork public for unlimited usage.

### Not receiving notifications?
- Verify all secrets are correctly set
- For Telegram: Make sure you've messaged your bot at least once
- For SendGrid: Verify your sender email is authenticated
- Check the workflow logs for error messages

### Getting too many/few notifications?
- Adjust the labels in `config/repos.json`
- The tool only sends unassigned issues
- Check if repositories have issues with your specified labels

## FAQ

**Q: How often does it check for new issues?**
A: Every 10 minutes by default. You can change this in `.github/workflows/watch-issues.yml`.

**Q: Will I get duplicate notifications?**
A: No! The tool remembers which issues it has already notified you about.

**Q: Does it work with private repositories?**
A: Yes, as long as your GitHub token has access to them.

**Q: Can I use both Telegram and Email?**
A: Yes! Configure both and you'll receive notifications on both channels.

**Q: What if I want to stop notifications temporarily?**
A: Go to Actions → IssuePing Watch → "..." → "Disable workflow"

## Future Roadmap

* Digest mode (daily or weekly summaries)
* Opt-in auto-comment feature for github issues
* GitHub App integration for faster real-time updates
* AI features to get automatically get a user's skills and get them the matching issues/repos

## Contributing

We welcome contributions of any kind: improvements, new features.

## Security

Never expose your tokens or API keys in code or logs. All secrets must be stored in GitHub Secrets.
