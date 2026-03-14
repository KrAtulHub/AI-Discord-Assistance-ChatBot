🤖 AI Discord Assistance ChatBot

Intelligent Discord bot powered by OpenRouter (free models) and Tavily web search.
Add it to your server and get smart, up-to-date answers in any channel.

➕ Invite Bot to Your Server === https://discord.com/channels/1482285214557409282/1482344434380177573

✨ Features

Natural chat: AI answers messages without requiring !ai every time

Command framework: !ai, !web, !ping for structured interactions

Live internet search: !web fetches fresh data from Tavily

Free & auto-updated models: Always uses a current free OpenRouter model

Safety & rate limits: Per-user cooldowns and error handling

Logging: Full logs at logs/bot.log for debugging

📁 Project Structure

bot.py – Main bot logic

.env – API keys (not committed)

requirements.txt – Dependencies

logs/ – Runtime logs (bot.log)

.gitignore – Ignores .env, venvs, caches, logs

⚙️ Setup

Clone repo:

git clone https://github.com/KrAtulHub/AI-Discord-Assistance-ChatBot.git
cd AI-Discord-Assistance-ChatBot

Create .env:

DISCORD_API_KEY=YOUR_DISCORD_BOT_TOKEN
OPENROUTER_API_KEY=YOUR_OPENROUTER_KEY
TAVILY_API_KEY=YOUR_TAVILY_KEY

Install dependencies:

pip install -r requirements.txt

Run bot:

python bot.py

You should see: Bot connected as ...

💬 Usage

1. Natural Chat (no prefix)
Just type in any channel the bot can read:

Explain what a database is
How do I center a div in CSS?
Write a motivational quote

2. Commands

!ai <question> – Ask AI directly

!web <query> – AI + live web search

!ping – Health check

🧠 How It Works

Discord Layer: discord.py with commands.Bot

AI Layer: OpenRouter openrouter/free for concise answers

Web Layer: Tavily fetches snippets for up-to-date context

Resilience: Friendly messages for rate limits, errors, or empty responses

🚀 Ideas to Improve

Restrict replies to certain channels

Add slash commands (/ask, /web)

Per-guild customization: prefixes, cooldowns, allowed channels

Integrate OpenRouter function calling

🤝 License

Free to use, modify, and extend. If helpful, leave a ⭐ on GitHub!
