import os
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("COMMAND_PREFIX", "!")
CHANNEL_NAME = os.getenv("CHANNEL_NAME", "Zyno")
YOUTUBE_URL = os.getenv("YOUTUBE_URL", "https://youtube.com/@yourchannel")
INSTAGRAM_URL = os.getenv("INSTAGRAM_URL", "")
TIKTOK_URL = os.getenv("TIKTOK_URL", "")
DISCORD_INVITE_URL = os.getenv("DISCORD_INVITE_URL", "")
WELCOME_CHANNEL_ID = os.getenv("WELCOME_CHANNEL_ID", "")
ANNOUNCEMENT_CHANNEL_ID = os.getenv("ANNOUNCEMENT_CHANNEL_ID", "")

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN is missing. Add it to your .env file.")


def channel_id_from(value: str) -> Optional[int]:
    """Convert an optional channel ID into an integer."""
    if not value.strip():
        return None
    try:
        return int(value)
    except ValueError:
        raise RuntimeError(f"Invalid channel ID: {value}") from None


WELCOME_CHANNEL = channel_id_from(WELCOME_CHANNEL_ID)
ANNOUNCEMENT_CHANNEL = channel_id_from(ANNOUNCEMENT_CHANNEL_ID)

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(
    command_prefix=PREFIX,
    intents=intents,
    help_command=None,
    description=f"The official {CHANNEL_NAME} community bot.",
)


def brand_embed(title: str, description: str) -> discord.Embed:
    """Create a consistent Zyno themed embed."""
    embed = discord.Embed(
        title=f"{CHANNEL_NAME} | {title}",
        description=description,
        color=discord.Color.from_rgb(124, 92, 255),
    )
    embed.set_footer(text=f"Built for the {CHANNEL_NAME} community")
    return embed


@bot.event
async def on_ready() -> None:
    """Log in and publish the slash commands."""
    if bot.user is None:
        return
    try:
        synced = await bot.tree.sync()
        print(f"Logged in as {bot.user} | synced {len(synced)} slash commands")
    except discord.HTTPException as error:
        print(f"The bot is online, but slash command syncing failed: {error}")


@bot.event
async def on_member_join(member: discord.Member) -> None:
    """Welcome new members when a welcome channel is configured."""
    if WELCOME_CHANNEL is None:
        return
    channel = member.guild.get_channel(WELCOME_CHANNEL)
    if not isinstance(channel, discord.TextChannel):
        return
    embed = brand_embed(
        "Welcome",
        f"Welcome to the **{CHANNEL_NAME}** community, {member.mention}!\n"
        "Check out the latest videos and say hello.",
    )
    await channel.send(embed=embed)


@bot.tree.command(name="zyno", description="Show the Zyno community welcome card.")
async def zyno(interaction: discord.Interaction) -> None:
    embed = brand_embed(
        "Community Hub",
        f"Welcome to the official **{CHANNEL_NAME}** server.\n\n"
        "Watch the videos, meet the community, and stay tuned for the next upload.",
    )
    embed.add_field(name="YouTube", value=f"[Watch the channel]({YOUTUBE_URL})", inline=False)
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="youtube", description="Show the Zyno YouTube channel.")
async def youtube(interaction: discord.Interaction) -> None:
    embed = brand_embed(
        "YouTube",
        f"Catch the latest **{CHANNEL_NAME}** videos here:\n{YOUTUBE_URL}",
    )
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="socials", description="Show the configured Zyno social links.")
async def socials(interaction: discord.Interaction) -> None:
    links = []
    if YOUTUBE_URL:
        links.append(f"▶️ [YouTube]({YOUTUBE_URL})")
    if INSTAGRAM_URL:
        links.append(f"📸 [Instagram]({INSTAGRAM_URL})")
    if TIKTOK_URL:
        links.append(f"🎵 [TikTok]({TIKTOK_URL})")
    if DISCORD_INVITE_URL:
        links.append(f"💬 [Invite a friend]({DISCORD_INVITE_URL})")

    description = "\n".join(links) if links else "Add social URLs to the .env file to display them here."
    await interaction.response.send_message(embed=brand_embed("Socials", description))


@bot.tree.command(name="announce", description="Post a Zyno announcement in the configured channel.")
@app_commands.describe(message="The announcement text to publish")
@app_commands.checks.has_permissions(manage_messages=True)
async def announce(interaction: discord.Interaction, message: str) -> None:
    if ANNOUNCEMENT_CHANNEL is None:
        await interaction.response.send_message(
            "No announcement channel is configured. Set ANNOUNCEMENT_CHANNEL_ID in .env.",
            ephemeral=True,
        )
        return

    channel = interaction.guild.get_channel(ANNOUNCEMENT_CHANNEL) if interaction.guild else None
    if not isinstance(channel, discord.TextChannel):
        await interaction.response.send_message(
            "The configured announcement channel could not be found in this server.",
            ephemeral=True,
        )
        return

    embed = brand_embed("Announcement", message)
    embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
    await channel.send(embed=embed)
    await interaction.response.send_message(f"Announcement posted in {channel.mention}.", ephemeral=True)


@announce.error
async def announce_error(interaction: discord.Interaction, error: app_commands.AppCommandError) -> None:
    if isinstance(error, app_commands.MissingPermissions):
        message = "You need the Manage Messages permission to use this command."
    else:
        message = "I could not post that announcement. Check my channel permissions."

    if interaction.response.is_done():
        await interaction.followup.send(message, ephemeral=True)
    else:
        await interaction.response.send_message(message, ephemeral=True)


@bot.tree.command(name="help", description="Show the Zyno bot commands.")
async def help_command(interaction: discord.Interaction) -> None:
    embed = brand_embed(
        "Commands",
        "Use these commands to explore the community:",
    )
    embed.add_field(name="/zyno", value="Show the community welcome card.", inline=False)
    embed.add_field(name="/youtube", value="Get the YouTube channel link.", inline=False)
    embed.add_field(name="/socials", value="Show configured social links.", inline=False)
    embed.add_field(name="/announce", value="Post a moderator announcement.", inline=False)
    await interaction.response.send_message(embed=embed)


bot.run(TOKEN)
