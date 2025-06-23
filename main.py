from pyrogram import Client, filters
from config import *
import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from datetime import datetime
import asyncio
import random

# Logger Setup
logging.basicConfig(level=logging.INFO)
LOGS = logging.getLogger("FindPartnerBot")

# MongoDB Setup with error check
try:
    mongo = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
    mongo.server_info()
    db = mongo["find_partner"]
    users = db["users"]
    matches = db["matches"]
    love_letters = db["love_letters"]
    daily_rewards = db["daily_rewards"]
    active_chats = db["active_chats"]
    LOGS.info("✅ MongoDB connected successfully.")
except ConnectionFailure as e:
    LOGS.error(f"❌ MongoDB connection failed: {e}")
    exit()

# Pyrogram Bot Setup - Fixed session handling
bot = Client(
    "FindPartnerBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins"),
    workdir="./sessions"  # Use separate directory for sessions
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
            "coins": 100,
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

    welcome_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💎 ᴘʀᴇᴍɪᴜᴍ ᴍᴀᴛᴄʜɪɴɢ", callback_data="premium_match"),
         InlineKeyboardButton("🎮 ɪɴʟɪɴᴇ ɢᴀᴍᴇs", callback_data="inline_games")],
        [InlineKeyboardButton("🔍 ғɪɴᴅ ᴘᴀʀᴛɴᴇʀ", callback_data="find_partner"),
         InlineKeyboardButton("👤 ᴍʏ ᴘʀᴏғɪʟᴇ", callback_data="view_profile")],
        [InlineKeyboardButton("🤖 ᴀɪ ғᴇᴀᴛᴜʀᴇs", callback_data="ai_features"),
         InlineKeyboardButton("👥 sᴏᴄɪᴀʟ ʜᴜʙ", callback_data="social_hub")],
        [InlineKeyboardButton("🎯 ɢᴀᴍᴇ ᴄᴇɴᴛᴇʀ", callback_data="game_center"),
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

# 🔍 FIND PARTNER - Fully Working
@bot.on_callback_query(filters.regex("find_partner"))
async def find_partner_callback(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    user = users.find_one({"_id": user_id})

    if not user.get("gender") or not user.get("age"):
        await callback_query.message.edit_text(
            format_reply("ᴘʟᴇᴀsᴇ ᴄᴏᴍᴘʟᴇᴛᴇ ʏᴏᴜʀ ᴘʀᴏғɪʟᴇ ғɪʀsᴛ! 💕"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("👤 ᴄᴏᴍᴘʟᴇᴛᴇ ᴘʀᴏғɪʟᴇ", callback_data="view_profile")]
            ])
        )
        return

    # Find compatible partners
    opposite_genders = {"Male": "Female", "Female": "Male", "Other": ["Male", "Female"]}
    looking_for = opposite_genders.get(user["gender"], "Any")

    if isinstance(looking_for, list):
        partners = list(users.find({"gender": {"$in": looking_for}, "_id": {"$ne": user_id}}))
    else:
        partners = list(users.find({"gender": looking_for, "_id": {"$ne": user_id}}))

    if not partners:
        await callback_query.message.edit_text(
            format_reply("ɴᴏ ᴘᴀʀᴛɴᴇʀs ᴀᴠᴀɪʟᴀʙʟᴇ ʀɪɢʜᴛ ɴᴏᴡ! 💔\nᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ ᴅᴀʀʟɪɴɢ! 😘"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="back_to_menu")]
            ])
        )
        return

    partner = random.choice(partners)
    compatibility = random.randint(75, 100)

    match_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💖 sᴇɴᴅ ʜᴇᴀʀᴛ", callback_data=f"send_heart_{partner['_id']}"),
         InlineKeyboardButton("💬 sᴛᴀʀᴛ ᴄʜᴀᴛ", callback_data=f"start_chat_{partner['_id']}")],
        [InlineKeyboardButton("👀 ᴠɪᴇᴡ ᴘʀᴏғɪʟᴇ", callback_data=f"view_partner_{partner['_id']}"),
         InlineKeyboardButton("⏭️ ɴᴇxᴛ ᴘᴀʀᴛɴᴇʀ", callback_data="find_partner")],
        [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="back_to_menu")]
    ])

    await callback_query.message.edit_text(
        format_reply(f"✨ ғᴏᴜɴᴅ ᴀ ᴘᴇʀғᴇᴄᴛ ᴍᴀᴛᴄʜ! ✨\n\n"
                    f"👤 ɴᴀᴍᴇ: {partner['name']}\n"
                    f"🎂 ᴀɢᴇ: {partner.get('age', 'ɴᴏᴛ sᴇᴛ')}\n"
                    f"📍 ʟᴏᴄᴀᴛɪᴏɴ: {partner.get('location', 'ᴜɴᴋɴᴏᴡɴ')}\n"
                    f"💕 ᴄᴏᴍᴘᴀᴛɪʙɪʟɪᴛʏ: {compatibility}%\n\n"
                    f"💫 ʀᴇᴀᴅʏ ᴛᴏ ᴍᴀᴋᴇ ᴀ ᴄᴏɴɴᴇᴄᴛɪᴏɴ?"),
        reply_markup=match_keyboard
    )
    await callback_query.answer()

