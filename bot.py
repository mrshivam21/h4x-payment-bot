import asyncio
import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import qrcode

# --- CONFIG ---
API_ID = 17963091
API_HASH = "cd65e421232d0a205426e5e015dc9acd"
BOT_TOKEN = "7752119330:AAH8m6A_fD8N_rE9B565l59L57Y1m39pEoo"
UPI_ID = "shivam2171@axl"

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "👋 Welcome! Click below to pay:",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Pay Now 💸", callback_data="pay")]])
    )

@app.on_callback_query(filters.regex("pay"))
async def pay(client, cb):
    url = f"upi://pay?pa={UPI_ID}&pn=User&am=100&cu=INR"
    img = qrcode.make(url)
    path = f"qr_{cb.from_user.id}.png"
    img.save(path)
    await cb.message.reply_photo(photo=path, caption="Scan to pay ₹100")
    if os.path.exists(path): os.remove(path)

# Render Fix: Simple start and idle
async def run_bot():
    await app.start()
    print("🚀 Bot Started Successfully!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_bot())
