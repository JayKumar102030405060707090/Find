
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import *
from pymongo import MongoClient
from datetime import datetime, timedelta
import random

client = MongoClient(MONGO_URL)
db = client['find_partner']
users = db['users']

def format_reply(text):
    tiny_caps_map = {
        'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ', 'f': 'ғ', 'g': 'ɢ', 'h': 'ʜ',
        'i': 'ɪ', 'j': 'ᴊ', 'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ', 'o': 'ᴏ', 'p': 'ᴘ',
        'q': 'ǫ', 'r': 'ʀ', 's': 's', 't': 'ᴛ', 'u': 'ᴜ', 'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x',
        'y': 'ʏ', 'z': 'ᴢ'
    }
    converted = ''.join(tiny_caps_map.get(char.lower(), char) for char in text)
    return f"❖ **{converted}**"

# Missing Profile Features
@Client.on_callback_query(filters.regex("add_photo"))
async def add_photo(bot, callback: CallbackQuery):
    await callback.message.edit_text(
        format_reply("📸 ᴘʜᴏᴛᴏ ғᴇᴀᴛᴜʀᴇ ᴄᴏᴍɪɴɢ sᴏᴏɴ! 🔜\n\nsᴇɴᴅ ᴀ ᴘʜᴏᴛᴏ ᴛᴏ ᴜᴘᴅᴀᴛᴇ ʏᴏᴜʀ ᴘʀᴏғɪʟᴇ!"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="view_profile")]
        ])
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("update_bio"))
async def update_bio(bot, callback: CallbackQuery):
    await callback.message.edit_text(
        format_reply("✍️ ʙɪᴏ ᴜᴘᴅᴀᴛᴇ ғᴇᴀᴛᴜʀᴇ ᴄᴏᴍɪɴɢ sᴏᴏɴ! 🔜\n\nsᴇɴᴅ ʏᴏᴜʀ ɴᴇᴡ ʙɪᴏ ᴛᴏ ᴜᴘᴅᴀᴛᴇ!"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="view_profile")]
        ])
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("upgrade_premium"))
async def upgrade_premium(bot, callback: CallbackQuery):
    premium_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💎 ᴍᴏɴᴛʜʟʏ - $4.99", callback_data="buy_premium_monthly"),
         InlineKeyboardButton("💎 ʏᴇᴀʀʟʏ - $39.99", callback_data="buy_premium_yearly")],
        [InlineKeyboardButton("🎁 ғʀᴇᴇ ᴛʀɪᴀʟ (3 ᴅᴀʏs)", callback_data="free_trial")],
        [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="view_profile")]
    ])
    
    await callback.message.edit_text(
        format_reply("💎 ᴜᴘɢʀᴀᴅᴇ ᴛᴏ ᴘʀᴇᴍɪᴜᴍ! 💎\n\n✨ sᴍᴀʀᴛ ᴍᴀᴛᴄʜɪɴɢ ᴀʟɢᴏʀɪᴛʜᴍ\n💌 ᴜɴʟɪᴍɪᴛᴇᴅ ᴍᴇssᴀɢᴇs\n🎯 ᴀᴅᴠᴀɴᴄᴇᴅ ғɪʟᴛᴇʀs\n🏆 ᴇxᴄʟᴜsɪᴠᴇ ғᴇᴀᴛᴜʀᴇs\n👑 ᴠɪᴘ ʙᴀᴅɢᴇ"),
        reply_markup=premium_keyboard
    )
    await callback.answer()

