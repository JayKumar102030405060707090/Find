
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import *
from pymongo import MongoClient
from datetime import datetime

client = MongoClient(MONGO_URL)
db = client['find_partner']
users = db['users']
step = db['step']

def format_reply(text):
    tiny_caps_map = {
        'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ', 'f': 'ғ', 'g': 'ɢ', 'h': 'ʜ',
        'i': 'ɪ', 'j': 'ᴊ', 'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ', 'o': 'ᴏ', 'p': 'ᴘ',
        'q': 'ǫ', 'r': 'ʀ', 's': 's', 't': 'ᴛ', 'u': 'ᴜ', 'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x',
        'y': 'ʏ', 'z': 'ᴢ'
    }
    converted = ''.join(tiny_caps_map.get(char.lower(), char) for char in text)
    return f"❖ **{converted}**"

@Client.on_callback_query(filters.regex("view_profile"))
async def view_profile_callback(bot, callback: CallbackQuery):
    await view_profile_logic(bot, callback.message, callback.from_user.id)
    await callback.answer()

@Client.on_message(filters.command("profile") & filters.private)
async def view_profile_command(bot, message: Message):
    await view_profile_logic(bot, message, message.from_user.id)

async def view_profile_logic(bot, message, user_id):
    user = users.find_one({"_id": user_id})

    if not user:
        await message.reply(format_reply("ᴘʟᴇᴀsᴇ ᴜsᴇ /sᴛᴀʀᴛ ғɪʀsᴛ, ʙᴇᴀᴜᴛɪғᴜʟ! 😘"))
        return

    name = user.get("name", "ɴᴏᴛ sᴇᴛ")
    age = user.get("age", "ɴᴏᴛ sᴇᴛ")
    gender = user.get("gender", "ɴᴏᴛ sᴇᴛ")
    location = user.get("location", "ɴᴏᴛ sᴇᴛ")
    interests = ", ".join(user.get("interests", [])) or "ɴᴏɴᴇ"
    bio = user.get("bio", "ɴᴏ ʙɪᴏ ʏᴇᴛ")
    coins = user.get("coins", 0)
    hearts = user.get("hearts_received", 0)
    matches = user.get("matches_count", 0)
    relationship_status = user.get("relationship_status", "sɪɴɢʟᴇ")
    premium = "✨ ᴘʀᴇᴍɪᴜᴍ" if user.get("premium", False) else "ʀᴇɢᴜʟᴀʀ"
    vip = "👑 ᴠɪᴘ" if user.get("vip_status", False) else ""

    profile_text = f"""
💎 **ʏᴏᴜʀ ᴘʀᴏғɪʟᴇ** 💎

👤 **ɴᴀᴍᴇ:** {name}
🎂 **ᴀɢᴇ:** {age}
🚻 **ɢᴇɴᴅᴇʀ:** {gender}
📍 **ʟᴏᴄᴀᴛɪᴏɴ:** {location}
💕 **sᴛᴀᴛᴜs:** {relationship_status}
🎯 **ɪɴᴛᴇʀᴇsᴛs:** {interests}
✨ **ʙɪᴏ:** {bio}

📊 **sᴛᴀᴛs:**
💰 **ᴄᴏɪɴs:** {coins}
💖 **ʜᴇᴀʀᴛs:** {hearts}
🎯 **ᴍᴀᴛᴄʜᴇs:** {matches}
💎 **ᴛʏᴘᴇ:** {premium} {vip}
"""

    profile_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✏️ ᴇᴅɪᴛ ᴘʀᴏғɪʟᴇ", callback_data="edit_profile"),
         InlineKeyboardButton("📸 ᴀᴅᴅ ᴘʜᴏᴛᴏ", callback_data="add_photo")],
        [InlineKeyboardButton("🎯 ᴀᴅᴅ ɪɴᴛᴇʀᴇsᴛs", callback_data="add_interests"),
         InlineKeyboardButton("✍️ ᴜᴘᴅᴀᴛᴇ ʙɪᴏ", callback_data="update_bio")],
        [InlineKeyboardButton("🔍 ғɪɴᴅ ᴍᴀᴛᴄʜ", callback_data="find_partner"),
         InlineKeyboardButton("💎 ɢᴏ ᴘʀᴇᴍɪᴜᴍ", callback_data="upgrade_premium")]
    ])

    await message.reply(
        format_reply(profile_text),
        reply_markup=profile_keyboard
    )

