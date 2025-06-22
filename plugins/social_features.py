
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import *
from pymongo import MongoClient
from datetime import datetime, timedelta
import random

client = MongoClient(MONGO_URL)
db = client['find_partner']
users = db['users']
groups = db['groups']
events = db['events']
stories = db['stories']

def format_reply(text):
    tiny_caps_map = {
        'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ', 'f': 'ғ', 'g': 'ɢ', 'h': 'ʜ',
        'i': 'ɪ', 'j': 'ᴊ', 'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ', 'o': 'ᴏ', 'p': 'ᴘ',
        'q': 'ǫ', 'r': 'ʀ', 's': 's', 't': 'ᴛ', 'u': 'ᴜ', 'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x',
        'y': 'ʏ', 'z': 'ᴢ'
    }
    converted = ''.join(tiny_caps_map.get(char.lower(), char) for char in text)
    return f"❖ **{converted}**"

@Client.on_callback_query(filters.regex("social_hub"))
async def social_hub_menu(bot, callback: CallbackQuery):
    social_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("👥 ᴊᴏɪɴ ɢʀᴏᴜᴘs", callback_data="join_groups"),
         InlineKeyboardButton("🎉 ᴇᴠᴇɴᴛs", callback_data="view_events")],
        [InlineKeyboardButton("📱 sᴛᴏʀɪᴇs", callback_data="view_stories"),
         InlineKeyboardButton("🏆 ʟᴇᴀᴅᴇʀʙᴏᴀʀᴅ", callback_data="leaderboard")],
        [InlineKeyboardButton("💝 ɢɪғᴛ sʜᴏᴘ", callback_data="gift_shop"),
         InlineKeyboardButton("🎭 ʀᴏʟᴇ ᴘʟᴀʏ", callback_data="roleplay_menu")],
        [InlineKeyboardButton("🌟 ᴍᴀᴋᴇ ғʀɪᴇɴᴅs", callback_data="friend_finder"),
         InlineKeyboardButton("💌 sᴇᴄʀᴇᴛ ᴀᴅᴍɪʀᴇʀ", callback_data="secret_admirer")]
    ])
    
    await callback.message.edit_text(
        format_reply("ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ sᴏᴄɪᴀʟ ʜᴜʙ! 🌟✨"),
        reply_markup=social_keyboard
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("join_groups"))
async def join_groups_menu(bot, callback: CallbackQuery):
    groups_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💕 ʀᴏᴍᴀɴᴛɪᴄs", callback_data="group_romantics"),
         InlineKeyboardButton("🎮 ɢᴀᴍᴇʀs", callback_data="group_gamers")],
        [InlineKeyboardButton("📚 ʙᴏᴏᴋ ʟᴏᴠᴇʀs", callback_data="group_books"),
         InlineKeyboardButton("🎵 ᴍᴜsɪᴄ ғᴀɴs", callback_data="group_music")],
        [InlineKeyboardButton("🏃 ғɪᴛɴᴇss", callback_data="group_fitness"),
         InlineKeyboardButton("🍳 ғᴏᴏᴅɪᴇs", callback_data="group_food")],
        [InlineKeyboardButton("🌍 ᴛʀᴀᴠᴇʟᴇʀs", callback_data="group_travel"),
         InlineKeyboardButton("🎨 ᴀʀᴛɪsᴛs", callback_data="group_art")]
    ])
    
    await callback.message.edit_text(
        format_reply("ᴊᴏɪɴ ɪɴᴛᴇʀᴇsᴛ ɢʀᴏᴜᴘs! 👥💫"),
        reply_markup=groups_keyboard
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("view_events"))
async def view_events_menu(bot, callback: CallbackQuery):
    events_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💕 sᴘᴇᴇᴅ ᴅᴀᴛɪɴɢ", callback_data="event_speed_dating"),
         InlineKeyboardButton("🎭 ʀᴏʟᴇᴘʟᴀʏ ɴɪɢʜᴛ", callback_data="event_roleplay")],
        [InlineKeyboardButton("🎵 ᴍᴜsɪᴄ ᴘᴀʀᴛʏ", callback_data="event_music"),
         InlineKeyboardButton("🎮 ɢᴀᴍᴇ ᴛᴏᴜʀɴᴀᴍᴇɴᴛ", callback_data="event_gaming")],
        [InlineKeyboardButton("🌙 ᴍɪᴅɴɪɢʜᴛ ᴄʜᴀᴛ", callback_data="event_midnight"),
         InlineKeyboardButton("☀️ ᴍᴏʀɴɪɴɢ ᴍᴇᴇᴛ", callback_data="event_morning")]
    ])
    
    await callback.message.edit_text(
        format_reply("ᴜᴘᴄᴏᴍɪɴɢ ᴇᴠᴇɴᴛs! 🎉✨"),
        reply_markup=events_keyboard
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("gift_shop"))
async def gift_shop_menu(bot, callback: CallbackQuery):
    gift_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🌹 ʀᴏsᴇ (10 ᴄᴏɪɴs)", callback_data="buy_rose"),
         InlineKeyboardButton("💐 ʙᴏᴜǫᴜᴇᴛ (50 ᴄᴏɪɴs)", callback_data="buy_bouquet")],
        [InlineKeyboardButton("💍 ʀɪɴɢ (100 ᴄᴏɪɴs)", callback_data="buy_ring"),
         InlineKeyboardButton("👑 ᴄʀᴏᴡɴ (200 ᴄᴏɪɴs)", callback_data="buy_crown")],
        [InlineKeyboardButton("🧸 ᴛᴇᴅᴅʏ (75 ᴄᴏɪɴs)", callback_data="buy_teddy"),
         InlineKeyboardButton("🍫 ᴄʜᴏᴄᴏʟᴀᴛᴇ (25 ᴄᴏɪɴs)", callback_data="buy_chocolate")],
        [InlineKeyboardButton("🎁 sᴜʀᴘʀɪsᴇ ʙᴏx (150 ᴄᴏɪɴs)", callback_data="buy_surprise")]
    ])
    
    user_data = users.find_one({"_id": callback.from_user.id})
    coins = user_data.get("coins", 0)
    
    await callback.message.edit_text(
        format_reply(f"ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ɢɪғᴛ sʜᴏᴘ! 💝\n\nʏᴏᴜʀ ᴄᴏɪɴs: {coins} 💰"),
        reply_markup=gift_keyboard
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("secret_admirer"))
async def secret_admirer_feature(bot, callback: CallbackQuery):
    admirer_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💌 sᴇɴᴅ ᴀɴᴏɴʏᴍᴏᴜs ᴍᴇssᴀɢᴇ", callback_data="send_anonymous"),
         InlineKeyboardButton("👀 ᴄʜᴇᴄᴋ ᴀᴅᴍɪʀᴇʀs", callback_data="check_admirers")],
        [InlineKeyboardButton("💕 sᴇɴᴅ ʜɪɴᴛ", callback_data="send_hint"),
         InlineKeyboardButton("🔍 ʀᴇᴠᴇᴀʟ ɪᴅᴇɴᴛɪᴛʏ", callback_data="reveal_identity")]
    ])
    
    await callback.message.edit_text(
        format_reply("sᴇᴄʀᴇᴛ ᴀᴅᴍɪʀᴇʀ sʏsᴛᴇᴍ! 💌✨\n\nsᴏᴍᴇᴏɴᴇ ᴍɪɢʜᴛ ʙᴇ ᴡᴀᴛᴄʜɪɴɢ ʏᴏᴜ... 👀💕"),
        reply_markup=admirer_keyboard
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("roleplay_menu"))
async def roleplay_menu(bot, callback: CallbackQuery):
    roleplay_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("👸 ᴘʀɪɴᴄᴇss & ᴘʀɪɴᴄᴇ", callback_data="rp_royalty"),
         InlineKeyboardButton("🕵️ ᴅᴇᴛᴇᴄᴛɪᴠᴇ sᴛᴏʀʏ", callback_data="rp_detective")],
        [InlineKeyboardButton("🧙 ᴍᴀɢɪᴄ ᴡᴏʀʟᴅ", callback_data="rp_magic"),
         InlineKeyboardButton("🚀 sᴘᴀᴄᴇ ᴀᴅᴠᴇɴᴛᴜʀᴇ", callback_data="rp_space")],
        [InlineKeyboardButton("🏫 sᴄʜᴏᴏʟ ʀᴏᴍᴀɴᴄᴇ", callback_data="rp_school"),
         InlineKeyboardButton("🌊 ᴍᴇʀᴍᴀɪᴅ ᴛᴀʟᴇ", callback_data="rp_mermaid")]
    ])
    
    await callback.message.edit_text(
        format_reply("ᴄʜᴏᴏsᴇ ʏᴏᴜʀ ʀᴏʟᴇᴘʟᴀʏ ᴀᴅᴠᴇɴᴛᴜʀᴇ! 🎭✨"),
        reply_markup=roleplay_keyboard
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("leaderboard"))
async def show_leaderboard(bot, callback: CallbackQuery):
    # Get top users by various metrics
    top_matches = users.find().sort("matches_count", -1).limit(5)
    top_coins = users.find().sort("coins", -1).limit(5)
    top_hearts = users.find().sort("hearts_received", -1).limit(5)
    
    leaderboard_text = "🏆 ʟᴇᴀᴅᴇʀʙᴏᴀʀᴅ 🏆\n\n"
    leaderboard_text += "💕 ᴍᴏsᴛ ᴍᴀᴛᴄʜᴇs:\n"
    
    for i, user in enumerate(top_matches, 1):
        name = user.get("name", "ᴀɴᴏɴʏᴍᴏᴜs")[:10]
        matches = user.get("matches_count", 0)
        leaderboard_text += f"{i}. {name} - {matches} ᴍᴀᴛᴄʜᴇs\n"
    
    leaderboard_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💰 ᴄᴏɪɴ ʟᴇᴀᴅᴇʀs", callback_data="coin_leaders"),
         InlineKeyboardButton("💖 ʜᴇᴀʀᴛ ʟᴇᴀᴅᴇʀs", callback_data="heart_leaders")],
        [InlineKeyboardButton("🎯 ᴍʏ ʀᴀɴᴋ", callback_data="my_rank")]
    ])
    
    await callback.message.edit_text(
        format_reply(leaderboard_text),
        reply_markup=leaderboard_keyboard
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("friend_finder"))
async def friend_finder_menu(bot, callback: CallbackQuery):
    friend_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔍 ғɪɴᴅ ʙʏ ɪɴᴛᴇʀᴇsᴛs", callback_data="find_by_interests"),
         InlineKeyboardButton("🌍 ғɪɴᴅ ʙʏ ʟᴏᴄᴀᴛɪᴏɴ", callback_data="find_by_location")],
        [InlineKeyboardButton("🎂 ғɪɴᴅ ʙʏ ᴀɢᴇ", callback_data="find_by_age"),
         InlineKeyboardButton("🎲 ʀᴀɴᴅᴏᴍ ғʀɪᴇɴᴅ", callback_data="random_friend")],
        [InlineKeyboardButton("👥 ғʀɪᴇɴᴅ ʀᴇǫᴜᴇsᴛs", callback_data="friend_requests"),
         InlineKeyboardButton("💫 ᴍᴜᴛᴜᴀʟ ғʀɪᴇɴᴅs", callback_data="mutual_friends")]
    ])
    
    await callback.message.edit_text(
        format_reply("ʟᴇᴛ's ғɪɴᴅ ʏᴏᴜʀ ɴᴇᴡ ʙᴇsᴛ ғʀɪᴇɴᴅ! 🌟👫"),
        reply_markup=friend_keyboard
    )
    await callback.answer()