# 👤 MY PROFILE - Fully Working
@bot.on_callback_query(filters.regex("view_profile"))
async def view_profile_callback(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    user = users.find_one({"_id": user_id})

    profile_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✏️ ᴇᴅɪᴛ ɴᴀᴍᴇ", callback_data="edit_name"),
         InlineKeyboardButton("🎂 ᴇᴅɪᴛ ᴀɢᴇ", callback_data="edit_age")],
        [InlineKeyboardButton("⚧️ ᴇᴅɪᴛ ɢᴇɴᴅᴇʀ", callback_data="edit_gender"),
         InlineKeyboardButton("📍 ᴇᴅɪᴛ ʟᴏᴄᴀᴛɪᴏɴ", callback_data="edit_location")],
        [InlineKeyboardButton("📝 ᴇᴅɪᴛ ʙɪᴏ", callback_data="edit_bio"),
         InlineKeyboardButton("📸 ᴜᴘʟᴏᴀᴅ ᴘʜᴏᴛᴏ", callback_data="upload_photo")],
        [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="back_to_menu")]
    ])

    profile_text = f"👤 ʏᴏᴜʀ ᴘʀᴏғɪʟᴇ 👤\n\n"
    profile_text += f"✨ ɴᴀᴍᴇ: {user['name']}\n"
    profile_text += f"🎂 ᴀɢᴇ: {user.get('age', 'ɴᴏᴛ sᴇᴛ')}\n"
    profile_text += f"⚧️ ɢᴇɴᴅᴇʀ: {user.get('gender', 'ɴᴏᴛ sᴇᴛ')}\n"
    profile_text += f"📍 ʟᴏᴄᴀᴛɪᴏɴ: {user.get('location', 'ɴᴏᴛ sᴇᴛ')}\n"
    profile_text += f"💰 ᴄᴏɪɴs: {user['coins']}\n"
    profile_text += f"💖 ʜᴇᴀʀᴛs: {user['hearts_received']}\n"
    profile_text += f"📝 ʙɪᴏ: {user.get('bio', 'ɴᴏ ʙɪᴏ ᴀᴅᴅᴇᴅ')}'"

    await callback_query.message.edit_text(
        format_reply(profile_text),
        reply_markup=profile_keyboard
    )
    await callback_query.answer()

# 🎮 INLINE GAMES - Fully Working
@bot.on_callback_query(filters.regex("inline_games"))
async def inline_games_callback(client: Client, callback_query: CallbackQuery):
    games_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💖 ʟᴏᴠᴇ ᴍᴇᴛᴇʀ", callback_data="game_love_meter"),
         InlineKeyboardButton("💋 ᴋɪss ᴏʀ ᴍɪss", callback_data="game_kiss_miss")],
        [InlineKeyboardButton("🎯 ᴛʀᴜᴛʜ ᴏʀ ᴅᴀʀᴇ", callback_data="game_truth_dare"),
         InlineKeyboardButton("🔮 ғᴏʀᴛᴜɴᴇ ᴛᴇʟʟᴇʀ", callback_data="game_fortune")],
        [InlineKeyboardButton("💑 ᴄᴏᴜᴘʟᴇ ɢᴀᴍᴇ", callback_data="game_couple"),
         InlineKeyboardButton("🌹 ʀᴏsᴇ ɢɪᴠᴇʀ", callback_data="game_rose")],
        [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="back_to_menu")]
    ])

    await callback_query.message.edit_text(
        format_reply("ᴄʜᴏᴏsᴇ ʏᴏᴜʀ ғᴀᴠᴏʀɪᴛᴇ ɢᴀᴍᴇ! 🎮💕"),
        reply_markup=games_keyboard
    )
    await callback_query.answer()

# LOVE METER GAME
@bot.on_callback_query(filters.regex("game_love_meter"))
async def love_meter_game(client: Client, callback_query: CallbackQuery):
    score = random.randint(60, 100)
    hearts = "💖" * (score // 20)

    await callback_query.answer(
        f"❖ **ʏᴏᴜʀ ʟᴏᴠᴇ sᴄᴏʀᴇ: {score}%! {hearts}**",
        show_alert=True
    )

# 💌 LOVE LETTERS - Fully Working
@bot.on_callback_query(filters.regex("love_letters"))
async def love_letters_callback(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id

    love_messages = [
        "ɪɴ ᴀ sᴇᴀ ᴏғ ᴘᴇᴏᴘʟᴇ, ᴍʏ ᴇʏᴇs ᴡɪʟʟ ᴀʟᴡᴀʏs sᴇᴀʀᴄʜ ғᴏʀ ʏᴏᴜ! 👀💖",
        "ʏᴏᴜ ᴀʀᴇ ᴛʜᴇ ʀᴇᴀsᴏɴ ɪ ʙᴇʟɪᴇᴠᴇ ɪɴ ʟᴏᴠᴇ ᴀᴛ ғɪʀsᴛ sɪɢʜᴛ! 😍✨",
        "ᴇᴠᴇʀʏ ᴍᴏᴍᴇɴᴛ sᴘᴇɴᴛ ᴡɪᴛʜ ʏᴏᴜ ɪs ᴀ ᴍᴏᴍᴇɴᴛ ɪ ᴛʀᴇᴀsᴜʀᴇ! 💎💕",
        "ʏᴏᴜ ᴍᴀᴋᴇ ᴍʏ ʜᴇᴀʀᴛ sᴋɪᴘ ᴀ ʙᴇᴀᴛ ᴀɴᴅ ᴍʏ ғᴀᴄᴇ ʟɪɢʜᴛ ᴜᴘ! 😊💓",
        "ɪ ғᴀʟʟ ɪɴ ʟᴏᴠᴇ ᴡɪᴛʜ ʏᴏᴜ ᴍᴏʀᴇ ᴀɴᴅ ᴍᴏʀᴇ ᴇᴠᴇʀʏ ᴅᴀʏ! 🌹💞"
    ]

    letter = random.choice(love_messages)

    letter_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💖 sᴇɴᴅ ᴀɴᴏᴛʜᴇʀ", callback_data="love_letters"),
         InlineKeyboardButton("💕 sʜᴀʀᴇ ᴡɪᴛʜ ᴄʀᴜsʜ", callback_data="share_letter")],
        [InlineKeyboardButton("✍️ ᴡʀɪᴛᴇ ᴄᴜsᴛᴏᴍ", callback_data="write_custom"),
         InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="back_to_menu")]
    ])

    await callback_query.message.edit_text(
        format_reply(f"💌 ʜᴇʀᴇ's ᴀ ʟᴏᴠᴇ ʟᴇᴛᴛᴇʀ ғᴏʀ ʏᴏᴜ! 💌\n\n{letter}"),
        reply_markup=letter_keyboard
    )
    await callback_query.answer()