@Client.on_callback_query(filters.regex("edit_profile"))
async def edit_profile_callback(bot, callback: CallbackQuery):
    await edit_profile_logic(bot, callback.message, callback.from_user.id)
    await callback.answer()

@Client.on_message(filters.command("editprofile") & filters.private)
async def edit_profile_command(bot, message: Message):
    await edit_profile_logic(bot, message, message.from_user.id)

async def edit_profile_logic(bot, message, user_id):
    step.update_one({"_id": user_id}, {"$set": {"step": "name"}}, upsert=True)
    
    skip_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⏭️ sᴋɪᴘ", callback_data="skip_name")]
    ])
    
    await message.reply(
        format_reply("ʟᴇᴛ's ᴍᴀᴋᴇ ʏᴏᴜʀ ᴘʀᴏғɪʟᴇ ᴀᴍᴀᴢɪɴɢ! ✨\n\nsᴇɴᴅ ʏᴏᴜʀ ɴᴀᴍᴇ:"),
        reply_markup=skip_keyboard
    )

@Client.on_callback_query(filters.regex("add_interests"))
async def add_interests_callback(bot, callback: CallbackQuery):
    interests_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎵 ᴍᴜsɪᴄ", callback_data="interest_music"),
         InlineKeyboardButton("🎬 ᴍᴏᴠɪᴇs", callback_data="interest_movies")],
        [InlineKeyboardButton("📚 ʀᴇᴀᴅɪɴɢ", callback_data="interest_reading"),
         InlineKeyboardButton("🏃 sᴘᴏʀᴛs", callback_data="interest_sports")],
        [InlineKeyboardButton("🍳 ᴄᴏᴏᴋɪɴɢ", callback_data="interest_cooking"),
         InlineKeyboardButton("🌍 ᴛʀᴀᴠᴇʟ", callback_data="interest_travel")],
        [InlineKeyboardButton("🎮 ɢᴀᴍɪɴɢ", callback_data="interest_gaming"),
         InlineKeyboardButton("🎨 ᴀʀᴛ", callback_data="interest_art")],
        [InlineKeyboardButton("✅ ᴅᴏɴᴇ", callback_data="interests_done")]
    ])
    
    await callback.message.edit_text(
        format_reply("sᴇʟᴇᴄᴛ ʏᴏᴜʀ ɪɴᴛᴇʀᴇsᴛs! 🎯"),
        reply_markup=interests_keyboard
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("interest_"))
async def handle_interest_selection(bot, callback: CallbackQuery):
    interest = callback.data.split("_")[1]
    user_id = callback.from_user.id
    
    user = users.find_one({"_id": user_id})
    current_interests = user.get("interests", [])
    
    if interest not in current_interests:
        current_interests.append(interest)
        users.update_one({"_id": user_id}, {"$set": {"interests": current_interests}})
        await callback.answer(format_reply(f"{interest} ᴀᴅᴅᴇᴅ! 💕"))
    else:
        await callback.answer(format_reply(f"{interest} ᴀʟʀᴇᴀᴅʏ ᴀᴅᴅᴇᴅ! 😊"))

@Client.on_callback_query(filters.regex("user_stats"))
async def user_statistics(bot, callback: CallbackQuery):
    user = users.find_one({"_id": callback.from_user.id})
    
    stats_text = f"""
📊 **ʏᴏᴜʀ sᴛᴀᴛɪsᴛɪᴄs** 📊

💰 **ᴄᴏɪɴs:** {user.get('coins', 0)}
💖 **ʜᴇᴀʀᴛs ʀᴇᴄᴇɪᴠᴇᴅ:** {user.get('hearts_received', 0)}
🎯 **ᴛᴏᴛᴀʟ ᴍᴀᴛᴄʜᴇs:** {user.get('matches_count', 0)}
👥 **ʀᴇғᴇʀʀᴀʟs:** {user.get('ref_count', 0)}
⭐ **ᴄᴏᴍᴘᴀᴛɪʙɪʟɪᴛʏ sᴄᴏʀᴇ:** {user.get('compatibility_score', 0)}%
📅 **ᴊᴏɪɴᴇᴅ:** {user.get('joined_at', 'N/A')[:10]}
"""

    stats_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📈 ɪᴍᴘʀᴏᴠᴇ sᴄᴏʀᴇ", callback_data="improve_score"),
         InlineKeyboardButton("💰 ᴇᴀʀɴ ᴍᴏʀᴇ", callback_data="earn_coins")],
        [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="view_profile")]
    ])
    
    await callback.message.edit_text(
        format_reply(stats_text),
        reply_markup=stats_keyboard
    )
    await callback.answer()

