# IssuePing

A simple &amp; powerful tool to help beginner and experienced developers contribute to open source without wasting hours searching for issues.

## Problem Statement

For many developers, especially beginners, contributing to open source is exciting but overwhelming. They spend endless time refreshing repositories, scanning for the right labels, and checking if issues are already taken. During Hacktoberfest and other open source drives, this becomes even more frustrating because by the time you find the right issue, someone else might already be assigned. The result: lost motivation and wasted time.

## Inspiration

This project was born from the same struggle. As students and new contributors, we wanted to help but found ourselves chasing issues instead of solving them. The idea was simple: what if there was a way to **bring the issues to you**, instead of you chasing them? A tool that works quietly in the background, filters issues by your preferences, and instantly notifies you when something relevant appears.

We wanted to design something minimal, something that could be set up in minutes, without the complexity of running servers or managing heavy infrastructure. GitHub Actions gave us the perfect platform: free, reliable, and already familiar to developers.

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

* `TELEGRAM_BOT_TOKEN` (if using Telegram)
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
      "labels": ["hacktoberfest"]
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

## Roadmap

* Digest mode (daily or weekly summaries)
* Opt-in auto-comment feature
* GitHub App integration for faster real-time updates

## Contributing

We welcome contributions of any kind: improvements, new features, or better docs. See `CONTRIBUTING.md` for details.

## Security

Never expose your tokens or API keys in code or logs. All secrets must be stored in GitHub Secrets.

## License

MIT License
