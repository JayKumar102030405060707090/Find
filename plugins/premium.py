
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