@Client.on_message(filters.text & filters.private)
async def catch_profile_updates(bot, message: Message):
    user_id = message.from_user.id
    current = step.find_one({"_id": user_id})
    if not current:
        return

    current_step = current.get("step")

    if current_step == "name":
        step.update_one({"_id": user_id}, {"$set": {"name": message.text, "step": "age"}})
        await message.reply(
            format_reply("ʙᴇᴀᴜᴛɪғᴜʟ ɴᴀᴍᴇ! 😍 ɴᴏᴡ sᴇɴᴅ ʏᴏᴜʀ ᴀɢᴇ:"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⏭️ sᴋɪᴘ", callback_data="skip_age")]
            ])
        )
        return

    if current_step == "age":
        if not message.text.isdigit() or int(message.text) < 13 or int(message.text) > 80:
            return await message.reply(format_reply("ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ᴀ ᴠᴀʟɪᴅ ᴀɢᴇ (13-80)! 😊"))
        
        step.update_one({"_id": user_id}, {"$set": {"age": int(message.text), "step": "gender"}})
        
        gender_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("👨 ʙᴏʏ", callback_data="gender_male"),
             InlineKeyboardButton("👩 ɢɪʀʟ", callback_data="gender_female")],
            [InlineKeyboardButton("🌈 ᴏᴛʜᴇʀ", callback_data="gender_other")]
        ])
        
        await message.reply(
            format_reply("ᴘᴇʀғᴇᴄᴛ! ɴᴏᴡ sᴇʟᴇᴄᴛ ʏᴏᴜʀ ɢᴇɴᴅᴇʀ:"),
            reply_markup=gender_keyboard
        )
        return

    if current_step == "bio":
        data = step.find_one({"_id": user_id})
        users.update_one(
            {"_id": user_id},
            {"$set": {
                "name": data.get("name"),
                "age": data.get("age"),
                "gender": data.get("gender"),
                "location": data.get("location", "Not Set"),
                "bio": message.text
            }},
            upsert=True
        )
        step.delete_one({"_id": user_id})
        
        completion_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("👤 ᴠɪᴇᴡ ᴘʀᴏғɪʟᴇ", callback_data="view_profile"),
             InlineKeyboardButton("🔍 ғɪɴᴅ ᴍᴀᴛᴄʜ", callback_data="find_partner")]
        ])
        
        await message.reply(
            format_reply("ʏᴏᴜʀ ᴘʀᴏғɪʟᴇ ɪs ᴄᴏᴍᴘʟᴇᴛᴇ! ʏᴏᴜ ʟᴏᴏᴋ ᴀᴍᴀᴢɪɴɢ! ✨"),
            reply_markup=completion_keyboard
        )
        return

@Client.on_callback_query(filters.regex("gender_"))
async def handle_gender_selection(bot, callback: CallbackQuery):
    gender = callback.data.split("_")[1]
    user_id = callback.from_user.id
    
    step.update_one({"_id": user_id}, {"$set": {"gender": gender, "step": "bio"}})
    
    await callback.message.edit_text(
        format_reply("ɢʀᴇᴀᴛ ᴄʜᴏɪᴄᴇ! ɴᴏᴡ ᴡʀɪᴛᴇ ᴀ ᴄᴜᴛᴇ ʙɪᴏ ᴀʙᴏᴜᴛ ʏᴏᴜʀsᴇʟғ:"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⏭️ sᴋɪᴘ ʙɪᴏ", callback_data="skip_bio")]
        ])
    )
    await callback.answer()
