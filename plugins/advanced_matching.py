
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import *
from pymongo import MongoClient
from datetime import datetime
import random
import math

client = MongoClient(MONGO_URL)
db = client['find_partner']
users = db['users']
compatibility_data = db['compatibility_data']

def format_reply(text):
    tiny_caps_map = {
        'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ', 'f': 'ғ', 'g': 'ɢ', 'h': 'ʜ',
        'i': 'ɪ', 'j': 'ᴊ', 'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ', 'o': 'ᴏ', 'p': 'ᴘ',
        'q': 'ǫ', 'r': 'ʀ', 's': 's', 't': 'ᴛ', 'u': 'ᴜ', 'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x',
        'y': 'ʏ', 'z': 'ᴢ'
    }
    converted = ''.join(tiny_caps_map.get(char.lower(), char) for char in text)
    return f"❖ **{converted}**"

def calculate_compatibility_score(user1_data, user2_data):
    score = 0
    
    # Age compatibility (20 points max)
    age1 = user1_data.get("age", 25)
    age2 = user2_data.get("age", 25)
    age_diff = abs(age1 - age2)
    if age_diff <= 2:
        score += 20
    elif age_diff <= 5:
        score += 15
    elif age_diff <= 10:
        score += 10
    else:
        score += 5
    
    # Interest compatibility (30 points max)
    interests1 = set(user1_data.get("interests", []))
    interests2 = set(user2_data.get("interests", []))
    common_interests = len(interests1.intersection(interests2))
    score += min(common_interests * 10, 30)
    
    # Personality compatibility (25 points max)
    personality1 = user1_data.get("personality_type", "balanced")
    personality2 = user2_data.get("personality_type", "balanced")
    
    compatibility_matrix = {
        ("romantic", "romantic"): 25,
        ("romantic", "deep"): 20,
        ("playful", "playful"): 25,
        ("playful", "romantic"): 15,
        ("deep", "deep"): 25,
        ("deep", "romantic"): 20
    }
    
    score += compatibility_matrix.get((personality1, personality2), 10)
    
    # Activity level compatibility (15 points max)
    activity1 = user1_data.get("activity_level", 50)
    activity2 = user2_data.get("activity_level", 50)
    activity_diff = abs(activity1 - activity2)
    score += max(15 - activity_diff // 10, 0)
    
    # Location bonus (10 points max)
    if user1_data.get("location") == user2_data.get("location"):
        score += 10
    
    return min(score, 100)

@Client.on_callback_query(filters.regex("smart_matching"))
async def smart_matching_system(bot, callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data = users.find_one({"_id": user_id})
    
    if not user_data.get("premium", False):
        await callback.message.edit_text(
            format_reply("sᴍᴀʀᴛ ᴍᴀᴛᴄʜɪɴɢ ɪs ᴀ ᴘʀᴇᴍɪᴜᴍ ғᴇᴀᴛᴜʀᴇ! 💎"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💎 ᴜᴘɢʀᴀᴅᴇ ɴᴏᴡ", callback_data="upgrade_premium")]
            ])
        )
        await callback.answer()
        return
    
    # Find best matches using AI algorithm
    all_users = users.find({"_id": {"$ne": user_id}})
    matches_with_scores = []
    
    for potential_match in all_users:
        score = calculate_compatibility_score(user_data, potential_match)
        if score >= 70:  # Only high compatibility matches
            matches_with_scores.append({
                "user": potential_match,
                "score": score
            })
    
    # Sort by compatibility score
    matches_with_scores.sort(key=lambda x: x["score"], reverse=True)
    top_matches = matches_with_scores[:5]
    
    if not top_matches:
        await callback.message.edit_text(
            format_reply("ɴᴏ ʜɪɢʜ-ᴄᴏᴍᴘᴀᴛɪʙɪʟɪᴛʏ ᴍᴀᴛᴄʜᴇs ғᴏᴜɴᴅ ʀɪɢʜᴛ ɴᴏᴡ! 💔\nᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ ᴏʀ ᴜᴘᴅᴀᴛᴇ ʏᴏᴜʀ ᴘʀᴏғɪʟᴇ! ✨")
        )
        await callback.answer()
        return
    
    match_keyboard = []
    for i, match_data in enumerate(top_matches):
        match = match_data["user"]
        score = match_data["score"]
        name = match.get("name", "ᴀɴᴏɴʏᴍᴏᴜs")[:15]
        match_keyboard.append([
            InlineKeyboardButton(
                f"💖 {name} ({score}% ᴄᴏᴍᴘᴀᴛɪʙʟᴇ)",
                callback_data=f"view_match:{match['_id']}"
            )
        ])
    
    match_keyboard.append([
        InlineKeyboardButton("🔄 ʀᴇғʀᴇsʜ ᴍᴀᴛᴄʜᴇs", callback_data="smart_matching")
    ])
    
    await callback.message.edit_text(
        format_reply("ʏᴏᴜʀ ᴛᴏᴘ sᴍᴀʀᴛ ᴍᴀᴛᴄʜᴇs! 🧠💕"),
        reply_markup=InlineKeyboardMarkup(match_keyboard)
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("soulmate_finder"))
async def soulmate_finder_system(bot, callback: CallbackQuery):
    soulmate_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💫 ᴀsᴛʀᴏʟᴏɢʏ ᴍᴀᴛᴄʜ", callback_data="astrology_match"),
         InlineKeyboardButton("🔮 ᴘsʏᴄʜɪᴄ ʀᴇᴀᴅɪɴɢ", callback_data="psychic_reading")],
        [InlineKeyboardButton("💭 ᴅʀᴇᴀᴍ ᴀɴᴀʟʏsɪs", callback_data="dream_analysis"),
         InlineKeyboardButton("🌟 ᴅᴇsᴛɪɴʏ ᴍᴀᴛᴄʜ", callback_data="destiny_match")],
        [InlineKeyboardButton("💝 sᴏᴜʟ ᴄᴏɴɴᴇᴄᴛɪᴏɴ", callback_data="soul_connection"),
         InlineKeyboardButton("🎭 ᴘᴀsᴛ ʟɪғᴇ ʀᴇᴀᴅɪɴɢ", callback_data="past_life")]
    ])
    
    await callback.message.edit_text(
        format_reply("ᴅɪsᴄᴏᴠᴇʀ ʏᴏᴜʀ sᴏᴜʟᴍᴀᴛᴇ ᴛʜʀᴏᴜɢʜ ᴍʏsᴛɪᴄᴀʟ ᴍᴇᴛʜᴏᴅs! 🔮✨"),
        reply_markup=soulmate_keyboard
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("astrology_match"))
async def astrology_matching(bot, callback: CallbackQuery):
    zodiac_signs = [
        "♈ ᴀʀɪᴇs", "♉ ᴛᴀᴜʀᴜs", "♊ ɢᴇᴍɪɴɪ", "♋ ᴄᴀɴᴄᴇʀ",
        "♌ ʟᴇᴏ", "♍ ᴠɪʀɢᴏ", "♎ ʟɪʙʀᴀ", "♏ sᴄᴏʀᴘɪᴏ",
        "♐ sᴀɢɪᴛᴛᴀʀɪᴜs", "♑ ᴄᴀᴘʀɪᴄᴏʀɴ", "♒ ᴀǫᴜᴀʀɪᴜs", "♓ ᴘɪsᴄᴇs"
    ]
    
    # Create zodiac keyboard
    zodiac_buttons = []
    for i in range(0, len(zodiac_signs), 3):
        row = []
        for j in range(3):
            if i + j < len(zodiac_signs):
                sign = zodiac_signs[i + j]
                row.append(InlineKeyboardButton(sign, callback_data=f"zodiac_{i+j}"))
        zodiac_buttons.append(row)
    
    await callback.message.edit_text(
        format_reply("sᴇʟᴇᴄᴛ ʏᴏᴜʀ ᴢᴏᴅɪᴀᴄ sɪɢɴ ғᴏʀ ᴀsᴛʀᴏʟᴏɢɪᴄᴀʟ ᴍᴀᴛᴄʜɪɴɢ! ✨🔮"),
        reply_markup=InlineKeyboardMarkup(zodiac_buttons)
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("love_predictions"))
async def love_predictions_system(bot, callback: CallbackQuery):
    predictions = [
        "ᴀ ᴍʏsᴛᴇʀɪᴏᴜs sᴛʀᴀɴɢᴇʀ ᴡɪʟʟ ᴇɴᴛᴇʀ ʏᴏᴜʀ ʟɪғᴇ sᴏᴏɴ... 🌟",
        "ʏᴏᴜʀ ɴᴇxᴛ ʟᴏᴠᴇ ᴡɪʟʟ ʙᴇ ᴇᴠᴇɴ sᴛʀᴏɴɢᴇʀ ᴛʜᴀɴ ʏᴏᴜ ɪᴍᴀɢɪɴᴇ! 💪💕",
        "sᴏᴍᴇᴏɴᴇ ɪs ᴛʜɪɴᴋɪɴɢ ᴀʙᴏᴜᴛ ʏᴏᴜ ʀɪɢʜᴛ ɴᴏᴡ... 👀💭",
        "ᴀ ʀᴏᴍᴀɴᴛɪᴄ sᴜʀᴘʀɪsᴇ ᴀᴡᴀɪᴛs ʏᴏᴜ ᴛʜɪs ᴡᴇᴇᴋ! 🎁✨",
        "ʏᴏᴜʀ ʜᴇᴀʀᴛ ɪs ᴀʙᴏᴜᴛ ᴛᴏ ғɪɴᴅ ɪᴛs ᴍɪssɪɴɢ ᴘɪᴇᴄᴇ... 🧩💖"
    ]
    
    prediction = random.choice(predictions)
    
    prediction_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔮 ᴀɴᴏᴛʜᴇʀ ᴘʀᴇᴅɪᴄᴛɪᴏɴ", callback_data="love_predictions"),
         InlineKeyboardButton("💕 ғɪɴᴅ ʟᴏᴠᴇ ɴᴏᴡ", callback_data="find_partner")],
        [InlineKeyboardButton("📱 sʜᴀʀᴇ ᴘʀᴇᴅɪᴄᴛɪᴏɴ", callback_data="share_prediction")]
    ])
    
    await callback.message.edit_text(
        format_reply(f"🔮 ʟᴏᴠᴇ ᴘʀᴇᴅɪᴄᴛɪᴏɴ 🔮\n\n{prediction}"),
        reply_markup=prediction_keyboard
    )
    await callback.answer()
