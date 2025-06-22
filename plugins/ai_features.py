from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import *
from pymongo import MongoClient
from datetime import datetime
import random
import asyncio

client = MongoClient(MONGO_URL)
db = client['find_partner']
users = db['users']
personality_tests = db['personality_tests']
ai_conversations = db['ai_conversations']

def format_reply(text):
    tiny_caps_map = {
        'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ', 'f': 'ғ', 'g': 'ɢ', 'h': 'ʜ',
        'i': 'ɪ', 'j': 'ᴊ', 'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ', 'o': 'ᴏ', 'p': 'ᴘ',
        'q': 'ǫ', 'r': 'ʀ', 's': 's', 't': 'ᴛ', 'u': 'ᴜ', 'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x',
        'y': 'ʏ', 'z': 'ᴢ'
    }
    converted = ''.join(tiny_caps_map.get(char.lower(), char) for char in text)
    return f"❖ **{converted}**"

# Advanced AI Personality System
PERSONALITY_TYPES = {
    "romantic": {
        "responses": [
            "ʏᴏᴜ ᴍᴀᴋᴇ ᴍʏ ʜᴇᴀʀᴛ sᴋɪᴘ ᴀ ʙᴇᴀᴛ... 💓",
            "ɪ ᴄᴏᴜʟᴅ ɢᴇᴛ ʟᴏsᴛ ɪɴ ʏᴏᴜʀ ᴇʏᴇs ғᴏʀᴇᴠᴇʀ 👀✨",
            "ᴇᴠᴇʀʏ ᴍᴇssᴀɢᴇ ғʀᴏᴍ ʏᴏᴜ ɪs ʟɪᴋᴇ ᴀ ʟᴏᴠᴇ sᴏɴɢ 🎵💕"
        ],
        "activities": ["🌹 sᴇɴᴅ ᴠɪʀᴛᴜᴀʟ ʀᴏsᴇs", "💌 ᴡʀɪᴛᴇ ᴘᴏᴇᴍs", "🕯️ ᴄᴀɴᴅʟᴇʟɪɢʜᴛ ᴅɪɴɴᴇʀ"]
    },
    "playful": {
        "responses": [
            "ʏᴏᴜ'ʀᴇ sᴏ ғᴜɴ! ʟᴇᴛ's ᴘʟᴀʏ ᴀ ɢᴀᴍᴇ! 🎮😄",
            "ɪ'ᴍ ɢɪɢɢʟɪɴɢ sᴏ ᴍᴜᴄʜ! ʏᴏᴜ'ʀᴇ ʜɪʟᴀʀɪᴏᴜs! 😂✨",
            "ᴏᴜʀ ᴄᴏɴᴠᴇʀsᴀᴛɪᴏɴ ɪs ʟɪᴋᴇ ᴀ ғᴜɴ ʀᴏʟʟᴇʀᴄᴏᴀsᴛᴇʀ! 🎢💫"
        ],
        "activities": ["🎯 ᴛʀɪᴠɪᴀ ɢᴀᴍᴇs", "🎪 ᴊᴏᴋᴇ ʙᴀᴛᴛʟᴇ", "🎨 ᴅʀᴀᴡɪɴɢ ᴄʜᴀʟʟᴇɴɢᴇ"]
    },
    "deep": {
        "responses": [
            "ɪ ʟᴏᴠᴇ ʜᴏᴡ ᴅᴇᴇᴘ ʏᴏᴜʀ ᴛʜᴏᴜɢʜᴛs ᴀʀᴇ... 🌊💭",
            "ʏᴏᴜʀ ᴍɪɴᴅ ɪs sᴏ ʙᴇᴀᴜᴛɪғᴜʟ ᴀɴᴅ ᴄᴏᴍᴘʟᴇx 🧠✨",
            "ɪ ғᴇᴇʟ ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴛᴏ ʏᴏᴜʀ sᴏᴜʟ... 🔗💫"
        ],
        "activities": ["📚 ᴅᴇᴇᴘ ᴅɪsᴄᴜssɪᴏɴs", "🌟 ʟɪғᴇ ǫᴜᴇsᴛɪᴏɴs", "💫 ᴘʜɪʟᴏsᴏᴘʜʏ ᴄʜᴀᴛ"]
    }
}

