
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

@Client.on_callback_query(filters.regex("premium_match"))
async def premium_matching_menu(bot, callback: CallbackQuery):
    user_data = users.find_one({"_id": callback.from_user.id})
    
    if user_data.get("premium", False):
        premium_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("💎 sᴍᴀʀᴛ ᴍᴀᴛᴄʜɪɴɢ", callback_data="smart_match"),
             InlineKeyboardButton("🎯 ᴛᴀʀɢᴇᴛᴇᴅ sᴇᴀʀᴄʜ", callback_data="targeted_search")],
            [InlineKeyboardButton("🌟 ᴠɪᴘ ᴄʜᴀᴛs", callback_data="vip_chats"),
             InlineKeyboardButton("💌 ᴘʀɪᴠᴀᴛᴇ ᴍᴇssᴀɢᴇs", callback_data="private_messages")],
            [InlineKeyboardButton("🏆 ᴇxᴄʟᴜsɪᴠᴇ ᴄʟᴜʙ", callback_data="exclusive_club")]
        ])
        
        await callback.message.edit_text(
            format_reply("ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴘʀᴇᴍɪᴜᴍ ᴍᴀᴛᴄʜɪɴɢ! ✨"),
            reply_markup=premium_keyboard
        )
    else:
        upgrade_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("💎 ᴜᴘɢʀᴀᴅᴇ ᴛᴏ ᴘʀᴇᴍɪᴜᴍ", callback_data="upgrade_premium")],
            [InlineKeyboardButton("🎁 ғʀᴇᴇ ᴛʀɪᴀʟ", callback_data="free_trial")]
        ])
        
        await callback.message.edit_text(
            format_reply("ᴜɴʟᴏᴄᴋ ᴘʀᴇᴍɪᴜᴍ ғᴇᴀᴛᴜʀᴇs! 💎\n\n✨ sᴍᴀʀᴛ ᴍᴀᴛᴄʜɪɴɢ\n💌 ᴘʀɪᴠᴀᴛᴇ ᴍᴇssᴀɢᴇs\n🎯 ᴛᴀʀɢᴇᴛᴇᴅ sᴇᴀʀᴄʜ\n🏆 ᴇxᴄʟᴜsɪᴠᴇ ᴄʟᴜʙ"),
            reply_markup=upgrade_keyboard
        )
    
    await callback.answer()

@Client.on_callback_query(filters.regex("vip_status"))
async def vip_status_menu(bot, callback: CallbackQuery):
    user_data = users.find_one({"_id": callback.from_user.id})
    
    if user_data.get("vip_status", False):
        vip_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("👑 ᴠɪᴘ ʟᴏᴜɴɢᴇ", callback_data="vip_lounge"),
             InlineKeyboardButton("💎 ᴇxᴄʟᴜsɪᴠᴇ ᴍᴀᴛᴄʜᴇs", callback_data="exclusive_matches")],
            [InlineKeyboardButton("🎭 ᴠɪᴘ ᴇᴠᴇɴᴛs", callback_data="vip_events"),
             InlineKeyboardButton("🏅 ᴠɪᴘ ʙᴀᴅɢᴇs", callback_data="vip_badges")]
        ])
        
        await callback.message.edit_text(
            format_reply("ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ᴠɪᴘ ᴄʟᴜʙ! 👑"),
            reply_markup=vip_keyboard
        )
    else:
        vip_upgrade_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("👑 ʙᴇᴄᴏᴍᴇ ᴠɪᴘ", callback_data="become_vip")],
            [InlineKeyboardButton("🎁 ᴠɪᴘ ᴛʀɪᴀʟ", callback_data="vip_trial")]
        ])
        
        await callback.message.edit_text(
            format_reply("ᴊᴏɪɴ ᴛʜᴇ ᴇʟɪᴛᴇ ᴠɪᴘ ᴄʟᴜʙ! 👑\n\n💎 ᴇxᴄʟᴜsɪᴠᴇ ᴍᴀᴛᴄʜᴇs\n🎭 sᴘᴇᴄɪᴀʟ ᴇᴠᴇɴᴛs\n🏅 ᴜɴɪǫᴜᴇ ʙᴀᴅɢᴇs\n👑 ᴠɪᴘ ʟᴏᴜɴɢᴇ ᴀᴄᴄᴇss"),
            reply_markup=vip_upgrade_keyboard
        )
    
    await callback.answer()

