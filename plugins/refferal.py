
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import *
from pymongo import MongoClient
from datetime import datetime

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

@Client.on_message(filters.command("refer") & filters.private)
async def refer_command(bot, message: Message):
    user_id = message.from_user.id
    user_data = users.find_one({"_id": user_id})
    
    if not user_data:
        return await message.reply(format_reply("ᴘʟᴇᴀsᴇ ᴜsᴇ /sᴛᴀʀᴛ ғɪʀsᴛ! 😊"))
    
    ref_count = user_data.get('ref_count', 0)
    total_earned = ref_count * REFERRAL_COIN
    ref_link = f"https://t.me/{BOT_USERNAME}?start={user_id}"
    
    refer_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📤 sʜᴀʀᴇ ʀᴇғ ʟɪɴᴋ", url=f"https://t.me/share/url?url={ref_link}&text=Join the best dating bot! 💕")],
        [InlineKeyboardButton("👥 ᴍʏ ʀᴇғᴇʀʀᴀʟs", callback_data="my_referrals"),
         InlineKeyboardButton("🎁 ʀᴇғ ʙᴏɴᴜs", callback_data="ref_bonus")]
    ])
    
    await message.reply(
        format_reply(f"💎 ʀᴇғᴇʀʀᴀʟ sʏsᴛᴇᴍ 💎\n\n"
                    f"👥 ᴛᴏᴛᴀʟ ʀᴇғᴇʀʀᴀʟs: {ref_count}\n"
                    f"💰 ᴛᴏᴛᴀʟ ᴇᴀʀɴᴇᴅ: {total_earned} ᴄᴏɪɴs\n"
                    f"🎯 ᴇᴀʀɴ {REFERRAL_COIN} ᴄᴏɪɴs ᴘᴇʀ ʀᴇғᴇʀʀᴀʟ!\n\n"
                    f"📎 ʏᴏᴜʀ ʀᴇғ ʟɪɴᴋ:\n`{ref_link}`"),
        reply_markup=refer_keyboard
    )

@Client.on_callback_query(filters.regex("my_referrals"))
async def my_referrals_callback(bot, callback: CallbackQuery):
    user_data = users.find_one({"_id": callback.from_user.id})
    ref_count = user_data.get('ref_count', 0)
    total_earned = ref_count * REFERRAL_COIN
    
    # Get list of referred users
    referred_users = list(users.find({"ref_by": callback.from_user.id}))
    
    if referred_users:
        ref_list = "\n".join([f"👤 {user.get('name', 'Unknown')}" for user in referred_users[:10]])
        if len(referred_users) > 10:
            ref_list += f"\n... ᴀɴᴅ {len(referred_users) - 10} ᴍᴏʀᴇ"
    else:
        ref_list = "ɴᴏ ʀᴇғᴇʀʀᴀʟs ʏᴇᴛ 😔"
    
    await callback.message.edit_text(
        format_reply(f"👥 ʏᴏᴜʀ ʀᴇғᴇʀʀᴀʟs 👥\n\n"
                    f"📊 ᴛᴏᴛᴀʟ: {ref_count}\n"
                    f"💰 ᴇᴀʀɴᴇᴅ: {total_earned} ᴄᴏɪɴs\n\n"
                    f"📝 ʀᴇғᴇʀʀᴇᴅ ᴜsᴇʀs:\n{ref_list}"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="back_to_menu")]
        ])
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("ref_bonus"))
async def ref_bonus_callback(bot, callback: CallbackQuery):
    user_data = users.find_one({"_id": callback.from_user.id})
    ref_count = user_data.get('ref_count', 0)
    
    # Bonus rewards for milestones
    bonus_rewards = {
        5: {"coins": 50, "title": "ғɪʀsᴛ 5 ʀᴇғs"},
        10: {"coins": 100, "title": "10 ʀᴇғs ᴍᴀsᴛᴇʀ"},
        25: {"coins": 250, "title": "25 ʀᴇғs ᴄʜᴀᴍᴘɪᴏɴ"},
        50: {"coins": 500, "title": "50 ʀᴇғs ʟᴇɢᴇɴᴅ"},
        100: {"coins": 1000, "title": "100 ʀᴇғs ɢᴏᴅ"}
    }
    
    earned_bonuses = []
    available_bonuses = []
    
    for milestone, reward in bonus_rewards.items():
        if ref_count >= milestone:
            earned_bonuses.append(f"✅ {reward['title']}: +{reward['coins']} ᴄᴏɪɴs")
        else:
            available_bonuses.append(f"🔒 {reward['title']}: +{reward['coins']} ᴄᴏɪɴs ({milestone - ref_count} ᴍᴏʀᴇ)")
    
    bonus_text = "🎁 ʀᴇғᴇʀʀᴀʟ ʙᴏɴᴜsᴇs 🎁\n\n"
    
    if earned_bonuses:
        bonus_text += "✨ ᴇᴀʀɴᴇᴅ ʙᴏɴᴜsᴇs:\n" + "\n".join(earned_bonuses) + "\n\n"
    
    if available_bonuses:
        bonus_text += "🎯 ᴜᴘᴄᴏᴍɪɴɢ ʙᴏɴᴜsᴇs:\n" + "\n".join(available_bonuses[:3])
    
    await callback.message.edit_text(
        format_reply(bonus_text),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📤 sʜᴀʀᴇ ʀᴇғ ʟɪɴᴋ", callback_data="share_ref_link")],
            [InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="back_to_menu")]
        ])
    )
    await callback.answer()

@Client.on_callback_query(filters.regex("share_ref_link"))
async def share_ref_link_callback(bot, callback: CallbackQuery):
    user_id = callback.from_user.id
    ref_link = f"https://t.me/{BOT_USERNAME}?start={user_id}"
    
    await callback.answer(
        format_reply(f"ʏᴏᴜʀ ʀᴇғ ʟɪɴᴋ ᴄᴏᴘɪᴇᴅ! 📋\n{ref_link}"),
        show_alert=True
    )