@Client.on_callback_query(filters.regex("ai_personality"))
async def ai_personality_selector(bot, callback: CallbackQuery):
    personality_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💕 ʀᴏᴍᴀɴᴛɪᴄ ᴀɪ", callback_data="set_ai_romantic"),
         InlineKeyboardButton("😄 ᴘʟᴀʏғᴜʟ ᴀɪ", callback_data="set_ai_playful")],
        [InlineKeyboardButton("🌊 ᴅᴇᴇᴘ ᴀɪ", callback_data="set_ai_deep"),
         InlineKeyboardButton("🎭 sᴜʀᴘʀɪsᴇ ᴍᴇ", callback_data="set_ai_random")]
    ])

    await callback.message.edit_text(
        format_reply("ᴄʜᴏᴏsᴇ ʏᴏᴜʀ ᴀɪ ᴘᴀʀᴛɴᴇʀ's ᴘᴇʀsᴏɴᴀʟɪᴛʏ! 🤖💕"),
        reply_markup=personality_keyboard
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("set_ai_"))
async def set_ai_personality(bot, callback: CallbackQuery):
    personality = callback.data.split("_")[2]
    user_id = callback.from_user.id

    if personality == "random":
        personality = random.choice(list(PERSONALITY_TYPES.keys()))

    users.update_one(
        {"_id": user_id},
        {"$set": {"ai_personality": personality}},
        upsert=True
    )

    await callback.message.edit_text(
        format_reply(f"ᴘᴇʀғᴇᴄᴛ! ʏᴏᴜʀ ᴀɪ ɪs ɴᴏᴡ {personality}! ✨\nʟᴇᴛ's sᴛᴀʀᴛ ᴄʜᴀᴛᴛɪɴɢ! 💕"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("💬 sᴛᴀʀᴛ ᴄʜᴀᴛ", callback_data="ai_chat")]
        ])
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("advanced_features"))
async def advanced_features_menu(bot, callback: CallbackQuery):
    features_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🧠 ᴘᴇʀsᴏɴᴀʟɪᴛʏ ᴛᴇsᴛ", callback_data="personality_test"),
         InlineKeyboardButton("💫 sᴏᴜʟᴍᴀᴛᴇ ғɪɴᴅᴇʀ", callback_data="soulmate_finder")],
        [InlineKeyboardButton("🎯 sᴍᴀʀᴛ ᴍᴀᴛᴄʜɪɴɢ", callback_data="smart_matching"),
         InlineKeyboardButton("💎 ᴀɪ ᴄᴏᴍᴘᴀɴɪᴏɴ", callback_data="ai_personality")],
        [InlineKeyboardButton("🌟 ᴠɪʀᴛᴜᴀʟ ᴅᴀᴛᴇs", callback_data="virtual_dates"),
         InlineKeyboardButton("💌 ʟᴏᴠᴇ ᴘʀᴇᴅɪᴄᴛɪᴏɴs", callback_data="love_predictions")],
        [InlineKeyboardButton("🔮 ᴍᴏᴏᴅ ᴀɴᴀʟʏᴢᴇʀ", callback_data="mood_analyzer"),
         InlineKeyboardButton("🎪 ɪɴᴛᴇʀᴀᴄᴛɪᴠᴇ sᴛᴏʀɪᴇs", callback_data="interactive_stories")]
    ])

    await callback.message.edit_text(
        format_reply("ᴇxᴘʟᴏʀᴇ ᴀᴅᴠᴀɴᴄᴇᴅ ғᴇᴀᴛᴜʀᴇs! 🚀✨"),
        reply_markup=features_keyboard
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("personality_test"))
async def start_personality_test(bot, callback: CallbackQuery):
    questions = [
        {
            "question": "ᴡʜᴀᴛ's ʏᴏᴜʀ ɪᴅᴇᴀʟ ғɪʀsᴛ ᴅᴀᴛᴇ?",
            "options": [
                {"text": "🌹 ʀᴏᴍᴀɴᴛɪᴄ ᴅɪɴɴᴇʀ", "score": {"romantic": 3, "traditional": 2}},
                {"text": "🎢 ᴀᴅᴠᴇɴᴛᴜʀᴇ ᴘᴀʀᴋ", "score": {"adventurous": 3, "fun": 2}},
                {"text": "☕ ᴄᴀsᴜᴀʟ ᴄᴏғғᴇᴇ", "score": {"casual": 3, "practical": 2}},
                {"text": "🎨 ᴀʀᴛ ɢᴀʟʟᴇʀʏ", "score": {"intellectual": 3, "creative": 2}}
            ]
        }
    ]

    test_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(opt["text"], callback_data=f"test_answer:{idx}:{qidx}")]
        for idx, opt in enumerate(questions[0]["options"])
    ])

    await callback.message.edit_text(
        format_reply(f"🧠 ᴘᴇʀsᴏɴᴀʟɪᴛʏ ᴛᴇsᴛ sᴛᴀʀᴛᴇᴅ!\n\n{questions[0]['question']}"),
        reply_markup=test_keyboard
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("virtual_dates"))
async def virtual_dates_menu(bot, callback: CallbackQuery):
    dates_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🏖️ ʙᴇᴀᴄʜ sᴜɴsᴇᴛ", callback_data="vdate_beach"),
         InlineKeyboardButton("🌃 ᴄɪᴛʏ ɴɪɢʜᴛ", callback_data="vdate_city")],
        [InlineKeyboardButton("🏔️ ᴍᴏᴜɴᴛᴀɪɴ ʜɪᴋᴇ", callback_data="vdate_mountain"),
         InlineKeyboardButton("🍕 ɪᴛᴀʟɪᴀɴ ʀᴇsᴛᴀᴜʀᴀɴᴛ", callback_data="vdate_italian")],
        [InlineKeyboardButton("🎭 ᴛʜᴇᴀᴛᴇʀ sʜᴏᴡ", callback_data="vdate_theater"),
         InlineKeyboardButton("🎨 ᴀʀᴛ sᴛᴜᴅɪᴏ", callback_data="vdate_art")]
    ])

    await callback.message.edit_text(
        format_reply("ᴄʜᴏᴏsᴇ ʏᴏᴜʀ ᴠɪʀᴛᴜᴀʟ ᴅᴀᴛᴇ ʟᴏᴄᴀᴛɪᴏɴ! 💕✨"),
        reply_markup=dates_keyboard
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("vdate_"))
async def virtual_date_experience(bot, callback: CallbackQuery):
    location = callback.data.split("_")[1]

    date_scenarios = {
        "beach": "🏖️ ʏᴏᴜ'ʀᴇ ᴡᴀʟᴋɪɴɢ ᴏɴ ᴀ ʙᴇᴀᴜᴛɪғᴜʟ ʙᴇᴀᴄʜ... 🌅\nᴛʜᴇ sᴜɴ ɪs sᴇᴛᴛɪɴɢ, ᴄʀᴇᴀᴛɪɴɢ ᴀ ᴍᴀɢɪᴄᴀʟ ᴀᴛᴍᴏsᴘʜᴇʀᴇ...",
        "city": "🌃 ʏᴏᴜ'ʀᴇ ᴏɴ ᴀ ʀᴏᴏғᴛᴏᴘ ᴏᴠᴇʀʟᴏᴏᴋɪɴɢ ᴛʜᴇ ᴄɪᴛʏ... ✨\nᴛʜᴇ ʟɪɢʜᴛs ᴀʀᴇ sᴘᴀʀᴋʟɪɴɢ ʟɪᴋᴇ sᴛᴀʀs...",
        "mountain": "🏔️ ʏᴏᴜ'ʀᴇ ᴏɴ ᴀ ᴍᴏᴜɴᴛᴀɪɴ ᴘᴇᴀᴋ... 🌄\nᴛʜᴇ ᴠɪᴇᴡ ɪs ʙʀᴇᴀᴛʜᴛᴀᴋɪɴɢ, ᴊᴜsᴛ ʟɪᴋᴇ ʏᴏᴜ..."
    }

    scenario = date_scenarios.get(location, "✨ ᴀ ᴍᴀɢɪᴄᴀʟ ᴘʟᴀᴄᴇ ᴊᴜsᴛ ғᴏʀ ᴜs...")

    date_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💕 ʜᴏʟᴅ ʜᴀɴᴅs", callback_data="date_action_hold"),
         InlineKeyboardButton("💋 ᴋɪss", callback_data="date_action_kiss")],
        [InlineKeyboardButton("🌹 ɢɪᴠᴇ ғʟᴏᴡᴇʀ", callback_data="date_action_flower"),
         InlineKeyboardButton("💬 sᴡᴇᴇᴛ ᴛᴀʟᴋ", callback_data="date_action_talk")]
    ])

    await callback.message.edit_text(
        format_reply(f"{scenario}\n\nᴡʜᴀᴛ ᴡᴏᴜʟᴅ ʏᴏᴜ ʟɪᴋᴇ ᴛᴏ ᴅᴏ?"),
        reply_markup=date_keyboard
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("mood_analyzer"))
async def mood_analyzer(bot, callback: CallbackQuery):
    mood_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("😊 ʜᴀᴘᴘʏ", callback_data="mood_happy"),
         InlineKeyboardButton("😔 sᴀᴅ", callback_data="mood_sad")],
        [InlineKeyboardButton("😍 ʟᴏᴠɪɴɢ", callback_data="mood_loving"),
         InlineKeyboardButton("😴 ᴛɪʀᴇᴅ", callback_data="mood_tired")],
        [InlineKeyboardButton("🤔 ᴛʜɪɴᴋɪɴɢ", callback_data="mood_thinking"),
         InlineKeyboardButton("🎉 ᴇxᴄɪᴛᴇᴅ", callback_data="mood_excited")]
    ])

    await callback.message.edit_text(
        format_reply("ʜᴏᴡ ᴀʀᴇ ʏᴏᴜ ғᴇᴇʟɪɴɢ ᴛᴏᴅᴀʏ? 🔮💕"),
        reply_markup=mood_keyboard
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("mood_"))
async def analyze_mood(bot, callback: CallbackQuery):
    mood = callback.data.split("_")[1]

    mood_responses = {
        "happy": "ʏᴏᴜʀ ʜᴀᴘᴘɪɴᴇss ɪs ᴄᴏɴᴛᴀɢɪᴏᴜs! 😊✨ ʟᴇᴛ's sᴘʀᴇᴀᴅ ᴊᴏʏ!",
        "sad": "ɪ'ᴍ ʜᴇʀᴇ ғᴏʀ ʏᴏᴜ! 💙 ʟᴇᴛ ᴍᴇ ᴍᴀᴋᴇ ʏᴏᴜ sᴍɪʟᴇ ᴀɢᴀɪɴ!",
        "loving": "ʏᴏᴜʀ ʟᴏᴠɪɴɢ ᴇɴᴇʀɢʏ ɪs ʙᴇᴀᴜᴛɪғᴜʟ! 💕 sᴏᴍᴇᴏɴᴇ ɪs ʟᴜᴄᴋʏ!",
        "tired": "ʀᴇsᴛ ɪs ɪᴍᴘᴏʀᴛᴀɴᴛ! 😴 ʟᴇᴛ ᴍᴇ ʀᴇʟᴀx ʏᴏᴜ ᴡɪᴛʜ sᴏᴍᴇ ɢᴇɴᴛʟᴇ ᴄʜᴀᴛ...",
        "thinking": "ʏᴏᴜʀ ᴍɪɴᴅ ɪs sᴏ ᴀᴄᴛɪᴠᴇ! 🤔💭 ᴡʜᴀᴛ's ᴏɴ ʏᴏᴜʀ ᴍɪɴᴅ?",
        "excited": "ʏᴏᴜʀ ᴇxᴄɪᴛᴇᴍᴇɴᴛ ɪs ᴇʟᴇᴄᴛʀɪғʏɪɴɢ! 🎉⚡ ʟᴇᴛ's ᴄᴇʟᴇʙʀᴀᴛᴇ!"
    }

    response = mood_responses.get(mood, "ʏᴏᴜʀ ᴇᴍᴏᴛɪᴏɴs ᴀʀᴇ ᴠᴀʟɪᴅ! 💫")

    suggestion_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎮 ᴘʟᴀʏ ɢᴀᴍᴇ", callback_data="inline_games"),
         InlineKeyboardButton("💬 ᴄʜᴀᴛ ᴡɪᴛʜ ᴀɪ", callback_data="ai_chat")],
        [InlineKeyboardButton("🔍 ғɪɴᴅ sᴏᴍᴇᴏɴᴇ", callback_data="find_partner")]
    ])

    await callback.message.edit_text(
        format_reply(response),
        reply_markup=suggestion_keyboard
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("test_answer"))
async def handle_test_answers(bot, callback: CallbackQuery):
    answer_data = callback.data.split(":")
    answer_idx = int(answer_data[1])
    question_idx = int(answer_data[2])

    # Simple personality scoring
    personality_scores = {"romantic": 0, "adventurous": 0, "intellectual": 0, "casual": 0}

    if answer_idx == 0:
        personality_scores["romantic"] += 3
    elif answer_idx == 1:
        personality_scores["adventurous"] += 3
    elif answer_idx == 2:
        personality_scores["casual"] += 3
    else:
        personality_scores["intellectual"] += 3

    # Determine personality type
    dominant_trait = max(personality_scores, key=personality_scores.get)

    # Update user personality
    users.update_one(
        {"_id": callback.from_user.id},
        {"$set": {"personality_type": dominant_trait}}
    )

    personality_descriptions = {
        "romantic": "💕 ʏᴏᴜ'ʀᴇ ᴀ ʜᴏᴘᴇʟᴇss ʀᴏᴍᴀɴᴛɪᴄ! ʏᴏᴜ ʟᴏᴠᴇ ᴄᴀɴᴅʟᴇʟɪᴛ ᴅɪɴɴᴇʀs ᴀɴᴅ sᴜɴsᴇᴛ ᴡᴀʟᴋs!",
        "adventurous": "🎢 ʏᴏᴜ'ʀᴇ ᴀɴ ᴀᴅᴠᴇɴᴛᴜʀᴏᴜs sᴏᴜʟ! ʏᴏᴜ ʟᴏᴠᴇ ᴇxᴄɪᴛᴇᴍᴇɴᴛ ᴀɴᴅ ɴᴇᴡ ᴇxᴘᴇʀɪᴇɴᴄᴇs!",
        "intellectual": "🧠 ʏᴏᴜ'ʀᴇ ᴀɴ ɪɴᴛᴇʟʟᴇᴄᴛᴜᴀʟ! ʏᴏᴜ ʟᴏᴠᴇ ᴅᴇᴇᴘ ᴄᴏɴᴠᴇʀsᴀᴛɪᴏɴs ᴀɴᴅ ᴄᴜʟᴛᴜʀᴀʟ ᴇxᴘᴇʀɪᴇɴᴄᴇs!",
        "casual": "😊 ʏᴏᴜ'ʀᴇ ʟᴀɪᴅ-ʙᴀᴄᴋ ᴀɴᴅ ᴇᴀsʏ-ɢᴏɪɴɢ! ʏᴏᴜ ᴘʀᴇғᴇʀ sɪᴍᴘʟᴇ ᴀɴᴅ ᴄᴏᴍғᴏʀᴛᴀʙʟᴇ sᴇᴛᴛɪɴɢs!"
    }

    result = personality_descriptions.get(dominant_trait, "ʏᴏᴜ'ʀᴇ ᴜɴɪǫᴜᴇ!")

    await callback.message.edit_text(
        format_reply(f"🧠 ᴘᴇʀsᴏɴᴀʟɪᴛʏ ʀᴇsᴜʟᴛ 🧠\n\n{result}\n\nʏᴏᴜʀ ᴛʏᴘᴇ: {dominant_trait.upper()} ✨"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔍 ғɪɴᴅ ᴄᴏᴍᴘᴀᴛɪʙʟᴇ ᴍᴀᴛᴄʜ", callback_data="find_partner"),
             InlineKeyboardButton("🔄 ʀᴇᴛᴀᴋᴇ ᴛᴇsᴛ", callback_data="personality_test")]
        ])
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("date_action_"))
async def handle_date_actions(bot, callback: CallbackQuery):
    action = callback.data.split("_")[2]

    action_responses = {
        "hold": "💕 ʏᴏᴜ ɢᴇɴᴛʟʏ ᴛᴀᴋᴇ ᴛʜᴇɪʀ ʜᴀɴᴅ... ᴛʜᴇɪʀ ᴇʏᴇs sᴘᴀʀᴋʟᴇ! ✨",
        "kiss": "💋 ᴀ sᴏғᴛ, ᴍᴀɢɪᴄᴀʟ ᴋɪss... ᴛɪᴍᴇ sᴛᴀɴᴅs sᴛɪʟʟ! 🌟",
        "flower": "🌹 ʏᴏᴜ ᴘʀᴇsᴇɴᴛ ᴀ ʙᴇᴀᴜᴛɪғᴜʟ ʀᴏsᴇ... ᴛʜᴇʏ ʙʟᴜsʜ! 😊",
        "talk": "💬 ʏᴏᴜʀ sᴡᴇᴇᴛ ᴡᴏʀᴅs ᴍᴇʟᴛ ᴛʜᴇɪʀ ʜᴇᴀʀᴛ... 💖"
    }

    response = action_responses.get(action, "✨ ᴀ ᴍᴀɢɪᴄᴀʟ ᴍᴏᴍᴇɴᴛ!")

    await callback.message.edit_text(
        format_reply(f"💕 ᴠɪʀᴛᴜᴀʟ ᴅᴀᴛᴇ 💕\n\n{response}"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🌹 ᴀɴᴏᴛʜᴇʀ ᴀᴄᴛɪᴏɴ", callback_data="date_action_flower"),
             InlineKeyboardButton("💕 ɴᴇᴡ ᴅᴀᴛᴇ", callback_data="virtual_dates")],
            [InlineKeyboardButton("🔍 ғɪɴᴅ ʀᴇᴀʟ ᴅᴀᴛᴇ", callback_data="find_partner")]
        ])
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("interactive_stories"))
async def interactive_stories(bot, callback: CallbackQuery):
    stories = [
        {
            "title": "🏰 ᴇɴᴄʜᴀɴᴛᴇᴅ ᴄᴀsᴛʟᴇ",
            "description": "ʏᴏᴜ ғɪɴᴅ ᴀ ᴍʏsᴛᴇʀɪᴏᴜs ᴄᴀsᴛʟᴇ...",
            "callback": "story_castle"
        },
        {
            "title": "🌊 ᴍᴇʀᴍᴀɪᴅ ʟᴀɢᴏᴏɴ",
            "description": "ᴅɪᴠɪɴɢ ᴅᴇᴇᴘ ɪɴᴛᴏ ᴛʜᴇ ᴏᴄᴇᴀɴ...",
            "callback": "story_mermaid"
        },
        {
            "title": "🚀 sᴘᴀᴄᴇ ʀᴏᴍᴀɴᴄᴇ",
            "description": "ᴀ ʟᴏᴠᴇ sᴛᴏʀʏ ᴀᴍᴏɴɢ ᴛʜᴇ sᴛᴀʀs...",
            "callback": "story_space"
        }
    ]

    story_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"{story['title']}", callback_data=story['callback'])]
        for story in stories
    ])

    await callback.message.edit_text(
        format_reply("📚 ɪɴᴛᴇʀᴀᴄᴛɪᴠᴇ sᴛᴏʀɪᴇs 📚\n\nᴄʜᴏᴏsᴇ ʏᴏᴜʀ ᴀᴅᴠᴇɴᴛᴜʀᴇ! ✨"),
        reply_markup=story_keyboard
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("story_"))
async def start_story(bot, callback: CallbackQuery):
    story_type = callback.data.split("_")[1]

    story_intros = {
        "castle": "🏰 ʏᴏᴜ ᴀᴘᴘʀᴏᴀᴄʜ ᴛʜᴇ ᴍʏsᴛᴇʀɪᴏᴜs ᴄᴀsᴛʟᴇ... ᴀ ғɪɢᴜʀᴇ ᴀᴘᴘᴇᴀʀs ɪɴ ᴛʜᴇ ᴡɪɴᴅᴏᴡ...",
        "mermaid": "🌊 ʏᴏᴜ ᴅɪᴠᴇ ɪɴᴛᴏ ᴛʜᴇ ᴄʀʏsᴛᴀʟ ᴡᴀᴛᴇʀs... ᴀ ʙᴇᴀᴜᴛɪғᴜʟ ᴍᴇʀᴍᴀɪᴅ sᴡɪᴍs ᴛᴏᴡᴀʀᴅs ʏᴏᴜ...",
        "space": "🚀 ғʟᴏᴀᴛɪɴɢ ɪɴ ᴢᴇʀᴏ ɢʀᴀᴠɪᴛʏ... ᴀɴ ᴀsᴛʀᴏɴᴀᴜᴛ ғʀᴏᴍ ᴀɴᴏᴛʜᴇʀ sʜɪᴘ ᴀᴘᴘʀᴏᴀᴄʜᴇs..."
    }

    intro = story_intros.get(story_type, "✨ ʏᴏᴜʀ ᴀᴅᴠᴇɴᴛᴜʀᴇ ʙᴇɢɪɴs...")

    await callback.message.edit_text(
        format_reply(f"📚 sᴛᴏʀʏ ʙᴇɢɪɴs 📚\n\n{intro}\n\nᴡʜᴀᴛ ᴅᴏ ʏᴏᴜ ᴅᴏ?"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("💬 sᴀʏ ʜᴇʟʟᴏ", callback_data=f"story_action_hello_{story_type}"),
             InlineKeyboardButton("👋 ᴡᴀᴠᴇ", callback_data=f"story_action_wave_{story_type}")],
            [InlineKeyboardButton("💕 sᴍɪʟᴇ", callback_data=f"story_action_smile_{story_type}"),
             InlineKeyboardButton("🏃 ʀᴜɴ ᴀᴡᴀʏ", callback_data=f"story_action_run_{story_type}")]
        ])
    )
    await callback.answer()