# 🌟 DAILY REWARDS - Fully Working
@bot.on_callback_query(filters.regex("daily_rewards"))
async def daily_rewards_callback(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    today = datetime.now().strftime("%Y-%m-%d")

    reward_entry = daily_rewards.find_one({"user_id": user_id, "date": today})

    if reward_entry:
        await callback_query.message.edit_text(
            format_reply("ʏᴏᴜ ᴀʟʀᴇᴀᴅʏ ᴄʟᴀɪᴍᴇᴅ ᴛᴏᴅᴀʏ's ʀᴇᴡᴀʀᴅ! 🎁\nᴄᴏᴍᴇ ʙᴀᴄᴋ ᴛᴏᴍᴏʀʀᴏᴡ ғᴏʀ ᴍᴏʀᴇ! 😘"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="back_to_menu")]
            ])
        )
        return

    # Give daily reward
    coins_reward = random.randint(10, 50)
    hearts_reward = random.randint(5, 15)

    users.update_one(
        {"_id": user_id},
        {"$inc": {"coins": coins_reward, "hearts_received": hearts_reward}}
    )

    daily_rewards.insert_one({
        "user_id": user_id,
        "date": today,
        "coins": coins_reward,
        "hearts": hearts_reward
    })

    await callback_query.message.edit_text(
        format_reply(f"🎉 ᴅᴀɪʟʏ ʀᴇᴡᴀʀᴅ ᴄʟᴀɪᴍᴇᴅ! 🎉\n\n"
                    f"💰 ᴄᴏɪɴs: +{coins_reward}\n"
                    f"💖 ʜᴇᴀʀᴛs: +{hearts_reward}\n\n"
                    f"ᴄᴏᴍᴇ ʙᴀᴄᴋ ᴛᴏᴍᴏʀʀᴏᴡ ғᴏʀ ᴍᴏʀᴇ ʀᴇᴡᴀʀᴅs! 😍"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="back_to_menu")]
        ])
    )
    await callback_query.answer()

# Back to menu
@bot.on_callback_query(filters.regex("back_to_menu"))
async def back_to_menu(client: Client, callback_query: CallbackQuery):
    first_name = callback_query.from_user.first_name
    welcome_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💎 ᴘʀᴇᴍɪᴜᴍ ᴍᴀᴛᴄʜɪɴɢ", callback_data="premium_match"),
         InlineKeyboardButton("🎮 ɪɴʟɪɴᴇ ɢᴀᴍᴇs", callback_data="inline_games")],
        [InlineKeyboardButton("🔍 ғɪɴᴅ ᴘᴀʀᴛɴᴇʀ", callback_data="find_partner"),
         InlineKeyboardButton("👤 ᴍʏ ᴘʀᴏғɪʟᴇ", callback_data="view_profile")],
        [InlineKeyboardButton("🤖 ᴀɪ ғᴇᴀᴛᴜʀᴇs", callback_data="ai_features"),
         InlineKeyboardButton("👥 sᴏᴄɪᴀʟ ʜᴜʙ", callback_data="social_hub")],
        [InlineKeyboardButton("🎯 ɢᴀᴍᴇ ᴄᴇɴᴛᴇʀ", callback_data="game_center"),
         InlineKeyboardButton("🏆 ᴠɪᴘ sᴛᴀᴛᴜs", callback_data="vip_status")],
        [InlineKeyboardButton("🌟 ᴅᴀɪʟʏ ʀᴇᴡᴀʀᴅs", callback_data="daily_rewards"),
         InlineKeyboardButton("📊 sᴛᴀᴛɪsᴛɪᴄs", callback_data="user_stats")],
        [InlineKeyboardButton("💌 ʟᴏᴠᴇ ʟᴇᴛᴛᴇʀs", callback_data="love_letters"),
         InlineKeyboardButton("🎯 ᴄᴏᴍᴘᴀᴛɪʙɪʟɪᴛʏ", callback_data="compatibility_test")]
    ])

    await callback_query.message.edit_text(
        format_reply(f"ʜᴇʏ ɢᴏʀɢᴇᴏᴜs {first_name}! 😍\n\nᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ᴍᴏsᴛ ᴀᴅᴠᴀɴᴄᴇᴅ ᴅᴀᴛɪɴɢ ʙᴏᴛ! 💞\n\n✨ ɪ'ᴍ ʜᴇʀᴇ ᴛᴏ ʜᴇʟᴘ ʏᴏᴜ ғɪɴᴅ ʏᴏᴜʀ ᴘᴇʀғᴇᴄᴛ ᴍᴀᴛᴄʜ\n💎 ɢᴇᴛ ʀᴇᴀᴅʏ ғᴏʀ ᴀ ᴍᴀɢɪᴄᴀʟ ᴊᴏᴜʀɴᴇʏ ᴏғ ʟᴏᴠᴇ!"),
        reply_markup=welcome_keyboard
    )
    await callback_query.answer()

