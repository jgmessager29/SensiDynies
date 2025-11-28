# SensiDynies Discord Bot

## Overview
SensiDynies is a Discord bot built with Python and the discord.py library. It provides basic bot functionality including ping/pong commands, server information, and customizable presence status.

## Project Structure
```
.
├── main.py          # Main bot entry point
├── .gitignore       # Git ignore file
├── pyproject.toml   # Python project configuration
└── replit.md        # This documentation file
```

## Features
- **Bot Connection**: Automatic connection to Discord using bot token
- **Ping Command**: `!ping` - Check bot latency
- **Hello Command**: `!hello` - Get a friendly greeting
- **Info Command**: `!info` - Display bot information in an embed
- **Custom Presence**: Bot shows "Watching for !ping commands" status
- **Error Handling**: Graceful handling of command errors

## Commands
| Command | Description |
|---------|-------------|
| `!ping` | Check if the bot is responsive and see latency |
| `!hello` | Get a friendly greeting from the bot |
| `!info` | Display bot information |
| `!help` | Show list of available commands |

## Setup Instructions

### 1. Get Your Discord Bot Token
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application or select an existing one
3. Go to the "Bot" section
4. Click "Reset Token" to generate a new token
5. Copy the token

### 2. Configure Environment Variable
Set the `DISCORD_BOT_TOKEN` secret in Replit:
- The token should be stored as a secret for security

### 3. Enable Required Intents
In the Discord Developer Portal:
1. Go to your application's Bot settings
2. Enable "MESSAGE CONTENT INTENT" under Privileged Gateway Intents
3. Save changes

### 4. Invite the Bot to Your Server
1. Go to OAuth2 > URL Generator
2. Select scopes: `bot`, `applications.commands`
3. Select permissions: `Send Messages`, `Read Message History`, `Embed Links`
4. Copy the generated URL and open it to invite the bot

## Running the Bot
The bot runs automatically when you start the Replit. It will:
1. Load the Discord token from environment variables
2. Connect to Discord
3. Set the bot's presence status
4. Listen for commands

## Technical Details
- **Python Version**: 3.11+
- **Discord.py Version**: 2.6+
- **Command Prefix**: `!`

## Recent Changes
- November 27, 2025: Initial bot setup with basic commands

## User Preferences
- Bot name: SensiDynies
- Command prefix: `!`
- Standard API token approach (no special integrations)
