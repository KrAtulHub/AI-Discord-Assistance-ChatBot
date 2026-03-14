import discord
import asyncio
import logging
import os
import time
from datetime import datetime

import requests
from aiohttp import web
from discord.ext import commands
from openai import OpenAI
from dotenv import load_dotenv

# -------------------------
# Config & setup
# -------------------------

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not DISCORD_TOKEN:
    raise ValueError("DISCORD_API_KEY missing in .env")
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY missing in .env")

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, "bot.log"), encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger("discord-bot")

COOLDOWN_SECONDS = 5
_last_message_ts: dict[int, float] = {}

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

ai_client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_API_KEY)


def tavily_search(query: str) -> str:
    """Use Tavily to search the web and return a short text summary."""
    if not TAVILY_API_KEY:
        return "Web search API key (TAVILY_API_KEY) is missing."

    try:
        resp = requests.post(
            "https://api.tavily.com/search",
            json={
                "api_key": TAVILY_API_KEY,
                "query": query,
                "max_results": 5,
            },
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()
        results = data.get("results", [])
        if not results:
            return "No web results found."

        snippets: list[str] = []
        for r in results:
            text = r.get("content") or r.get("snippet") or ""
            if text:
                snippets.append(text.strip())

        combined = "\n\n".join(snippets)
        return combined[:3000]
    except Exception as e:
        log.warning("Tavily search failed: %s", e)
        return "Web search failed."


async def send_long_message(channel: discord.abc.Messageable, content: str) -> None:
    """Send content in chunks under Discord's 2000 char limit."""
    max_len = 1900
    text = content.strip()
    while text:
        if len(text) <= max_len:
            await channel.send(text)
            break
        split_at = text.rfind("\n", 0, max_len)
        if split_at == -1:
            split_at = max_len
        chunk, text = text[:split_at], text[split_at:]
        await channel.send(chunk.strip())


async def call_openrouter(question: str, web_context: str | None = None) -> str:
    """Call OpenRouter using the free-model router, with optional web context."""
    system_prompt = (
        "You are a helpful, concise assistant. "
        "Use bullet points and short paragraphs. "
        "Avoid greetings and sign-offs. "
        "Do not answer with unsafe or illegal instructions."
    )

    messages: list[dict[str, str]] = [{"role": "system", "content": system_prompt}]

    if web_context:
        user_content = f"Question: {question}\n\nWeb search results:\n{web_context}"
    else:
        user_content = question

    messages.append({"role": "user", "content": user_content})

    try:
        response = await asyncio.to_thread(
            ai_client.chat.completions.create,
            model="openrouter/free",
            messages=messages,
        )
        content = response.choices[0].message.content
        if not content or not content.strip():
            return "⚠️ I couldn't generate a useful answer. Please try rephrasing your question."
        return content.strip()
    except Exception as e:
        text = str(e)
        log.error("OpenRouter API error: %s", text)

        low = text.lower()
        if "429" in low or "rate" in low:
            return "⚠️ I'm being rate-limited by the AI API. Please wait a few seconds and try again."
        if "503" in low or "unavailable" in low:
            return "⚠️ The AI service is temporarily unavailable. Please try again later."

        return "⚠️ AI API error. Please try again in a moment."


async def handle_ai_question(
    channel: discord.abc.Messageable,
    author: discord.abc.User,
    question: str,
    use_web: bool = False,
) -> None:
    """Shared logic to handle AI or AI+web questions."""
    log.info("User %s asked (%s): %s", author, "web" if use_web else "ai", question)

    lower_q = question.lower()
    if "today" in lower_q and "date" in lower_q:
        today = datetime.now().strftime("%B %d, %Y")
        await channel.send(f"Today is **{today}**.")
        return

    await channel.send("🤖 Thinking...")

    web_context = None
    if use_web:
        await channel.send("🌐 Searching the web...")
        web_context = tavily_search(question)

    answer = await call_openrouter(question, web_context=web_context)
    await send_long_message(channel, answer)


@bot.event
async def on_ready():
    log.info("Bot connected as %s", bot.user)


@bot.command(name="ping")
async def ping(ctx: commands.Context):
    await ctx.send("pong")


@bot.command(name="ai")
@commands.cooldown(1, COOLDOWN_SECONDS, commands.BucketType.user)
async def ai_cmd(ctx: commands.Context, *, question: str | None = None):
    if not question:
        await ctx.send("⚠️ Please type your question after the command, or just chat without `!ai`.")
        return
    await handle_ai_question(ctx.channel, ctx.author, question, use_web=False)


@bot.command(name="web")
@commands.cooldown(1, COOLDOWN_SECONDS, commands.BucketType.user)
async def web_cmd(ctx: commands.Context, *, question: str | None = None):
    if not question:
        await ctx.send("⚠️ Ask a question after `!web` so I know what to search for.")
        return
    await handle_ai_question(ctx.channel, ctx.author, question, use_web=True)


@ai_cmd.error
@web_cmd.error
async def command_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"⏳ Slow down! Try again in {error.retry_after:.1f} seconds.")
        return
    log.warning("Command error for %s: %s", ctx.command, error)
    await ctx.send("⚠️ Something went wrong handling that command.")


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    await bot.process_commands(message)

    if message.content.startswith("!"):
        return

    question = message.content.strip()
    if not question:
        return

    now = time.time()
    last = _last_message_ts.get(message.author.id, 0)
    if now - last < COOLDOWN_SECONDS:
        return
    _last_message_ts[message.author.id] = now

    await handle_ai_question(message.channel, message.author, question, use_web=False)


async def health_check(request: web.Request) -> web.Response:
    return web.Response(text="OK")


async def start_web_server() -> None:
    app = web.Application()
    app.router.add_get("/", health_check)
    app.router.add_get("/health", health_check)
    port = int(os.getenv("PORT", 8080))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    log.info("Health check server started on port %d", port)


async def main() -> None:
    await start_web_server()
    await bot.start(DISCORD_TOKEN)


asyncio.run(main())