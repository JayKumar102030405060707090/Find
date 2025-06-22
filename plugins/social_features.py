
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

@Client.on_callback_query(filters.regex("group_"))
async def join_group(bot, callback: CallbackQuery):
    group_type = callback.data.split("_")[1]
    
    group_names = {
        "romantics": "💕 ʀᴏᴍᴀɴᴛɪᴄs ᴄɪʀᴄʟᴇ",
        "gamers": "🎮 ɢᴀᴍᴇʀs ᴜɴɪᴛᴇᴅ",
        "books": "📚 ʙᴏᴏᴋ ʟᴏᴠᴇʀs",
        "music": "🎵 ᴍᴜsɪᴄ ғᴀɴs",
        "fitness": "🏃 ғɪᴛɴᴇss ʜᴇʀᴏᴇs",
        "food": "🍳 ғᴏᴏᴅɪᴇ ᴄʟᴜʙ",
        "travel": "🌍 ᴛʀᴀᴠᴇʟ ʙᴜᴅᴅɪᴇs",
        "art": "🎨 ᴀʀᴛɪsᴛɪᴄ sᴏᴜʟs"
    }
    
    group_name = group_names.get(group_type, "ɢʀᴏᴜᴘ")
    
    # Add user to group
    users.update_one(
        {"_id": callback.from_user.id},
        {"$addToSet": {"joined_groups": group_type}}
    )
    
    await callback.message.edit_text(
        format_reply(f"🎉 ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ {group_name}! 🎉\n\nʏᴏᴜ'ᴠᴇ sᴜᴄᴄᴇssғᴜʟʟʏ ᴊᴏɪɴᴇᴅ ᴛʜᴇ ɢʀᴏᴜᴘ! ✨"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("👥 ᴠɪᴇᴡ ᴍᴇᴍʙᴇʀs", callback_data=f"view_group_{group_type}"),
             InlineKeyboardButton("💬 ɢʀᴏᴜᴘ ᴄʜᴀᴛ", callback_data=f"chat_group_{group_type}")],
            [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="join_groups")]
        ])
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("event_"))
async def join_event(bot, callback: CallbackQuery):
    event_type = callback.data.split("_")[1]
    
    events = {
        "speed": "💕 sᴘᴇᴇᴅ ᴅᴀᴛɪɴɢ ᴇᴠᴇɴᴛ",
        "roleplay": "🎭 ʀᴏʟᴇᴘʟᴀʏ ɴɪɢʜᴛ",
        "music": "🎵 ᴍᴜsɪᴄ ᴘᴀʀᴛʏ",
        "gaming": "🎮 ɢᴀᴍᴇ ᴛᴏᴜʀɴᴀᴍᴇɴᴛ",
        "midnight": "🌙 ᴍɪᴅɴɪɢʜᴛ ᴄʜᴀᴛ",
        "morning": "☀️ ᴍᴏʀɴɪɴɢ ᴍᴇᴇᴛ"
    }
    
    event_name = events.get(event_type, "ᴇᴠᴇɴᴛ")
    
    await callback.message.edit_text(
        format_reply(f"🎉 {event_name} 🎉\n\nʏᴏᴜ'ʀᴇ ʀᴇɢɪsᴛᴇʀᴇᴅ! ᴇᴠᴇɴᴛ sᴛᴀʀᴛs sᴏᴏɴ! ⏰"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🎯 ᴊᴏɪɴ ɴᴏᴡ", callback_data=f"start_event_{event_type}"),
             InlineKeyboardButton("📅 ᴍᴏʀᴇ ᴇᴠᴇɴᴛs", callback_data="view_events")]
        ])
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("buy_"))
async def buy_gift(bot, callback: CallbackQuery):
    gift_type = callback.data.split("_")[1]
    user_data = users.find_one({"_id": callback.from_user.id})
    
    gift_prices = {
        "rose": 10, "bouquet": 50, "ring": 100, "crown": 200,
        "teddy": 75, "chocolate": 25, "surprise": 150
    }
    
    price = gift_prices.get(gift_type, 10)
    
    if user_data.get("coins", 0) >= price:
        users.update_one(
            {"_id": callback.from_user.id},
            {"$inc": {"coins": -price}, "$addToSet": {"gifts_owned": gift_type}}
        )
        
        await callback.message.edit_text(
            format_reply(f"🎁 ɢɪғᴛ ᴘᴜʀᴄʜᴀsᴇᴅ! 🎁\n\nʏᴏᴜ ʙᴏᴜɢʜᴛ ᴀ {gift_type}! 💕\nʀᴇᴀᴅʏ ᴛᴏ sᴇɴᴅ ᴛᴏ sᴏᴍᴇᴏɴᴇ sᴘᴇᴄɪᴀʟ! ✨"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💝 sᴇɴᴅ ɢɪғᴛ", callback_data=f"send_gift_{gift_type}"),
                 InlineKeyboardButton("🛒 ʙᴜʏ ᴍᴏʀᴇ", callback_data="gift_shop")]
            ])
        )
    else:
        await callback.message.edit_text(
            format_reply(f"💔 ɪɴsᴜғғɪᴄɪᴇɴᴛ ᴄᴏɪɴs!\n\nɴᴇᴇᴅᴇᴅ: {price} ᴄᴏɪɴs\nʏᴏᴜ ʜᴀᴠᴇ: {user_data.get('coins', 0)} ᴄᴏɪɴs"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💰 ᴇᴀʀɴ ᴄᴏɪɴs", callback_data="earn_coins")]
            ])
        )
    
    await callback.answer()

