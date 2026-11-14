# Zyno's Crew Discord Bot

Zyno's Crew is a branded Discord bot for a YouTube creator community, with slash commands, social link sharing, welcome messages, and moderator announcements.

## Install

1. Install Python 3.10 or newer.
2. Create a Discord application and bot in the Discord Developer Portal.
3. Copy `.env.example` to `.env`.
4. Set `DISCORD_TOKEN` in `.env` to your bot token. Keep the token private.
5. Configure `CHANNEL_NAME`, `YOUTUBE_URL`, and any optional social links.
6. Optionally set `WELCOME_CHANNEL_ID` and `ANNOUNCEMENT_CHANNEL_ID` to Discord text channel IDs.
7. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

8. Invite the bot using the `bot` and `applications.commands` scopes.
9. Give the bot View Channels, Send Messages, and Embed Links permissions. It also needs permission to send messages in the configured welcome and announcement channels.
10. Enable the Server Members Intent in the Discord Developer Portal if you want welcome messages.
11. Start the bot:

   ```bash
   python main.py
   ```

## Use

Use the following slash commands in your Discord server:

- `/zyno` displays the branded community welcome card and YouTube link.
- `/youtube` displays the configured YouTube channel link.
- `/socials` displays the configured YouTube, Instagram, TikTok, and Discord invite links.
- `/announce message` posts a branded announcement in the configured announcement channel. The user must have Manage Messages permission.
- `/help` displays the available commands.

Slash commands may take a short time to appear after the bot first starts because they are synchronized globally. Enable Developer Mode in Discord to copy channel IDs.

---

More Discord bot projects by EnderDevelopment: https://github.com/EnderDevelopment

Project page: https://dash.enderdevelopment.com/community/3ac3c2a9-e48b-4a62-9ba7-c8d05d17b4ac?utm_source=github&utm_medium=readme&utm_campaign=auto_publish&utm_content=3ac3c2a9-e48b-4a62-9ba7-c8d05d17b4ac