@Client.on_callback_query(filters.regex("daily_rewards"))
async def daily_rewards(bot, callback: CallbackQuery):
    user_data = users.find_one({"_id": callback.from_user.id})
    last_reward = user_data.get("last_daily_reward")
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    if last_reward != today:
        reward_coins = random.randint(10, 50)
        bonus_hearts = random.randint(1, 5)
        
        users.update_one(
            {"_id": callback.from_user.id},
            {
                "$inc": {"coins": reward_coins, "hearts_received": bonus_hearts},
                "$set": {"last_daily_reward": today}
            }
        )
        
        await callback.message.edit_text(
            format_reply(f"ᴅᴀɪʟʏ ʀᴇᴡᴀʀᴅ ᴄʟᴀɪᴍᴇᴅ! 🎁\n\n💰 +{reward_coins} ᴄᴏɪɴs\n💖 +{bonus_hearts} ʜᴇᴀʀᴛs\n\nᴄᴏᴍᴇ ʙᴀᴄᴋ ᴛᴏᴍᴏʀʀᴏᴡ ғᴏʀ ᴍᴏʀᴇ!"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🎮 ᴘʟᴀʏ ɢᴀᴍᴇs", callback_data="inline_games"),
                 InlineKeyboardButton("🔍 ғɪɴᴅ ᴍᴀᴛᴄʜ", callback_data="find_partner")]
            ])
        )
    else:
        next_reward_time = (datetime.now() + timedelta(days=1)).replace(hour=0, minute=0, second=0)
        hours_left = int((next_reward_time - datetime.now()).total_seconds() // 3600)
        
        await callback.message.edit_text(
            format_reply(f"ʏᴏᴜ'ᴠᴇ ᴀʟʀᴇᴀᴅʏ ᴄʟᴀɪᴍᴇᴅ ᴛᴏᴅᴀʏ's ʀᴇᴡᴀʀᴅ! ⏰\n\nɴᴇxᴛ ʀᴇᴡᴀʀᴅ ɪɴ: {hours_left} ʜᴏᴜʀs"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💰 ᴇᴀʀɴ ᴍᴏʀᴇ ᴄᴏɪɴs", callback_data="earn_coins")]
            ])
        )
    
    await callback.answer()

