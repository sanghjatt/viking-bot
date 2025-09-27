import random
from pyrogram import Client, filters
from pyrogram.types import ChatPermissions
from flask import Flask
from threading import Thread

app_web = Flask('')

@app_web.route('/')
def home():
    return "Viking Bot is alive!"

def run():
    app_web.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
    
# Initialize bot
app = Client(
    "viking_bot",
    api_id=24206775,  # ✅ your API ID (integer, no quotes)
    api_hash="ca0e7556d7bcb2cda125b2828a9e9444",  # ✅ your API hash (string)
    bot_token="8407292379:AAH-qdXxDsk_9xmUvnG3PWKNhrGb34zWlNs"  # ✅ your bot token
)

# --- Commands ---

# /start
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("🛡 Welcome, warrior! The gates of Valhalla await your deeds.")

# /ping
@app.on_message(filters.command("ping"))
async def ping(client, message):
    await message.reply_text("⚡ The ravens return swiftly — bot is alive!")

# /info
@app.on_message(filters.command("info"))
async def info(client, message):
    await message.reply_text("🧠 *Ragnar Lothbrok*: A legendary Norse hero, king, and warrior — destined for Valhalla!")

# /banhammer
@app.on_message(filters.command("banhammer") & filters.group)
async def banhammer(client, message):
    if not message.from_user:
        return await message.reply("⚠️ You must be a human to use this!")
    member = await client.get_chat_member(message.chat.id, message.from_user.id)
    if member.status not in ["administrator", "owner"]:
        return await message.reply("⚠️ Only clan chiefs may cast the banhammer!")
    if not message.reply_to_message:
        return await message.reply("⚔️ Reply to the enemy you wish to banish!")
    await client.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    await message.reply(f"💀 {message.reply_to_message.from_user.mention} was banished from the clan!")

# /callback (unban)
@app.on_message(filters.command("callback") & filters.group)
async def callback(client, message):
    member = await client.get_chat_member(message.chat.id, message.from_user.id)
    if member.status not in ["administrator", "owner"]:
        return await message.reply("⚠️ Only clan chiefs can call back fallen warriors!")
    if not message.reply_to_message:
        return await message.reply("🕊 Reply to a warrior to call them back to the clan.")
    user_id = message.reply_to_message.from_user.id
    await client.unban_chat_member(message.chat.id, user_id)
    await message.reply(f"🕊 {message.reply_to_message.from_user.mention} has been called back to Valhalla!")

# /clan
@app.on_message(filters.command("clan") & filters.group)
async def clan(client, message):
    admins = await client.get_chat_administrators(message.chat.id)
    text = "⚔️ Clan Chiefs:\n"
    for admin in admins:
        text += f"• {admin.user.mention}\n"
    await message.reply(text)

# /raven
@app.on_message(filters.command("raven"))
async def raven(client, message):
    user = message.from_user
    text = f"🕊 Raven Report:\n\n⚔️ Name: {user.first_name}\n🧙 ID: `{user.id}`\n🏰 Username: @{user.username if user.username else 'None'}"
    await message.reply(text)

# /rune
@app.on_message(filters.command("rune"))
async def rune(client, message):
    runes = [
        "ᚠ Fehu - Wealth and Prosperity",
        "ᚢ Uruz - Strength and Power",
        "ᚦ Thurisaz - Protection and Challenges",
        "ᚨ Ansuz - Wisdom and Communication",
        "ᚱ Raido - Journey and Movement",
        "ᚺ Hagalaz - Transformation through Trials",
    ]
    rune = random.choice(runes)
    await message.reply(f"🔮 Rune Cast: {rune}")

# /stats
groups = set()
users = set()

@app.on_message(filters.command("stats"))
async def stats(client, message):
 if message.from_user.id != 7908917401:
    return await message.reply("⚠️ Only the Allfather can view these stats!")
    await message.reply(f"📊 *Clan Stats:*\n🏰 Groups: {len(groups)}\n🧝 Users: {len(users)}")

@app.on_message(filters.group)
async def track_groups(client, message):
    groups.add(message.chat.id)

@app.on_message(filters.private)
async def track_users(client, message):
    users.add(message.from_user.id)

# /help
@app.on_message(filters.command("help"))
async def help_cmd(client, message):
    help_text = (
        "🧭 *Viking Bot Commands:*\n\n"
        "/start - to start the bot\n"
        "/ping - to check if bot is alive\n"
        "/info - biography of Ragnar Lothbrok\n"
        "/banhammer - ban a user\n"
        "/callback - unban a user\n"
        "/clan - check who are the clan chiefs\n"
        "/raven - user’s info\n"
        "/rune - random Viking rune\n"
        "/stats - clan statistics (only Allfather)\n\n"
        "⚔️ For more help, summon the Allfather: [Message Owner](https://t.me/sanghajatt)"
    )
    await message.reply(help_text, disable_web_page_preview=True)

# /mute
@app.on_message(filters.command("mute") & filters.group)
async def mute_user(client, message):
    member = await client.get_chat_member(message.chat.id, message.from_user.id)
    if member.status not in ["administrator", "owner"]:
        return await message.reply("⚠️ Only clan chiefs can silence a warrior.")
    if not message.reply_to_message:
        return await message.reply("⚔️ Reply to a warrior to silence them.")
    await client.restrict_chat_member(
        message.chat.id,
        message.reply_to_message.from_user.id,
        ChatPermissions()
    )
    await message.reply(f"🔕 {message.reply_to_message.from_user.mention} has been silenced by the chief!")

# /unmute
@app.on_message(filters.command("unmute") & filters.group)
async def unmute_user(client, message):
    member = await client.get_chat_member(message.chat.id, message.from_user.id)
    if member.status not in ["administrator", "owner"]:
        return await message.reply("⚠️ Only clan chiefs can restore voices.")
    if not message.reply_to_message:
        return await message.reply("⚔️ Reply to a warrior to restore their voice.")
    await client.restrict_chat_member(
        message.chat.id,
        message.reply_to_message.from_user.id,
        ChatPermissions(can_send_messages=True)
    )
    await message.reply(f"🔊 {message.reply_to_message.from_user.mention} may now speak again!")

# /duel
@app.on_message(filters.command("duel") & filters.group)
async def duel(client, message):
    if not message.reply_to_message:
        return await message.reply("⚔️ Reply to challenge a warrior to a duel!")
    challenger = message.from_user.first_name
    opponent = message.reply_to_message.from_user.first_name
    winner = random.choice([challenger, opponent])
    await message.reply(f"🩸 The duel begins between {challenger} and {opponent}!\n🏆 {winner} emerges victorious!")

# Run bot
app.run()