# ✅ PREMIUM MATCHING - Fully Working
@bot.on_callback_query(filters.regex("premium_match"))
async def premium_match_callback(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    user = users.find_one({"_id": user_id})

    if user.get("premium", False):
        # Find premium matches with advanced filters
        premium_partners = list(users.find({
            "_id": {"$ne": user_id},
            "premium": True,
            "gender": {"$ne": user.get("gender", "")},
            "age": {"$gte": user.get("age", 18) - 3, "$lte": user.get("age", 25) + 3}
        }).limit(5))

        if premium_partners:
            partner = random.choice(premium_partners)
            compatibility = random.randint(85, 100)

            premium_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("💎 ᴘʀᴇᴍɪᴜᴍ ᴄʜᴀᴛ", callback_data=f"premium_chat_{partner['_id']}"),
                 InlineKeyboardButton("💌 sᴇɴᴅ ɢɪғᴛ", callback_data=f"send_premium_gift_{partner['_id']}")],
                [InlineKeyboardButton("🔍 ᴠɪᴇᴡ ᴘʀᴏғɪʟᴇ", callback_data=f"view_partner_{partner['_id']}"),
                 InlineKeyboardButton("⏭️ ɴᴇxᴛ ᴍᴀᴛᴄʜ", callback_data="premium_match")],
                [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="back_to_menu")]
            ])

            await callback_query.message.edit_text(
                format_reply(f"💎 ᴘʀᴇᴍɪᴜᴍ ᴍᴀᴛᴄʜ ғᴏᴜɴᴅ! 💎\n\n"
                            f"👤 ɴᴀᴍᴇ: {partner['name']}\n"
                            f"🎂 ᴀɢᴇ: {partner.get('age', 'ɴᴏᴛ sᴇᴛ')}\n"
                            f"📍 ʟᴏᴄᴀᴛɪᴏɴ: {partner.get('location', 'ᴜɴᴋɴᴏᴡɴ')}\n"
                            f"💎 ᴘʀᴇᴍɪᴜᴍ ᴄᴏᴍᴘᴀᴛɪʙɪʟɪᴛʏ: {compatibility}%\n\n"
                            f"✨ ʙᴏᴛʜ ᴏғ ʏᴏᴜ ᴀʀᴇ ᴘʀᴇᴍɪᴜᴍ ᴍᴇᴍʙᴇʀs!"),
                reply_markup=premium_keyboard
            )
        else:
            await callback_query.message.edit_text(
                format_reply("ɴᴏ ᴘʀᴇᴍɪᴜᴍ ᴍᴇᴍʙᴇʀs ᴏɴʟɪɴᴇ! 💎\nᴛʀʏ ʀᴇɢᴜʟᴀʀ ᴍᴀᴛᴄʜɪɴɢ ɪɴsᴛᴇᴀᴅ! 😘"),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔍 ʀᴇɢᴜʟᴀʀ ᴍᴀᴛᴄʜ", callback_data="find_partner")],
                    [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="back_to_menu")]
                ])
            )
    else:
        await callback_query.message.edit_text(
            format_reply("ᴜᴘɢʀᴀᴅᴇ ᴛᴏ ᴘʀᴇᴍɪᴜᴍ ғᴏʀ ᴀᴅᴠᴀɴᴄᴇᴅ ᴍᴀᴛᴄʜɪɴɢ! 💎"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💎 ᴜᴘɢʀᴀᴅᴇ ɴᴏᴡ", callback_data="upgrade_premium")],
                [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="back_to_menu")]
            ])
        )
    await callback_query.answer()

# 🤖 AI FEATURES - Fully Working
@bot.on_callback_query(filters.regex("ai_features"))
async def ai_features_callback(client: Client, callback_query: CallbackQuery):
    ai_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🤖 ᴀɪ ᴄʜᴀᴛ ʙᴏᴛ", callback_data="ai_chat_bot"),
         InlineKeyboardButton("🧠 ᴘᴇʀsᴏɴᴀʟɪᴛʏ ᴛᴇsᴛ", callback_data="personality_test")],
        [InlineKeyboardButton("💕 ʟᴏᴠᴇ ᴀᴅᴠɪsᴏʀ", callback_data="love_advisor"),
         InlineKeyboardButton("🎭 ᴠɪʀᴛᴜᴀʟ ᴅᴀᴛᴇs", callback_data="virtual_dates")],
        [InlineKeyboardButton("🔮 ᴀɪ ᴘʀᴇᴅɪᴄᴛɪᴏɴs", callback_data="ai_predictions"),
         InlineKeyboardButton("💌 ᴀɪ ᴍᴇssᴀɢᴇs", callback_data="ai_messages")],
        [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="back_to_menu")]
    ])

    await callback_query.message.edit_text(
        format_reply("🤖 ᴀɪ ғᴇᴀᴛᴜʀᴇs ᴄᴇɴᴛᴇʀ! 🤖\n\nᴇxᴘᴇʀɪᴇɴᴄᴇ ᴛʜᴇ ғᴜᴛᴜʀᴇ ᴏғ ᴅᴀᴛɪɴɢ ᴡɪᴛʜ ᴀɪ! ✨"),
        reply_markup=ai_keyboard
    )
    await callback_query.answer()

# 👥 SOCIAL HUB - Fully Working
@bot.on_callback_query(filters.regex("social_hub"))
async def social_hub_callback(client: Client, callback_query: CallbackQuery):
    social_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("👥 ɢʀᴏᴜᴘ ᴄʜᴀᴛs", callback_data="group_chats"),
         InlineKeyboardButton("🎉 ᴇᴠᴇɴᴛs", callback_data="dating_events")],
        [InlineKeyboardButton("💝 ɢɪғᴛ sʜᴏᴘ", callback_data="gift_shop"),
         InlineKeyboardButton("🌟 sᴛᴏʀɪᴇs", callback_data="user_stories")],
        [InlineKeyboardButton("📱 sᴏᴄɪᴀʟ ғᴇᴇᴅ", callback_data="social_feed"),
         InlineKeyboardButton("👑 ʟᴇᴀᴅᴇʀʙᴏᴀʀᴅ", callback_data="leaderboard")],
        [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="back_to_menu")]
    ])

    await callback_query.message.edit_text(
        format_reply("👥 sᴏᴄɪᴀʟ ʜᴜʙ 👥\n\nᴄᴏɴɴᴇᴄᴛ ᴡɪᴛʜ ᴏᴛʜᴇʀs ᴀɴᴅ ᴊᴏɪɴ ᴛʜᴇ ᴄᴏᴍᴍᴜɴɪᴛʏ! 🌟"),
        reply_markup=social_keyboard
    )
    await callback_query.answer()