@Client.on_callback_query(filters.regex("earn_coins"))
async def earn_coins_menu(bot, callback: CallbackQuery):
    earn_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎯 ɪɴᴠɪᴛᴇ ғʀɪᴇɴᴅs", callback_data="invite_friends"),
         InlineKeyboardButton("🎮 ᴘʟᴀʏ ɢᴀᴍᴇs", callback_data="play_for_coins")],
        [InlineKeyboardButton("📝 ᴄᴏᴍᴘʟᴇᴛᴇ ᴛᴀsᴋs", callback_data="daily_tasks"),
         InlineKeyboardButton("🎁 ᴡᴀᴛᴄʜ ᴀᴅs", callback_data="watch_ads")],
        [InlineKeyboardButton("💎 ʙᴜʏ ᴄᴏɪɴs", callback_data="buy_coins")]
    ])
    
    await callback.message.edit_text(
        format_reply("ᴄʜᴏᴏsᴇ ʜᴏᴡ ᴛᴏ ᴇᴀʀɴ ᴄᴏɪɴs! 💰"),
        reply_markup=earn_keyboard
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("compatibility_test"))
async def compatibility_test(bot, callback: CallbackQuery):
    questions = [
        "ᴡʜᴀᴛ's ʏᴏᴜʀ ɪᴅᴇᴀʟ ᴅᴀᴛᴇ?",
        "ᴡʜᴀᴛ's ᴍᴏsᴛ ɪᴍᴘᴏʀᴛᴀɴᴛ ɪɴ ᴀ ʀᴇʟᴀᴛɪᴏɴsʜɪᴘ?",
        "ᴅᴏ ʏᴏᴜ ᴘʀᴇғᴇʀ ʀᴏᴍᴀɴᴛɪᴄ ᴏʀ ᴀᴅᴠᴇɴᴛᴜʀᴏᴜs ᴅᴀᴛᴇs?"
    ]
    
    test_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🌹 ʀᴏᴍᴀɴᴛɪᴄ", callback_data="compat_romantic"),
         InlineKeyboardButton("🎢 ᴀᴅᴠᴇɴᴛᴜʀᴏᴜs", callback_data="compat_adventure")],
        [InlineKeyboardButton("🏠 ᴄᴏᴢʏ ʜᴏᴍᴇ", callback_data="compat_cozy"),
         InlineKeyboardButton("🌍 ᴛʀᴀᴠᴇʟ", callback_data="compat_travel")]
    ])
    
    await callback.message.edit_text(
        format_reply("ʟᴇᴛ's ғɪɴᴅ ʏᴏᴜʀ ᴘᴇʀғᴇᴄᴛ ᴍᴀᴛᴄʜ ᴛʏᴘᴇ! 💕\n\nᴡʜᴀᴛ's ʏᴏᴜʀ ɪᴅᴇᴀʟ ᴅᴀᴛᴇ?"),
        reply_markup=test_keyboard
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("upgrade_premium"))
async def upgrade_premium(bot, callback: CallbackQuery):
    upgrade_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💎 1 ᴍᴏɴᴛʜ - 500 ᴄᴏɪɴs", callback_data="buy_premium_1"),
         InlineKeyboardButton("💎 3 ᴍᴏɴᴛʜs - 1200 ᴄᴏɪɴs", callback_data="buy_premium_3")],
        [InlineKeyboardButton("💎 6 ᴍᴏɴᴛʜs - 2000 ᴄᴏɪɴs", callback_data="buy_premium_6"),
         InlineKeyboardButton("💎 1 ʏᴇᴀʀ - 3500 ᴄᴏɪɴs", callback_data="buy_premium_12")],
        [InlineKeyboardButton("🎁 ғʀᴇᴇ ᴛʀɪᴀʟ (24ʜ)", callback_data="free_trial")]
    ])
    
    await callback.message.edit_text(
        format_reply("💎 ᴘʀᴇᴍɪᴜᴍ ᴍᴇᴍʙᴇʀsʜɪᴘ 💎\n\n✨ sᴍᴀʀᴛ ᴍᴀᴛᴄʜɪɴɢ\n🎯 ᴀᴅᴠᴀɴᴄᴇᴅ ғɪʟᴛᴇʀs\n💌 ᴜɴʟɪᴍɪᴛᴇᴅ ᴍᴇssᴀɢᴇs\n🏆 ᴇxᴄʟᴜsɪᴠᴇ ғᴇᴀᴛᴜʀᴇs\n👑 ᴘʀᴇᴍɪᴜᴍ ʙᴀᴅɢᴇ"),
        reply_markup=upgrade_keyboard
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("buy_premium_"))
async def buy_premium(bot, callback: CallbackQuery):
    duration = callback.data.split("_")[2]
    user_data = users.find_one({"_id": callback.from_user.id})
    
    prices = {"1": 500, "3": 1200, "6": 2000, "12": 3500}
    price = prices.get(duration, 500)
    
    if user_data.get("coins", 0) >= price:
        users.update_one(
            {"_id": callback.from_user.id},
            {
                "$inc": {"coins": -price},
                "$set": {"premium": True, "premium_expires": datetime.now().isoformat()}
            }
        )
        
        await callback.message.edit_text(
            format_reply(f"🎉 ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴛɪᴠᴀᴛᴇᴅ! 🎉\n\nᴅᴜʀᴀᴛɪᴏɴ: {duration} ᴍᴏɴᴛʜ(s)\nᴇɴᴊᴏʏ ᴀʟʟ ᴘʀᴇᴍɪᴜᴍ ғᴇᴀᴛᴜʀᴇs! ✨"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💎 ᴇxᴘʟᴏʀᴇ ғᴇᴀᴛᴜʀᴇs", callback_data="premium_match")]
            ])
        )
    else:
        await callback.message.edit_text(
            format_reply(f"💰 ɪɴsᴜғғɪᴄɪᴇɴᴛ ᴄᴏɪɴs!\n\nɴᴇᴇᴅᴇᴅ: {price} ᴄᴏɪɴs\nʏᴏᴜ ʜᴀᴠᴇ: {user_data.get('coins', 0)} ᴄᴏɪɴs"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💰 ᴇᴀʀɴ ᴄᴏɪɴs", callback_data="earn_coins")]
            ])
        )
    await callback.answer()

