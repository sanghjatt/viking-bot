#!/usr/bin/env python3
# ⚔️ Viking Bot - Render Deployment

import os
import random
import asyncio
from aiohttp import web
from pyrogram import Client, filters
from pyrogram.enums import ChatMembersFilter
from pyrogram import idle

# --- CONFIG ---
API_ID = int(os.getenv("API_ID", 24206775))
API_HASH = os.getenv("API_HASH", "ca0e7556d7bcb2cda125b2828a9e9444")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8407292379:AAH-qdXxDsk_9xmUvnG3PWKNhrGb34zWlNs")

# --- Keep Alive (Web Server) ---
async def handle(request):
    return web.Response(text="⚔️ Viking Bot is alive and ready for battle!")

async def run_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(os.getenv("PORT", 8080)))
    await site.start()

# --- Bot Setup ---
app = Client("viking", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- Commands ---
@app.on_message(filters.command("start"))
def start(client, message):
    message.reply_photo(
        photo="https://endtrz.vercel.app/46869768.jpg",
        caption="⚔️ Welcome, warrior! ⚔️\n\nSummon me with /ping, /info, /rune, or /raven."
    )

@app.on_message(filters.command("ping"))
def ping(client, message):
    message.reply_photo(
        photo="https://endtrz.vercel.app/e02b960b.jpg",
        caption="⚔️ By Odin’s beard! ⚔️\n\nThe ravens have flown — I am being ready for the fight, warrior! 🪓🔥"
    )

@app.on_message(filters.command("info"))
def info(client, message):
    message.reply_photo(
        photo="https://endtrz.vercel.app/11e9d2db.jpg",
        caption="༒︎The Great Viking༒︎\n\nI am Ragnar Lothbrok, born of legend and blood of Odin..."
    )

@app.on_message(filters.command("raven"))
def raven(client, message):
    user = message.reply_to_message.from_user if message.reply_to_message else message.from_user
    info = f"🪶 Raven’s Whisper:\n\nName: {user.first_name}\nUsername: @{user.username if user.username else 'N/A'}\nUser ID: {user.id}"
    message.reply_text(info)

@app.on_message(filters.command("banhammer") & filters.group)
async def banhammer(client, message):
    if not message.reply_to_message:
        return await message.reply_text("⚠️ Reply to the warrior you wish to cast out.")
    try:
        user = message.reply_to_message.from_user
        await client.ban_chat_member(message.chat.id, user.id)
        await message.reply_text(f"🔨 By Thor’s hammer, [{user.first_name}](tg://user?id={user.id}) has been cast out of Midgard!")
    except Exception as e:
        await message.reply_text(f"⚠️ Failed: {e}")

@app.on_message(filters.command("clan") & filters.group)
async def clan(client, message):
    try:
        admins = []
        async for member in client.get_chat_members(message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS):
            admins.append(member.user.first_name)
        text = "🛡️ Clan Chiefs:\n" + "\n".join(f"• {name}" for name in admins)
        await message.reply_text(text)
    except Exception as e:
        await message.reply_text(f"⚠️ Failed to summon clan chiefs: {e}")

# --- Runes ---
runes = [
    {"symbol": "ᚠ Fehu", "meaning": "Wealth & Prosperity", "desc": "🪙 Fortune & success", "image": "https://endtrz.vercel.app/ccf1bdb8.jpg"},
    {"symbol": "ᚢ Uruz", "meaning": "Strength & Endurance", "desc": "🐂 Rune of power", "image": "https://endtrz.vercel.app/5f4e3f2a.jpg"},
    {"symbol": "ᚦ Thurisaz", "meaning": "Protection & Challenge", "desc": "⚡ Trials & awakening", "image": "https://endtrz.vercel.app/0d1258ed.jpg"},
    {"symbol": "ᚨ Ansuz", "meaning": "Wisdom & Communication", "desc": "🪶 Rune of Odin", "image": "https://endtrz.vercel.app/1873432a.jpg"},
    {"symbol": "ᛉ Algiz", "meaning": "Protection & Defense", "desc": "🛡️ Shield against chaos", "image": "https://endtrz.vercel.app/5fb68124.jpg"},
    {"symbol": "ᛏ Tiwaz", "meaning": "Honor & Justice", "desc": "⚔️ Rune of Tyr", "image": "https://endtrz.vercel.app/02828827.jpg"},
    {"symbol": "ᛟ Othala", "meaning": "Heritage & Legacy", "desc": "🏰 Clan & home", "image": "https://endtrz.vercel.app/dc2606a3.jpg"},
]

@app.on_message(filters.command("rune"))
def rune(client, message):
    r = random.choice(runes)
    message.reply_photo(
        photo=r["image"],
        caption=f"🔮 **{r['symbol']}**\n**Meaning:** {r['meaning']}\n{r['desc']}"
    )

# --- Run Bot + Server ---
async def main():
    print("✅ Viking Bot marching on Render...")
    await asyncio.gather(run_server(), app.start())
    await idle()

asyncio.run(main())

if __name__ == "__main__":
    print("Viking bot started ✅")
    app.run()