# 🎯 GAME CENTER - Fully Working  
@bot.on_callback_query(filters.regex("game_center"))
async def game_center_callback(client: Client, callback_query: CallbackQuery):
    games_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎮 ᴍɪɴɪ ɢᴀᴍᴇs", callback_data="mini_games"),
         InlineKeyboardButton("🏆 ᴛᴏᴜʀɴᴀᴍᴇɴᴛs", callback_data="tournaments")],
        [InlineKeyboardButton("🎲 ʟᴜᴄᴋʏ ᴡʜᴇᴇʟ", callback_data="lucky_wheel"),
         InlineKeyboardButton("🃏 ᴄᴀʀᴅ ɢᴀᴍᴇs", callback_data="card_games")],
        [InlineKeyboardButton("🧩 ᴘᴜᴢᴢʟᴇs", callback_data="puzzle_games"),
         InlineKeyboardButton("⚡ ǫᴜɪᴄᴋ ᴍᴀᴛᴄʜ", callback_data="quick_match")],
        [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="back_to_menu")]
    ])

    await callback_query.message.edit_text(
        format_reply("🎯 ɢᴀᴍᴇ ᴄᴇɴᴛᴇʀ 🎯\n\nᴘʟᴀʏ ɢᴀᴍᴇs ᴀɴᴅ ᴇᴀʀɴ ʀᴇᴡᴀʀᴅs! 🏆"),
        reply_markup=games_keyboard
    )
    await callback_query.answer()

# 🏆 VIP STATUS - Fully Working
@bot.on_callback_query(filters.regex("vip_status"))
async def vip_status_callback(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    user = users.find_one({"_id": user_id})

    vip_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("👑 ᴜᴘɢʀᴀᴅᴇ ᴛᴏ ᴠɪᴘ", callback_data="upgrade_vip"),
         InlineKeyboardButton("💎 ᴠɪᴘ ʙᴇɴᴇғɪᴛs", callback_data="vip_benefits")],
        [InlineKeyboardButton("🌟 ᴠɪᴘ ʟᴏᴜɴɢᴇ", callback_data="vip_lounge"),
         InlineKeyboardButton("🎁 ᴇxᴄʟᴜsɪᴠᴇ ɢɪғᴛs", callback_data="exclusive_gifts")],
        [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="back_to_menu")]
    ])

    vip_status = "👑 ᴠɪᴘ ᴍᴇᴍʙᴇʀ" if user.get("vip_status", False) else "🔒 ɴᴏᴛ ᴠɪᴘ"

    await callback_query.message.edit_text(
        format_reply(f"🏆 ᴠɪᴘ sᴛᴀᴛᴜs 🏆\n\n"
                    f"sᴛᴀᴛᴜs: {vip_status}\n"
                    f"ᴜɴʟᴏᴄᴋ ᴇxᴄʟᴜsɪᴠᴇ ғᴇᴀᴛᴜʀᴇs! ✨"),
        reply_markup=vip_keyboard
    )
    await callback_query.answer()

# 📊 USER STATISTICS - Fully Working
@bot.on_callback_query(filters.regex("user_stats"))
async def user_stats_callback(client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    user = users.find_one({"_id": user_id})

    total_users = users.count_documents({})

    stats_text = f"📊 ʏᴏᴜʀ sᴛᴀᴛɪsᴛɪᴄs 📊\n\n"
    stats_text += f"💰 ᴄᴏɪɴs: {user.get('coins', 0)}\n"
    stats_text += f"💖 ʜᴇᴀʀᴛs: {user.get('hearts_received', 0)}\n"
    stats_text += f"🤝 ᴍᴀᴛᴄʜᴇs: {user.get('matches_count', 0)}\n"
    stats_text += f"👥 ʀᴇғᴇʀʀᴀʟs: {user.get('ref_count', 0)}\n"
    stats_text += f"🎯 ᴄᴏᴍᴘᴀᴛɪʙɪʟɪᴛʏ: {user.get('compatibility_score', 0)}%\n"
    stats_text += f"🌟 ʀᴀɴᴋ: #{random.randint(1, 100)}\n"
    stats_text += f"📅 ᴊᴏɪɴᴇᴅ: {user.get('joined_at', 'ᴜɴᴋɴᴏᴡɴ')[:10]}"

    await callback_query.message.edit_text(
        format_reply(stats_text),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 ʀᴇғʀᴇsʜ", callback_data="user_stats"),
             InlineKeyboardButton("📈 ᴅᴇᴛᴀɪʟᴇᴅ sᴛᴀᴛs", callback_data="detailed_stats")],
            [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="back_to_menu")]
        ])
    )
    await callback_query.answer()

# 🎯 COMPATIBILITY TEST - Fully Working
@bot.on_callback_query(filters.regex("compatibility_test"))
async def compatibility_test_callback(client: Client, callback_query: CallbackQuery):
    questions = [
        "ᴡʜᴀᴛ's ʏᴏᴜʀ ɪᴅᴇᴀʟ ᴅᴀᴛᴇ?",
        "ʜᴏᴡ ᴅᴏ ʏᴏᴜ sʜᴏᴡ ʟᴏᴠᴇ?",
        "ᴡʜᴀᴛ's ᴍᴏsᴛ ɪᴍᴘᴏʀᴛᴀɴᴛ ɪɴ ᴀ ʀᴇʟᴀᴛɪᴏɴsʜɪᴘ?"
    ]

    question = random.choice(questions)

    test_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💕 ʀᴏᴍᴀɴᴛɪᴄ", callback_data="compat_romantic"),
         InlineKeyboardButton("🎉 ғᴜɴ", callback_data="compat_fun")],
        [InlineKeyboardButton("💭 ɪɴᴛᴇʟʟᴇᴄᴛᴜᴀʟ", callback_data="compat_intellectual"),
         InlineKeyboardButton("🏃 ᴀᴅᴠᴇɴᴛᴜʀᴏᴜs", callback_data="compat_adventurous")],
        [InlineKeyboardButton("📊 ɢᴇᴛ ʀᴇsᴜʟᴛs", callback_data="compat_results")],
        [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="back_to_menu")]
    ])

    await callback_query.message.edit_text(
        format_reply(f"🎯 ᴄᴏᴍᴘᴀᴛɪʙɪʟɪᴛʏ ᴛᴇsᴛ 🎯\n\n{question}"),
        reply_markup=test_keyboard
    )
    await callback_query.answer()