@Client.on_callback_query(filters.regex("send_anonymous"))
async def send_anonymous_message(bot, callback: CallbackQuery):
    await callback.message.edit_text(
        format_reply("💌 sᴇɴᴅ ᴀɴᴏɴʏᴍᴏᴜs ᴍᴇssᴀɢᴇ 💌\n\nᴛʏᴘᴇ ʏᴏᴜʀ sᴇᴄʀᴇᴛ ᴍᴇssᴀɢᴇ ᴀɴᴅ ɪ'ʟʟ ᴅᴇʟɪᴠᴇʀ ɪᴛ! 🤫"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="secret_admirer")]
        ])
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("check_admirers"))
async def check_admirers(bot, callback: CallbackQuery):
    admirer_count = random.randint(0, 5)
    
    await callback.message.edit_text(
        format_reply(f"👀 sᴇᴄʀᴇᴛ ᴀᴅᴍɪʀᴇʀs 👀\n\nʏᴏᴜ ʜᴀᴠᴇ {admirer_count} sᴇᴄʀᴇᴛ ᴀᴅᴍɪʀᴇʀs! 💕"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("💌 ʀᴇᴀᴅ ᴍᴇssᴀɢᴇs", callback_data="read_admirers"),
             InlineKeyboardButton("🔍 ʀᴇᴠᴇᴀʟ ᴏɴᴇ", callback_data="reveal_identity")]
        ])
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("send_hint"))
async def send_hint(bot, callback: CallbackQuery):
    hints = [
        "ɪ ʟɪᴋᴇ ʏᴏᴜʀ sᴍɪʟᴇ... 😊",
        "ʏᴏᴜʀ ᴘʀᴏғɪʟᴇ ᴄᴀᴜɢʜᴛ ᴍʏ ᴇʏᴇ... 👀",
        "ʏᴏᴜ sᴇᴇᴍ ɪɴᴛᴇʀᴇsᴛɪɴɢ... 💫"
    ]
    
    hint = random.choice(hints)
    
    await callback.message.edit_text(
        format_reply(f"💕 ʜɪɴᴛ sᴇɴᴛ! 💕\n\n\"{hint}\"\n\nsᴏᴍᴇᴏɴᴇ ᴡɪʟʟ ʀᴇᴄᴇɪᴠᴇ ᴛʜɪs ᴍʏsᴛᴇʀɪᴏᴜs ʜɪɴᴛ! 🤫"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("💌 sᴇɴᴅ ᴀɴᴏᴛʜᴇʀ", callback_data="send_hint")]
        ])
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("reveal_identity"))
async def reveal_identity(bot, callback: CallbackQuery):
    user_data = users.find_one({"_id": callback.from_user.id})
    
    if user_data.get("coins", 0) >= REVEAL_COST:
        users.update_one(
            {"_id": callback.from_user.id},
            {"$inc": {"coins": -REVEAL_COST}}
        )
        
        fake_names = ["ᴀʟᴇx", "ᴊᴏʀᴅᴀɴ", "ᴄᴀsᴇʏ", "ᴀᴠᴇʀʏ"]
        revealed_name = random.choice(fake_names)
        
        await callback.message.edit_text(
            format_reply(f"🔍 ɪᴅᴇɴᴛɪᴛʏ ʀᴇᴠᴇᴀʟᴇᴅ! 🔍\n\nʏᴏᴜʀ sᴇᴄʀᴇᴛ ᴀᴅᴍɪʀᴇʀ ɪs: {revealed_name}! 💕"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💬 ᴍᴇssᴀɢᴇ ᴛʜᴇᴍ", callback_data="message_admirer")]
            ])
        )
    else:
        await callback.message.edit_text(
            format_reply(f"💔 ɴᴇᴇᴅ {REVEAL_COST} ᴄᴏɪɴs ᴛᴏ ʀᴇᴠᴇᴀʟ!\n\nʏᴏᴜ ʜᴀᴠᴇ: {user_data.get('coins', 0)} ᴄᴏɪɴs"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💰 ᴇᴀʀɴ ᴄᴏɪɴs", callback_data="earn_coins")]
            ])
        )
    
    await callback.answer()