@Client.on_callback_query(filters.regex("free_trial"))
async def free_trial(bot, callback: CallbackQuery):
    users.update_one(
        {"_id": callback.from_user.id},
        {"$set": {"premium": True, "trial_user": True, "trial_expires": (datetime.now() + timedelta(hours=24)).isoformat()}}
    )
    
    await callback.message.edit_text(
        format_reply("🎁 ғʀᴇᴇ ᴛʀɪᴀʟ ᴀᴄᴛɪᴠᴀᴛᴇᴅ! 🎁\n\n24 ʜᴏᴜʀs ᴏғ ғᴜʟʟ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇss! ✨\nᴇɴᴊᴏʏ ᴀʟʟ ғᴇᴀᴛᴜʀᴇs!"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("💎 sᴛᴀʀᴛ ᴜsɪɴɢ", callback_data="premium_match")]
        ])
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("smart_match"))
async def smart_match(bot, callback: CallbackQuery):
    await callback.message.edit_text(
        format_reply("🧠 sᴍᴀʀᴛ ᴍᴀᴛᴄʜɪɴɢ ᴀᴄᴛɪᴠᴀᴛᴇᴅ! 🧠\n\nᴀɴᴀʟʏᴢɪɴɢ ʏᴏᴜʀ ᴘʀᴇғᴇʀᴇɴᴄᴇs... 🔍"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔍 ғɪɴᴅ ᴍᴀᴛᴄʜ", callback_data="find_partner")]
        ])
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("targeted_search"))
async def targeted_search(bot, callback: CallbackQuery):
    search_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎂 ʙʏ ᴀɢᴇ", callback_data="search_age"),
         InlineKeyboardButton("📍 ʙʏ ʟᴏᴄᴀᴛɪᴏɴ", callback_data="search_location")],
        [InlineKeyboardButton("🎯 ʙʏ ɪɴᴛᴇʀᴇsᴛs", callback_data="search_interests"),
         InlineKeyboardButton("💎 ᴘʀᴇᴍɪᴜᴍ ᴏɴʟʏ", callback_data="search_premium")]
    ])
    
    await callback.message.edit_text(
        format_reply("🎯 ᴛᴀʀɢᴇᴛᴇᴅ sᴇᴀʀᴄʜ 🎯\n\nᴄʜᴏᴏsᴇ ʏᴏᴜʀ sᴇᴀʀᴄʜ ᴄʀɪᴛᴇʀɪᴀ:"),
        reply_markup=search_keyboard
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("vip_chats"))
async def vip_chats(bot, callback: CallbackQuery):
    await callback.message.edit_text(
        format_reply("👑 ᴠɪᴘ ᴄʜᴀᴛ ʀᴏᴏᴍs 👑\n\n🌟 ᴇxᴄʟᴜsɪᴠᴇ ᴀᴄᴄᴇss ᴛᴏ ᴘʀᴇᴍɪᴜᴍ ᴍᴇᴍʙᴇʀs\n💎 ʜɪɢʜ-ǫᴜᴀʟɪᴛʏ ᴄᴏɴᴠᴇʀsᴀᴛɪᴏɴs\n✨ ᴠᴇʀɪғɪᴇᴅ ᴜsᴇʀs ᴏɴʟʏ"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("💬 ᴊᴏɪɴ ᴠɪᴘ ᴄʜᴀᴛ", callback_data="join_vip_chat")]
        ])
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("private_messages"))
async def private_messages(bot, callback: CallbackQuery):
    await callback.message.edit_text(
        format_reply("💌 ᴘʀɪᴠᴀᴛᴇ ᴍᴇssᴀɢɪɴɢ 💌\n\n📨 sᴇɴᴅ ᴅɪʀᴇᴄᴛ ᴍᴇssᴀɢᴇs\n🔒 ᴇɴᴄʀʏᴘᴛᴇᴅ ᴄʜᴀᴛs\n👀 ʀᴇᴀᴅ ʀᴇᴄᴇɪᴘᴛs"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("💌 sᴇɴᴅ ᴍᴇssᴀɢᴇ", callback_data="send_private_msg")]
        ])
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("exclusive_club"))
async def exclusive_club(bot, callback: CallbackQuery):
    await callback.message.edit_text(
        format_reply("🏆 ᴇxᴄʟᴜsɪᴠᴇ ᴄʟᴜʙ 🏆\n\n👑 ᴇʟɪᴛᴇ ᴍᴇᴍʙᴇʀs ᴏɴʟʏ\n💎 sᴘᴇᴄɪᴀʟ ᴇᴠᴇɴᴛs\n🌟 ᴘʀɪᴠᴀᴛᴇ ɢᴀᴛʜᴇʀɪɴɢs"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🚪 ᴇɴᴛᴇʀ ᴄʟᴜʙ", callback_data="enter_club")]
        ])
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("invite_friends"))
async def invite_friends(bot, callback: CallbackQuery):
    user_id = callback.from_user.id
    invite_link = f"https://t.me/YourBotUsername?start={user_id}"
    
    await callback.message.edit_text(
        format_reply(f"👥 ɪɴᴠɪᴛᴇ ғʀɪᴇɴᴅs 👥\n\n🎁 ᴇᴀʀɴ 5 ᴄᴏɪɴs ᴘᴇʀ ʀᴇғᴇʀʀᴀʟ!\n\nʏᴏᴜʀ ɪɴᴠɪᴛᴇ ʟɪɴᴋ:\n{invite_link}"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📱 sʜᴀʀᴇ ʟɪɴᴋ", url=f"https://t.me/share/url?url={invite_link}")]
        ])
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("play_for_coins"))
async def play_for_coins(bot, callback: CallbackQuery):
    await callback.message.edit_text(
        format_reply("🎮 ᴘʟᴀʏ & ᴇᴀʀɴ 🎮\n\n🎯 ᴘʟᴀʏ ɢᴀᴍᴇs ᴛᴏ ᴇᴀʀɴ ᴄᴏɪɴs!\n💰 ᴜᴘ ᴛᴏ 50 ᴄᴏɪɴs ᴘᴇʀ ɢᴀᴍᴇ!"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🎮 sᴛᴀʀᴛ ɢᴀᴍɪɴɢ", callback_data="mini_games")]
        ])
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("daily_tasks"))
async def daily_tasks(bot, callback: CallbackQuery):
    await callback.message.edit_text(
        format_reply("📝 ᴅᴀɪʟʏ ᴛᴀsᴋs 📝\n\n✅ sᴇɴᴅ 5 ᴍᴇssᴀɢᴇs: +10 ᴄᴏɪɴs\n✅ ᴍᴀᴋᴇ 1 ᴍᴀᴛᴄʜ: +20 ᴄᴏɪɴs\n✅ ᴘʟᴀʏ 3 ɢᴀᴍᴇs: +15 ᴄᴏɪɴs"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🎯 sᴛᴀʀᴛ ᴛᴀsᴋs", callback_data="daily_challenges")]
        ])
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("watch_ads"))
async def watch_ads(bot, callback: CallbackQuery):
    # Simulate ad watching
    coins_earned = random.randint(5, 15)
    users.update_one(
        {"_id": callback.from_user.id},
        {"$inc": {"coins": coins_earned}}
    )
    
    await callback.message.edit_text(
        format_reply(f"📺 ᴀᴅ ᴡᴀᴛᴄʜᴇᴅ! 📺\n\nᴇᴀʀɴᴇᴅ: {coins_earned} ᴄᴏɪɴs! 💰\n\nᴛʜᴀɴᴋ ʏᴏᴜ ғᴏʀ sᴜᴘᴘᴏʀᴛɪɴɢ ᴜs! ❤️"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📺 ᴡᴀᴛᴄʜ ᴀɴᴏᴛʜᴇʀ", callback_data="watch_ads"),
             InlineKeyboardButton("💰 ᴠɪᴇᴡ ᴄᴏɪɴs", callback_data="view_profile")]
        ])
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("buy_coins"))
async def buy_coins(bot, callback: CallbackQuery):
    coin_packages = InlineKeyboardMarkup([
        [InlineKeyboardButton("💰 100 ᴄᴏɪɴs - $1", callback_data="buy_package_100"),
         InlineKeyboardButton("💰 500 ᴄᴏɪɴs - $4", callback_data="buy_package_500")],
        [InlineKeyboardButton("💰 1000 ᴄᴏɪɴs - $7", callback_data="buy_package_1000"),
         InlineKeyboardButton("💰 2500 ᴄᴏɪɴs - $15", callback_data="buy_package_2500")]
    ])
    
    await callback.message.edit_text(
        format_reply("💰 ᴄᴏɪɴ ᴘᴀᴄᴋᴀɢᴇs 💰\n\nᴄʜᴏᴏsᴇ ʏᴏᴜʀ ᴘᴀᴄᴋᴀɢᴇ:"),
        reply_markup=coin_packages
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("compat_"))
async def handle_compatibility_answers(bot, callback: CallbackQuery):
    answer = callback.data.split("_")[1]
    
    # Update user's compatibility preferences
    users.update_one(
        {"_id": callback.from_user.id},
        {"$set": {"compatibility_preference": answer}}
    )
    
    compatibility_score = random.randint(70, 95)
    
    await callback.message.edit_text(
        format_reply(f"💕 ᴄᴏᴍᴘᴀᴛɪʙɪʟɪᴛʏ ʀᴇsᴜʟᴛ 💕\n\nʏᴏᴜʀ ᴄʜᴏɪᴄᴇ: {answer}\n\nᴄᴏᴍᴘᴀᴛɪʙɪʟɪᴛʏ sᴄᴏʀᴇ: {compatibility_score}%! 🎯"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔍 ғɪɴᴅ ᴄᴏᴍᴘᴀᴛɪʙʟᴇ ᴍᴀᴛᴄʜ", callback_data="find_partner")]
        ])
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("share_love_letter"))
async def share_love_letter(bot, callback: CallbackQuery):
    await callback.message.edit_text(
        format_reply("💌 ʟᴏᴠᴇ ʟᴇᴛᴛᴇʀ sʜᴀʀᴇᴅ! 💌\n\nsᴏᴍᴇᴏɴᴇ sᴘᴇᴄɪᴀʟ ᴡɪʟʟ ʀᴇᴄᴇɪᴠᴇ ʏᴏᴜʀ ʜᴇᴀʀᴛғᴇʟᴛ ᴍᴇssᴀɢᴇ! ✨"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("💕 sᴇɴᴅ ᴀɴᴏᴛʜᴇʀ", callback_data="love_letters")]
        ])
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("write_custom_letter"))
async def write_custom_letter(bot, callback: CallbackQuery):
    await callback.message.edit_text(
        format_reply("✍️ ᴡʀɪᴛᴇ ᴄᴜsᴛᴏᴍ ʟᴇᴛᴛᴇʀ ✍️\n\nᴛʏᴘᴇ ʏᴏᴜʀ ʜᴇᴀʀᴛғᴇʟᴛ ᴍᴇssᴀɢᴇ ᴀɴᴅ ɪ'ʟʟ ᴍᴀᴋᴇ ɪᴛ ʙᴇᴀᴜᴛɪғᴜʟ! 💕"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="love_letters")]
        ])
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("love_letters"))
async def love_letters_feature(bot, callback: CallbackQuery):
    love_quotes = [
        "ʏᴏᴜ ᴀʀᴇ ᴛʜᴇ sᴜɴsʜɪɴᴇ ᴛʜᴀᴛ ʙʀɪɢʜᴛᴇɴs ᴍʏ ᴅᴀʏ! ☀️💕",
        "ɪɴ ᴀ sᴇᴀ ᴏғ ᴘᴇᴏᴘʟᴇ, ᴍʏ ᴇʏᴇs ᴡɪʟʟ ᴀʟᴡᴀʏs sᴇᴀʀᴄʜ ғᴏʀ ʏᴏᴜ! 👀💖",
        "ʏᴏᴜ'ʀᴇ ɴᴏᴛ ᴊᴜsᴛ ᴍʏ ʟᴏᴠᴇ, ʏᴏᴜ'ʀᴇ ᴍʏ ʙᴇsᴛ ғʀɪᴇɴᴅ! 👫💕",
        "ᴇᴠᴇʀʏ ᴍᴏᴍᴇɴᴛ sᴘᴇɴᴛ ᴡɪᴛʜ ʏᴏᴜ ɪs ᴀ ᴍᴏᴍᴇɴᴛ ᴛʀᴇᴀsᴜʀᴇᴅ! 💎⏰"
    ]
    
    selected_quote = random.choice(love_quotes)
    
    letters_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💌 sᴇɴᴅ ᴀɴᴏᴛʜᴇʀ", callback_data="love_letters"),
         InlineKeyboardButton("💕 sʜᴀʀᴇ ᴡɪᴛʜ ᴄʀᴜsʜ", callback_data="share_love_letter")],
        [InlineKeyboardButton("✍️ ᴡʀɪᴛᴇ ᴄᴜsᴛᴏᴍ", callback_data="write_custom_letter")]
    ])
    
    await callback.message.edit_text(
        format_reply(f"ʜᴇʀᴇ's ᴀ ʟᴏᴠᴇ ʟᴇᴛᴛᴇʀ ғᴏʀ ʏᴏᴜ! 💌\n\n{selected_quote}"),
        reply_markup=letters_keyboard
    )
    await callback.answer()