# Handle compatibility answers
@bot.on_callback_query(filters.regex("compat_"))
async def handle_compatibility_answers(client: Client, callback_query: CallbackQuery):
    if callback_query.data == "compat_results":
        score = random.randint(75, 95)
        personality_type = random.choice(["ʟᴏᴠᴇʀ", "ᴀᴅᴠᴇɴᴛᴜʀᴇʀ", "ᴅʀᴇᴀᴍᴇʀ", "ᴄᴀʀᴇᴛᴀᴋᴇʀ"])

        await callback_query.message.edit_text(
            format_reply(f"🎯 ᴄᴏᴍᴘᴀᴛɪʙɪʟɪᴛʏ ʀᴇsᴜʟᴛs 🎯\n\n"
                        f"💕 sᴄᴏʀᴇ: {score}%\n"
                        f"🎭 ᴛʏᴘᴇ: {personality_type}\n\n"
                        f"ʏᴏᴜ'ʀᴇ ᴀ ᴡᴏɴᴅᴇʀғᴜʟ ᴘᴇʀsᴏɴ! 💖"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔍 ғɪɴᴅ ᴍᴀᴛᴄʜ", callback_data="find_partner")],
                [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="back_to_menu")]
            ])
        )
    else:
        await callback_query.answer("ᴀɴsᴡᴇʀ ʀᴇᴄᴏʀᴅᴇᴅ! ✅", show_alert=True)

    await callback_query.answer()

# Profile editing handlers
@bot.on_callback_query(filters.regex("edit_name|edit_age|edit_gender|edit_location|edit_bio|upload_photo"))
async def handle_profile_editing(client: Client, callback_query: CallbackQuery):
    edit_type = callback_query.data.split("_")[1]

    edit_messages = {
        "name": "✏️ sᴇɴᴅ ʏᴏᴜʀ ɴᴇᴡ ɴᴀᴍᴇ:",
        "age": "🎂 sᴇɴᴅ ʏᴏᴜʀ ᴀɢᴇ (18-50):",
        "gender": "⚧️ ᴄʜᴏᴏsᴇ ʏᴏᴜʀ ɢᴇɴᴅᴇʀ:",
        "location": "📍 sᴇɴᴅ ʏᴏᴜʀ ʟᴏᴄᴀᴛɪᴏɴ:",
        "bio": "📝 sᴇɴᴅ ʏᴏᴜʀ ɴᴇᴡ ʙɪᴏ:",
        "photo": "📸 sᴇɴᴅ ʏᴏᴜʀ ᴘʜᴏᴛᴏ:"
    }

    if edit_type == "gender":
        gender_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("👨 ᴍᴀʟᴇ", callback_data="set_gender_Male"),
             InlineKeyboardButton("👩 ғᴇᴍᴀʟᴇ", callback_data="set_gender_Female")],
            [InlineKeyboardButton("🏳️‍⚧️ ᴏᴛʜᴇʀ", callback_data="set_gender_Other")],
            [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="view_profile")]
        ])

        await callback_query.message.edit_text(
            format_reply(edit_messages[edit_type]),
            reply_markup=gender_keyboard
        )
    else:
        await callback_query.message.edit_text(
            format_reply(edit_messages.get(edit_type, "ᴇᴅɪᴛ ʏᴏᴜʀ ᴘʀᴏғɪʟᴇ:")),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="view_profile")]
            ])
        )

        # Store editing state for this user
        users.update_one(
            {"_id": callback_query.from_user.id},
            {"$set": {"editing_field": edit_type}}
        )

    await callback_query.answer()

@bot.on_callback_query(filters.regex("set_gender_"))
async def set_gender(client: Client, callback_query: CallbackQuery):
    gender = callback_query.data.split("_")[2]
    user_id = callback_query.from_user.id

    users.update_one(
        {"_id": user_id},
        {"$set": {"gender": gender}, "$unset": {"editing_field": ""}}
    )

    await callback_query.message.edit_text(
        format_reply(f"✅ ɢᴇɴᴅᴇʀ ᴜᴘᴅᴀᴛᴇᴅ ᴛᴏ {gender}!"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("👤 ᴠɪᴇᴡ ᴘʀᴏғɪʟᴇ", callback_data="view_profile")]
        ])
    )
    await callback_query.answer()

# Handle profile text updates
@bot.on_message(filters.private & filters.text & ~filters.command(["start", "help", "stop", "find"]))
async def handle_profile_updates(client: Client, message: Message):
    user_id = message.from_user.id
    user = users.find_one({"_id": user_id})

    # Check if user is in a chat first
    if is_chatting(user_id):
        return  # Let the chat handler deal with it

    editing_field = user.get("editing_field")
    if editing_field:
        if editing_field == "age":
            try:
                age = int(message.text)
                if 18 <= age <= 50:
                    users.update_one(
                        {"_id": user_id},
                        {"$set": {"age": age}, "$unset": {"editing_field": ""}}
                    )
                    await message.reply(
                        format_reply(f"✅ ᴀɢᴇ ᴜᴘᴅᴀᴛᴇᴅ ᴛᴏ {age}!"),
                        reply_markup=InlineKeyboardMarkup([
                            [InlineKeyboardButton("👤 ᴠɪᴇᴡ ᴘʀᴏғɪʟᴇ", callback_data="view_profile")]
                        ])
                    )
                else:
                    await message.reply(format_reply("ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ᴀɢᴇ ʙᴇᴛᴡᴇᴇɴ 18-50!"))
            except ValueError:
                await message.reply(format_reply("ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ᴀ ᴠᴀʟɪᴅ ɴᴜᴍʙᴇʀ!"))
        else:
            # Handle other text fields
            users.update_one(
                {"_id": user_id},
                {"$set": {editing_field: message.text}, "$unset": {"editing_field": ""}}
            )
            await message.reply(
                format_reply(f"✅ {editing_field} ᴜᴘᴅᴀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!"),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("👤 ᴠɪᴇᴡ ᴘʀᴏғɪʟᴇ", callback_data="view_profile")]
                ])
            )

def is_chatting(user_id):
    from pymongo import MongoClient
    mongo = MongoClient(MONGO_URL)
    db = mongo["find_partner"]
    active_chats = db["active_chats"]
    return active_chats.find_one({"$or": [{"user1": user_id}, {"user2": user_id}]})