@Client.on_callback_query(filters.regex("rp_"))
async def start_roleplay(bot, callback: CallbackQuery):
    rp_type = callback.data.split("_")[1]
    
    roleplays = {
        "royalty": "👸 ᴘʀɪɴᴄᴇss & ᴘʀɪɴᴄᴇ",
        "detective": "🕵️ ᴅᴇᴛᴇᴄᴛɪᴠᴇ sᴛᴏʀʏ",
        "magic": "🧙 ᴍᴀɢɪᴄ ᴡᴏʀʟᴅ",
        "space": "🚀 sᴘᴀᴄᴇ ᴀᴅᴠᴇɴᴛᴜʀᴇ",
        "school": "🏫 sᴄʜᴏᴏʟ ʀᴏᴍᴀɴᴄᴇ",
        "mermaid": "🌊 ᴍᴇʀᴍᴀɪᴅ ᴛᴀʟᴇ"
    }
    
    rp_name = roleplays.get(rp_type, "ʀᴏʟᴇᴘʟᴀʏ")
    
    await callback.message.edit_text(
        format_reply(f"🎭 {rp_name} 🎭\n\nʏᴏᴜʀ ʀᴏʟᴇᴘʟᴀʏ ᴀᴅᴠᴇɴᴛᴜʀᴇ ɪs sᴛᴀʀᴛɪɴɢ! ✨"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🎭 sᴛᴀʀᴛ ᴀᴄᴛɪɴɢ", callback_data=f"act_{rp_type}"),
             InlineKeyboardButton("👥 ғɪɴᴅ ᴘᴀʀᴛɴᴇʀ", callback_data="find_rp_partner")]
        ])
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("coin_leaders"))
async def coin_leaders(bot, callback: CallbackQuery):
    top_coins = users.find().sort("coins", -1).limit(5)
    
    leaderboard_text = "💰 ᴄᴏɪɴ ʟᴇᴀᴅᴇʀs 💰\n\n"
    for i, user in enumerate(top_coins, 1):
        name = user.get("name", "ᴀɴᴏɴʏᴍᴏᴜs")[:10]
        coins = user.get("coins", 0)
        leaderboard_text += f"{i}. {name} - {coins} ᴄᴏɪɴs\n"
    
    await callback.message.edit_text(
        format_reply(leaderboard_text),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="leaderboard")]
        ])
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("heart_leaders"))
async def heart_leaders(bot, callback: CallbackQuery):
    top_hearts = users.find().sort("hearts_received", -1).limit(5)
    
    leaderboard_text = "💖 ʜᴇᴀʀᴛ ʟᴇᴀᴅᴇʀs 💖\n\n"
    for i, user in enumerate(top_hearts, 1):
        name = user.get("name", "ᴀɴᴏɴʏᴍᴏᴜs")[:10]
        hearts = user.get("hearts_received", 0)
        leaderboard_text += f"{i}. {name} - {hearts} ʜᴇᴀʀᴛs\n"
    
    await callback.message.edit_text(
        format_reply(leaderboard_text),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="leaderboard")]
        ])
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("my_rank"))
async def my_rank(bot, callback: CallbackQuery):
    user_data = users.find_one({"_id": callback.from_user.id})
    
    # Calculate rank position
    higher_coins = users.count_documents({"coins": {"$gt": user_data.get("coins", 0)}})
    rank_position = higher_coins + 1
    
    await callback.message.edit_text(
        format_reply(f"🏅 ʏᴏᴜʀ ʀᴀɴᴋ 🏅\n\nᴘᴏsɪᴛɪᴏɴ: #{rank_position}\nᴄᴏɪɴs: {user_data.get('coins', 0)}\nʜᴇᴀʀᴛs: {user_data.get('hearts_received', 0)}"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📈 ɪᴍᴘʀᴏᴠᴇ ʀᴀɴᴋ", callback_data="earn_coins")]
        ])
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

