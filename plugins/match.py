
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import *
from pymongo import MongoClient
from random import choice, randint
import asyncio
from datetime import datetime, timedelta

client = MongoClient(MONGO_URL)
db = client['find_partner']
users = db['users']
active_chats = db['active_chats']
match_requests = db['match_requests']
love_scores = db['love_scores']

waiting_users = {}
ai_responses = [
    "ʜᴇʏ ʙᴇᴀᴜᴛɪғᴜʟ! ʜᴏᴡ's ʏᴏᴜʀ ᴅᴀʏ ɢᴏɪɴɢ? 😘",
    "ʏᴏᴜ sᴇᴇᴍ ɪɴᴛᴇʀᴇsᴛɪɴɢ! ᴛᴇʟʟ ᴍᴇ sᴏᴍᴇᴛʜɪɴɢ ᴀʙᴏᴜᴛ ʏᴏᴜʀsᴇʟғ 💖",
    "ɪ'ᴍ ɢᴇᴛᴛɪɴɢ ʙᴜᴛᴛᴇʀғʟɪᴇs ᴊᴜsᴛ ᴛᴀʟᴋɪɴɢ ᴛᴏ ʏᴏᴜ! 🦋",
    "ᴅᴏ ʏᴏᴜ ʙᴇʟɪᴇᴠᴇ ɪɴ ʟᴏᴠᴇ ᴀᴛ ғɪʀsᴛ ᴍᴇssᴀɢᴇ? 💕",
    "ʏᴏᴜ'ʀᴇ ᴍᴀᴋɪɴɢ ᴍʏ ʜᴇᴀʀᴛ sᴋɪᴘ ᴀ ʙᴇᴀᴛ! 💓",
    "ɪ ᴡɪsʜ ɪ ᴄᴏᴜʟᴅ sᴇɴᴅ ʏᴏᴜ ᴀ ʜᴜɢ ᴛʜʀᴏᴜɢʜ ᴛʜɪs sᴄʀᴇᴇɴ! 🤗",
    "ᴀʀᴇ ʏᴏᴜ ᴀ ᴍᴀɢɪᴄɪᴀɴ? ʙᴇᴄᴀᴜsᴇ ʏᴏᴜ'ᴠᴇ ᴄᴀsᴛ ᴀ sᴘᴇʟʟ ᴏɴ ᴍᴇ! ✨"
]

def format_reply(text):
    tiny_caps_map = {
        'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ', 'f': 'ғ', 'g': 'ɢ', 'h': 'ʜ',
        'i': 'ɪ', 'j': 'ᴊ', 'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ', 'o': 'ᴏ', 'p': 'ᴘ',
        'q': 'ǫ', 'r': 'ʀ', 's': 's', 't': 'ᴛ', 'u': 'ᴜ', 'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x',
        'y': 'ʏ', 'z': 'ᴢ'
    }
    converted = ''.join(tiny_caps_map.get(char.lower(), char) for char in text)
    return f"❖ **{converted}**"

def is_chatting(user_id):
    return active_chats.find_one({"$or": [{"user1": user_id}, {"user2": user_id}]})

@Client.on_callback_query(filters.regex("find_partner"))
async def find_partner_callback(bot, callback: CallbackQuery):
    await find_partner_logic(bot, callback.message, callback.from_user.id)
    await callback.answer()

@Client.on_message(filters.command("find") & filters.private)
async def find_partner_command(bot, message: Message):
    await find_partner_logic(bot, message, message.from_user.id)

async def find_partner_logic(bot, message, user_id):
    if is_chatting(user_id):
        return await message.reply(format_reply("ʏᴏᴜ'ʀᴇ ᴀʟʀᴇᴀᴅʏ ɪɴ ᴀ ᴄʜᴀᴛ! ᴜsᴇ /sᴛᴏᴘ ᴛᴏ ᴇɴᴅ ɪᴛ ғɪʀsᴛ 💕"))

    user_data = users.find_one({"_id": user_id})
    if not user_data:
        return await message.reply(format_reply("ᴘʟᴇᴀsᴇ ᴜsᴇ /sᴛᴀʀᴛ ғɪʀsᴛ, ʙᴇᴀᴜᴛɪғᴜʟ! 😘"))

    # Premium matching
    if user_data.get("premium", False):
        await premium_matching(bot, message, user_id, user_data)
    else:
        await regular_matching(bot, message, user_id)

async def premium_matching(bot, message, user_id, user_data):
    # Find compatible matches based on interests, age, location
    compatible_users = users.find({
        "_id": {"$ne": user_id},
        "age": {"$gte": user_data.get("age", 18) - 5, "$lte": user_data.get("age", 25) + 5},
        "interests": {"$in": user_data.get("interests", [])},
        "looking_for": user_data.get("gender")
    }).limit(3)

    matches = list(compatible_users)
    if matches:
        match_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"💎 {match['name']} ({match.get('age', 'N/A')})", 
                                callback_data=f"select_match:{match['_id']}")] 
            for match in matches[:3]
        ] + [[InlineKeyboardButton("🎲 ʀᴀɴᴅᴏᴍ ᴍᴀᴛᴄʜ", callback_data="random_match")]])
        
        await message.reply(
            format_reply("ʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ᴍᴀᴛᴄʜᴇs ᴀʀᴇ ʀᴇᴀᴅʏ! 💎"),
            reply_markup=match_keyboard
        )
    else:
        await regular_matching(bot, message, user_id)