# Premium Purchase Handlers
@Client.on_callback_query(filters.regex("buy_premium_"))
async def buy_premium(bot, callback: CallbackQuery):
    plan = callback.data.split("_")[2]
    price = "$4.99" if plan == "monthly" else "$39.99"
    
    users.update_one(
        {"_id": callback.from_user.id},
        {"$set": {"premium": True, "premium_plan": plan, "premium_activated": str(datetime.now())}},
        upsert=True
    )
    
    await callback.message.edit_text(
        format_reply(f"🎉 ᴄᴏɴɢʀᴀᴛᴜʟᴀᴛɪᴏɴs! 🎉\n\nʏᴏᴜ ᴀʀᴇ ɴᴏᴡ ᴀ ᴘʀᴇᴍɪᴜᴍ ᴍᴇᴍʙᴇʀ!\n💎 {plan} ᴘʟᴀɴ - {price}\n\nᴇɴᴊᴏʏ ᴀʟʟ ᴘʀᴇᴍɪᴜᴍ ғᴇᴀᴛᴜʀᴇs! ✨"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🎯 sᴍᴀʀᴛ ᴍᴀᴛᴄʜɪɴɢ", callback_data="smart_matching"),
             InlineKeyboardButton("💌 ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ", callback_data="private_messages")]
        ])
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("free_trial"))
async def free_trial(bot, callback: CallbackQuery):
    users.update_one(
        {"_id": callback.from_user.id},
        {"$set": {"premium": True, "trial_ends": str(datetime.now() + timedelta(days=3))}},
        upsert=True
    )
    
    await callback.message.edit_text(
        format_reply("🎁 ғʀᴇᴇ ᴛʀɪᴀʟ ᴀᴄᴛɪᴠᴀᴛᴇᴅ! 🎁\n\nᴇɴᴊᴏʏ 3 ᴅᴀʏs ᴏғ ᴘʀᴇᴍɪᴜᴍ ғᴇᴀᴛᴜʀᴇs! ✨\n\nᴛʀɪᴀʟ ᴇɴᴅs ɪɴ 72 ʜᴏᴜʀs ⏰"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🎯 sᴍᴀʀᴛ ᴍᴀᴛᴄʜɪɴɢ", callback_data="smart_matching")]
        ])
    )
    await callback.answer()

# Missing Game Features
@Client.on_callback_query(filters.regex("game_"))
async def handle_mini_games(bot, callback: CallbackQuery):
    game_type = callback.data.split("_")[1]
    
    game_results = {
        "aim": {"score": random.randint(50, 100), "reward": 15},
        "puzzle": {"score": random.randint(60, 100), "reward": 20},
        "rhythm": {"score": random.randint(40, 100), "reward": 25},
        "cards": {"score": random.randint(30, 100), "reward": 18},
        "bottle": {"score": random.randint(1, 10), "reward": 10},
        "dice": {"score": random.randint(1, 6), "reward": 12},
        "stars": {"score": random.randint(20, 100), "reward": 22},
        "memory": {"score": random.randint(40, 100), "reward": 28}
    }
    
    result = game_results.get(game_type, {"score": 50, "reward": 15})
    
    users.update_one(
        {"_id": callback.from_user.id},
        {"$inc": {"coins": result["reward"], "games_played": 1}},
        upsert=True
    )
    
    await callback.message.edit_text(
        format_reply(f"🎮 ɢᴀᴍᴇ ʀᴇsᴜʟᴛ! 🎮\n\n📊 sᴄᴏʀᴇ: {result['score']}\n💰 ᴇᴀʀɴᴇᴅ: {result['reward']} ᴄᴏɪɴs!"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 ᴘʟᴀʏ ᴀɢᴀɪɴ", callback_data="mini_games"),
             InlineKeyboardButton("🎯 ᴍᴏʀᴇ ɢᴀᴍᴇs", callback_data="game_center")]
        ])
    )
    await callback.answer()