@Client.on_callback_query(filters.regex("find_by_interests"))
async def find_by_interests(bot, callback: CallbackQuery):
    user_data = users.find_one({"_id": callback.from_user.id})
    user_interests = user_data.get("interests", [])
    
    if user_interests:
        # Find users with similar interests
        friends = list(users.find({
            "_id": {"$ne": callback.from_user.id},
            "interests": {"$in": user_interests}
        }).limit(3))
        
        if friends:
            friend_buttons = []
            for friend in friends:
                name = friend.get("name", "ᴀɴᴏɴʏᴍᴏᴜs")[:15]
                common_interests = len(set(friend.get("interests", [])).intersection(set(user_interests)))
                friend_buttons.append([
                    InlineKeyboardButton(f"👤 {name} ({common_interests} ᴄᴏᴍᴍᴏɴ)", 
                                       callback_data=f"add_friend:{friend['_id']}")
                ])
            
            await callback.message.edit_text(
                format_reply("👥 ғʀɪᴇɴᴅs ᴡɪᴛʜ sɪᴍɪʟᴀʀ ɪɴᴛᴇʀᴇsᴛs! 👥"),
                reply_markup=InlineKeyboardMarkup(friend_buttons)
            )
        else:
            await callback.message.edit_text(
                format_reply("😔 ɴᴏ ғʀɪᴇɴᴅs ғᴏᴜɴᴅ ᴡɪᴛʜ sɪᴍɪʟᴀʀ ɪɴᴛᴇʀᴇsᴛs!\nᴛʀʏ ᴀᴅᴅɪɴɢ ᴍᴏʀᴇ ɪɴᴛᴇʀᴇsᴛs ᴛᴏ ʏᴏᴜʀ ᴘʀᴏғɪʟᴇ! ✨"),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🎯 ᴀᴅᴅ ɪɴᴛᴇʀᴇsᴛs", callback_data="add_interests")]
                ])
            )
    else:
        await callback.message.edit_text(
            format_reply("😊 ᴀᴅᴅ ɪɴᴛᴇʀᴇsᴛs ᴛᴏ ғɪɴᴅ ʟɪᴋᴇ-ᴍɪɴᴅᴇᴅ ғʀɪᴇɴᴅs!"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🎯 ᴀᴅᴅ ɪɴᴛᴇʀᴇsᴛs", callback_data="add_interests")]
            ])
        )
    
    await callback.answer()

@Client.on_callback_query(filters.regex("find_by_location"))
async def find_by_location(bot, callback: CallbackQuery):
    user_data = users.find_one({"_id": callback.from_user.id})
    user_location = user_data.get("location")
    
    if user_location and user_location != "Not Set":
        friends = list(users.find({
            "_id": {"$ne": callback.from_user.id},
            "location": user_location
        }).limit(5))
        
        if friends:
            friend_buttons = []
            for friend in friends:
                name = friend.get("name", "ᴀɴᴏɴʏᴍᴏᴜs")[:15]
                friend_buttons.append([
                    InlineKeyboardButton(f"📍 {name} ({user_location})", 
                                       callback_data=f"add_friend:{friend['_id']}")
                ])
            
            await callback.message.edit_text(
                format_reply(f"📍 ғʀɪᴇɴᴅs ɴᴇᴀʀ {user_location}! 📍"),
                reply_markup=InlineKeyboardMarkup(friend_buttons)
            )
        else:
            await callback.message.edit_text(
                format_reply(f"😔 ɴᴏ ғʀɪᴇɴᴅs ғᴏᴜɴᴅ ɪɴ {user_location}!\nᴛʀʏ ᴇxᴘᴀɴᴅɪɴɢ ʏᴏᴜʀ sᴇᴀʀᴄʜ! 🌍"))
        )
    else:
        await callback.message.edit_text(
            format_reply("📍 ᴀᴅᴅ ʏᴏᴜʀ ʟᴏᴄᴀᴛɪᴏɴ ᴛᴏ ғɪɴᴅ ɴᴇᴀʀʙʏ ғʀɪᴇɴᴅs!"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✏️ ᴇᴅɪᴛ ᴘʀᴏғɪʟᴇ", callback_data="edit_profile")]
            ])
        )
    
    await callback.answer()

