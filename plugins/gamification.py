
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import *
from pymongo import MongoClient
from datetime import datetime, timedelta
import random

client = MongoClient(MONGO_URL)
db = client['find_partner']
users = db['users']
achievements = db['achievements']
challenges = db['challenges']
quests = db['quests']

def format_reply(text):
    tiny_caps_map = {
        'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ', 'f': 'ғ', 'g': 'ɢ', 'h': 'ʜ',
        'i': 'ɪ', 'j': 'ᴊ', 'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ', 'o': 'ᴏ', 'p': 'ᴘ',
        'q': 'ǫ', 'r': 'ʀ', 's': 's', 't': 'ᴛ', 'u': 'ᴜ', 'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x',
        'y': 'ʏ', 'z': 'ᴢ'
    }
    converted = ''.join(tiny_caps_map.get(char.lower(), char) for char in text)
    return f"❖ **{converted}**"

ACHIEVEMENTS = {
    "first_match": {"name": "💕 ғɪʀsᴛ ʟᴏᴠᴇ", "desc": "ᴍᴀᴋᴇ ʏᴏᴜʀ ғɪʀsᴛ ᴍᴀᴛᴄʜ", "reward": 50},
    "social_butterfly": {"name": "🦋 sᴏᴄɪᴀʟ ʙᴜᴛᴛᴇʀғʟʏ", "desc": "ᴄʜᴀᴛ ᴡɪᴛʜ 10 ᴘᴇᴏᴘʟᴇ", "reward": 100},
    "heartbreaker": {"name": "💔 ʜᴇᴀʀᴛʙʀᴇᴀᴋᴇʀ", "desc": "ʀᴇᴄᴇɪᴠᴇ 100 ʜᴇᴀʀᴛs", "reward": 200},
    "premium_member": {"name": "💎 ᴘʀᴇᴍɪᴜᴍ ᴇʟɪᴛᴇ", "desc": "ᴜᴘɢʀᴀᴅᴇ ᴛᴏ ᴘʀᴇᴍɪᴜᴍ", "reward": 300},
    "game_master": {"name": "🎮 ɢᴀᴍᴇ ᴍᴀsᴛᴇʀ", "desc": "ᴘʟᴀʏ 50 ɢᴀᴍᴇs", "reward": 150}
}