async def regular_matching(bot, message, user_id):
    # Check for waiting users
    for other_id, data in waiting_users.items():
        if other_id != user_id:
            del waiting_users[other_id]
            active_chats.insert_one({
                "user1": user_id, 
                "user2": other_id, 
                "revealed": False,
                "started_at": str(datetime.now()),
                "messages_count": 0,
                "love_score": 0
            })
            
            await bot.send_message(other_id, format_reply("ᴍᴀᴛᴄʜ ғᴏᴜɴᴅ! ʏᴏᴜ'ʀᴇ ɴᴏᴡ ᴄʜᴀᴛᴛɪɴɢ ᴀɴᴏɴʏᴍᴏᴜsʟʏ! 💕"))
            await bot.send_message(user_id, format_reply("ᴍᴀᴛᴄʜ ғᴏᴜɴᴅ! ʏᴏᴜ'ʀᴇ ɴᴏᴡ ᴄʜᴀᴛᴛɪɴɢ ᴀɴᴏɴʏᴍᴏᴜsʟʏ! 💕"))
            return

    waiting_users[user_id] = {"started": datetime.now()}
    
    waiting_msg = await message.reply(
        format_reply("sᴇᴀʀᴄʜɪɴɢ ғᴏʀ ʏᴏᴜʀ ᴘᴇʀғᴇᴄᴛ ᴍᴀᴛᴄʜ... 💖"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🤖 ᴄʜᴀᴛ ᴡɪᴛʜ ᴀɪ", callback_data="ai_chat")]
        ])
    )

    await asyncio.sleep(15)

    if user_id in waiting_users:
        del waiting_users[user_id]
        active_chats.insert_one({
            "user1": user_id, 
            "user2": "AI_USER", 
            "revealed": False,
            "started_at": str(datetime.now()),
            "is_ai": True
        })
        await waiting_msg.edit_text(format_reply("ɴᴏ ʜᴜᴍᴀɴ ғᴏᴜɴᴅ, ʙᴜᴛ ɪ'ᴍ ʜᴇʀᴇ ғᴏʀ ʏᴏᴜ! 🤖💕"))

