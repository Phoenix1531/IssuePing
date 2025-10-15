# IssuePing

A simple &amp; powerful tool to help beginner and experienced developers contribute to open source without wasting hours searching for issues.

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