# Missing Social Features
@Client.on_callback_query(filters.regex("group_"))
async def join_interest_group(bot, callback: CallbackQuery):
    group_type = callback.data.split("_")[1]
    
    users.update_one(
        {"_id": callback.from_user.id},
        {"$addToSet": {"joined_groups": group_type}},
        upsert=True
    )
    
    await callback.message.edit_text(
        format_reply(f"🎉 ᴊᴏɪɴᴇᴅ {group_type} ɢʀᴏᴜᴘ! 🎉\n\nʏᴏᴜ ᴄᴀɴ ɴᴏᴡ ᴄʜᴀᴛ ᴡɪᴛʜ ᴏᴛʜᴇʀ {group_type} ᴇɴᴛʜᴜsɪᴀsᴛs!"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("💬 ɢʀᴏᴜᴘ ᴄʜᴀᴛ", callback_data=f"group_chat_{group_type}"),
             InlineKeyboardButton("👥 ᴍᴇᴍʙᴇʀs", callback_data=f"group_members_{group_type}")],
            [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="social_hub")]
        ])
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("event_"))
async def join_event(bot, callback: CallbackQuery):
    event_type = callback.data.split("_")[1]
    
    events = {
        "speed": "💕 sᴘᴇᴇᴅ ᴅᴀᴛɪɴɢ ᴇᴠᴇɴᴛ\n⏰ ᴇᴠᴇʀʏ sᴀᴛᴜʀᴅᴀʏ 8 ᴘᴍ",
        "roleplay": "🎭 ʀᴏʟᴇᴘʟᴀʏ ɴɪɢʜᴛ\n⏰ ᴇᴠᴇʀʏ ғʀɪᴅᴀʏ 9 ᴘᴍ",
        "music": "🎵 ᴍᴜsɪᴄ ᴘᴀʀᴛʏ\n⏰ ᴇᴠᴇʀʏ sᴜɴᴅᴀʏ 7 ᴘᴍ",
        "gaming": "🎮 ɢᴀᴍᴇ ᴛᴏᴜʀɴᴀᴍᴇɴᴛ\n⏰ ᴇᴠᴇʀʏ ᴡᴇᴅɴᴇsᴅᴀʏ 8 ᴘᴍ",
        "midnight": "🌙 ᴍɪᴅɴɪɢʜᴛ ᴄʜᴀᴛ\n⏰ ᴇᴠᴇʀʏ ɴɪɢʜᴛ 12 ᴀᴍ",
        "morning": "☀️ ᴍᴏʀɴɪɴɢ ᴍᴇᴇᴛ\n⏰ ᴇᴠᴇʀʏ ᴅᴀʏ 8 ᴀᴍ"
    }
    
    event_info = events.get(event_type, "🎉 sᴘᴇᴄɪᴀʟ ᴇᴠᴇɴᴛ")
    
    await callback.message.edit_text(
        format_reply(f"🎉 ᴇᴠᴇɴᴛ ɪɴғᴏ 🎉\n\n{event_info}\n\n✅ ʏᴏᴜ'ʀᴇ ʀᴇɢɪsᴛᴇʀᴇᴅ!"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔔 ʀᴇᴍɪɴᴅᴇʀ", callback_data=f"reminder_{event_type}"),
             InlineKeyboardButton("📅 ᴄᴀʟᴇɴᴅᴀʀ", callback_data="event_calendar")],
            [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="view_events")]
        ])
    )
    await callback.answer()

# Gift Shop Features
@Client.on_callback_query(filters.regex("buy_"))
async def buy_gift(bot, callback: CallbackQuery):
    gift_type = callback.data.split("_")[1]
    
    gift_prices = {
        "rose": 10, "bouquet": 50, "ring": 100, "crown": 200,
        "teddy": 75, "chocolate": 25, "surprise": 150
    }
    
    price = gift_prices.get(gift_type, 10)
    user_data = users.find_one({"_id": callback.from_user.id})
    current_coins = user_data.get("coins", 0)
    
    if current_coins >= price:
        users.update_one(
            {"_id": callback.from_user.id},
            {"$inc": {"coins": -price}, "$addToSet": {"gifts": gift_type}}
        )
        
        await callback.message.edit_text(
            format_reply(f"🎁 ɢɪғᴛ ᴘᴜʀᴄʜᴀsᴇᴅ! 🎁\n\n{gift_type.upper()} ᴀᴅᴅᴇᴅ ᴛᴏ ʏᴏᴜʀ ɪɴᴠᴇɴᴛᴏʀʏ!\n💰 -{price} ᴄᴏɪɴs"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💌 sᴇɴᴅ ɢɪғᴛ", callback_data=f"send_gift_{gift_type}"),
                 InlineKeyboardButton("🛍️ ʙᴜʏ ᴍᴏʀᴇ", callback_data="gift_shop")]
            ])
        )
    else:
        await callback.message.edit_text(
            format_reply(f"💔 ɴᴏᴛ ᴇɴᴏᴜɢʜ ᴄᴏɪɴs! 💔\n\nʏᴏᴜ ɴᴇᴇᴅ {price} ᴄᴏɪɴs ʙᴜᴛ ʜᴀᴠᴇ {current_coins}"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💰 ᴇᴀʀɴ ᴄᴏɪɴs", callback_data="earn_coins"),
                 InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="gift_shop")]
            ])
        )
    
    await callback.answer()