@Client.on_callback_query(filters.regex("ai_chat"))
async def ai_chat_callback(bot, callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id in waiting_users:
        del waiting_users[user_id]
        active_chats.insert_one({
            "user1": user_id, 
            "user2": "AI_USER", 
            "revealed": False,
            "started_at": str(datetime.now()),
            "is_ai": True
        })
        await callback.message.edit_text(format_reply("ɴᴏᴡ ᴄʜᴀᴛᴛɪɴɢ ᴡɪᴛʜ ᴀɪ! ɪ'ᴍ ʜᴇʀᴇ ᴛᴏ ᴍᴀᴋᴇ ʏᴏᴜ sᴍɪʟᴇ! 🤖💕"))
    await callback.answer()

@Client.on_callback_query(filters.regex("inline_games"))
async def inline_games_menu(bot, callback: CallbackQuery):
    games_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💖 ʟᴏᴠᴇ ᴍᴇᴛᴇʀ", callback_data="love_meter"),
         InlineKeyboardButton("💋 ᴋɪss ᴏʀ ᴍɪss", callback_data="kiss_or_miss")],
        [InlineKeyboardButton("🎤 ᴛʀᴜᴛʜ ᴏʀ ᴅᴀʀᴇ", callback_data="truth_or_dare"),
         InlineKeyboardButton("🔮 ғᴏʀᴛᴜɴᴇ ᴛᴇʟʟᴇʀ", callback_data="fortune_teller")],
        [InlineKeyboardButton("💑 ᴄᴏᴜᴘʟᴇ ɢᴀᴍᴇ", callback_data="couple_game"),
         InlineKeyboardButton("🎯 ғʟɪʀᴛ ᴄʜᴀʟʟᴇɴɢᴇ", callback_data="flirt_challenge")],
        [InlineKeyboardButton("🌹 ʀᴏsᴇ ɢɪᴠᴇʀ", callback_data="rose_giver"),
         InlineKeyboardButton("💌 ʟᴏᴠᴇ ǫᴜᴏᴛᴇs", callback_data="love_quotes")]
    ])
    
    await callback.message.edit_text(
        format_reply("ᴄʜᴏᴏsᴇ ʏᴏᴜʀ ғᴀᴠᴏʀɪᴛᴇ ɢᴀᴍᴇ! 🎮💕"),
        reply_markup=games_keyboard
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("love_meter"))
async def love_meter_game(bot, callback: CallbackQuery):
    compatibility = randint(60, 100)
    hearts = "💖" * (compatibility // 20)
    await callback.answer(
        format_reply(f"ʏᴏᴜʀ ʟᴏᴠᴇ sᴄᴏʀᴇ: {compatibility}%! {hearts}"),
        show_alert=True
    )

@Client.on_callback_query(filters.regex("kiss_or_miss"))
async def kiss_or_miss_game(bot, callback: CallbackQuery):
    result = choice([
        "ᴋɪss! 💋 ʏᴏᴜ'ʀᴇ ɪʀʀᴇsɪsᴛɪʙʟᴇ!",
        "ᴍɪss! 😜 ʙᴜᴛ ɪ sᴛɪʟʟ ᴀᴅᴏʀᴇ ʏᴏᴜ!",
        "ᴋɪss! 💕 ʏᴏᴜ'ʀᴇ ᴀᴍᴀᴢɪɴɢ!",
        "ᴍɪss! 🌹 ʙᴜᴛ ʜᴇʀᴇ's ᴀ ʀᴏsᴇ!"
    ])
    await callback.answer(format_reply(result), show_alert=True)

@Client.on_callback_query(filters.regex("truth_or_dare"))
async def truth_or_dare_game(bot, callback: CallbackQuery):
    questions = [
        "ᴛʀᴜᴛʜ: ᴡʜᴀᴛ's ʏᴏᴜʀ ɪᴅᴇᴀʟ ᴅᴀᴛᴇ? 💕",
        "ᴅᴀʀᴇ: sᴇɴᴅ ᴀ ғʟɪʀᴛʏ ᴇᴍᴏᴊɪ! 😘",
        "ᴛʀᴜᴛʜ: ᴅᴏ ʏᴏᴜ ʙᴇʟɪᴇᴠᴇ ɪɴ ʟᴏᴠᴇ ᴀᴛ ғɪʀsᴛ sɪɢʜᴛ? 💖",
        "ᴅᴀʀᴇ: ᴅᴇsᴄʀɪʙᴇ ʏᴏᴜʀ ᴄʀᴜsʜ ɪɴ 3 ᴡᴏʀᴅs! 💭"
    ]
    await callback.answer(format_reply(choice(questions)), show_alert=True)

@Client.on_message(filters.private & filters.text & ~filters.command(["start", "help", "stop", "profile"]))
async def handle_chat_messages(bot, message: Message):
    user_id = message.from_user.id
    chat = is_chatting(user_id)

    if not chat:
        return

    partner_id = chat["user1"] if chat["user2"] == user_id else chat["user2"]

    # Update message count
    active_chats.update_one(
        {"_id": chat["_id"]},
        {"$inc": {"messages_count": 1}}
    )

    if partner_id == "AI_USER":
        await asyncio.sleep(randint(1, 3))
        response = choice(ai_responses)
        await message.reply(format_reply(response))
        
        # Add some interactive elements
        if randint(1, 5) == 1:  # 20% chance
            await message.reply(
                format_reply("ʟᴇᴛ's ᴘʟᴀʏ ᴀ ɢᴀᴍᴇ! 🎮"),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("💖 ʟᴏᴠᴇ ᴍᴇᴛᴇʀ", callback_data="love_meter"),
                     InlineKeyboardButton("💋 ᴋɪss ᴏʀ ᴍɪss", callback_data="kiss_or_miss")]
                ])
            )
    else:
        try:
            await bot.send_message(partner_id, message.text)
        except Exception as e:
            await message.reply(format_reply("sᴏʀʀʏ, ᴄᴏᴜʟᴅɴ'ᴛ sᴇɴᴅ ᴍᴇssᴀɢᴇ! 😔"))

@Client.on_message(filters.command("stop") & filters.private)
async def stop_chat(bot, message: Message):
    user_id = message.from_user.id
    chat = is_chatting(user_id)

    if chat:
        partner_id = chat["user1"] if chat["user2"] == user_id else chat["user2"]
        
        # Update user stats
        users.update_one({"_id": user_id}, {"$inc": {"matches_count": 1}})
        
        active_chats.delete_one({"_id": chat["_id"]})
        
        if partner_id != "AI_USER":
            await bot.send_message(partner_id, format_reply("ʏᴏᴜʀ ᴄʜᴀᴛ ᴘᴀʀᴛɴᴇʀ ʟᴇғᴛ! 💔"))
        
        await message.reply(
            format_reply("ʏᴏᴜ ʟᴇғᴛ ᴛʜᴇ ᴄʜᴀᴛ! ʜᴏᴘᴇ ᴛᴏ sᴇᴇ ʏᴏᴜ sᴏᴏɴ! 💕"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔍 ғɪɴᴅ ɴᴇᴡ ᴍᴀᴛᴄʜ", callback_data="find_partner"),
                 InlineKeyboardButton("🎮 ᴘʟᴀʏ ɢᴀᴍᴇs", callback_data="inline_games")]
            ])
        )
    else:
        await message.reply(format_reply("ʏᴏᴜ'ʀᴇ ɴᴏᴛ ᴄʜᴀᴛᴛɪɴɢ ᴡɪᴛʜ ᴀɴʏᴏɴᴇ! 💭"))
