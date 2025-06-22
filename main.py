
from pyrogram import Client, filters
from config import *
import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
import asyncio

# Logger Setup
logging.basicConfig(level=logging.INFO)
LOGS = logging.getLogger("FindPartnerBot")

# MongoDB Setup with error check
try:
    mongo = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
    mongo.server_info()
    db = mongo["find_partner"]
    users = db["users"]
    LOGS.info("✅ MongoDB connected successfully.")
except ConnectionFailure as e:
    LOGS.error(f"❌ MongoDB connection failed: {e}")
    exit()

# Pyrogram Bot Setup
bot = Client(
    "FindPartnerBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins")
)

def format_reply(text):
    """Convert text to TinyCaps and format with bold"""
    tiny_caps_map = {
        'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ', 'f': 'ғ', 'g': 'ɢ', 'h': 'ʜ',
        'i': 'ɪ', 'j': 'ᴊ', 'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ', 'o': 'ᴏ', 'p': 'ᴘ',
        'q': 'ǫ', 'r': 'ʀ', 's': 's', 't': 'ᴛ', 'u': 'ᴜ', 'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x',
        'y': 'ʏ', 'z': 'ᴢ'
    }
    converted = ''.join(tiny_caps_map.get(char.lower(), char) for char in text)
    return f"❖ **{converted}**"

@bot.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    username = message.from_user.username or "None"

    user = users.find_one({"_id": user_id})

    if not user:
        users.insert_one({
            "_id": user_id,
            "name": first_name,
            "username": username,
            "coins": 100,  # Welcome bonus
            "gender": None,
            "age": None,
            "location": None,
            "interests": [],
            "premium": False,
            "vip_status": False,
            "ref_by": None,
            "ref_count": 0,
            "verified": False,
            "profile_photo": None,
            "relationship_status": "Single",
            "looking_for": None,
            "bio": "",
            "compatibility_score": 0,
            "matches_count": 0,
            "hearts_received": 0,
            "joined_at": str(datetime.now())
        })

        # Referral handling
        if len(message.command) > 1:
            try:
                referrer_id = int(message.command[1])
                if referrer_id != user_id:
                    ref_user = users.find_one({"_id": referrer_id})
                    if ref_user:
                        users.update_one({"_id": referrer_id}, {"$inc": {"coins": REFERRAL_COIN, "ref_count": 1}})
                        users.update_one({"_id": user_id}, {"$set": {"ref_by": referrer_id}})
                        await client.send_message(
                            referrer_id,
                            format_reply(f"ʏᴏᴜ ᴇᴀʀɴᴇᴅ {REFERRAL_COIN} ᴄᴏɪɴs ғᴏʀ ʀᴇғᴇʀʀɪɴɢ {first_name}! 🎉")
                        )
            except Exception as e:
                LOGS.warning(f"Referral error: {e}")

    # Premium Welcome Interface
    welcome_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💎 ᴘʀᴇᴍɪᴜᴍ ᴍᴀᴛᴄʜɪɴɢ", callback_data="premium_match"),
         InlineKeyboardButton("🎮 ɪɴʟɪɴᴇ ɢᴀᴍᴇs", callback_data="inline_games")],
        [InlineKeyboardButton("🔍 ғɪɴᴅ ᴘᴀʀᴛɴᴇʀ", callback_data="find_partner"),
         InlineKeyboardButton("👤 ᴍʏ ᴘʀᴏғɪʟᴇ", callback_data="view_profile")],
        [InlineKeyboardButton("💰 ᴇᴀʀɴ ᴄᴏɪɴs", callback_data="earn_coins"),
         InlineKeyboardButton("🏆 ᴠɪᴘ sᴛᴀᴛᴜs", callback_data="vip_status")],
        [InlineKeyboardButton("🌟 ᴅᴀɪʟʏ ʀᴇᴡᴀʀᴅs", callback_data="daily_rewards"),
         InlineKeyboardButton("📊 sᴛᴀᴛɪsᴛɪᴄs", callback_data="user_stats")],
        [InlineKeyboardButton("💌 ʟᴏᴠᴇ ʟᴇᴛᴛᴇʀs", callback_data="love_letters"),
         InlineKeyboardButton("🎯 ᴄᴏᴍᴘᴀᴛɪʙɪʟɪᴛʏ", callback_data="compatibility_test")]
    ])

    await message.reply_text(
        format_reply(f"ʜᴇʏ ɢᴏʀɢᴇᴏᴜs {first_name}! 😍\n\nᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ᴍᴏsᴛ ᴀᴅᴠᴀɴᴄᴇᴅ ᴅᴀᴛɪɴɢ ʙᴏᴛ! 💞\n\n✨ ɪ'ᴍ ʜᴇʀᴇ ᴛᴏ ʜᴇʟᴘ ʏᴏᴜ ғɪɴᴅ ʏᴏᴜʀ ᴘᴇʀғᴇᴄᴛ ᴍᴀᴛᴄʜ\n💎 ɢᴇᴛ ʀᴇᴀᴅʏ ғᴏʀ ᴀ ᴍᴀɢɪᴄᴀʟ ᴊᴏᴜʀɴᴇʏ ᴏғ ʟᴏᴠᴇ!"),
        reply_markup=welcome_keyboard,
        quote=True
    )

    # Send to log group
    try:
        await client.send_message(
            LOG_GROUP_ID,
            f"#NEW_GORGEOUS_USER 💎\nID: `{user_id}`\nName: [{first_name}](tg://user?id={user_id})\nUsername: @{username}"
        )
    except Exception as e:
        LOGS.warning(f"Log group error: {e}")

# Load all modules
try:
    from admin import commands
except Exception as e:
    LOGS.warning(f"Admin module not loaded: {e}")

if __name__ == "__main__":
    LOGS.info("✅ Advanced Dating Bot is starting...")
    bot.run()