@Client.on_callback_query(filters.regex("game_center"))
async def game_center_menu(bot, callback: CallbackQuery):
    game_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🏆 ᴀᴄʜɪᴇᴠᴇᴍᴇɴᴛs", callback_data="view_achievements"),
         InlineKeyboardButton("🎯 ᴄʜᴀʟʟᴇɴɢᴇs", callback_data="daily_challenges")],
        [InlineKeyboardButton("🗡️ ǫᴜᴇsᴛs", callback_data="view_quests"),
         InlineKeyboardButton("🎪 ᴍɪɴɪ ɢᴀᴍᴇs", callback_data="mini_games")],
        [InlineKeyboardButton("⚔️ ᴘᴠᴘ ʙᴀᴛᴛʟᴇs", callback_data="pvp_battles"),
         InlineKeyboardButton("🎲 ʟᴜᴄᴋʏ ᴡʜᴇᴇʟ", callback_data="lucky_wheel")],
        [InlineKeyboardButton("🏅 ʀᴀɴᴋɪɴɢ sʏsᴛᴇᴍ", callback_data="ranking_system"),
         InlineKeyboardButton("💰 ʀᴇᴡᴀʀᴅ sʜᴏᴘ", callback_data="reward_shop")]
    ])
    
    await callback.message.edit_text(
        format_reply("ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ɢᴀᴍᴇ ᴄᴇɴᴛᴇʀ! 🎮✨"),
        reply_markup=game_keyboard
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("view_achievements"))
async def view_achievements_menu(bot, callback: CallbackQuery):
    user_data = users.find_one({"_id": callback.from_user.id})
    user_achievements = user_data.get("achievements", [])
    
    achievements_text = "🏆 ʏᴏᴜʀ ᴀᴄʜɪᴇᴠᴇᴍᴇɴᴛs 🏆\n\n"
    
    for ach_id, ach_data in ACHIEVEMENTS.items():
        status = "✅" if ach_id in user_achievements else "❌"
        achievements_text += f"{status} {ach_data['name']}\n   {ach_data['desc']}\n   ʀᴇᴡᴀʀᴅ: {ach_data['reward']} ᴄᴏɪɴs\n\n"
    
    achievement_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎯 ᴄʜᴇᴄᴋ ᴘʀᴏɢʀᴇss", callback_data="check_progress"),
         InlineKeyboardButton("🏆 ᴇᴀʀɴ ᴍᴏʀᴇ", callback_data="earn_achievements")]
    ])
    
    await callback.message.edit_text(
        format_reply(achievements_text),
        reply_markup=achievement_keyboard
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("daily_challenges"))
async def daily_challenges_menu(bot, callback: CallbackQuery):
    today = datetime.now().strftime("%Y-%m-%d")
    user_data = users.find_one({"_id": callback.from_user.id})
    completed_today = user_data.get(f"challenges_{today}", [])
    
    daily_challenges = [
        {"id": "send_hearts", "name": "💖 sᴇɴᴅ 5 ʜᴇᴀʀᴛs", "reward": 20, "progress": 0, "target": 5},
        {"id": "play_games", "name": "🎮 ᴘʟᴀʏ 3 ɢᴀᴍᴇs", "reward": 30, "progress": 0, "target": 3},
        {"id": "chat_minutes", "name": "💬 ᴄʜᴀᴛ ғᴏʀ 10 ᴍɪɴᴜᴛᴇs", "reward": 25, "progress": 0, "target": 10},
        {"id": "make_friends", "name": "👥 ᴍᴀᴋᴇ 2 ɴᴇᴡ ғʀɪᴇɴᴅs", "reward": 40, "progress": 0, "target": 2}
    ]
    
    challenges_text = "🎯 ᴅᴀɪʟʏ ᴄʜᴀʟʟᴇɴɢᴇs 🎯\n\n"
    challenge_buttons = []
    
    for i, challenge in enumerate(daily_challenges):
        status = "✅" if challenge["id"] in completed_today else "⏳"
        challenges_text += f"{status} {challenge['name']}\n   ʀᴇᴡᴀʀᴅ: {challenge['reward']} ᴄᴏɪɴs\n\n"
        
        if challenge["id"] not in completed_today:
            challenge_buttons.append(
                InlineKeyboardButton(f"🎯 {challenge['name'][:10]}...", 
                                   callback_data=f"challenge_{challenge['id']}")
            )
    
    # Create keyboard with 2 buttons per row
    keyboard_rows = [challenge_buttons[i:i+2] for i in range(0, len(challenge_buttons), 2)]
    keyboard_rows.append([InlineKeyboardButton("🔄 ʀᴇғʀᴇsʜ", callback_data="daily_challenges")])
    
    challenge_keyboard = InlineKeyboardMarkup(keyboard_rows)
    
    await callback.message.edit_text(
        format_reply(challenges_text),
        reply_markup=challenge_keyboard
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("mini_games"))
async def mini_games_menu(bot, callback: CallbackQuery):
    games_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎯 ᴀɪᴍ ᴛʀᴀɪɴᴇʀ", callback_data="game_aim"),
         InlineKeyboardButton("🧩 ᴘᴜᴢᴢʟᴇ ᴍᴀsᴛᴇʀ", callback_data="game_puzzle")],
        [InlineKeyboardButton("🎵 ʀʜʏᴛʜᴍ ɢᴀᴍᴇ", callback_data="game_rhythm"),
         InlineKeyboardButton("🃏 ᴄᴀʀᴅ ᴍᴀᴛᴄʜ", callback_data="game_cards")],
        [InlineKeyboardButton("🎪 sᴘɪɴ ᴛʜᴇ ʙᴏᴛᴛʟᴇ", callback_data="game_bottle"),
         InlineKeyboardButton("🎲 ᴅɪᴄᴇ ʀᴏʟʟ", callback_data="game_dice")],
        [InlineKeyboardButton("🌟 sᴛᴀʀ ᴄᴀᴛᴄʜᴇʀ", callback_data="game_stars"),
         InlineKeyboardButton("💫 ᴍᴇᴍᴏʀʏ ɢᴀᴍᴇ", callback_data="game_memory")]
    ])
    
    await callback.message.edit_text(
        format_reply("ᴄʜᴏᴏsᴇ ʏᴏᴜʀ ғᴀᴠᴏʀɪᴛᴇ ᴍɪɴɪ ɢᴀᴍᴇ! 🎮✨"),
        reply_markup=games_keyboard
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("lucky_wheel"))
async def lucky_wheel_game(bot, callback: CallbackQuery):
    user_data = users.find_one({"_id": callback.from_user.id})
    last_spin = user_data.get("last_wheel_spin")
    today = datetime.now().strftime("%Y-%m-%d")
    
    if last_spin == today:
        await callback.answer(
            format_reply("ʏᴏᴜ'ᴠᴇ ᴀʟʀᴇᴀᴅʏ sᴘᴜɴ ᴛᴏᴅᴀʏ! ᴄᴏᴍᴇ ʙᴀᴄᴋ ᴛᴏᴍᴏʀʀᴏᴡ! 🎲"),
            show_alert=True
        )
        return
    
    prizes = [
        {"name": "💰 50 ᴄᴏɪɴs", "value": 50, "type": "coins"},
        {"name": "💖 10 ʜᴇᴀʀᴛs", "value": 10, "type": "hearts"},
        {"name": "🎁 sᴜʀᴘʀɪsᴇ ɢɪғᴛ", "value": 1, "type": "gift"},
        {"name": "💎 ᴘʀᴇᴍɪᴜᴍ ᴅᴀʏ", "value": 1, "type": "premium_day"},
        {"name": "🔄 ᴛʀʏ ᴀɢᴀɪɴ", "value": 0, "type": "nothing"},
        {"name": "💰 100 ᴄᴏɪɴs", "value": 100, "type": "coins"}
    ]
    
    won_prize = random.choice(prizes)
    
    # Update user data
    update_data = {"last_wheel_spin": today}
    if won_prize["type"] == "coins":
        update_data["$inc"] = {"coins": won_prize["value"]}
    elif won_prize["type"] == "hearts":
        update_data["$inc"] = {"hearts_received": won_prize["value"]}
    
    users.update_one({"_id": callback.from_user.id}, {"$set": update_data})
    
    wheel_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎮 ᴘʟᴀʏ ɢᴀᴍᴇs", callback_data="mini_games"),
         InlineKeyboardButton("💰 ᴇᴀʀɴ ᴍᴏʀᴇ", callback_data="earn_coins")]
    ])
    
    await callback.message.edit_text(
        format_reply(f"🎲 ʟᴜᴄᴋʏ ᴡʜᴇᴇʟ ʀᴇsᴜʟᴛ! 🎲\n\n🎉 ʏᴏᴜ ᴡᴏɴ: {won_prize['name']}! 🎉"),
        reply_markup=wheel_keyboard
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("ranking_system"))
async def ranking_system_menu(bot, callback: CallbackQuery):
    user_data = users.find_one({"_id": callback.from_user.id})
    
    # Calculate user rank based on multiple factors
    matches = user_data.get("matches_count", 0)
    hearts = user_data.get("hearts_received", 0)
    coins = user_data.get("coins", 0)
    
    total_score = matches * 10 + hearts * 2 + coins * 0.1
    
    # Determine rank
    if total_score >= 1000:
        rank = "👑 ʟᴇɢᴇɴᴅᴀʀʏ"
        rank_color = "🌟"
    elif total_score >= 500:
        rank = "💎 ᴅɪᴀᴍᴏɴᴅ"
        rank_color = "💎"
    elif total_score >= 250:
        rank = "🏆 ɢᴏʟᴅ"
        rank_color = "🏆"
    elif total_score >= 100:
        rank = "🥈 sɪʟᴠᴇʀ"
        rank_color = "🥈"
    else:
        rank = "🥉 ʙʀᴏɴᴢᴇ"
        rank_color = "🥉"
    
    rank_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📈 ɪᴍᴘʀᴏᴠᴇ ʀᴀɴᴋ", callback_data="improve_rank"),
         InlineKeyboardButton("🏆 ʀᴀɴᴋ ʀᴇᴡᴀʀᴅs", callback_data="rank_rewards")],
        [InlineKeyboardButton("📊 ᴅᴇᴛᴀɪʟᴇᴅ sᴛᴀᴛs", callback_data="detailed_stats")]
    ])
    
    await callback.message.edit_text(
        format_reply(f"🏅 ʏᴏᴜʀ ʀᴀɴᴋɪɴɢ 🏅\n\n{rank_color} ʀᴀɴᴋ: {rank}\n📊 sᴄᴏʀᴇ: {total_score:.0f}\n\n💕 ᴍᴀᴛᴄʜᴇs: {matches}\n💖 ʜᴇᴀʀᴛs: {hearts}\n💰 ᴄᴏɪɴs: {coins}"),
        reply_markup=rank_keyboard
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("pvp_battles"))
async def pvp_battles_menu(bot, callback: CallbackQuery):
    battle_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⚔️ ғɪɴᴅ ᴏᴘᴘᴏɴᴇɴᴛ", callback_data="find_opponent"),
         InlineKeyboardButton("🏆 ʙᴀᴛᴛʟᴇ ʜɪsᴛᴏʀʏ", callback_data="battle_history")],
        [InlineKeyboardButton("💪 ᴛʀᴀɪɴɪɴɢ ᴍᴏᴅᴇ", callback_data="training_mode"),
         InlineKeyboardButton("🎯 sᴋɪʟʟ ᴍᴀᴛᴄʜ", callback_data="skill_match")],
        [InlineKeyboardButton("🏅 ᴛᴏᴜʀɴᴀᴍᴇɴᴛ", callback_data="tournament"),
         InlineKeyboardButton("👑 ᴄʜᴀᴍᴘɪᴏɴsʜɪᴘ", callback_data="championship")]
    ])
    
    await callback.message.edit_text(
        format_reply("ʀᴇᴀᴅʏ ғᴏʀ ʙᴀᴛᴛʟᴇ? ⚔️🔥"),
        reply_markup=battle_keyboard
    )
    await callback.answer()