# Challenge Features  
@Client.on_callback_query(filters.regex("challenge_"))
async def complete_challenge(bot, callback: CallbackQuery):
    challenge_type = callback.data.split("_")[1]
    today = datetime.now().strftime("%Y-%m-%d")
    
    challenge_rewards = {
        "send_hearts": 20,
        "play_games": 30, 
        "chat_minutes": 25,
        "make_friends": 40
    }
    
    reward = challenge_rewards.get(challenge_type, 20)
    
    users.update_one(
        {"_id": callback.from_user.id},
        {
            "$inc": {"coins": reward},
            "$addToSet": {f"challenges_{today}": challenge_type}
        }
    )
    
    await callback.message.edit_text(
        format_reply(f"🎯 ᴄʜᴀʟʟᴇɴɢᴇ ᴄᴏᴍᴘʟᴇᴛᴇᴅ! 🎯\n\n✅ {challenge_type.replace('_', ' ').title()}\n💰 +{reward} ᴄᴏɪɴs ᴇᴀʀɴᴇᴅ!"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 ᴍᴏʀᴇ ᴄʜᴀʟʟᴇɴɢᴇs", callback_data="daily_challenges"),
             InlineKeyboardButton("🎮 ᴘʟᴀʏ ɢᴀᴍᴇs", callback_data="mini_games")]
        ])
    )
    await callback.answer()

# Advanced Matching Features
@Client.on_callback_query(filters.regex("zodiac_"))
async def zodiac_compatibility(bot, callback: CallbackQuery):
    zodiac_index = int(callback.data.split("_")[1])
    zodiac_signs = ["aries", "taurus", "gemini", "cancer", "leo", "virgo", 
                   "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"]
    
    selected_sign = zodiac_signs[zodiac_index]
    
    users.update_one(
        {"_id": callback.from_user.id},
        {"$set": {"zodiac_sign": selected_sign}}
    )
    
    compatibility_score = random.randint(60, 95)
    
    await callback.message.edit_text(
        format_reply(f"✨ ᴀsᴛʀᴏʟᴏɢɪᴄᴀʟ ᴍᴀᴛᴄʜɪɴɢ ✨\n\nʏᴏᴜʀ sɪɢɴ: {selected_sign.upper()}\nᴄᴏᴍᴘᴀᴛɪʙɪʟɪᴛʏ sᴄᴏʀᴇ: {compatibility_score}%\n\n🔮 sᴇᴀʀᴄʜɪɴɢ ғᴏʀ ᴄᴏᴍᴘᴀᴛɪʙʟᴇ sɪɢɴs..."),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔍 ғɪɴᴅ ᴍᴀᴛᴄʜ", callback_data="find_partner"),
             InlineKeyboardButton("🔮 ɴᴇᴡ ʀᴇᴀᴅɪɴɢ", callback_data="astrology_match")]
        ])
    )
    await callback.answer()

# Skip handlers for profile setup
@Client.on_callback_query(filters.regex("skip_"))
async def skip_profile_step(bot, callback: CallbackQuery):
    step_type = callback.data.split("_")[1]
    user_id = callback.from_user.id
    
    if step_type == "name":
        await callback.message.edit_text(
            format_reply("sᴇɴᴅ ʏᴏᴜʀ ᴀɢᴇ:"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⏭️ sᴋɪᴘ", callback_data="skip_age")]
            ])
        )
    elif step_type == "age":
        gender_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("👨 ʙᴏʏ", callback_data="gender_male"),
             InlineKeyboardButton("👩 ɢɪʀʟ", callback_data="gender_female")],
            [InlineKeyboardButton("🌈 ᴏᴛʜᴇʀ", callback_data="gender_other")]
        ])
        await callback.message.edit_text(
            format_reply("sᴇʟᴇᴄᴛ ʏᴏᴜʀ ɢᴇɴᴅᴇʀ:"),
            reply_markup=gender_keyboard
        )
    elif step_type == "bio":
        await callback.message.edit_text(
            format_reply("ᴘʀᴏғɪʟᴇ sᴇᴛᴜᴘ ᴄᴏᴍᴘʟᴇᴛᴇ! ✨"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("👤 ᴠɪᴇᴡ ᴘʀᴏғɪʟᴇ", callback_data="view_profile")]
            ])
        )
    
    await callback.answer()

# Interests done handler
@Client.on_callback_query(filters.regex("interests_done"))
async def interests_completed(bot, callback: CallbackQuery):
    await callback.message.edit_text(
        format_reply("✅ ɪɴᴛᴇʀᴇsᴛs ᴜᴘᴅᴀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ! ✅"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("👤 ᴠɪᴇᴡ ᴘʀᴏғɪʟᴇ", callback_data="view_profile"),
             InlineKeyboardButton("🔍 ғɪɴᴅ ᴍᴀᴛᴄʜ", callback_data="find_partner")]
        ])
    )
    await callback.answer()
