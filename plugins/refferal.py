from pyrogram import Client, filters
from pyrogram.types import Message
from config import *
from pymongo import MongoClient

client = MongoClient(MONGO_URL)
db = client['find_partner']
users = db['users']

@Client.on_message(filters.command("refer") & filters.private)
async def refer(bot, message: Message):
    user_id = message.from_user.id
    ref_link = f"https://t.me/{BOT_USERNAME}?start={user_id}"
    await message.reply_text(
        f"🎁 *Refer & Earn!*\n\n"
        f"Invite your friends and earn 5 coins per referral.\n"
        f"Here is your link:\n`{ref_link}`\n\n"
        f"Make sure your friend opens this link and starts the bot.",
        parse_mode="Markdown"
    )

# Referral handling is now integrated into main.py start handler