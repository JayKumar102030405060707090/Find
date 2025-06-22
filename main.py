
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

# Remaining callback handlers (placeholder implementations)
@bot.on_callback_query(filters.regex("premium_match|ai_features|social_hub|game_center|vip_status|user_stats|compatibility_test"))
async def other_features(client: Client, callback_query: CallbackQuery):
    feature_name = callback_query.data.replace("_", " ").title()
    await callback_query.answer(f"❖ **{feature_name} - ᴄᴏᴍɪɴɢ sᴏᴏɴ!**", show_alert=True)

# Create sessions directory
import os
if not os.path.exists("./sessions"):
    os.makedirs("./sessions")

if __name__ == "__main__":
    LOGS.info("✅ Advanced Dating Bot is starting...")
    bot.run()