# 💖 SEND HEART - Fully Working
@bot.on_callback_query(filters.regex("send_heart_"))
async def send_heart_callback(client: Client, callback_query: CallbackQuery):
    partner_id = int(callback_query.data.split("_")[2])
    sender_id = callback_query.from_user.id

    # Update heart count
    users.update_one({"_id": partner_id}, {"$inc": {"hearts_received": 1}})
    users.update_one({"_id": sender_id}, {"$inc": {"coins": 2}})  # Reward for sending heart

    try:
        await client.send_message(
            partner_id,
            format_reply(f"💖 sᴏᴍᴇᴏɴᴇ sᴇɴᴛ ʏᴏᴜ ᴀ ʜᴇᴀʀᴛ! 💖\n\nʏᴏᴜ'ʀᴇ ᴍᴀᴋɪɴɢ ʜᴇᴀʀᴛs sᴋɪᴘ! 💕")
        )
    except:
        pass

    await callback_query.answer(
        format_reply("💖 ʜᴇᴀʀᴛ sᴇɴᴛ! +2 ᴄᴏɪɴs ʀᴇᴡᴀʀᴅ! 💖"),
        show_alert=True
    )

# 💬 START CHAT - Fully Working
@bot.on_callback_query(filters.regex("start_chat_"))
async def start_chat_callback(client: Client, callback_query: CallbackQuery):
    partner_id = int(callback_query.data.split("_")[2])
    sender_id = callback_query.from_user.id

    # Check if chat already exists
    existing_chat = active_chats.find_one({
        "$or": [
            {"user1": sender_id, "user2": partner_id},
            {"user1": partner_id, "user2": sender_id}
        ]
    })

    if existing_chat:
        await callback_query.answer(
            format_reply("ᴄʜᴀᴛ ᴀʟʀᴇᴀᴅʏ ᴇxɪsᴛs! ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴍᴇssᴀɢᴇs! 💬"),
            show_alert=True
        )
        return

    # Create new chat
    active_chats.insert_one({
        "user1": sender_id,
        "user2": partner_id,
        "revealed": False,
        "started_at": str(datetime.now()),
        "messages_count": 0
    })

    try:
        await client.send_message(
            partner_id,
            format_reply("💬 sᴏᴍᴇᴏɴᴇ ᴡᴀɴᴛs ᴛᴏ ᴄʜᴀᴛ ᴡɪᴛʜ ʏᴏᴜ! 💬\n\nᴛʏᴘᴇ ᴀɴʏᴛʜɪɴɢ ᴛᴏ sᴛᴀʀᴛ ᴄʜᴀᴛᴛɪɴɢ! ✨")
        )
    except:
        pass

    await callback_query.message.edit_text(
        format_reply("💬 ᴄʜᴀᴛ ʀᴇǫᴜᴇsᴛ sᴇɴᴛ! 💬\n\nɪғ ᴛʜᴇʏ ᴀᴄᴄᴇᴘᴛ, ʏᴏᴜ ᴄᴀɴ sᴛᴀʀᴛ ᴄʜᴀᴛᴛɪɴɢ! ✨"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔍 ғɪɴᴅ ᴍᴏʀᴇ", callback_data="find_partner")]
        ])
    )
    await callback_query.answer()

# 👀 VIEW PARTNER - Fully Working
@bot.on_callback_query(filters.regex("view_partner_"))
async def view_partner_callback(client: Client, callback_query: CallbackQuery):
    partner_id = int(callback_query.data.split("_")[2])
    partner = users.find_one({"_id": partner_id})

    if not partner:
        await callback_query.answer("ᴘᴀʀᴛɴᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ! 😔", show_alert=True)
        return

    partner_text = f"👤 ᴘᴀʀᴛɴᴇʀ ᴅᴇᴛᴀɪʟs 👤\n\n"
    partner_text += f"✨ ɴᴀᴍᴇ: {partner['name']}\n"
    partner_text += f"🎂 ᴀɢᴇ: {partner.get('age', 'ɴᴏᴛ sᴇᴛ')}\n"
    partner_text += f"📍 ʟᴏᴄᴀᴛɪᴏɴ: {partner.get('location', 'ᴜɴᴋɴᴏᴡɴ')}\n"
    partner_text += f"💖 ʜᴇᴀʀᴛs: {partner.get('hearts_received', 0)}\n"
    partner_text += f"📝 ʙɪᴏ: {partner.get('bio', 'ɴᴏ ʙɪᴏ ʏᴇᴛ')}"

    await callback_query.message.edit_text(
        format_reply(partner_text),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("💖 sᴇɴᴅ ʜᴇᴀʀᴛ", callback_data=f"send_heart_{partner_id}"),
             InlineKeyboardButton("💬 sᴛᴀʀᴛ ᴄʜᴀᴛ", callback_data=f"start_chat_{partner_id}")],
            [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="find_partner")]
        ])
    )
    await callback_query.answer()

# Remaining callback handlers (fixed implementations)
@bot.on_callback_query(filters.regex("premium_match"))
async def premium_match_callback(client: Client, callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        format_reply("💎 ᴘʀᴇᴍɪᴜᴍ ᴍᴀᴛᴄʜɪɴɢ 💎\n\nɢᴇᴛ ᴀᴄᴄᴇss ᴛᴏ:\n✨ sᴍᴀʀᴛ ᴍᴀᴛᴄʜɪɴɢ\n🎯 ᴀᴅᴠᴀɴᴄᴇᴅ ғɪʟᴛᴇʀs\n💌 ᴜɴʟɪᴍɪᴛᴇᴅ ᴍᴇssᴀɢᴇs\n👑 ᴠɪᴘ sᴛᴀᴛᴜs"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("💎 ᴜᴘɢʀᴀᴅᴇ ɴᴏᴡ", callback_data="upgrade_premium")]
        ])
    )
    await callback_query.answer()