@Client.on_callback_query(filters.regex("find_by_age"))
async def find_by_age(bot, callback: CallbackQuery):
    user_data = users.find_one({"_id": callback.from_user.id})
    user_age = user_data.get("age")
    
    if user_age:
        # Find friends within 5 years age range
        friends = list(users.find({
            "_id": {"$ne": callback.from_user.id},
            "age": {"$gte": user_age - 5, "$lte": user_age + 5}
        }).limit(5))
        
        if friends:
            friend_buttons = []
            for friend in friends:
                name = friend.get("name", "ᴀɴᴏɴʏᴍᴏᴜs")[:15]
                age = friend.get("age", "N/A")
                friend_buttons.append([
                    InlineKeyboardButton(f"🎂 {name} ({age})", 
                                       callback_data=f"add_friend:{friend['_id']}")
                ])
            
            await callback.message.edit_text(
                format_reply("🎂 ғʀɪᴇɴᴅs ɪɴ ʏᴏᴜʀ ᴀɢᴇ ɢʀᴏᴜᴘ! 🎂"),
                reply_markup=InlineKeyboardMarkup(friend_buttons)
            )
        else:
            await callback.message.edit_text(
                format_reply("😔 ɴᴏ ғʀɪᴇɴᴅs ғᴏᴜɴᴅ ɪɴ ʏᴏᴜʀ ᴀɢᴇ ʀᴀɴɢᴇ!"))
        )
    else:
        await callback.message.edit_text(
            format_reply("🎂 ᴀᴅᴅ ʏᴏᴜʀ ᴀɢᴇ ᴛᴏ ғɪɴᴅ ᴀɢᴇ-ᴀᴘᴘʀᴏᴘʀɪᴀᴛᴇ ғʀɪᴇɴᴅs!"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✏️ ᴇᴅɪᴛ ᴘʀᴏғɪʟᴇ", callback_data="edit_profile")]
            ])
        )
    
    await callback.answer()

@Client.on_callback_query(filters.regex("random_friend"))
async def random_friend(bot, callback: CallbackQuery):
    # Find a random user
    pipeline = [
        {"$match": {"_id": {"$ne": callback.from_user.id}}},
        {"$sample": {"size": 1}}
    ]
    
    random_users = list(users.aggregate(pipeline))
    
    if random_users:
        friend = random_users[0]
        name = friend.get("name", "ᴀɴᴏɴʏᴍᴏᴜs")
        age = friend.get("age", "N/A")
        location = friend.get("location", "ᴜɴᴋɴᴏᴡɴ")
        
        await callback.message.edit_text(
            format_reply(f"🎲 ʀᴀɴᴅᴏᴍ ғʀɪᴇɴᴅ 🎲\n\n👤 {name}\n🎂 {age}\n📍 {location}"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("👥 ᴀᴅᴅ ғʀɪᴇɴᴅ", callback_data=f"add_friend:{friend['_id']}"),
                 InlineKeyboardButton("💬 sᴀʏ ʜɪ", callback_data=f"say_hi:{friend['_id']}")],
                [InlineKeyboardButton("🎲 ᴀɴᴏᴛʜᴇʀ ʀᴀɴᴅᴏᴍ", callback_data="random_friend")]
            ])
        )
    else:
        await callback.message.edit_text(
            format_reply("😔 ɴᴏ ᴜsᴇʀs ᴀᴠᴀɪʟᴀʙʟᴇ ʀɪɢʜᴛ ɴᴏᴡ!"))
        )
    
    await callback.answer()
