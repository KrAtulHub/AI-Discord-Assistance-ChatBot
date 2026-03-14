# AI Discord Assistance ChatBot
Intelligent Discord chatbot powered by **OpenRouter** (free models) and **Tavily** web search.  
Just drop it into your server and get smart, up‑to‑date answers in any channel.
---
### ✨ Features
- **Chat without prefixes**  
  - Bot answers normal messages directly (no need for `!ai` every time).
- **Command framework (`discord.ext.commands`)**  
  - Clean, extensible structure with `!ai`, `!web`, `!ping` commands.
- **Free & auto‑updated models**  
  - Uses OpenRouter’s `openrouter/free` router to always pick a current free model.
- **Live internet search**  
  - `!web` uses Tavily to fetch fresh information from the web.
- **Rate‑limits & safety**  
  - Per‑user cooldowns, friendly rate‑limit messages, and basic safety guardrails.
- **Nice formatting**  
  - Long replies are automatically split under Discord’s 2000‑character limit.
- **Logging**  
  - Logs all activity and errors to `logs/bot.log` for easy debugging.
---
### 📁 Project structure
- `bot.py` – main Discord bot (commands, AI, Tavily, logging, cooldowns)
- `.env` – secrets (not committed to git)
- `requirements.txt` – Python dependencies
- `logs/` – runtime logs (`bot.log`, auto‑created)
- `.gitignore` – ignores `.env`, venvs, caches, and logs
---
### 🔧 Prerequisites
- Python **3.10+**
- A **Discord bot** application and token  
  (from the [Discord Developer Portal](https://discord.com/developers/applications))
- An **OpenRouter API key** (`https://openrouter.ai`)
- A **Tavily API key** (`https://app.tavily.com`)
In your bot’s settings (Developer Portal → Bot):
- Enable **Message Content Intent** under *Privileged Gateway Intents*.
- Invite the bot to your server with permissions to **read** and **send** messages.
---
### ⚙️ Setup
1. **Clone this repo**
   ```bash
   git clone https://github.com/KrAtulHub/AI-Discord-Assistance-ChatBot.git
   cd AI-Discord-Assistance-ChatBot
Create and fill .env

DISCORD_API_KEY=YOUR_DISCORD_BOT_TOKEN
OPENROUTER_API_KEY=YOUR_OPENROUTER_KEY
TAVILY_API_KEY=YOUR_TAVILY_KEY
Install dependencies

pip install -r requirements.txt
Run the bot

python bot.py
If everything is correct, you should see logs like:

Bot connected as ...
Shard ID None has connected to Gateway ...
💬 Usage
You can interact with the bot in two ways:

1. Natural chat (no prefix)
Just type a message in any channel where the bot can read:

Explain what a database is
How do I center a div in CSS?
Write a short motivational quote
The bot will reply using AI (with per‑user cooldown to avoid spam).

2. Commands
!ai <question> – Explicit AI command

Example:
!ai summarize the latest Union Budget of India
!web <question> – AI + live web search

Example:
!web latest news about AI regulation in 2026
The bot:

Calls Tavily to fetch relevant pages.
Sends the combined web context to the AI.
Returns an up‑to‑date, concise answer.
!ping – Health check

Responds with pong if the bot is alive.
🧠 How it works
Discord layer

Uses discord.py and commands.Bot for clean command handling.
on_message:
Processes commands.
If message doesn’t start with !, treats it as an AI question (with cooldown).
AI layer (OpenRouter)

Uses openrouter/free router:
Always picks a currently available free model.
System prompt enforces:
Concise answers
Bullet points and short paragraphs
No greetings/sign‑offs
Basic safety restrictions
Web layer (Tavily)

!web calls Tavily’s search API with your TAVILY_API_KEY.
Extracts snippets and passes them as context to the AI for fresher answers.
Resilience

Friendly messages for:
Rate limits (429)
Temporary outages (503)
Empty AI responses
📝 Logging
All logs go to:

Console, and
logs/bot.log
Includes:

Startup info
User questions (anonymized to Discord usernames)
Errors from Tavily/OpenRouter
You can tail the log while debugging:

tail -f logs/bot.log
🚀 Ideas for improvement
Restrict AI replies to specific channels only.
Add slash commands (/ask, /web) with Discord’s interactions API.
Add per‑guild configuration (prefix, cooldowns, allowed channels).
Add support for function calling / tools via OpenRouter.
🤝 License
Use, modify, and extend this bot freely in your own servers.
If you find it useful, a ⭐ on the GitHub repo is always appreciated!
