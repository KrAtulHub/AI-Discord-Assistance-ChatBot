# AI Discord Assistance Bot

Simple Discord bot that connects to OpenRouter for AI responses and Tavily for web search.

## Project structure

- `bot.py` – main bot code
- `.env` – secrets (Discord token, OpenRouter key, Tavily key)
- `requirements.txt` – Python dependencies
- `logs/` – runtime logs (`bot.log`)

## Setup

1. Create and fill `.env`:

   ```env
   DISCORD_API_KEY=YOUR_DISCORD_BOT_TOKEN
   OPENROUTER_API_KEY=YOUR_OPENROUTER_KEY
   TAVILY_API_KEY=YOUR_TAVILY_KEY
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the bot:

   ```bash
   python bot.py
   ```

## Usage

- Just type a normal message and the bot will answer with AI.
- `!ai question` – explicit AI command with cooldown.
- `!web question` – AI answer using live web search.
- `!ping` – health check.