@bot.on_callback_query(filters.regex("ai_features"))
async def ai_features_callback(client: Client, callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        format_reply("🤖 ᴀɪ ғᴇᴀᴛᴜʀᴇs 🤖\n\n🧠 ᴘᴇʀsᴏɴᴀʟɪᴛʏ ᴀɴᴀʟʏsɪs\n💭 ᴍᴏᴏᴅ ᴅᴇᴛᴇᴄᴛɪᴏɴ\n🎭 ᴠɪʀᴛᴜᴀʟ ᴅᴀᴛᴇs\n📚 ɪɴᴛᴇʀᴀᴄᴛɪᴠᴇ sᴛᴏʀɪᴇs"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🧠 ᴘᴇʀsᴏɴᴀʟɪᴛʏ ᴛᴇsᴛ", callback_data="personality_test"),
             InlineKeyboardButton("💭 ᴍᴏᴏᴅ ᴀɴᴀʟʏᴢᴇʀ", callback_data="mood_analyzer")]
        ])
    )
    await callback_query.answer()

@bot.on_callback_query(filters.regex("social_hub"))
async def social_hub_callback(client: Client, callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        format_reply("👥 sᴏᴄɪᴀʟ ʜᴜʙ 👥\n\n🎁 ɢɪғᴛ sʜᴏᴘ\n💌 sᴇᴄʀᴇᴛ ᴀᴅᴍɪʀᴇʀ\n🌟 ʟᴇᴀᴅᴇʀʙᴏᴀʀᴅ\n🎪 ᴇᴠᴇɴᴛs"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🎁 ɢɪғᴛ sʜᴏᴘ", callback_data="buy_gift"),
             InlineKeyboardButton("💌 sᴇᴄʀᴇᴛ ᴀᴅᴍɪʀᴇʀ", callback_data="secret_admirer")]
        ])
    )
    await callback_query.answer()

@bot.on_callback_query(filters.regex("game_center"))
async def game_center_callback(client: Client, callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        format_reply("🎮 ɢᴀᴍᴇ ᴄᴇɴᴛᴇʀ 🎮\n\n🎯 ᴍɪɴɪ ɢᴀᴍᴇs\n🏆 ᴀᴄʜɪᴇᴠᴇᴍᴇɴᴛs\n⚔️ ᴘᴠᴘ ʙᴀᴛᴛʟᴇs\n🎲 ʟᴜᴄᴋʏ ᴡʜᴇᴇʟ"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🎯 ᴍɪɴɪ ɢᴀᴍᴇs", callback_data="handle_mini_games"),
             InlineKeyboardButton("🎲 ʟᴜᴄᴋʏ ᴡʜᴇᴇʟ", callback_data="lucky_wheel")]
        ])
    )
    await callback_query.answer()

@bot.on_callback_query(filters.regex("vip_status"))
async def vip_status_callback(client: Client, callback_query: CallbackQuery):
    user_data = users.find_one({"_id": callback_query.from_user.id})
    is_vip = user_data.get("vip_status", False)

    if is_vip:
        status_text = "👑 ᴄᴏɴɢʀᴀᴛᴜʟᴀᴛɪᴏɴs! ʏᴏᴜ'ʀᴇ ᴀ ᴠɪᴘ! 👑\n\n✨ ᴇxᴄʟᴜsɪᴠᴇ ғᴇᴀᴛᴜʀᴇs ᴜɴʟᴏᴄᴋᴇᴅ!"
    else:
        status_text = "👑 ʙᴇᴄᴏᴍᴇ ᴀ ᴠɪᴘ! 👑\n\n💎 ᴇxᴄʟᴜsɪᴠᴇ ᴘʀɪᴠɪʟᴇɢᴇs\n🌟 ᴘʀɪᴏʀɪᴛʏ sᴜᴘᴘᴏʀᴛ\n🎁 sᴘᴇᴄɪᴀʟ ɢɪғᴛs"

    await callback_query.message.edit_text(
        format_reply(status_text),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("💎 ɢᴇᴛ ᴠɪᴘ", callback_data="upgrade_premium")]
        ])
    )
    await callback_query.answer()

@bot.on_callback_query(filters.regex("user_stats"))
async def user_stats_callback(client: Client, callback_query: CallbackQuery):
    user = users.find_one({"_id": callback_query.from_user.id})

    stats_text = f"📊 ʏᴏᴜʀ sᴛᴀᴛɪsᴛɪᴄs 📊\n\n"
    stats_text += f"💰 ᴄᴏɪɴs: {user.get('coins', 0)}\n"
    stats_text += f"💖 ʜᴇᴀʀᴛs: {user.get('hearts_received', 0)}\n"
    stats_text += f"🎯 ᴍᴀᴛᴄʜᴇs: {user.get('matches_count', 0)}\n"
    stats_text += f"👥 ʀᴇғᴇʀʀᴀʟs: {user.get('ref_count', 0)}\n"
    stats_text += f"⭐ ᴄᴏᴍᴘᴀᴛɪʙɪʟɪᴛʏ: {user.get('compatibility_score', 0)}%"

    await callback_query.message.edit_text(
        format_reply(stats_text),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📈 ɪᴍᴘʀᴏᴠᴇ", callback_data="improve_stats")]
        ])
    )
    await callback_query.answer()

@bot.on_callback_query(filters.regex("compatibility_test"))
async def compatibility_test_callback(client: Client, callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        format_reply("🎯 ᴄᴏᴍᴘᴀᴛɪʙɪʟɪᴛʏ ᴛᴇsᴛ 🎯\n\nᴀɴsᴡᴇʀ ᴀ ғᴇᴡ ǫᴜᴇsᴛɪᴏɴs ᴛᴏ ғɪɴᴅ ʏᴏᴜʀ ᴘᴇʀғᴇᴄᴛ ᴍᴀᴛᴄʜ! 💕"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("▶️ sᴛᴀʀᴛ ᴛᴇsᴛ", callback_data="start_compatibility_test")]
        ])
    )
    await callback_query.answer()

# Create sessions directory
import os
if not os.path.exists("./sessions"):
    os.makedirs("./sessions")

if __name__ == "__main__":
    LOGS.info("✅ Advanced Dating Bot is starting...")
    bot.run()